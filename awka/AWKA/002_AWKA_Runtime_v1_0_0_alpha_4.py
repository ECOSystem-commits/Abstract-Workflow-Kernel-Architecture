#!/usr/bin/env python3
"""AWKA executable reference Runtime v1.0.0-alpha.4.

This module implements the domain-independent runtime contracts required by
001_AWKA_Constitution_v1.0.0-alpha.4.json. It intentionally contains no domain
entities, business rules, field definitions, workflow semantics, or domain
renderers.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence
import json

VERSION = "1.0.0-alpha.4"
CONSTITUTION_API = "1.0"
RUNTIME_API = "1.0"
DOMAIN_RUNTIME_API = "1.0"


class AWKAError(Exception):
    """Base class for controlled AWKA runtime failures."""


class BootstrapError(AWKAError):
    pass


class StructuralError(AWKAError):
    pass


class AuthorizationError(AWKAError):
    pass


class PreconditionFailure(AWKAError):
    pass


class ValidationError(AWKAError):
    pass


class ConcurrencyConflict(AWKAError):
    pass


class RegistryLocked(AWKAError):
    pass


class CapabilityNotRegistered(AWKAError):
    pass


class RendererPurityError(AWKAError):
    pass


class AtomicCommitError(AWKAError):
    pass


class IdempotencyConflict(AWKAError):
    pass


def canonical_json(value: Any) -> str:
    """Serialize a JSON-compatible value deterministically."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_digest(value: Any) -> str:
    """Return a lowercase SHA-256 digest for a JSON-compatible value."""
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def require_sha256(value: str, field_name: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise StructuralError(f"{field_name} must be a 64-character lowercase SHA-256 digest")
    if any(character not in "0123456789abcdef" for character in value):
        raise StructuralError(f"{field_name} must be a 64-character lowercase SHA-256 digest")


@dataclass(frozen=True)
class Actor:
    actor_id: str
    actor_type: str
    roles: tuple[str, ...]
    authority_scope: tuple[str, ...] = ()
    authentication_context: str = "conversation"
    delegation: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class Event:
    event_sequence: int
    event_id: str
    event_type: str
    correlation_id: str
    actor_id: str
    details: Mapping[str, Any]


@dataclass(frozen=True)
class Snapshot:
    snapshot_id: str
    version: int
    prior_version: Optional[int]
    state: Mapping[str, Any]
    state_digest: str
    correlation_id: str


@dataclass(frozen=True)
class CapabilityResult:
    invocation_id: str
    outcome: str
    mutation_occurred: bool
    prior_version: int
    new_version: Optional[int]
    prior_state_digest: str
    result_state_digest: str
    failure_code: Optional[str] = None


@dataclass
class CandidateTransaction:
    prior_state: Dict[str, Any]
    candidate_state: Dict[str, Any]
    staged_evidence: List[Dict[str, Any]] = field(default_factory=list)
    staged_events: List[Event] = field(default_factory=list)
    staged_snapshot: Optional[Snapshot] = None


class AWKAKernel:
    """Minimal domain-independent AWKA reference runtime."""

    DEFINITION_REGISTRIES = (
        "capability_registry",
        "validator_registry",
        "renderer_registry",
        "workflow_registry",
        "entity_registry",
        "tool_registry",
        "schema_registry",
        "policy_registry",
    )

    INSTANCE_STORES = (
        "workflow_instance_store",
        "canonical_state_store",
        "evidence_store",
        "event_store",
        "snapshot_store",
        "artifact_receipt_store",
    )

    KERNEL_STATES = (
        "BOOT",
        "VALIDATING",
        "INITIALIZING",
        "READY",
        "DOMAIN_ACTIVATING",
        "ACTIVE",
        "ERROR",
        "SHUTTING_DOWN",
        "SHUTDOWN",
    )

    DOMAIN_STATES = (
        "DOMAIN_ABSENT",
        "DOMAIN_VALIDATING",
        "DOMAIN_REGISTERING",
        "DOMAIN_VERIFYING",
        "DOMAIN_FREEZING",
        "DOMAIN_ACTIVE",
        "DOMAIN_ERROR",
        "DOMAIN_DEACTIVATED",
    )

    def __init__(self, constitution: Mapping[str, Any]):
        self.constitution = deepcopy(dict(constitution))
        self.kernel_state = "BOOT"
        self.domain_state = "DOMAIN_ABSENT"
        self.definition_registries: Dict[str, Dict[str, Any]] = {
            name: {} for name in self.DEFINITION_REGISTRIES
        }
        self.definition_registries_locked = False
        self.workflow_instances: Dict[str, Dict[str, Any]] = {}
        self.canonical_states: Dict[str, Dict[str, Any]] = {}
        self.evidence_records: List[Dict[str, Any]] = []
        self.events: List[Event] = []
        self.snapshots: Dict[str, List[Snapshot]] = {}
        self.artifact_receipts: List[Dict[str, Any]] = []
        self.idempotency_cache: Dict[str, CapabilityResult] = {}
        self.active_domain_descriptor: Optional[Dict[str, Any]] = None

    def bootstrap(self) -> None:
        """Validate the Constitution and initialize an empty READY Kernel."""
        if self.kernel_state != "BOOT":
            raise BootstrapError("bootstrap is permitted only from BOOT")
        self.kernel_state = "VALIDATING"
        self._validate_constitution()
        self._append_event(
            event_type="KERNEL_BOOT_STARTED",
            correlation_id="BOOT",
            actor_id="AWKA-KERNEL",
            details={"runtime_version": VERSION},
        )
        self.kernel_state = "INITIALIZING"
        if any(self.definition_registries[name] for name in self.DEFINITION_REGISTRIES):
            self.kernel_state = "ERROR"
            raise BootstrapError("Definition Registries must be empty during bootstrap")
        if self.workflow_instances or self.canonical_states or self.snapshots:
            self.kernel_state = "ERROR"
            raise BootstrapError("Instance Stores must be empty during bootstrap")
        self.kernel_state = "READY"
        self._append_event(
            event_type="KERNEL_READY",
            correlation_id="BOOT",
            actor_id="AWKA-KERNEL",
            details={"definition_registries": len(self.DEFINITION_REGISTRIES)},
        )

    def build_candidate_registries(self) -> Dict[str, Dict[str, Any]]:
        """Return isolated temporary registries for atomic Domain Activation."""
        if self.kernel_state != "READY":
            raise PreconditionFailure("candidate registries require a READY Kernel")
        if self.definition_registries_locked:
            raise RegistryLocked("Definition Registries are frozen")
        return {name: {} for name in self.DEFINITION_REGISTRIES}

    @staticmethod
    def candidate_register(
        candidate_registries: Dict[str, Dict[str, Any]],
        registry_name: str,
        definition_id: str,
        definition: Mapping[str, Any],
    ) -> None:
        if registry_name not in candidate_registries:
            raise StructuralError(f"Unknown Definition Registry: {registry_name}")
        if not isinstance(definition_id, str) or not definition_id:
            raise StructuralError("definition_id is required")
        if definition_id in candidate_registries[registry_name]:
            raise StructuralError(f"Duplicate definition: {definition_id}")
        candidate_registries[registry_name][definition_id] = deepcopy(dict(definition))

    def activate_domain(
        self,
        candidate_registries: Mapping[str, Mapping[str, Any]],
        verifier: Callable[[Mapping[str, Mapping[str, Any]]], None],
        domain_descriptor: Mapping[str, Any],
        correlation_id: str,
    ) -> None:
        """Validate, atomically publish, and freeze a Domain Runtime Definition."""
        if self.kernel_state != "READY":
            raise PreconditionFailure("Domain Activation requires READY")
        if self.active_domain_descriptor is not None:
            raise PreconditionFailure("A Domain Runtime is already active")
        if any(self.definition_registries[name] for name in self.DEFINITION_REGISTRIES):
            raise StructuralError("Published Definition Registries must be empty before activation")
        if set(candidate_registries) != set(self.DEFINITION_REGISTRIES):
            raise StructuralError("Candidate Definition Registry set is incomplete")

        self.kernel_state = "DOMAIN_ACTIVATING"
        self.domain_state = "DOMAIN_VALIDATING"
        temporary = deepcopy({name: dict(values) for name, values in candidate_registries.items()})
        try:
            self.domain_state = "DOMAIN_REGISTERING"
            self._validate_candidate_registry_references(temporary)
            self.domain_state = "DOMAIN_VERIFYING"
            verifier(temporary)
            self.domain_state = "DOMAIN_FREEZING"

            # Atomic publication point. No published registry is modified before this block.
            published = deepcopy(temporary)
            descriptor = deepcopy(dict(domain_descriptor))
            self.definition_registries = published
            self.active_domain_descriptor = descriptor
            self.definition_registries_locked = True
            self.domain_state = "DOMAIN_ACTIVE"
            self.kernel_state = "ACTIVE"
            self._append_event(
                event_type="DOMAIN_ACTIVATION_SUCCEEDED",
                correlation_id=correlation_id,
                actor_id="AWKA-KERNEL",
                details={"domain_id": descriptor.get("domain_id")},
            )
        except Exception as error:
            self.domain_state = "DOMAIN_ERROR"
            self.kernel_state = "READY"
            self.definition_registries = {
                name: {} for name in self.DEFINITION_REGISTRIES
            }
            self.active_domain_descriptor = None
            self.definition_registries_locked = False
            self._append_event(
                event_type="DOMAIN_ACTIVATION_FAILED",
                correlation_id=correlation_id,
                actor_id="AWKA-KERNEL",
                details={"error_type": type(error).__name__, "error": str(error)},
            )
            raise

    def register_definition_after_activation(
        self, registry_name: str, definition_id: str, definition: Mapping[str, Any]
    ) -> None:
        if self.definition_registries_locked:
            raise RegistryLocked(definition_id)
        self.candidate_register(
            self.definition_registries, registry_name, definition_id, definition
        )

    def create_workflow_instance(
        self,
        workflow_instance_id: str,
        initial_state: Mapping[str, Any],
        capability_id: str,
        invocation_id: str,
        correlation_id: str,
        actor: Actor,
    ) -> CapabilityResult:
        if self.kernel_state != "ACTIVE":
            raise PreconditionFailure("Workflow creation requires ACTIVE Kernel")
        if workflow_instance_id in self.workflow_instances:
            raise StructuralError(f"Duplicate Workflow Instance: {workflow_instance_id}")
        self.workflow_instances[workflow_instance_id] = {"created": False}
        self.canonical_states[workflow_instance_id] = {}
        self.snapshots[workflow_instance_id] = []
        try:
            result = self.invoke_capability(
                workflow_instance_id=workflow_instance_id,
                capability_id=capability_id,
                inputs={"replace_state": deepcopy(dict(initial_state))},
                expected_prior_version=0,
                expected_prior_state_digest=canonical_digest({}),
                invocation_id=invocation_id,
                correlation_id=correlation_id,
                actor=actor,
            )
            self.workflow_instances[workflow_instance_id] = {
                "created": True,
                "active_version": result.new_version,
            }
            return result
        except Exception:
            self.workflow_instances.pop(workflow_instance_id, None)
            self.canonical_states.pop(workflow_instance_id, None)
            self.snapshots.pop(workflow_instance_id, None)
            raise

    def invoke_capability(
        self,
        workflow_instance_id: str,
        capability_id: str,
        inputs: Mapping[str, Any],
        expected_prior_version: int,
        expected_prior_state_digest: str,
        invocation_id: str,
        correlation_id: str,
        actor: Actor,
    ) -> CapabilityResult:
        """Execute an authorized, validated, optimistic, atomic state transition."""
        if self.kernel_state != "ACTIVE":
            raise PreconditionFailure("Capability invocation requires ACTIVE Kernel")
        if invocation_id in self.idempotency_cache:
            return deepcopy(self.idempotency_cache[invocation_id])
        capability = self.definition_registries["capability_registry"].get(capability_id)
        if capability is None:
            raise CapabilityNotRegistered(capability_id)
        self._authorize(capability, actor)

        prior_state = deepcopy(self.canonical_states.get(workflow_instance_id, {}))
        prior_snapshots = self.snapshots.get(workflow_instance_id, [])
        prior_version = prior_snapshots[-1].version if prior_snapshots else 0
        prior_digest = canonical_digest(prior_state)
        require_sha256(expected_prior_state_digest, "expected_prior_state_digest")
        if expected_prior_version != prior_version or expected_prior_state_digest != prior_digest:
            raise ConcurrencyConflict("CONCURRENCY_CONFLICT")

        self._append_event(
            event_type="CAPABILITY_REQUESTED",
            correlation_id=correlation_id,
            actor_id=actor.actor_id,
            details={
                "workflow_instance_id": workflow_instance_id,
                "capability_id": capability_id,
                "invocation_id": invocation_id,
            },
        )

        candidate_state = self._construct_candidate_state(prior_state, inputs)
        transaction = CandidateTransaction(prior_state, candidate_state)
        transaction.staged_evidence = deepcopy(list(inputs.get("evidence_records", [])))
        self._execute_validators(capability, workflow_instance_id, candidate_state, inputs, actor)

        candidate_digest = canonical_digest(candidate_state)
        next_version = prior_version + 1
        transaction.staged_snapshot = Snapshot(
            snapshot_id=f"{workflow_instance_id}-SNAP-{next_version:06d}",
            version=next_version,
            prior_version=prior_version or None,
            state=deepcopy(candidate_state),
            state_digest=candidate_digest,
            correlation_id=correlation_id,
        )
        transaction.staged_events.append(
            Event(
                event_sequence=len(self.events) + 1,
                event_id=f"EVT-{len(self.events) + 1:08d}",
                event_type="STATE_CHANGED",
                correlation_id=correlation_id,
                actor_id=actor.actor_id,
                details={
                    "workflow_instance_id": workflow_instance_id,
                    "capability_id": capability_id,
                    "version": next_version,
                    "prior_state_digest": prior_digest,
                    "result_state_digest": candidate_digest,
                },
            )
        )

        self._commit_transaction(workflow_instance_id, transaction)
        result = CapabilityResult(
            invocation_id=invocation_id,
            outcome="accepted",
            mutation_occurred=True,
            prior_version=prior_version,
            new_version=next_version,
            prior_state_digest=prior_digest,
            result_state_digest=candidate_digest,
        )
        self.idempotency_cache[invocation_id] = deepcopy(result)
        if workflow_instance_id in self.workflow_instances:
            self.workflow_instances[workflow_instance_id]["active_version"] = next_version
        return result

    def restore_as_new_version(
        self,
        workflow_instance_id: str,
        source_version: int,
        restore_capability_id: str,
        invocation_id: str,
        correlation_id: str,
        actor: Actor,
    ) -> CapabilityResult:
        source_snapshot = next(
            snapshot
            for snapshot in self.snapshots[workflow_instance_id]
            if snapshot.version == source_version
        )
        current_state = self.canonical_states[workflow_instance_id]
        current_version = self.snapshots[workflow_instance_id][-1].version
        return self.invoke_capability(
            workflow_instance_id=workflow_instance_id,
            capability_id=restore_capability_id,
            inputs={
                "replace_state": deepcopy(dict(source_snapshot.state)),
                "evidence_records": [
                    {
                        "evidence_type": "historical_snapshot_restore",
                        "source_snapshot_id": source_snapshot.snapshot_id,
                    }
                ],
            },
            expected_prior_version=current_version,
            expected_prior_state_digest=canonical_digest(current_state),
            invocation_id=invocation_id,
            correlation_id=correlation_id,
            actor=actor,
        )

    def render_artifact(
        self,
        workflow_instance_id: str,
        version: int,
        renderer_id: str,
        render_tool: Callable[[Snapshot, Mapping[str, Any]], bytes],
        options: Optional[Mapping[str, Any]] = None,
    ) -> bytes:
        renderer = self.definition_registries["renderer_registry"].get(renderer_id)
        if renderer is None:
            raise StructuralError(f"Unregistered renderer: {renderer_id}")
        snapshot = next(
            item for item in self.snapshots[workflow_instance_id] if item.version == version
        )
        require_sha256(snapshot.state_digest, "snapshot.state_digest")
        before = self._governed_store_digest()
        artifact = render_tool(snapshot, deepcopy(dict(options or {})))
        if not isinstance(artifact, bytes):
            raise StructuralError("Renderer tool must return bytes")
        after = self._governed_store_digest()
        if before != after:
            raise RendererPurityError(renderer_id)
        return artifact

    def record_artifact_receipt(self, receipt: Mapping[str, Any]) -> None:
        require_sha256(str(receipt.get("snapshot_digest", "")), "snapshot_digest")
        require_sha256(str(receipt.get("artifact_digest", "")), "artifact_digest")
        self.artifact_receipts.append(deepcopy(dict(receipt)))

    def query_snapshot(self, workflow_instance_id: str, version: int) -> Snapshot:
        return deepcopy(
            next(
                item
                for item in self.snapshots[workflow_instance_id]
                if item.version == version
            )
        )

    def shutdown(self) -> None:
        if self.kernel_state == "SHUTDOWN":
            return
        self.kernel_state = "SHUTTING_DOWN"
        self._append_event(
            event_type="KERNEL_SHUTDOWN_REQUESTED",
            correlation_id="SHUTDOWN",
            actor_id="AWKA-KERNEL",
            details={},
        )
        self.kernel_state = "SHUTDOWN"
        self._append_event(
            event_type="KERNEL_SHUTDOWN_COMPLETED",
            correlation_id="SHUTDOWN",
            actor_id="AWKA-KERNEL",
            details={},
        )

    def _validate_constitution(self) -> None:
        document = self.constitution.get("document", {})
        if document.get("document_id") != "AWKA-CONSTITUTION":
            self.kernel_state = "ERROR"
            raise BootstrapError("Invalid Constitution document_id")
        if document.get("document_version") != VERSION:
            self.kernel_state = "ERROR"
            raise BootstrapError("Constitution version mismatch")
        identity = self.constitution.get("kernel_identity", {})
        if identity.get("business_knowledge_allowed_in_kernel") is not False:
            self.kernel_state = "ERROR"
            raise BootstrapError("Kernel must remain domain independent")
        invariants = self.constitution.get("kernel_invariants", [])
        if len(invariants) != 15:
            self.kernel_state = "ERROR"
            raise BootstrapError("Expected 15 Kernel invariants")

    def _validate_candidate_registry_references(
        self, registries: Mapping[str, Mapping[str, Any]]
    ) -> None:
        validators = registries["validator_registry"]
        tools = registries["tool_registry"]
        for capability_id, capability in registries["capability_registry"].items():
            for validator_id in capability.get("validator_ids", []):
                if validator_id not in validators:
                    raise StructuralError(
                        f"{capability_id} references missing validator {validator_id}"
                    )
        for renderer_id, renderer in registries["renderer_registry"].items():
            for tool_id in renderer.get("tool_ids", []):
                if tool_id not in tools:
                    raise StructuralError(
                        f"{renderer_id} references missing tool {tool_id}"
                    )

    @staticmethod
    def _construct_candidate_state(
        prior_state: Mapping[str, Any], inputs: Mapping[str, Any]
    ) -> Dict[str, Any]:
        if "replace_state" in inputs:
            replacement = inputs["replace_state"]
            if not isinstance(replacement, Mapping):
                raise StructuralError("replace_state must be an object")
            return deepcopy(dict(replacement))
        patch = inputs.get("state_patch", {})
        if not isinstance(patch, Mapping):
            raise StructuralError("state_patch must be an object")
        candidate = deepcopy(dict(prior_state))
        candidate.update(deepcopy(dict(patch)))
        return candidate

    def _execute_validators(
        self,
        capability: Mapping[str, Any],
        workflow_instance_id: str,
        candidate_state: Mapping[str, Any],
        inputs: Mapping[str, Any],
        actor: Actor,
    ) -> None:
        for validator_id in capability.get("validator_ids", []):
            validator = self.definition_registries["validator_registry"].get(validator_id)
            if validator is None:
                raise ValidationError(f"Missing validator: {validator_id}")
            function = validator.get("callable")
            if function is None:
                if validator.get("force_fail"):
                    raise ValidationError(validator_id)
                continue
            result = function(
                workflow_instance_id=workflow_instance_id,
                candidate_state=deepcopy(dict(candidate_state)),
                inputs=deepcopy(dict(inputs)),
                actor=actor,
            )
            if result is not True:
                raise ValidationError(f"{validator_id}: {result}")

    @staticmethod
    def _authorize(capability: Mapping[str, Any], actor: Actor) -> None:
        required_roles = set(capability.get("authorization", {}).get("roles", []))
        if required_roles and not required_roles.intersection(actor.roles):
            raise AuthorizationError("Actor lacks a required role")

    def _commit_transaction(
        self, workflow_instance_id: str, transaction: CandidateTransaction
    ) -> None:
        prior_state = deepcopy(self.canonical_states.get(workflow_instance_id, {}))
        prior_snapshot_count = len(self.snapshots.get(workflow_instance_id, []))
        prior_evidence_count = len(self.evidence_records)
        prior_event_count = len(self.events)
        try:
            self.canonical_states[workflow_instance_id] = deepcopy(
                transaction.candidate_state
            )
            self.evidence_records.extend(deepcopy(transaction.staged_evidence))
            self.events.extend(deepcopy(transaction.staged_events))
            self.snapshots[workflow_instance_id].append(
                deepcopy(transaction.staged_snapshot)
            )
        except Exception as error:
            self.canonical_states[workflow_instance_id] = prior_state
            del self.snapshots[workflow_instance_id][prior_snapshot_count:]
            del self.evidence_records[prior_evidence_count:]
            del self.events[prior_event_count:]
            raise AtomicCommitError(str(error))

    def _append_event(
        self,
        event_type: str,
        correlation_id: str,
        actor_id: str,
        details: Mapping[str, Any],
    ) -> None:
        event = Event(
            event_sequence=len(self.events) + 1,
            event_id=f"EVT-{len(self.events) + 1:08d}",
            event_type=event_type,
            correlation_id=correlation_id,
            actor_id=actor_id,
            details=deepcopy(dict(details)),
        )
        self.events.append(event)

    def _governed_store_digest(self) -> str:
        payload = {
            "workflow_instances": self.workflow_instances,
            "canonical_states": self.canonical_states,
            "evidence_records": self.evidence_records,
            "events": [event.__dict__ for event in self.events],
            "snapshots": {
                key: [snapshot.__dict__ for snapshot in values]
                for key, values in self.snapshots.items()
            },
            "definition_registries": self.definition_registries,
        }
        return canonical_digest(payload)


RUNTIME_CONTRACT = {
    "runtime_id": "AWKA-REFERENCE-RUNTIME",
    "runtime_version": VERSION,
    "constitution_api": CONSTITUTION_API,
    "runtime_api": RUNTIME_API,
    "domain_runtime_api": DOMAIN_RUNTIME_API,
    "kernel_services": [
        "CANONICAL_STATE_MANAGER",
        "CAPABILITY_MANAGER",
        "VALIDATOR_MANAGER",
        "EVIDENCE_MANAGER",
        "SNAPSHOT_MANAGER",
        "RENDERER_MANAGER",
        "TOOL_DISPATCHER",
        "WORKFLOW_MANAGER",
        "EVENT_AUDIT_MANAGER",
        "IDENTITY_AUTHORITY_MANAGER",
        "POLICY_MANAGER",
        "QUERY_MANAGER",
    ],
    "definition_registries": list(AWKAKernel.DEFINITION_REGISTRIES),
    "instance_stores": list(AWKAKernel.INSTANCE_STORES),
    "domain_activation_atomic": True,
    "definition_registries_frozen_after_activation": True,
    "optimistic_concurrency_required": True,
    "artifact_generation_inside_state_transaction": False,
    "restore_strategy": "restore_as_new_version",
}


def release_contract() -> Dict[str, Any]:
    return {
        "version": VERSION,
        "uploaded_components": [
            "001_AWKA_Constitution_v1.0.0-alpha.4.json",
            "002_AWKA_Runtime_v1_0_0_alpha_4.py",
            "003_AWKA_Verification_v1_0_0_alpha_4.py",
        ],
        "boot_directive_delivery": "current_user_message",
        "boot_directive_is_file_component": False,
        "boot_directive_requires_sha256": False,
        "hashed_executable_components": [
            "002_AWKA_Runtime_v1_0_0_alpha_4.py",
            "003_AWKA_Verification_v1_0_0_alpha_4.py",
        ],
        "workflow_instance_creation_during_bootstrap": False,
        "domain_activation_during_bootstrap": False,
    }
