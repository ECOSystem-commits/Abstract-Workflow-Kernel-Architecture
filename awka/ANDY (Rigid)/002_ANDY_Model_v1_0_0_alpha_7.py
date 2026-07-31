#!/usr/bin/env python3
"""ANDY Domain Runtime Model v1.0.0-alpha.7.

Kernel-Enforced Runtime and Multi-Artifact Workflow Hardening Release.

This executable reference model defines the ANDY alpha.7 domain contract and
reference algorithms. It preserves alpha.6 lifecycle direction while adding
peer-review-driven hardening for activation-admission evidence, proof classes,
multi-stage progression, artifact-set export, artifact body resolution,
Capability-specific contracts, event equivalence, concurrency classes, semantic
policy-to-Validator mapping, complete Snapshot digests, restore/reopen behavior,
Adapter Route Evidence persistence, parser hardening, and explicit BLOCKED
semantics.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

VERSION = "1.0.0-alpha.7"
AWKA_VERSION = "1.0.0-alpha.4"
DOMAIN_ID = "ANDY.DOMAIN.RUNTIME"
DOMAIN_NAME = "ANDY Domain Runtime"
DOMAIN_FULL_NAME = "Adopted Narrative Directional Yielder"
NAMESPACE_ROOT = "ANDY"
WORKFLOW_INSTANCE_TYPE = "ANDY.NARRATIVE.INSTANCE"
PRIMARY_WORKFLOW_ID = "ANDY.WF.NARRATIVE_PROCEDURE"

COMMON_ROLES = ["andy_owner", "andy_operator", "andy_approver", "andy_admin"]
APPROVER_ROLES = ["andy_owner", "andy_approver"]
ADMIN_ROLES = ["andy_owner", "andy_admin"]

PROOF_CLASSES = [
    "declared_only",
    "loaded_and_queryable",
    "model_reference_behavior_proven",
    "kernel_admission_proven",
    "kernel_capability_enforced",
    "executable_conformance_proven",
]

WORKFLOW_STATES = [
    "UNINITIALIZED",
    "NARRATIVE_LOADED",
    "STAGE_READY",
    "PROMPT_SUBMITTED",
    "STAGE_EXECUTING",
    "STAGE_REVIEW_ACTIVE",
    "STAGE_COMPLETION_PENDING",
    "STAGE_COMPLETE_CONFIRMED",
    "STAGE_ADVANCED",
    "WORKFLOW_COMPLETE",
    "FINAL_EXPORT_READY",
    "EXPORTED",
    "CLOSED",
    "REOPENED",
    "BLOCKED",
]

REMOVED_ALPHA2_GLOBAL_ARTIFACT_STATES = [
    "DRAFT_GENERATED",
    "FEEDBACK_PENDING",
    "REVISION_REQUESTED",
    "ARTIFACT_ACCEPTED",
    "ARTIFACT_REJECTED",
    "ERROR",
]

ARTIFACT_VERSION_STATUSES = [
    "draft",
    "registered",
    "revision_requested",
    "accepted_pending_evidence",
    "accepted_dependency_eligible",
    "rejected",
    "disallowed",
    "superseded",
    "inactive",
    "archived",
    "restored_as_new_version",
    "nongoverned_out_of_band",
]

SLOT_DISPOSITIONS = ["unresolved", "satisfied", "rejected", "disallowed", "deferred", "waived", "blocked"]

FORBIDDEN_FINAL_EXPORT_PHRASES = [
    "Draft Artifact",
    "Draft candidate",
    "not accepted",
    "not evidenced",
    "not dependency-eligible",
    "To make it dependency-eligible",
    "not yet registered",
    "not part of active context",
]

FINAL_EXPORT_REQUIRED_VISIBLE_FIELDS = [
    "Workflow Instance",
    "Artifact Set",
    "Artifact Version",
    "Accepted Artifact",
    "Evidence Packet",
    "Artifact Receipt",
    "Artifact Status",
    "Export Status",
    "Renderer",
]

ARTIFACT_RECEIPT_REQUIRED_FIELDS = [
    "artifact_receipt_id",
    "workflow_instance_id",
    "selected_snapshot_id",
    "selected_snapshot_digest",
    "artifact_name_or_reference",
    "source_artifact_reference",
    "source_artifact_digest",
    "source_artifact_status_at_export",
    "artifact_version_id",
    "accepted_artifact_id",
    "evidence_packet_id",
    "exported_artifact_digest",
    "final_projection_digest",
    "final_projection_status",
    "export_projection_qa_result",
    "renderer_id",
    "renderer_version",
    "selected_workflow_version",
    "active_version_at_request",
    "export_format",
    "validation_or_QA_result",
    "operation_status",
    "export_status",
    "export_timestamp",
    "body_resolution_method",
    "body_resolution_digest",
    "body_resolution_status",
]

ARTIFACT_SET_RECEIPT_REQUIRED_FIELDS = [
    "artifact_set_receipt_id",
    "workflow_instance_id",
    "selected_snapshot_id",
    "selected_snapshot_digest",
    "artifact_set_id",
    "member_receipt_ids",
    "ordered_member_manifest_digest",
    "package_digest",
    "renderer_id",
    "renderer_version",
    "export_status",
    "operation_status",
    "export_timestamp",
]

EXPORT_PROJECTION_QA_REQUIRED_FIELDS = [
    "export_projection_qa_id",
    "workflow_instance_id",
    "artifact_set_id",
    "artifact_version_ids",
    "accepted_artifact_ids",
    "evidence_packet_ids",
    "artifact_receipt_ids",
    "source_artifact_digests",
    "exported_artifact_digest",
    "forbidden_phrase_scan_result",
    "visible_status_match_result",
    "required_lineage_fields_present",
    "body_rewrite_policy_result",
    "lifecycle_projection_result",
    "qa_status",
    "diagnostic",
]

BODY_RESOLUTION_REQUIRED_FIELDS = [
    "body_resolution_record_id",
    "artifact_version_id",
    "artifact_body_ref",
    "resolution_method",
    "expected_digest",
    "resolved_digest",
    "media_type",
    "size_bytes",
    "resolution_status",
    "diagnostic",
]

COMPOSITE_OPERATION_STATUSES = [
    "candidate_validating",
    "validated_ready_to_commit",
    "partially_committed",
    "committed",
    "failed_no_commit",
    "failed_partial_commit",
    "rolled_back",
]

PRIMITIVE_CAPABILITY_IDS = [
    "ANDY.CAP.CREATE_WORKFLOW_INSTANCE",
    "ANDY.CAP.LOAD_NARRATIVE",
    "ANDY.CAP.VALIDATE_NARRATIVE",
    "ANDY.CAP.SUBMIT_STAGE_PROMPT",
    "ANDY.CAP.UPDATE_STAGE_PROMPT",
    "ANDY.CAP.EXECUTE_STAGE",
    "ANDY.CAP.OPEN_STAGE_REVIEW",
    "ANDY.CAP.GENERATE_DRAFT_ARTIFACT",
    "ANDY.CAP.REGISTER_ARTIFACT",
    "ANDY.CAP.SUBMIT_FEEDBACK",
    "ANDY.CAP.REQUEST_REVISION",
    "ANDY.CAP.REVISE_ARTIFACT",
    "ANDY.CAP.ACCEPT_ARTIFACT",
    "ANDY.CAP.ATTACH_EVIDENCE_PACKET",
    "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE",
    "ANDY.CAP.REJECT_ARTIFACT",
    "ANDY.CAP.DEFER_OPTIONAL_ARTIFACT_SLOT",
    "ANDY.CAP.EVALUATE_STAGE_COMPLETION",
    "ANDY.CAP.CONFIRM_STAGE_COMPLETE",
    "ANDY.CAP.ADVANCE_STAGE",
    "ANDY.CAP.RECONSTRUCT_CONTEXT",
    "ANDY.CAP.BLOCK_WORKFLOW",
    "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION",
    "ANDY.CAP.RESTORE_AS_NEW_VERSION",
    "ANDY.CAP.FINALIZE_WORKFLOW",
    "ANDY.CAP.EXPORT_ARTIFACT_SET",
    "ANDY.CAP.CLOSE_WORKFLOW",
]

COMPOSITE_CAPABILITY_IDS = [
    "ANDY.CAP.ADOPT_NARRATIVE",
    "ANDY.CAP.RUN_STAGE_TO_REVIEW",
    "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE",
]

ENTITY_IDS = [
    "ANDY.ENTITY.NARRATIVE_WORKFLOW",
    "ANDY.ENTITY.NARRATIVE_DEFINITION",
    "ANDY.ENTITY.STAGE_RECORD",
    "ANDY.ENTITY.NARRATIVE_STAGE",
    "ANDY.ENTITY.STAGE_PROMPT_VERSION",
    "ANDY.ENTITY.ARTIFACT_SLOT",
    "ANDY.ENTITY.ARTIFACT_SLOT_DISPOSITION",
    "ANDY.ENTITY.ARTIFACT_REGISTRATION",
    "ANDY.ENTITY.ARTIFACT_VERSION",
    "ANDY.ENTITY.ACCEPTED_ARTIFACT",
    "ANDY.ENTITY.REJECTION_RECORD",
    "ANDY.ENTITY.EVIDENCE_PACKET",
    "ANDY.ENTITY.DEPENDENCY_EDGE",
    "ANDY.ENTITY.ARTIFACT_RECEIPT",
    "ANDY.ENTITY.ADAPTER_ROUTE_EVIDENCE",
    "ANDY.ENTITY.COMPOSITE_OPERATION_RUN",
    "ANDY.ENTITY.EVENT_DEFINITION",
    "ANDY.ENTITY.EVENT_RECORD",
    "ANDY.ENTITY.ARTIFACT_SET",
    "ANDY.ENTITY.ARTIFACT_SET_MEMBER",
    "ANDY.ENTITY.ARTIFACT_SET_RECEIPT",
    "ANDY.ENTITY.ARTIFACT_BODY_RESOLUTION_RECORD",
    "ANDY.ENTITY.SNAPSHOT_RECORD",
    "ANDY.ENTITY.ACTIVATION_ADMISSION_REPORT",
]

VALIDATOR_IDS = [
    "ANDY.VAL.AUTHORITY",
    "ANDY.VAL.NARRATIVE",
    "ANDY.VAL.STAGE",
    "ANDY.VAL.STAGE_PROMPT",
    "ANDY.VAL.INTERACTION_ADAPTER",
    "ANDY.VAL.ARTIFACT",
    "ANDY.VAL.ARTIFACT_SLOT",
    "ANDY.VAL.ARTIFACT_SLOT_DISPOSITION",
    "ANDY.VAL.DISALLOWED_ARTIFACT",
    "ANDY.VAL.REJECTION",
    "ANDY.VAL.FEEDBACK",
    "ANDY.VAL.ACCEPTANCE",
    "ANDY.VAL.EVIDENCE",
    "ANDY.VAL.DEPENDENCY",
    "ANDY.VAL.DRAFT_ISOLATION",
    "ANDY.VAL.CONTEXT",
    "ANDY.VAL.WORKFLOW",
    "ANDY.VAL.WORKFLOW_GRAPH",
    "ANDY.VAL.BUSINESS",
    "ANDY.VAL.SNAPSHOT",
    "ANDY.VAL.PRESENTATION",
    "ANDY.VAL.EXPORT",
    "ANDY.VAL.ACTIVATION_ADMISSION",
    "ANDY.VAL.COMPOSITE_OPERATION",
    "ANDY.VAL.FINAL_EXPORT_PROJECTION",
    "ANDY.VAL.CONCURRENCY",
    "ANDY.VAL.ARTIFACT_BODY_RESOLUTION",
    "ANDY.VAL.EVENT_CONTRACT",
    "ANDY.VAL.ARTIFACT_SET_EXPORT",
    "ANDY.VAL.POLICY_VALIDATOR_MAPPING",
]

RENDERER_IDS = [
    "ANDY.RENDER.STAGE_REVIEW",
    "ANDY.RENDER.ARTIFACT_REGISTRY",
    "ANDY.RENDER.ARTIFACT_VERSION_HISTORY",
    "ANDY.RENDER.REJECTION_HISTORY",
    "ANDY.RENDER.EVIDENCE_PACKET",
    "ANDY.RENDER.NARRATIVE_CONTEXT",
    "ANDY.RENDER.FINAL_ARTIFACT_SET",
    "ANDY.RENDER.ARTIFACT_SET_MANIFEST",
    "ANDY.RENDER.AUDIT_DIAGNOSTIC",
    "ANDY.RENDER.JSON_EXPORT",
]

TOOL_IDS = [
    "ANDY.TOOL.ARTIFACT_GENERATOR",
    "ANDY.TOOL.TEXT_RENDERER",
    "ANDY.TOOL.FILE_EXPORTER",
    "ANDY.TOOL.JSON_EXPORTER",
    "ANDY.TOOL.DIAGNOSTIC_RENDERER",
    "ANDY.TOOL.DIGEST_CALCULATOR",
    "ANDY.TOOL.ARTIFACT_BODY_RESOLVER",
    "ANDY.TOOL.CANONICAL_SERIALIZER",
]

SCHEMA_IDS = [
    "ANDY.SCHEMA.CANONICAL_MODEL",
    "ANDY.SCHEMA.INTERACTION_ADAPTER_CONTRACT",
    "ANDY.SCHEMA.ADAPTER_ROUTE_EVIDENCE",
    "ANDY.SCHEMA.COMPOSITE_OPERATION_RUN",
    "ANDY.SCHEMA.EXPORT_PROJECTION_QA",
    "ANDY.SCHEMA.ACTIVATION_ADMISSION_REPORT",
    "ANDY.SCHEMA.ARTIFACT_BODY_RESOLUTION_RECORD",
    "ANDY.SCHEMA.ARTIFACT_SET_MANIFEST",
    "ANDY.SCHEMA.EVENT_DEFINITION",
    "ANDY.SCHEMA.PROOF_CLASS_REPORT",
    "ANDY.SCHEMA.CONCURRENCY_CONTRACT",
]

POLICY_IDS = [
    "ANDY.POLICY.LINEAR_NARRATIVE_ONLY",
    "ANDY.POLICY.USER_STAGE_PROMPT_REQUIRED",
    "ANDY.POLICY.EXACT_PROMPT_COMMAND_REQUIRED",
    "ANDY.POLICY.NO_AUTONOMOUS_PROMPT_CAPTURE",
    "ANDY.POLICY.STAGE_PROMPTS_VERSIONED",
    "ANDY.POLICY.ONE_ACTIVE_PROMPT_PER_STAGE",
    "ANDY.POLICY.STAGE_REVIEW_ACTIVE_FOR_ARTIFACT_DECISIONS",
    "ANDY.POLICY.ARTIFACTS_REGISTERED_BEFORE_REVIEW",
    "ANDY.POLICY.REQUIRED_ARTIFACT_SLOTS_SATISFIED",
    "ANDY.POLICY.OPTIONAL_SLOT_DEFERRAL_AUTHORIZED",
    "ANDY.POLICY.ONE_ACCEPTED_VERSION_PER_ARTIFACT",
    "ANDY.POLICY.ACCEPTED_PENDING_EVIDENCE_NOT_DEPENDENCY_ELIGIBLE",
    "ANDY.POLICY.EVIDENCE_PACKET_PROMOTES_DEPENDENCY_ELIGIBILITY",
    "ANDY.POLICY.DISALLOWED_ARTIFACTS_REJECTED",
    "ANDY.POLICY.REJECTION_HISTORY_PRESERVED",
    "ANDY.POLICY.ACCEPTED_DEPENDENCY_ELIGIBLE_ARTIFACTS_ONLY",
    "ANDY.POLICY.DRAFT_ISOLATION",
    "ANDY.POLICY.EVIDENCE_PACKET_REQUIRED",
    "ANDY.POLICY.NO_CONVERSATION_AUTHORITY",
    "ANDY.POLICY.NO_OUT_OF_BAND_ARTIFACTS",
    "ANDY.POLICY.ARTIFACT_BODY_BY_REFERENCE",
    "ANDY.POLICY.RESTORE_AS_NEW_VERSION",
    "ANDY.POLICY.ARTIFACT_RECEIPT_REQUIRED",
    "ANDY.POLICY.EXPORT_AFTER_FINAL_BYTES_HASH",
    "ANDY.POLICY.WORKFLOW_GRAPH_INTEGRITY_REQUIRED",
    "ANDY.POLICY.ACTIVATION_ADMISSION_REQUIRES_REAL_REPORT",
    "ANDY.POLICY.CAPABILITY_SPECIFIC_CONCURRENCY",
    "ANDY.POLICY.VERIFICATION_ASSERTIONS_MUST_RAISE",
    "ANDY.POLICY.COMPOSITE_CAPABILITIES_PRESERVE_PRIMITIVE_EVENTS",
    "ANDY.POLICY.COMPOSITE_CAPABILITIES_DECLARE_PARTIAL_COMMIT",
    "ANDY.POLICY.NO_FALSE_DEPENDENCY_PROMOTION",
    "ANDY.POLICY.MACRO_COMMANDS_REQUIRE_EXPLICIT_PAYLOADS",
    "ANDY.POLICY.FINAL_EXPORT_MUST_NOT_LEAK_DRAFT_STATUS",
    "ANDY.POLICY.RUNTIME_STATE_SERIALIZATION_MUST_BE_CONSISTENT",
    "ANDY.POLICY.MULTI_STAGE_PROGRESSION_REQUIRED",
    "ANDY.POLICY.ARTIFACT_SET_EXPORT_INCLUDES_ALL_SELECTED_MEMBERS",
    "ANDY.POLICY.ARTIFACT_BODY_RESOLUTION_DIGEST_VERIFIED",
    "ANDY.POLICY.EVENT_CONTRACT_EQUIVALENCE_REQUIRED",
    "ANDY.POLICY.POLICY_VALIDATOR_MAPPING_SEMANTIC",
    "ANDY.POLICY.ADAPTER_ROUTE_EVIDENCE_PERSISTED",
    "ANDY.POLICY.SEMANTIC_RESULT_DIGEST_REQUIRED",
    "ANDY.POLICY.PROOF_CLASSIFICATION_REQUIRED",
]

POLICY_VALIDATOR_MAP = {
    "ANDY.POLICY.EXACT_PROMPT_COMMAND_REQUIRED": ["ANDY.VAL.INTERACTION_ADAPTER"],
    "ANDY.POLICY.NO_AUTONOMOUS_PROMPT_CAPTURE": ["ANDY.VAL.INTERACTION_ADAPTER"],
    "ANDY.POLICY.EVIDENCE_PACKET_PROMOTES_DEPENDENCY_ELIGIBILITY": ["ANDY.VAL.EVIDENCE", "ANDY.VAL.DEPENDENCY"],
    "ANDY.POLICY.ARTIFACT_BODY_BY_REFERENCE": ["ANDY.VAL.ARTIFACT", "ANDY.VAL.ARTIFACT_BODY_RESOLUTION"],
    "ANDY.POLICY.ARTIFACT_RECEIPT_REQUIRED": ["ANDY.VAL.EXPORT"],
    "ANDY.POLICY.ACTIVATION_ADMISSION_REQUIRES_REAL_REPORT": ["ANDY.VAL.ACTIVATION_ADMISSION"],
    "ANDY.POLICY.CAPABILITY_SPECIFIC_CONCURRENCY": ["ANDY.VAL.CONCURRENCY"],
    "ANDY.POLICY.RUNTIME_STATE_SERIALIZATION_MUST_BE_CONSISTENT": ["ANDY.VAL.SNAPSHOT"],
    "ANDY.POLICY.FINAL_EXPORT_MUST_NOT_LEAK_DRAFT_STATUS": ["ANDY.VAL.FINAL_EXPORT_PROJECTION"],
    "ANDY.POLICY.MACRO_COMMANDS_REQUIRE_EXPLICIT_PAYLOADS": ["ANDY.VAL.INTERACTION_ADAPTER"],
    "ANDY.POLICY.MULTI_STAGE_PROGRESSION_REQUIRED": ["ANDY.VAL.WORKFLOW", "ANDY.VAL.STAGE"],
    "ANDY.POLICY.ARTIFACT_SET_EXPORT_INCLUDES_ALL_SELECTED_MEMBERS": ["ANDY.VAL.ARTIFACT_SET_EXPORT", "ANDY.VAL.EXPORT"],
    "ANDY.POLICY.ARTIFACT_BODY_RESOLUTION_DIGEST_VERIFIED": ["ANDY.VAL.ARTIFACT_BODY_RESOLUTION"],
    "ANDY.POLICY.EVENT_CONTRACT_EQUIVALENCE_REQUIRED": ["ANDY.VAL.EVENT_CONTRACT"],
    "ANDY.POLICY.POLICY_VALIDATOR_MAPPING_SEMANTIC": ["ANDY.VAL.POLICY_VALIDATOR_MAPPING"],
    "ANDY.POLICY.ADAPTER_ROUTE_EVIDENCE_PERSISTED": ["ANDY.VAL.INTERACTION_ADAPTER"],
    "ANDY.POLICY.SEMANTIC_RESULT_DIGEST_REQUIRED": ["ANDY.VAL.ACTIVATION_ADMISSION"],
    "ANDY.POLICY.PROOF_CLASSIFICATION_REQUIRED": ["ANDY.VAL.ACTIVATION_ADMISSION"],
}

WORKFLOW_TRANSITIONS = [
    ("UNINITIALIZED", "NARRATIVE_LOADED", "ANDY.CAP.LOAD_NARRATIVE"),
    ("NARRATIVE_LOADED", "STAGE_READY", "ANDY.CAP.VALIDATE_NARRATIVE"),
    ("STAGE_READY", "PROMPT_SUBMITTED", "ANDY.CAP.SUBMIT_STAGE_PROMPT"),
    ("PROMPT_SUBMITTED", "PROMPT_SUBMITTED", "ANDY.CAP.UPDATE_STAGE_PROMPT"),
    ("PROMPT_SUBMITTED", "STAGE_EXECUTING", "ANDY.CAP.EXECUTE_STAGE"),
    ("STAGE_EXECUTING", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.OPEN_STAGE_REVIEW"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.REGISTER_ARTIFACT"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.ACCEPT_ARTIFACT"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.ATTACH_EVIDENCE_PACKET"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.REJECT_ARTIFACT"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.SUBMIT_FEEDBACK"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.REQUEST_REVISION"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.REVISE_ARTIFACT"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_REVIEW_ACTIVE", "ANDY.CAP.DEFER_OPTIONAL_ARTIFACT_SLOT"),
    ("STAGE_REVIEW_ACTIVE", "STAGE_COMPLETION_PENDING", "ANDY.CAP.EVALUATE_STAGE_COMPLETION"),
    ("STAGE_COMPLETION_PENDING", "STAGE_COMPLETE_CONFIRMED", "ANDY.CAP.CONFIRM_STAGE_COMPLETE"),
    ("STAGE_COMPLETE_CONFIRMED", "STAGE_ADVANCED", "ANDY.CAP.ADVANCE_STAGE"),
    ("STAGE_ADVANCED", "STAGE_READY", "ANDY.CAP.ADVANCE_STAGE"),
    ("STAGE_ADVANCED", "WORKFLOW_COMPLETE", "ANDY.CAP.ADVANCE_STAGE"),
    ("WORKFLOW_COMPLETE", "FINAL_EXPORT_READY", "ANDY.CAP.FINALIZE_WORKFLOW"),
    ("FINAL_EXPORT_READY", "EXPORTED", "ANDY.CAP.EXPORT_ARTIFACT_SET"),
    ("EXPORTED", "CLOSED", "ANDY.CAP.CLOSE_WORKFLOW"),
    ("CLOSED", "REOPENED", "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION"),
    ("REOPENED", "STAGE_READY", "ANDY.CAP.RESTORE_AS_NEW_VERSION"),
]

COMPOSITE_CAPABILITY_CONTRACTS = {
    "ANDY.CAP.ADOPT_NARRATIVE": {
        "composite": True,
        "primitive_sequence": ["ANDY.CAP.LOAD_NARRATIVE", "ANDY.CAP.VALIDATE_NARRATIVE"],
        "commit_policy": "all_or_none",
        "rollback_policy": "discard_candidate_on_failure_commit_no_canonical_narrative",
        "partial_commit_allowed": False,
        "start_state": "UNINITIALIZED",
        "success_state": "STAGE_READY",
        "option_a_two_phase_candidate_validation": True,
    },
    "ANDY.CAP.RUN_STAGE_TO_REVIEW": {
        "composite": True,
        "primitive_sequence": ["ANDY.CAP.SUBMIT_STAGE_PROMPT", "ANDY.CAP.EXECUTE_STAGE", "ANDY.CAP.OPEN_STAGE_REVIEW"],
        "commit_policy": "safe_partial_commit",
        "partial_commit_policy": "prompt_commit_is_durable_execution_or_review_failure_preserves_prompt_and_reports_failed_step",
        "partial_commit_allowed": True,
        "start_state": "STAGE_READY",
        "success_state": "STAGE_REVIEW_ACTIVE",
    },
    "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE": {
        "composite": True,
        "primitive_sequence": [
            "ANDY.CAP.REGISTER_ARTIFACT",
            "ANDY.CAP.ACCEPT_ARTIFACT",
            "ANDY.CAP.ATTACH_EVIDENCE_PACKET",
            "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE",
        ],
        "commit_policy": "safe_partial_commit",
        "partial_commit_policy": "preserve_successful_prior_steps_but_dependency_eligible_must_remain_false_until_all_required_steps_succeed",
        "partial_commit_allowed": True,
        "start_state": "STAGE_REVIEW_ACTIVE",
        "success_state": "STAGE_REVIEW_ACTIVE",
        "no_false_dependency_promotion": True,
    },
}

INTERACTION_ADAPTER_CONTRACT = {
    "contract_id": "ANDY.ADAPTER.INTERACTION_CONTRACT",
    "version": VERSION,
    "autonomous_natural_language_prompt_capture_enabled": False,
    "vague_commands": ["Looks good.", "Approved.", "Continue.", "Next.", "Use that.", "Reject that.", "Fix it."],
    "max_payload_length": 4096,
    "patterns": [
        r"^Submit prompt for stage (STG-[0-9]+): (.+)$",
        r"^Adopt ANDY Narrative: (.+)$",
        r"^Adopt ANDY Narrative from uploaded file: (.+)$",
        r"^Run stage (STG-[0-9]+) with prompt: (.+)$",
        r"^Submit and execute stage (STG-[0-9]+): (.+)$",
        r"^Accept artifact with evidence for slot (SLOT-[0-9]+) in stage (STG-[0-9]+):(.+)$",
    ],
}

CAPABILITY_CONTRACT_REQUIRED_FIELDS = [
    "capability_id",
    "version",
    "purpose",
    "inputs",
    "outputs",
    "preconditions",
    "postconditions",
    "permitted_mutations",
    "validator_ids",
    "authorization",
    "events_emitted",
    "failure_effect",
    "idempotency",
    "concurrency_requirement",
    "composite",
    "body_authority",
]

CAPABILITY_INPUTS = {
    "ANDY.CAP.CREATE_WORKFLOW_INSTANCE": ["workflow_instance_id", "actor_reference", "invocation_id"],
    "ANDY.CAP.LOAD_NARRATIVE": ["workflow_instance_id", "narrative_id", "stages", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.VALIDATE_NARRATIVE": ["workflow_instance_id", "narrative_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.SUBMIT_STAGE_PROMPT": ["workflow_instance_id", "stage_id", "prompt_text_or_ref", "prompt_digest", "adapter_route_evidence_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.UPDATE_STAGE_PROMPT": ["workflow_instance_id", "stage_id", "prompt_version_id", "prompt_text_or_ref", "prompt_digest", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.EXECUTE_STAGE": ["workflow_instance_id", "stage_id", "active_prompt_version_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.OPEN_STAGE_REVIEW": ["workflow_instance_id", "stage_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.REGISTER_ARTIFACT": ["workflow_instance_id", "artifact_id", "artifact_version_id", "slot_id", "artifact_body_ref", "artifact_digest", "artifact_media_type", "artifact_size_bytes", "artifact_storage_class", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.ACCEPT_ARTIFACT": ["workflow_instance_id", "artifact_version_id", "acceptance_statement", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.ATTACH_EVIDENCE_PACKET": ["workflow_instance_id", "accepted_artifact_id", "evidence_packet_id", "source_inputs", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE": ["workflow_instance_id", "accepted_artifact_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.EVALUATE_STAGE_COMPLETION": ["workflow_instance_id", "stage_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.CONFIRM_STAGE_COMPLETE": ["workflow_instance_id", "stage_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.ADVANCE_STAGE": ["workflow_instance_id", "stage_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.FINALIZE_WORKFLOW": ["workflow_instance_id", "selected_snapshot_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.EXPORT_ARTIFACT_SET": ["workflow_instance_id", "selected_snapshot_id", "selected_snapshot_digest", "member_selection_policy", "renderer_id", "export_format", "output_reference", "actor_reference", "invocation_id"],
    "ANDY.CAP.CLOSE_WORKFLOW": ["workflow_instance_id", "artifact_set_receipt_id", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION": ["workflow_instance_id", "stage_id", "source_snapshot_id", "source_snapshot_digest", "actor_reference", "invocation_id", "expected_active_version"],
    "ANDY.CAP.RESTORE_AS_NEW_VERSION": ["workflow_instance_id", "source_snapshot_id", "source_snapshot_digest", "actor_reference", "invocation_id", "expected_active_version"],
}

CAPABILITY_OUTPUTS = {
    "ANDY.CAP.CREATE_WORKFLOW_INSTANCE": ["workflow_instance", "snapshot_reference", "events"],
    "ANDY.CAP.EXPORT_ARTIFACT_SET": ["artifact_set", "member_receipts", "aggregate_receipt", "export_projection_qa", "events"],
    "ANDY.CAP.RECONSTRUCT_CONTEXT": ["active_context", "selected_snapshot_digest"],
}

CONCURRENCY_BY_CAPABILITY = {
    "ANDY.CAP.CREATE_WORKFLOW_INSTANCE": {"class": "CREATE", "unique_key": "workflow_instance_id"},
    "ANDY.CAP.RECONSTRUCT_CONTEXT": {"class": "READ_OR_PROJECT", "requires_selected_snapshot_digest": True},
    "ANDY.CAP.EXPORT_ARTIFACT_SET": {"class": "EXPORT", "requires_selected_snapshot_digest": True, "idempotent_output_key": "output_reference"},
    "ANDY.CAP.RESTORE_AS_NEW_VERSION": {"class": "RESTORE", "requires_source_snapshot_digest": True, "requires_active_version": True},
    "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION": {"class": "RESTORE", "requires_source_snapshot_digest": True, "requires_active_version": True},
}

PRIMITIVE_EVENT_MAP = {
    "ANDY.CAP.CREATE_WORKFLOW_INSTANCE": ["ANDY.EVENT.WORKFLOW_INSTANCE_CREATED"],
    "ANDY.CAP.LOAD_NARRATIVE": ["ANDY.EVENT.NARRATIVE_LOADED"],
    "ANDY.CAP.VALIDATE_NARRATIVE": ["ANDY.EVENT.NARRATIVE_VALIDATED"],
    "ANDY.CAP.SUBMIT_STAGE_PROMPT": ["ANDY.EVENT.STAGE_PROMPT_SUBMITTED"],
    "ANDY.CAP.UPDATE_STAGE_PROMPT": ["ANDY.EVENT.STAGE_PROMPT_UPDATED"],
    "ANDY.CAP.EXECUTE_STAGE": ["ANDY.EVENT.STAGE_EXECUTED"],
    "ANDY.CAP.OPEN_STAGE_REVIEW": ["ANDY.EVENT.STAGE_REVIEW_OPENED"],
    "ANDY.CAP.GENERATE_DRAFT_ARTIFACT": ["ANDY.EVENT.DRAFT_ARTIFACT_GENERATED"],
    "ANDY.CAP.REGISTER_ARTIFACT": ["ANDY.EVENT.ARTIFACT_REGISTERED"],
    "ANDY.CAP.SUBMIT_FEEDBACK": ["ANDY.EVENT.FEEDBACK_SUBMITTED"],
    "ANDY.CAP.REQUEST_REVISION": ["ANDY.EVENT.REVISION_REQUESTED"],
    "ANDY.CAP.REVISE_ARTIFACT": ["ANDY.EVENT.ARTIFACT_REVISED"],
    "ANDY.CAP.ACCEPT_ARTIFACT": ["ANDY.EVENT.ARTIFACT_ACCEPTED_PENDING_EVIDENCE"],
    "ANDY.CAP.ATTACH_EVIDENCE_PACKET": ["ANDY.EVENT.EVIDENCE_PACKET_ATTACHED"],
    "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE": ["ANDY.EVENT.ARTIFACT_DEPENDENCY_ELIGIBLE"],
    "ANDY.CAP.REJECT_ARTIFACT": ["ANDY.EVENT.ARTIFACT_REJECTED"],
    "ANDY.CAP.DEFER_OPTIONAL_ARTIFACT_SLOT": ["ANDY.EVENT.OPTIONAL_ARTIFACT_SLOT_DEFERRED"],
    "ANDY.CAP.EVALUATE_STAGE_COMPLETION": ["ANDY.EVENT.STAGE_COMPLETION_EVALUATED"],
    "ANDY.CAP.CONFIRM_STAGE_COMPLETE": ["ANDY.EVENT.STAGE_COMPLETION_CONFIRMED"],
    "ANDY.CAP.ADVANCE_STAGE": ["ANDY.EVENT.STAGE_ADVANCED", "ANDY.EVENT.NEXT_STAGE_READY", "ANDY.EVENT.WORKFLOW_COMPLETE"],
    "ANDY.CAP.RECONSTRUCT_CONTEXT": ["ANDY.EVENT.CONTEXT_RECONSTRUCTED"],
    "ANDY.CAP.BLOCK_WORKFLOW": ["ANDY.EVENT.WORKFLOW_BLOCKED"],
    "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION": ["ANDY.EVENT.STAGE_REOPENED_AS_NEW_VERSION"],
    "ANDY.CAP.RESTORE_AS_NEW_VERSION": ["ANDY.EVENT.SNAPSHOT_RESTORED_AS_NEW_VERSION"],
    "ANDY.CAP.FINALIZE_WORKFLOW": ["ANDY.EVENT.WORKFLOW_FINALIZED"],
    "ANDY.CAP.EXPORT_ARTIFACT_SET": ["ANDY.EVENT.ARTIFACT_SET_EXPORTED"],
    "ANDY.CAP.CLOSE_WORKFLOW": ["ANDY.EVENT.WORKFLOW_CLOSED"],
}

COMPOSITE_EVENT_MAP = {
    "ANDY.CAP.ADOPT_NARRATIVE": ["ANDY.EVENT.COMPOSITE_OPERATION_STARTED", "ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED"],
    "ANDY.CAP.RUN_STAGE_TO_REVIEW": ["ANDY.EVENT.COMPOSITE_OPERATION_STARTED", "ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED", "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT"],
    "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE": ["ANDY.EVENT.COMPOSITE_OPERATION_STARTED", "ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED", "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT"],
}

EVENT_IDS = sorted(set([event for events in PRIMITIVE_EVENT_MAP.values() for event in events] + [event for events in COMPOSITE_EVENT_MAP.values() for event in events] + ["ANDY.EVENT.ACTIVATION_REPORT_VALIDATED", "ANDY.EVENT.SNAPSHOT_CREATED", "ANDY.EVENT.ADAPTER_ROUTE_EVIDENCE_RECORDED", "ANDY.EVENT.ARTIFACT_BODY_RESOLVED", "ANDY.EVENT.ARTIFACT_SET_RECEIPT_CREATED"]))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _canonical(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _canonical(value[k]) for k in sorted(value.keys(), key=str)}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return [_canonical(v) for v in sorted(value, key=str)]
    return str(value)


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    if isinstance(value, bytes):
        data = value
    elif isinstance(value, str):
        data = value.encode("utf-8")
    else:
        data = canonical_json(value).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _definition(definition_id: str, kind: str, **extra: Any) -> Dict[str, Any]:
    out = {"definition_id": definition_id, "kind": kind, "version": VERSION, "namespace": NAMESPACE_ROOT}
    out.update(extra)
    return out


def _concurrency_for(capability_id: str) -> Dict[str, Any]:
    return copy.deepcopy(CONCURRENCY_BY_CAPABILITY.get(capability_id, {"class": "MUTATE", "requires_active_version": True, "requires_state_digest": True}))


def _capability(capability_id: str, *, validators: Optional[List[str]] = None, roles: Optional[List[str]] = None, composite: bool = False) -> Dict[str, Any]:
    inputs = CAPABILITY_INPUTS.get(capability_id, ["workflow_instance_id", "actor_reference", "invocation_id", "expected_active_version", "capability_specific_payload"])
    outputs = CAPABILITY_OUTPUTS.get(capability_id, ["capability_result", "events", "snapshot_reference"])
    events = COMPOSITE_EVENT_MAP.get(capability_id) if composite else PRIMITIVE_EVENT_MAP.get(capability_id, [f"ANDY.EVENT.{capability_id.split('.')[-1]}"])
    validator_ids = validators or ["ANDY.VAL.AUTHORITY", "ANDY.VAL.WORKFLOW", "ANDY.VAL.CONCURRENCY", "ANDY.VAL.EVENT_CONTRACT"]
    return {
        "capability_id": capability_id,
        "version": VERSION,
        "purpose": f"Execute {capability_id} within the Kernel-enforced ANDY lifecycle.",
        "inputs": inputs,
        "outputs": outputs,
        "preconditions": ["ANDY Domain Runtime active", "actor authorized", "workflow state permits capability", "concurrency requirement satisfied"],
        "postconditions": ["permitted mutations only", "declared events emitted", "successor Snapshot created when state mutates"],
        "permitted_mutations": sorted(["canonical_state_store", "event_store", "snapshot_store"] + (["artifact_receipt_store"] if capability_id == "ANDY.CAP.EXPORT_ARTIFACT_SET" else []) + (["workflow_instance_store"] if capability_id in {"ANDY.CAP.CREATE_WORKFLOW_INSTANCE", "ANDY.CAP.BLOCK_WORKFLOW", "ANDY.CAP.CLOSE_WORKFLOW", "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION", "ANDY.CAP.RESTORE_AS_NEW_VERSION"} else [])),
        "validator_ids": validator_ids,
        "authorization": {"roles": roles or COMMON_ROLES},
        "events_emitted": events,
        "failure_effect": "no_false_success_no_unpermitted_mutation_prior_state_preserved",
        "idempotency": {"required": True, "key": "invocation_id"},
        "concurrency_requirement": _concurrency_for(capability_id),
        "composite": composite,
        "body_authority": "model_defined_contract_runtime_enforced",
        "proof_requirement": "kernel_capability_enforced" if not composite else "kernel_capability_enforced_composite_orchestration",
    }


def build_model() -> Dict[str, Any]:
    capabilities: Dict[str, Any] = {}
    for cid in PRIMITIVE_CAPABILITY_IDS:
        validators = ["ANDY.VAL.AUTHORITY", "ANDY.VAL.WORKFLOW", "ANDY.VAL.CONCURRENCY", "ANDY.VAL.EVENT_CONTRACT"]
        if cid in {"ANDY.CAP.SUBMIT_STAGE_PROMPT", "ANDY.CAP.UPDATE_STAGE_PROMPT"}:
            validators += ["ANDY.VAL.STAGE_PROMPT", "ANDY.VAL.INTERACTION_ADAPTER"]
        if cid in {"ANDY.CAP.REGISTER_ARTIFACT", "ANDY.CAP.REVISE_ARTIFACT"}:
            validators += ["ANDY.VAL.ARTIFACT", "ANDY.VAL.ARTIFACT_BODY_RESOLUTION"]
        if cid in {"ANDY.CAP.ACCEPT_ARTIFACT", "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE"}:
            validators += ["ANDY.VAL.ACCEPTANCE", "ANDY.VAL.EVIDENCE", "ANDY.VAL.DEPENDENCY"]
        if cid == "ANDY.CAP.ATTACH_EVIDENCE_PACKET":
            validators += ["ANDY.VAL.EVIDENCE"]
        if cid == "ANDY.CAP.EXPORT_ARTIFACT_SET":
            validators += ["ANDY.VAL.EXPORT", "ANDY.VAL.FINAL_EXPORT_PROJECTION", "ANDY.VAL.ARTIFACT_SET_EXPORT", "ANDY.VAL.ARTIFACT_BODY_RESOLUTION", "ANDY.VAL.SNAPSHOT"]
        if cid in {"ANDY.CAP.RESTORE_AS_NEW_VERSION", "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION"}:
            validators += ["ANDY.VAL.SNAPSHOT"]
        capabilities[cid] = _capability(cid, validators=sorted(set(validators)), roles=ADMIN_ROLES if cid in {"ANDY.CAP.RESTORE_AS_NEW_VERSION", "ANDY.CAP.REOPEN_STAGE_AS_NEW_VERSION"} else COMMON_ROLES)
    for cid in COMPOSITE_CAPABILITY_IDS:
        roles = APPROVER_ROLES if cid == "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE" else COMMON_ROLES
        cap = _capability(cid, validators=["ANDY.VAL.AUTHORITY", "ANDY.VAL.COMPOSITE_OPERATION", "ANDY.VAL.WORKFLOW", "ANDY.VAL.CONCURRENCY", "ANDY.VAL.EVENT_CONTRACT"], roles=roles, composite=True)
        cap.update(COMPOSITE_CAPABILITY_CONTRACTS[cid])
        capabilities[cid] = cap
    event_definitions = {eid: _definition(eid, "event_definition", event_id=eid) for eid in EVENT_IDS}
    return {
        "domain_id": DOMAIN_ID,
        "version": VERSION,
        "awka_version": AWKA_VERSION,
        "entities": {eid: _definition(eid, "entity") for eid in ENTITY_IDS},
        "capabilities": capabilities,
        "validator_definitions": {vid: _definition(vid, "validator", order=i + 1, blocking=True) for i, vid in enumerate(VALIDATOR_IDS)},
        "renderer_definitions": {rid: _definition(rid, "renderer", tool_binding_id=TOOL_IDS[min(i, len(TOOL_IDS) - 1)]) for i, rid in enumerate(RENDERER_IDS)},
        "workflow_definitions": {PRIMARY_WORKFLOW_ID: {"workflow_id": PRIMARY_WORKFLOW_ID, "states": WORKFLOW_STATES, "transitions": [{"from_state": a, "to_state": b, "capability_id": c} for a, b, c in WORKFLOW_TRANSITIONS], "terminal_states": ["CLOSED", "BLOCKED"]}},
        "tool_bindings": {tid: _definition(tid, "tool_binding") for tid in TOOL_IDS},
        "schemas": {sid: _definition(sid, "schema") for sid in SCHEMA_IDS},
        "business_rules": [_definition(pid, "policy", rule_id=pid, validator_ids=POLICY_VALIDATOR_MAP.get(pid, ["ANDY.VAL.WORKFLOW"])) for pid in POLICY_IDS],
        "event_definitions": event_definitions,
        "interaction_contract": INTERACTION_ADAPTER_CONTRACT,
        "proof_classes": PROOF_CLASSES,
    }


MODEL = build_model()


def validate_model() -> Dict[str, Any]:
    _require(len(MODEL["entities"]) == 24, "Expected 24 entities")
    _require(len(MODEL["capabilities"]) == 30, "Expected 30 capabilities")
    _require(len([c for c in MODEL["capabilities"].values() if c.get("composite") is not True]) == 27, "Expected 27 primitives")
    _require(len([c for c in MODEL["capabilities"].values() if c.get("composite") is True]) == 3, "Expected 3 composites")
    _require(len(MODEL["validator_definitions"]) == 30, "Expected 30 validators")
    _require(len(MODEL["renderer_definitions"]) == 10, "Expected 10 renderers")
    _require(len(MODEL["tool_bindings"]) == 8, "Expected 8 tool bindings")
    _require(len(MODEL["schemas"]) == 11, "Expected 11 schemas")
    _require(len(MODEL["workflow_definitions"]) == 1, "Expected one workflow")
    workflow = MODEL["workflow_definitions"][PRIMARY_WORKFLOW_ID]
    _require(len(workflow["states"]) == 15, "Expected 15 workflow states")
    _require(len(workflow["transitions"]) == 25, "Expected 25 workflow transitions")
    _require(len(MODEL["business_rules"]) == 42, "Expected 42 policies")
    _require(len(MODEL["proof_classes"]) == 6, "Expected 6 proof classes")
    _require("ANDY.VAL.ACTIVATION_ADMISSION" in MODEL["validator_definitions"], "Activation admission validator missing")
    _require("ANDY.VAL.ARTIFACT_BODY_RESOLUTION" in MODEL["validator_definitions"], "Body resolver validator missing")
    _require("ANDY.VAL.EVENT_CONTRACT" in MODEL["validator_definitions"], "Event contract validator missing")
    _require("ANDY.VAL.ARTIFACT_SET_EXPORT" in MODEL["validator_definitions"], "Artifact set export validator missing")
    _require("ANDY.VAL.POLICY_VALIDATOR_MAPPING" in MODEL["validator_definitions"], "Policy mapping validator missing")
    for cid, cap in MODEL["capabilities"].items():
        missing = [field for field in CAPABILITY_CONTRACT_REQUIRED_FIELDS if field not in cap]
        _require(not missing, f"Capability {cid} missing fields: {missing}")
        _require(cap["inputs"], f"Capability {cid} missing inputs")
        _require(cap["outputs"], f"Capability {cid} missing outputs")
        _require(cap["events_emitted"], f"Capability {cid} missing events")
        for vid in cap["validator_ids"]:
            _require(vid in MODEL["validator_definitions"], f"Capability {cid} references missing validator {vid}")
        for eid in cap["events_emitted"]:
            _require(eid in MODEL["event_definitions"], f"Capability {cid} references missing event {eid}")
    for rule in MODEL["business_rules"]:
        for vid in rule["validator_ids"]:
            _require(vid in MODEL["validator_definitions"], f"Policy {rule['rule_id']} references missing validator {vid}")
    return {
        "domain_id": DOMAIN_ID,
        "version": VERSION,
        "awka_version": AWKA_VERSION,
        "entities": 24,
        "capabilities": 30,
        "primitive_capabilities": 27,
        "composite_capabilities": 3,
        "validators": 30,
        "renderers": 10,
        "workflows": 1,
        "workflow_states": 15,
        "workflow_transitions": 25,
        "rules": 42,
        "tools": 8,
        "schemas": 11,
        "event_definitions": len(MODEL["event_definitions"]),
        "proof_classes": 6,
        "adapter_contracts": 1,
        "capability_contracts_specific": True,
        "event_contract_equivalence_declared": True,
        "semantic_policy_validator_mapping_declared": True,
        "artifact_body_resolution_required": True,
        "artifact_set_export_required": True,
        "multi_stage_progression_required": True,
        "semantic_result_digest_required": True,
    }


def domain_descriptor() -> Dict[str, Any]:
    return {
        "domain_id": DOMAIN_ID,
        "domain_name": DOMAIN_NAME,
        "domain_full_name": DOMAIN_FULL_NAME,
        "domain_version": VERSION,
        "awka_version": AWKA_VERSION,
        "workflow_instance_type": WORKFLOW_INSTANCE_TYPE,
        "primary_workflow_definition_id": PRIMARY_WORKFLOW_ID,
        "activation_creates_workflow_instance": False,
        "composite_capabilities_enabled": True,
        "primitive_lifecycle_preserved": True,
        "kernel_enforcement_required": True,
        "activation_admission_report_required": True,
        "artifact_set_export_required": True,
        "artifact_body_resolution_required": True,
        "event_registry_awka4_projection_required": True,
        "semantic_result_digest_required": True,
    }


def release_contract() -> Dict[str, Any]:
    return {
        "uploaded_components": ["001_ANDY_Manifest_v1.0.0-alpha.7.json", "002_ANDY_Model_v1_0_0_alpha_7.py", "003_ANDY_Verification_v1_0_0_alpha_7.py"],
        "activation_directive_delivery": "current_user_message_or_optional_000_file",
        "activation_directive_is_file_component": False,
        "activation_directive_requires_sha256": False,
        "planned_install_prompt_file": "000_ANDY_Install_Prompt_v1.0.0-alpha.7.txt",
        "hashed_components": ["002_ANDY_Model_v1_0_0_alpha_7.py", "003_ANDY_Verification_v1_0_0_alpha_7.py"],
        "workflow_creation_during_activation": False,
        "source_packet_creation_during_activation": False,
        "canonical_state_creation_during_activation": False,
        "snapshot_creation_during_activation": False,
        "artifact_creation_during_activation": False,
        "composite_operation_run_creation_during_activation": False,
        "activation_admission_requires_real_conformance_report": True,
        "kernel_capability_execution_required_for_kernel_proof": True,
        "final_export_projection_qa_required": True,
        "artifact_set_export_required": True,
        "artifact_body_resolution_required": True,
        "event_registry_awka4_projection_required": True,
    }


def semantic_result_digest(report: Mapping[str, Any]) -> str:
    subset = {
        "verification_suite": report.get("verification_suite"),
        "domain_id": report.get("domain_id"),
        "version": report.get("version"),
        "awka_version": report.get("awka_version"),
        "declared_tests": report.get("declared_tests"),
        "executed_tests": report.get("executed_tests"),
        "required_failures": report.get("required_failures"),
        "status": report.get("status"),
        "model_sha256": report.get("model_sha256"),
        "verification_sha256": report.get("verification_sha256"),
        "test_ids": sorted([item.get("test_id") for item in report.get("results", [])]),
        "failed_ids": sorted([item.get("test_id") for item in report.get("results", []) if item.get("passed") is not True]),
        "proof_class_summary": report.get("proof_class_summary", {}),
        "scenario_summary": report.get("scenario_summary", {}),
    }
    return _digest(subset)


def validate_activation_report(report: Mapping[str, Any], manifest: Mapping[str, Any], expected_semantic_digest: Optional[str] = None) -> Dict[str, Any]:
    required_groups = set(manifest.get("verification_contract", {}).get("required_test_groups", []))
    groups = set(report.get("test_groups", []))
    failures = [item.get("test_id") for item in report.get("results", []) if item.get("passed") is not True]
    model_contract = next((c for c in manifest.get("component_contracts", []) if c.get("component_id") == "ANDY-MODEL"), {})
    verification_contract = next((c for c in manifest.get("component_contracts", []) if c.get("component_id") == "ANDY-VERIFICATION"), {})
    actual_semantic = semantic_result_digest(report)
    defects: List[str] = []
    checks = {
        "suite": report.get("verification_suite") == "ANDY-DOMAIN-ACTIVATION-CONFORMANCE",
        "domain": report.get("domain_id") == DOMAIN_ID,
        "version": report.get("version") == VERSION,
        "awka": report.get("awka_version") == AWKA_VERSION,
        "counts": report.get("declared_tests") == report.get("executed_tests"),
        "failures_zero": report.get("required_failures") == 0 and not failures,
        "status": report.get("status") == "PASS",
        "model_hash": model_contract.get("sha256", "<PENDING") == "<PENDING_UNTIL_002_FINALIZED>" or report.get("model_sha256") == model_contract.get("sha256"),
        "verification_hash": verification_contract.get("sha256", "<PENDING") == "<PENDING_UNTIL_003_FINALIZED>" or report.get("verification_sha256") == verification_contract.get("sha256"),
        "groups": required_groups.issubset(groups),
        "classification": all("proof_class" in item and "test_kind" in item for item in report.get("results", [])),
        "semantic_digest": expected_semantic_digest is None or actual_semantic == expected_semantic_digest,
    }
    for key, ok in checks.items():
        if not ok:
            defects.append(key)
    return {
        "activation_admission_report_id": "AAR-001",
        "validation_status": "PASS" if not defects else "FAIL",
        "defects": defects,
        "semantic_result_digest": actual_semantic,
        "required_groups_missing": sorted(required_groups - groups),
        "failed_result_ids": failures,
        "checks": checks,
    }


def _put(registry: Dict[str, Any], item_id: str, item: Any) -> None:
    _require(item_id not in registry, f"Duplicate definition {item_id}")
    registry[item_id] = copy.deepcopy(item)


def _register_candidate(kernel: Any, candidate_registries: Dict[str, Dict[str, Any]], registry_name: str, definition_id: str, definition: Any) -> str:
    if hasattr(kernel, "candidate_register"):
        kernel.candidate_register(candidate_registries, registry_name, definition_id, copy.deepcopy(definition))
        return "kernel.candidate_register"
    _put(candidate_registries[registry_name], definition_id, definition)
    return "compatibility_fallback_put"


def populate_candidate_registries(kernel: Any, candidate_registries: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    validate_model()
    paths: List[str] = []
    event_registry_catalog_projection = {
        "definition_id": "ANDY.SCHEMA.EVENT_REGISTRY_CATALOG",
        "kind": "event_registry_catalog_projection",
        "version": VERSION,
        "namespace": NAMESPACE_ROOT,
        "projection_target": "schema_registry",
        "awka_compatibility_target": AWKA_VERSION,
        "canonical_semantics": "ANDY.REGISTRY.EVENT",
        "event_definition_count": len(MODEL["event_definitions"]),
        "event_definitions": copy.deepcopy(MODEL["event_definitions"]),
        "semantic_preservation": {
            "event_identity_preserved": True,
            "capability_event_contracts_resolve_against_catalog": True,
            "runtime_event_records_remain_governed_by_ANDY_ENTITY_EVENT_RECORD": True,
            "no_first_class_event_registry_publication_for_awka_alpha_4": True,
        },
    }
    schemas_for_publication = copy.deepcopy(MODEL["schemas"])
    schemas_for_publication[event_registry_catalog_projection["definition_id"]] = event_registry_catalog_projection
    registry_plan = [
        ("entity_registry", MODEL["entities"]),
        ("capability_registry", MODEL["capabilities"]),
        ("validator_registry", MODEL["validator_definitions"]),
        ("renderer_registry", MODEL["renderer_definitions"]),
        ("workflow_registry", MODEL["workflow_definitions"]),
        ("tool_registry", MODEL["tool_bindings"]),
        ("schema_registry", schemas_for_publication),
    ]
    for registry_name, definitions in registry_plan:
        if registry_name not in candidate_registries:
            candidate_registries[registry_name] = {}
        for definition_id, definition in definitions.items():
            paths.append(_register_candidate(kernel, candidate_registries, registry_name, definition_id, definition))
    if "policy_registry" not in candidate_registries:
        candidate_registries["policy_registry"] = {}
    for rule in MODEL["business_rules"]:
        paths.append(_register_candidate(kernel, candidate_registries, "policy_registry", rule["rule_id"], rule))
    candidate_registries.setdefault("_andy_registration_diagnostics", {})["candidate_registration_path"] = sorted(set(paths))
    return candidate_registries


def _empty_state(workflow_instance_id: str) -> Dict[str, Any]:
    return {
        "workflow_instance_id": workflow_instance_id,
        "workflow_instance_type": WORKFLOW_INSTANCE_TYPE,
        "current_state": "UNINITIALIZED",
        "previous_state": None,
        "active_version": 1,
        "narrative": None,
        "stage_order": [],
        "current_stage_id": None,
        "stage_records": {},
        "stage_prompt_versions": {},
        "active_prompt_version_by_stage": {},
        "artifact_slots": {},
        "slot_dispositions": {},
        "artifact_registrations": {},
        "artifact_versions": {},
        "accepted_artifacts": {},
        "rejection_records": {},
        "evidence_packets": {},
        "dependency_edges": {},
        "artifact_receipts": {},
        "artifact_set_receipts": {},
        "artifact_sets": {},
        "artifact_body_resolution_records": {},
        "export_projection_qas": {},
        "adapter_route_evidence_records": {},
        "composite_operation_runs": {},
        "snapshots": {},
        "draft_artifacts": {},
        "events": [],
        "invocation_history": {},
        "workflow_status": "initialized",
        "logical_sequence": 0,
    }


def _next_sequence(state: Dict[str, Any]) -> int:
    state["logical_sequence"] = int(state.get("logical_sequence", 0)) + 1
    return state["logical_sequence"]


def _emit(state: Dict[str, Any], event_id: str, **payload: Any) -> None:
    _require(event_id in MODEL["event_definitions"], f"Unregistered event {event_id}")
    seq = _next_sequence(state)
    state.setdefault("events", []).append({"event_id": event_id, "sequence": seq, "payload": _canonical(payload)})


def snapshot_state(state: Mapping[str, Any], snapshot_reason: str = "successor") -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    st_no_snapshots = copy.deepcopy(st)
    st_no_snapshots["snapshots"] = {}
    digest = _digest(st_no_snapshots)
    snapshot_id = f"{st['workflow_instance_id']}-SNAP-{st['active_version']:06d}"
    snapshot = {
        "snapshot_id": snapshot_id,
        "workflow_instance_id": st["workflow_instance_id"],
        "active_version": st["active_version"],
        "current_state": st["current_state"],
        "snapshot_reason": snapshot_reason,
        "canonical_state_digest": digest,
        "canonical_state": st_no_snapshots,
    }
    return snapshot


def _store_snapshot(state: Dict[str, Any], reason: str) -> None:
    snap = snapshot_state(state, reason)
    state.setdefault("snapshots", {})[snap["snapshot_id"]] = snap
    _emit(state, "ANDY.EVENT.SNAPSHOT_CREATED", snapshot_id=snap["snapshot_id"], snapshot_digest=snap["canonical_state_digest"])


def _bump(state: Dict[str, Any], new_state: str, event_id: Optional[str] = None, **event_payload: Any) -> Dict[str, Any]:
    state["previous_state"] = state.get("current_state")
    state["current_state"] = new_state
    state["active_version"] = int(state.get("active_version", 1)) + 1
    if event_id:
        _emit(state, event_id, **event_payload)
    _store_snapshot(state, reason=f"transition_to_{new_state}")
    return state


def new_workflow_state(workflow_instance_id: str) -> Dict[str, Any]:
    st = _empty_state(workflow_instance_id)
    _emit(st, "ANDY.EVENT.WORKFLOW_INSTANCE_CREATED", workflow_instance_id=workflow_instance_id)
    _store_snapshot(st, "workflow_instance_created")
    return st


def create_workflow_instance_state(workflow_instance_id: str) -> Dict[str, Any]:
    return new_workflow_state(workflow_instance_id)


def load_narrative(state: Mapping[str, Any], narrative_id: str, stages: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "UNINITIALIZED", "Load narrative requires UNINITIALIZED")
    _require(stages, "Narrative requires at least one stage")
    ids = [str(stage["stage_id"]) for stage in stages]
    _require(len(ids) == len(set(ids)), "Duplicate stage ids")
    st["narrative"] = {"narrative_id": narrative_id, "linear_stage_order": ids}
    st["stage_order"] = ids
    st["current_stage_id"] = ids[0]
    for order, stage in enumerate(stages, start=1):
        stage_id = str(stage["stage_id"])
        slots = list(stage.get("artifact_slots", []))
        st["stage_records"][stage_id] = {
            "stage_record_id": f"STR-{stage_id}",
            "stage_id": stage_id,
            "stage_order": order,
            "stage_status": "narrative_loaded",
            "active_prompt_version_id": None,
            "review_status": "not_open",
            "required_slot_count": sum(1 for slot in slots if slot.get("required", True)),
            "resolved_required_slot_count": 0,
            "optional_slot_count": sum(1 for slot in slots if not slot.get("required", True)),
            "resolved_optional_slot_count": 0,
            "completion_confirmed": False,
        }
        for slot in slots:
            slot_id = str(slot["artifact_slot_id"])
            st["artifact_slots"][slot_id] = {
                "stage_id": stage_id,
                "artifact_slot_id": slot_id,
                "required": bool(slot.get("required", True)),
                "slot_name": slot.get("slot_name", slot_id),
                "allowed_artifact_types": list(slot.get("allowed_artifact_types", [])),
                "disallowed_artifact_types": list(slot.get("disallowed_artifact_types", [])),
            }
            st["slot_dispositions"][slot_id] = {
                "slot_disposition_id": f"DSP-{slot_id}",
                "stage_id": stage_id,
                "artifact_slot_id": slot_id,
                "disposition": "unresolved",
                "resolved_by_artifact_version_id": None,
                "resolved_by_evidence_packet_id": None,
                "dependency_eligible": False,
            }
    return _bump(st, "NARRATIVE_LOADED", "ANDY.EVENT.NARRATIVE_LOADED", narrative_id=narrative_id)


def validate_narrative_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "NARRATIVE_LOADED", "Validate narrative requires NARRATIVE_LOADED")
    for stage_id in st["stage_order"]:
        st["stage_records"][stage_id]["stage_status"] = "stage_ready" if stage_id == st["current_stage_id"] else "waiting"
    return _bump(st, "STAGE_READY", "ANDY.EVENT.NARRATIVE_VALIDATED", current_stage_id=st["current_stage_id"])


def record_adapter_route_evidence(state: Dict[str, Any], command_pattern_id: str, matched_route: str, capability_id: Optional[str], stage_id: Optional[str], payload: Any, raw_message: str = "") -> str:
    evidence_id = f"ARE-{len(state.setdefault('adapter_route_evidence_records', {})) + 1:06d}"
    record = {
        "adapter_route_evidence_id": evidence_id,
        "message_digest": _digest(raw_message),
        "command_pattern_id": command_pattern_id,
        "matched_route": matched_route,
        "capability_id": capability_id,
        "stage_id": stage_id,
        "slot_id": payload.get("slot_id") if isinstance(payload, Mapping) else None,
        "actor_reference": "authorized_human",
        "invocation_id": evidence_id,
        "created_sequence": _next_sequence(state),
        "payload_digest": _digest(payload),
        "route_status": "mutating" if capability_id else "non_mutating",
    }
    state["adapter_route_evidence_records"][evidence_id] = record
    _emit(state, "ANDY.EVENT.ADAPTER_ROUTE_EVIDENCE_RECORDED", adapter_route_evidence_id=evidence_id)
    return evidence_id


def submit_stage_prompt_state(state: Mapping[str, Any], stage_id: str, prompt_text: str, adapter_route_evidence_id: Optional[str] = None) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "STAGE_READY", "Submit prompt requires STAGE_READY")
    _require(stage_id == st["current_stage_id"], "Wrong stage")
    _require(bool(prompt_text.strip()), "Prompt cannot be empty")
    if adapter_route_evidence_id is None:
        adapter_route_evidence_id = record_adapter_route_evidence(st, "submit_stage_prompt", "primitive_submit_stage_prompt", "ANDY.CAP.SUBMIT_STAGE_PROMPT", stage_id, {"prompt_digest": _digest(prompt_text)}, raw_message=prompt_text)
    count = len([p for p in st["stage_prompt_versions"] if p.startswith(f"PRM-{stage_id}")]) + 1
    prompt_id = f"PRM-{stage_id}-{count:03d}"
    st["stage_prompt_versions"][prompt_id] = {
        "stage_prompt_version_id": prompt_id,
        "stage_id": stage_id,
        "prompt_version_number": count,
        "prompt_digest": _digest(prompt_text),
        "prompt_status": "active",
        "active_for_generation": True,
        "adapter_route_evidence_id": adapter_route_evidence_id,
    }
    st["active_prompt_version_by_stage"][stage_id] = prompt_id
    st["stage_records"][stage_id]["active_prompt_version_id"] = prompt_id
    return _bump(st, "PROMPT_SUBMITTED", "ANDY.EVENT.STAGE_PROMPT_SUBMITTED", stage_id=stage_id, prompt_version_id=prompt_id)


def execute_stage_state(state: Mapping[str, Any], draft_text: Optional[str] = None) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "PROMPT_SUBMITTED", "Execute requires PROMPT_SUBMITTED")
    stage_id = st["current_stage_id"]
    text = draft_text or "ANDY Draft Artifact\nArtifact status: Draft candidate for stage review; not accepted, evidenced, or dependency-eligible.\nBody: generated draft content.\nTo make it dependency-eligible, run acceptance with evidence."
    digest = _digest(text)
    st["draft_artifacts"]["DRAFT-ART-001"] = {
        "artifact_ref": "DRAFT-ART-001.txt",
        "artifact_body_inline_demo_cache": text,
        "artifact_body_inline_demo_cache_is_authoritative": False,
        "artifact_digest": digest,
        "artifact_status": "draft",
        "dependency_eligible": False,
        "stage_id": stage_id,
        "slot_id": next((slot_id for slot_id, slot in st["artifact_slots"].items() if slot["stage_id"] == stage_id), None),
    }
    st["stage_records"][stage_id]["stage_status"] = "stage_executing"
    return _bump(st, "STAGE_EXECUTING", "ANDY.EVENT.STAGE_EXECUTED", stage_id=stage_id)


def open_stage_review_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "STAGE_EXECUTING", "Open review requires STAGE_EXECUTING")
    st["stage_records"][st["current_stage_id"]]["review_status"] = "active"
    return _bump(st, "STAGE_REVIEW_ACTIVE", "ANDY.EVENT.STAGE_REVIEW_OPENED", stage_id=st["current_stage_id"])


def _artifact_body_ref_for(artifact_id: str, artifact_version_id: str, artifact_ref: Optional[str]) -> str:
    return artifact_ref or f"andy-artifact://{artifact_id}/{artifact_version_id}"


def register_artifact_state(state: Mapping[str, Any], artifact_id: str, artifact_version_id: str, slot_id: str, digest: str, artifact_body: Optional[str] = None, artifact_ref: Optional[str] = None, media_type: str = "text/plain", storage_class: str = "demo_inline_cache") -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "STAGE_REVIEW_ACTIVE", "Register requires STAGE_REVIEW_ACTIVE")
    _require(slot_id in st["artifact_slots"], "Unknown slot")
    stage_id = st["artifact_slots"][slot_id]["stage_id"]
    body = artifact_body or st.get("draft_artifacts", {}).get("DRAFT-ART-001", {}).get("artifact_body_inline_demo_cache", "")
    ref = _artifact_body_ref_for(artifact_id, artifact_version_id, artifact_ref or st.get("draft_artifacts", {}).get("DRAFT-ART-001", {}).get("artifact_ref"))
    _require(not body or _digest(body) == digest, "Artifact digest must match provided body in demo mode")
    st["artifact_registrations"][artifact_id] = {"artifact_id": artifact_id, "artifact_slot_id": slot_id, "stage_id": stage_id, "artifact_ref": ref, "artifact_title": artifact_id}
    st["artifact_versions"][artifact_version_id] = {
        "artifact_version_id": artifact_version_id,
        "artifact_id": artifact_id,
        "stage_id": stage_id,
        "artifact_slot_id": slot_id,
        "artifact_status": "registered",
        "artifact_digest": digest,
        "dependency_eligible": False,
        "artifact_body_ref": ref,
        "artifact_media_type": media_type,
        "artifact_size_bytes": len(body.encode("utf-8")) if body else 0,
        "artifact_storage_class": storage_class,
        "artifact_body_inline_demo_cache": body,
        "artifact_body_inline_demo_cache_is_authoritative": False,
        "acceptance_statement": None,
    }
    _emit(st, "ANDY.EVENT.ARTIFACT_REGISTERED", artifact_version_id=artifact_version_id, slot_id=slot_id)
    return st


def accept_artifact_state(state: Mapping[str, Any], artifact_version_id: str, acceptance_statement: str = "I accept this artifact.") -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(artifact_version_id in st["artifact_versions"], "Artifact version missing")
    art = st["artifact_versions"][artifact_version_id]
    _require(art["artifact_status"] == "registered", "Artifact must be registered")
    accepted_id = f"ACC-{artifact_version_id}"
    art["artifact_status"] = "accepted_pending_evidence"
    art["acceptance_statement"] = acceptance_statement
    art["dependency_eligible"] = False
    st["accepted_artifacts"][accepted_id] = {"accepted_artifact_id": accepted_id, "artifact_version_id": artifact_version_id, "stage_id": art["stage_id"], "acceptance_status": "accepted_pending_evidence", "evidence_packet_id": None, "dependency_eligible": False}
    _emit(st, "ANDY.EVENT.ARTIFACT_ACCEPTED_PENDING_EVIDENCE", artifact_version_id=artifact_version_id, accepted_artifact_id=accepted_id)
    return st


def attach_evidence_packet_state(state: Mapping[str, Any], accepted_artifact_id: str, evidence_packet_id: str, source_inputs: str = "declared evidence") -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(accepted_artifact_id in st["accepted_artifacts"], "Accepted artifact missing")
    acc = st["accepted_artifacts"][accepted_artifact_id]
    art = st["artifact_versions"][acc["artifact_version_id"]]
    st["evidence_packets"][evidence_packet_id] = {"evidence_packet_id": evidence_packet_id, "accepted_artifact_id": accepted_artifact_id, "artifact_version_id": art["artifact_version_id"], "validation_status": "valid", "dependency_eligibility_result": "eligible", "source_inputs": source_inputs, "approval_statement": art.get("acceptance_statement"), "artifact_ref": art["artifact_body_ref"], "artifact_digest": art["artifact_digest"]}
    acc["evidence_packet_id"] = evidence_packet_id
    _emit(st, "ANDY.EVENT.EVIDENCE_PACKET_ATTACHED", accepted_artifact_id=accepted_artifact_id, evidence_packet_id=evidence_packet_id)
    return st


def promote_artifact_dependency_eligible_state(state: Mapping[str, Any], accepted_artifact_id: str) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(accepted_artifact_id in st["accepted_artifacts"], "Accepted artifact missing")
    acc = st["accepted_artifacts"][accepted_artifact_id]
    _require(acc.get("evidence_packet_id") in st["evidence_packets"], "Evidence required")
    art = st["artifact_versions"][acc["artifact_version_id"]]
    art["artifact_status"] = "accepted_dependency_eligible"
    art["dependency_eligible"] = True
    acc["acceptance_status"] = "accepted_dependency_eligible"
    acc["dependency_eligible"] = True
    slot_id = art["artifact_slot_id"]
    st["slot_dispositions"][slot_id].update({"disposition": "satisfied", "resolved_by_artifact_version_id": art["artifact_version_id"], "resolved_by_evidence_packet_id": acc["evidence_packet_id"], "dependency_eligible": True})
    stage_id = art["stage_id"]
    st["stage_records"][stage_id]["resolved_required_slot_count"] = sum(1 for disp in st["slot_dispositions"].values() if disp["stage_id"] == stage_id and st["artifact_slots"][disp["artifact_slot_id"]]["required"] and disp["disposition"] == "satisfied")
    _emit(st, "ANDY.EVENT.ARTIFACT_DEPENDENCY_ELIGIBLE", artifact_version_id=art["artifact_version_id"], accepted_artifact_id=accepted_artifact_id)
    return st


def evaluate_stage_completion_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "STAGE_REVIEW_ACTIVE", "Evaluate requires STAGE_REVIEW_ACTIVE")
    stage_id = st["current_stage_id"]
    for slot_id, slot in st["artifact_slots"].items():
        if slot["stage_id"] == stage_id and slot["required"]:
            _require(st["slot_dispositions"][slot_id]["disposition"] == "satisfied", f"Required slot unresolved: {slot_id}")
    return _bump(st, "STAGE_COMPLETION_PENDING", "ANDY.EVENT.STAGE_COMPLETION_EVALUATED", stage_id=stage_id)


def confirm_stage_complete_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "STAGE_COMPLETION_PENDING", "Confirm requires STAGE_COMPLETION_PENDING")
    stage_id = st["current_stage_id"]
    st["stage_records"][stage_id]["stage_status"] = "stage_complete_confirmed"
    st["stage_records"][stage_id]["completion_confirmed"] = True
    return _bump(st, "STAGE_COMPLETE_CONFIRMED", "ANDY.EVENT.STAGE_COMPLETION_CONFIRMED", stage_id=stage_id)


def advance_stage_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "STAGE_COMPLETE_CONFIRMED", "Advance requires STAGE_COMPLETE_CONFIRMED")
    stage_id = st["current_stage_id"]
    st["stage_records"][stage_id]["stage_status"] = "stage_advanced"
    st["stage_records"][stage_id]["review_status"] = "closed"
    order = st["stage_order"]
    idx = order.index(stage_id)
    st = _bump(st, "STAGE_ADVANCED", "ANDY.EVENT.STAGE_ADVANCED", stage_id=stage_id)
    if idx + 1 < len(order):
        next_stage_id = order[idx + 1]
        st["current_stage_id"] = next_stage_id
        st["stage_records"][next_stage_id]["stage_status"] = "stage_ready"
        st = _bump(st, "STAGE_READY", "ANDY.EVENT.NEXT_STAGE_READY", stage_id=next_stage_id)
    else:
        st["workflow_status"] = "workflow_complete"
        st = _bump(st, "WORKFLOW_COMPLETE", "ANDY.EVENT.WORKFLOW_COMPLETE", completed_stage_ids=list(order))
    return st


def finalize_workflow_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "WORKFLOW_COMPLETE", "Finalize requires WORKFLOW_COMPLETE")
    for stage_id in st["stage_order"]:
        rec = st["stage_records"][stage_id]
        _require(rec["stage_status"] == "stage_advanced", f"Stage not advanced: {stage_id}")
        _require(rec["completion_confirmed"] is True, f"Stage not confirmed: {stage_id}")
    eligible = sorted([vid for vid, art in st["artifact_versions"].items() if art.get("dependency_eligible")])
    _require(eligible, "No eligible artifacts")
    st["finalization_record"] = {"finalization_record_id": f"FIN-{st['workflow_instance_id']}-001", "workflow_instance_id": st["workflow_instance_id"], "finalization_status": "finalized", "completed_stage_ids": list(st["stage_order"]), "accepted_dependency_eligible_artifact_versions": eligible, "evidence_packet_ids": sorted(st["evidence_packets"]), "finalization_statement": "All linear stages complete; accepted artifact set is ready for export."}
    st["workflow_status"] = "final_export_ready"
    return _bump(st, "FINAL_EXPORT_READY", "ANDY.EVENT.WORKFLOW_FINALIZED", artifact_version_ids=eligible)


def resolve_artifact_body(artifact_version: Mapping[str, Any], resolver_context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    storage_class = artifact_version.get("artifact_storage_class")
    body_ref = artifact_version.get("artifact_body_ref")
    expected = artifact_version.get("artifact_digest")
    body = ""
    method = "unresolved"
    diagnostic = ""
    if resolver_context and body_ref in resolver_context.get("external_bodies", {}):
        raw = resolver_context["external_bodies"][body_ref]
        body = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        method = "external_reference"
    elif storage_class == "demo_inline_cache":
        body = str(artifact_version.get("artifact_body_inline_demo_cache", ""))
        method = "demo_inline_cache"
    else:
        diagnostic = "No resolver path available."
    resolved = _digest(body) if body else ""
    status = "PASS" if body_ref and body and resolved == expected else "FAIL"
    if status == "FAIL" and not diagnostic:
        diagnostic = "Artifact body resolution failed or digest mismatch."
    return {"body_resolution_record_id": f"BRR-{artifact_version.get('artifact_version_id')}", "artifact_version_id": artifact_version.get("artifact_version_id"), "artifact_body_ref": body_ref, "resolution_method": method, "resolved_body": body, "expected_digest": expected, "resolved_digest": resolved, "media_type": artifact_version.get("artifact_media_type"), "size_bytes": len(body.encode("utf-8")), "resolution_status": status, "diagnostic": diagnostic}


def _project_artifact_body_for_final_export(source_text: str) -> str:
    kept: List[str] = []
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        if line == "ANDY Draft Artifact" or line.startswith("Artifact status:") or line.startswith("To make it dependency-eligible"):
            continue
        if line.startswith("Body:"):
            kept.append(raw_line.split("Body:", 1)[1].strip())
        else:
            kept.append(raw_line)
    return "\n".join(line for line in kept if line.strip()).strip()


def render_final_export_projection(members: Sequence[Mapping[str, Any]], metadata: Mapping[str, Any]) -> str:
    lines = [
        "ANDY Final Export",
        f"Workflow Instance: {metadata['workflow_instance_id']}",
        f"Artifact Set: {metadata['artifact_set_id']}",
        f"Artifact Receipt: {metadata['artifact_set_receipt_id']}",
        "Artifact Status: accepted_dependency_eligible",
        "Export Status: EXPORTED",
        "Renderer: ANDY.RENDER.FINAL_ARTIFACT_SET",
        "",
        "Lifecycle Projection:",
        "- Projection method: structured_lifecycle_metadata_projection",
        "- Global body rewrite: false",
        "",
        "Artifact Set Members:",
    ]
    for member in members:
        lines += [
            f"- Artifact Version: {member['artifact_version_id']}",
            f"  Accepted Artifact: {member['accepted_artifact_id']}",
            f"  Evidence Packet: {member['evidence_packet_id']}",
            "  Artifact Body Projection:",
            f"  {member['artifact_body_projection']}",
        ]
    lines += ["", "Renderer Metadata:", "- Renderer ID: ANDY.RENDER.FINAL_ARTIFACT_SET", f"- Package Digest: {metadata['package_digest']}"]
    return "\n".join(lines) + "\n"


def validate_final_export_projection(projection_text: str, metadata: Mapping[str, Any]) -> Dict[str, Any]:
    forbidden = [phrase for phrase in FORBIDDEN_FINAL_EXPORT_PHRASES if phrase in projection_text]
    missing = [field for field in FINAL_EXPORT_REQUIRED_VISIBLE_FIELDS if field not in projection_text]
    visible_ok = "Artifact Status: accepted_dependency_eligible" in projection_text and "Export Status: EXPORTED" in projection_text
    body_rewrite_ok = "Global body rewrite: false" in projection_text
    lifecycle_ok = "Projection method: structured_lifecycle_metadata_projection" in projection_text
    qa_status = "PASS" if not forbidden and not missing and visible_ok and body_rewrite_ok and lifecycle_ok else "FAIL"
    qa = {"export_projection_qa_id": metadata.get("export_projection_qa_id", "EPQA-001"), "workflow_instance_id": metadata["workflow_instance_id"], "artifact_set_id": metadata["artifact_set_id"], "artifact_version_ids": metadata["artifact_version_ids"], "accepted_artifact_ids": metadata["accepted_artifact_ids"], "evidence_packet_ids": metadata["evidence_packet_ids"], "artifact_receipt_ids": metadata["artifact_receipt_ids"], "source_artifact_digests": metadata["source_artifact_digests"], "exported_artifact_digest": _digest(projection_text), "forbidden_phrase_scan_result": "PASS" if not forbidden else {"FAIL": forbidden}, "visible_status_match_result": "PASS" if visible_ok else "FAIL", "required_lineage_fields_present": "PASS" if not missing else {"FAIL": missing}, "body_rewrite_policy_result": "PASS" if body_rewrite_ok else "FAIL", "lifecycle_projection_result": "PASS" if lifecycle_ok else "FAIL", "qa_status": qa_status, "diagnostic": "" if qa_status == "PASS" else "Final export projection QA failed."}
    _require(set(EXPORT_PROJECTION_QA_REQUIRED_FIELDS).issubset(qa), "QA fields missing")
    return qa


def export_artifact_set_state(state: Mapping[str, Any], output_reference: str = "ANDY_Final_Artifact_Set.txt", resolver_context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "FINAL_EXPORT_READY", "Export requires FINAL_EXPORT_READY")
    snapshot = snapshot_state(st, "selected_for_export")
    selected_snapshot_digest = snapshot["canonical_state_digest"]
    artifact_version_ids = list(st["finalization_record"]["accepted_dependency_eligible_artifact_versions"])
    _require(artifact_version_ids, "No artifact-set members")
    artifact_set_id = f"ARTSET-{st['workflow_instance_id']}-001"
    members = []
    member_receipt_ids = []
    for idx, artifact_version_id in enumerate(artifact_version_ids, start=1):
        art = st["artifact_versions"][artifact_version_id]
        accepted_id = f"ACC-{artifact_version_id}"
        acc = st["accepted_artifacts"][accepted_id]
        evidence_id = acc["evidence_packet_id"]
        resolution = resolve_artifact_body(art, resolver_context)
        _require(resolution["resolution_status"] == "PASS", f"Body resolution failed for {artifact_version_id}: {resolution['diagnostic']}")
        st["artifact_body_resolution_records"][resolution["body_resolution_record_id"]] = {k: v for k, v in resolution.items() if k != "resolved_body"}
        _emit(st, "ANDY.EVENT.ARTIFACT_BODY_RESOLVED", artifact_version_id=artifact_version_id, resolution_method=resolution["resolution_method"])
        body_projection = _project_artifact_body_for_final_export(resolution["resolved_body"])
        member_digest = _digest({"artifact_version_id": artifact_version_id, "body_projection": body_projection})
        receipt_id = f"RCPT-{st['workflow_instance_id']}-{idx:04d}"
        receipt = {"artifact_receipt_id": receipt_id, "workflow_instance_id": st["workflow_instance_id"], "selected_snapshot_id": snapshot["snapshot_id"], "selected_snapshot_digest": selected_snapshot_digest, "artifact_name_or_reference": output_reference, "source_artifact_reference": art["artifact_body_ref"], "source_artifact_digest": art["artifact_digest"], "source_artifact_status_at_export": art["artifact_status"], "artifact_version_id": artifact_version_id, "accepted_artifact_id": accepted_id, "evidence_packet_id": evidence_id, "exported_artifact_digest": member_digest, "final_projection_digest": member_digest, "final_projection_status": "structured_member_projection", "export_projection_qa_result": "PASS", "renderer_id": "ANDY.RENDER.FINAL_ARTIFACT_SET", "renderer_version": VERSION, "selected_workflow_version": st["active_version"], "active_version_at_request": st["active_version"], "export_format": "TEXT", "validation_or_QA_result": "PASS: member body resolved and projected", "operation_status": "accepted", "export_status": "EXPORTED", "export_timestamp": "logical_time_not_wall_clock", "body_resolution_method": resolution["resolution_method"], "body_resolution_digest": resolution["resolved_digest"], "body_resolution_status": resolution["resolution_status"]}
        missing = [field for field in ARTIFACT_RECEIPT_REQUIRED_FIELDS if field not in receipt]
        _require(not missing, f"Member receipt missing fields: {missing}")
        st["artifact_receipts"][receipt_id] = receipt
        member_receipt_ids.append(receipt_id)
        members.append({"artifact_version_id": artifact_version_id, "accepted_artifact_id": accepted_id, "evidence_packet_id": evidence_id, "source_artifact_digest": art["artifact_digest"], "exported_member_digest": member_digest, "member_receipt_id": receipt_id, "artifact_body_projection": body_projection})
    ordered_member_manifest_digest = _digest(members)
    package_digest = _digest({"artifact_set_id": artifact_set_id, "members": members, "selected_snapshot_digest": selected_snapshot_digest})
    aggregate_receipt_id = f"RCPT-{st['workflow_instance_id']}-ARTSET-0001"
    aggregate_receipt = {"artifact_set_receipt_id": aggregate_receipt_id, "workflow_instance_id": st["workflow_instance_id"], "selected_snapshot_id": snapshot["snapshot_id"], "selected_snapshot_digest": selected_snapshot_digest, "artifact_set_id": artifact_set_id, "member_receipt_ids": member_receipt_ids, "ordered_member_manifest_digest": ordered_member_manifest_digest, "package_digest": package_digest, "renderer_id": "ANDY.RENDER.FINAL_ARTIFACT_SET", "renderer_version": VERSION, "export_status": "EXPORTED", "operation_status": "accepted", "export_timestamp": "logical_time_not_wall_clock"}
    missing_set = [field for field in ARTIFACT_SET_RECEIPT_REQUIRED_FIELDS if field not in aggregate_receipt]
    _require(not missing_set, f"Aggregate receipt missing fields: {missing_set}")
    st["artifact_set_receipts"][aggregate_receipt_id] = aggregate_receipt
    st["artifact_sets"][artifact_set_id] = {"artifact_set_id": artifact_set_id, "workflow_instance_id": st["workflow_instance_id"], "selected_snapshot_id": snapshot["snapshot_id"], "selected_snapshot_digest": selected_snapshot_digest, "members": members, "excluded_candidates": [], "aggregate_receipt_id": aggregate_receipt_id, "package_digest": package_digest}
    metadata = {"workflow_instance_id": st["workflow_instance_id"], "artifact_set_id": artifact_set_id, "artifact_set_receipt_id": aggregate_receipt_id, "artifact_version_ids": artifact_version_ids, "accepted_artifact_ids": [m["accepted_artifact_id"] for m in members], "evidence_packet_ids": [m["evidence_packet_id"] for m in members], "artifact_receipt_ids": member_receipt_ids, "source_artifact_digests": [m["source_artifact_digest"] for m in members], "package_digest": package_digest, "export_projection_qa_id": f"EPQA-{st['workflow_instance_id']}-001"}
    final_text = render_final_export_projection(members, metadata)
    qa = validate_final_export_projection(final_text, metadata)
    _require(qa["qa_status"] == "PASS", "Final projection QA failed")
    st["export_projection_qas"][qa["export_projection_qa_id"]] = qa
    st["exported_artifacts"] = {output_reference: final_text}
    st["workflow_status"] = "exported"
    _emit(st, "ANDY.EVENT.ARTIFACT_SET_RECEIPT_CREATED", artifact_set_receipt_id=aggregate_receipt_id)
    return _bump(st, "EXPORTED", "ANDY.EVENT.ARTIFACT_SET_EXPORTED", artifact_set_id=artifact_set_id, package_digest=package_digest)


def close_workflow_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] == "EXPORTED", "Close requires EXPORTED")
    _require(st.get("artifact_set_receipts"), "Artifact set receipt required before close")
    st["closure_record"] = {"closure_record_id": f"CLOSE-{st['workflow_instance_id']}-001", "workflow_instance_id": st["workflow_instance_id"], "closure_status": "closed", "closure_reason": "Workflow finalized and artifact set exported successfully.", "artifact_set_receipt_ids": sorted(st["artifact_set_receipts"].keys())}
    st["workflow_status"] = "closed"
    return _bump(st, "CLOSED", "ANDY.EVENT.WORKFLOW_CLOSED")


def serialize_runtime_state(state: Mapping[str, Any]) -> Dict[str, Any]:
    canonical = copy.deepcopy(dict(state))
    snapshot = snapshot_state(canonical, "serialization")
    summary = {"kernel_state": "ACTIVE", "domain_state": "DOMAIN_ACTIVE", "workflow_instance_id": canonical["workflow_instance_id"], "previous_state": canonical.get("previous_state"), "current_state": canonical["current_state"], "workflow_status": canonical.get("workflow_status"), "active_version": canonical["active_version"], "snapshot_id": snapshot["snapshot_id"], "snapshot_digest": snapshot["canonical_state_digest"], "next_registered_workflow_command": None if canonical["current_state"] == "CLOSED" else "TBD", "andy_events": list(canonical.get("events", []))}
    _require(summary["active_version"] == canonical["active_version"], "active_version mismatch")
    _require(summary["current_state"] == canonical["current_state"], "current_state mismatch")
    for rec in canonical.get("stage_records", {}).values():
        if rec.get("stage_status") == "stage_advanced":
            _require(rec.get("review_status") == "closed", "advanced stage review must be closed")
    return {"snapshot": summary, "canonical_state": canonical, "complete_snapshot": snapshot}


def active_context(state: Mapping[str, Any]) -> Dict[str, Any]:
    st = dict(state)
    return {"workflow_instance_id": st["workflow_instance_id"], "eligible_artifact_versions": sorted([vid for vid, art in st.get("artifact_versions", {}).items() if art.get("dependency_eligible")]), "evidence_packets": sorted(st.get("evidence_packets", {}).keys())}


def _record_composite_operation(state: Dict[str, Any], capability_id: str, stage_id: Optional[str], completed_steps: Sequence[str], failed_step: Optional[str], status: str, diagnostic: str = "") -> Dict[str, Any]:
    _require(status in COMPOSITE_OPERATION_STATUSES, "Invalid composite status")
    oid = f"CMPOP-{len(state.setdefault('composite_operation_runs', {})) + 1:03d}"
    contract = COMPOSITE_CAPABILITY_CONTRACTS[capability_id]
    state["composite_operation_runs"][oid] = {"composite_operation_id": oid, "workflow_instance_id": state.get("workflow_instance_id"), "stage_id": stage_id, "composite_capability_id": capability_id, "invocation_id": oid, "actor_reference": "authorized_human", "primitive_sequence": list(contract["primitive_sequence"]), "completed_steps": list(completed_steps), "failed_step": failed_step, "operation_status": status, "partial_commit_policy": contract.get("partial_commit_policy", contract.get("commit_policy")), "rollback_policy": contract.get("rollback_policy", "preserve_successful_prior_steps_and_report_failed_step"), "candidate_validation_result": "pass" if status == "committed" else "fail" if status.startswith("failed") else "not_applicable", "correlation_id": oid, "started_sequence": _next_sequence(state), "completed_sequence": _next_sequence(state), "diagnostic": diagnostic}
    return state


def adopt_narrative_state(state: Mapping[str, Any], narrative_id: str, stages: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    st = dict(state)
    _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_STARTED", capability_id="ANDY.CAP.ADOPT_NARRATIVE")
    new_state = validate_narrative_state(load_narrative(st, narrative_id, stages))
    _emit(new_state, "ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED", capability_id="ANDY.CAP.ADOPT_NARRATIVE")
    return _record_composite_operation(new_state, "ANDY.CAP.ADOPT_NARRATIVE", new_state.get("current_stage_id"), COMPOSITE_CAPABILITY_CONTRACTS["ANDY.CAP.ADOPT_NARRATIVE"]["primitive_sequence"], None, "committed")


def run_stage_to_review_state(state: Mapping[str, Any], stage_id: str, prompt_text: str, draft_text: Optional[str] = None, fail_after_prompt: bool = False, fail_after_execute: bool = False) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_STARTED", capability_id="ANDY.CAP.RUN_STAGE_TO_REVIEW")
    completed: List[str] = []
    st = submit_stage_prompt_state(st, stage_id, prompt_text)
    completed.append("ANDY.CAP.SUBMIT_STAGE_PROMPT")
    if fail_after_prompt:
        _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT", failed_step="ANDY.CAP.EXECUTE_STAGE")
        return _record_composite_operation(st, "ANDY.CAP.RUN_STAGE_TO_REVIEW", stage_id, completed, "ANDY.CAP.EXECUTE_STAGE", "failed_partial_commit", "Injected failure after prompt.")
    st = execute_stage_state(st, draft_text=draft_text)
    completed.append("ANDY.CAP.EXECUTE_STAGE")
    if fail_after_execute:
        _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT", failed_step="ANDY.CAP.OPEN_STAGE_REVIEW")
        return _record_composite_operation(st, "ANDY.CAP.RUN_STAGE_TO_REVIEW", stage_id, completed, "ANDY.CAP.OPEN_STAGE_REVIEW", "failed_partial_commit", "Injected failure after execution.")
    st = open_stage_review_state(st)
    completed.append("ANDY.CAP.OPEN_STAGE_REVIEW")
    _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED", capability_id="ANDY.CAP.RUN_STAGE_TO_REVIEW")
    return _record_composite_operation(st, "ANDY.CAP.RUN_STAGE_TO_REVIEW", stage_id, completed, None, "committed")


def accept_artifact_with_evidence_state(state: Mapping[str, Any], artifact_id: str, artifact_version_id: str, slot_id: str, digest: str, evidence_packet_id: str, artifact_body: Optional[str] = None, acceptance_statement: str = "I accept this artifact.", source_inputs: str = "declared sources", fail_after_register: bool = False, fail_after_accept: bool = False, fail_after_evidence: bool = False) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    stage_id = st.get("current_stage_id")
    _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_STARTED", capability_id="ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE")
    completed: List[str] = []
    st = register_artifact_state(st, artifact_id, artifact_version_id, slot_id, digest, artifact_body=artifact_body)
    completed.append("ANDY.CAP.REGISTER_ARTIFACT")
    if fail_after_register:
        _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT", failed_step="ANDY.CAP.ACCEPT_ARTIFACT")
        return _record_composite_operation(st, "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE", stage_id, completed, "ANDY.CAP.ACCEPT_ARTIFACT", "failed_partial_commit", "Injected failure after registration.")
    st = accept_artifact_state(st, artifact_version_id, acceptance_statement)
    completed.append("ANDY.CAP.ACCEPT_ARTIFACT")
    if fail_after_accept:
        _require(st["artifact_versions"][artifact_version_id]["dependency_eligible"] is False, "False promotion after accept")
        _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT", failed_step="ANDY.CAP.ATTACH_EVIDENCE_PACKET")
        return _record_composite_operation(st, "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE", stage_id, completed, "ANDY.CAP.ATTACH_EVIDENCE_PACKET", "failed_partial_commit", "Injected failure after acceptance.")
    accepted_id = f"ACC-{artifact_version_id}"
    st = attach_evidence_packet_state(st, accepted_id, evidence_packet_id, source_inputs)
    completed.append("ANDY.CAP.ATTACH_EVIDENCE_PACKET")
    if fail_after_evidence:
        _require(st["artifact_versions"][artifact_version_id]["dependency_eligible"] is False, "False promotion after evidence")
        _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_FAILED_PARTIAL_COMMIT", failed_step="ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE")
        return _record_composite_operation(st, "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE", stage_id, completed, "ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE", "failed_partial_commit", "Injected failure after evidence.")
    st = promote_artifact_dependency_eligible_state(st, accepted_id)
    completed.append("ANDY.CAP.PROMOTE_ARTIFACT_DEPENDENCY_ELIGIBLE")
    _emit(st, "ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED", capability_id="ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE")
    return _record_composite_operation(st, "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE", stage_id, completed, None, "committed")


def parse_accept_artifact_payload(payload: str) -> Dict[str, Any]:
    max_len = INTERACTION_ADAPTER_CONTRACT["max_payload_length"]
    if len(payload) > max_len:
        return {"valid": False, "fields": {}, "missing_fields": [], "blank_fields": [], "duplicate_fields": [], "unknown_fields": [], "diagnostic": "payload_too_large"}
    # Strict grammar: lowercase keys, single spaces between key groups, no unknown keys.
    pattern = re.compile(r"(?:^|\s)(artifact_ref|evidence_source|acceptance)=")
    matches = list(pattern.finditer(payload))
    values: Dict[str, str] = {}
    duplicates: List[str] = []
    for index, match in enumerate(matches):
        key = match.group(1)
        if key in values:
            duplicates.append(key)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(payload)
        values[key] = payload[start:end].strip()
    required = ["artifact_ref", "evidence_source", "acceptance"]
    missing = [key for key in required if key not in values]
    blank = [key for key in required if key in values and not values[key].strip()]
    unknown = re.findall(r"(?:^|\s)([A-Za-z_]+)=", payload)
    unknown_fields = [key for key in unknown if key not in required]
    bad_case = [key for key in unknown if key.lower() in required and key not in required]
    valid = not missing and not blank and not duplicates and not unknown_fields and not bad_case and len(matches) == 3
    return {"valid": valid, "fields": values, "missing_fields": missing, "blank_fields": blank, "duplicate_fields": duplicates, "unknown_fields": unknown_fields + bad_case, "diagnostic": "" if valid else "invalid_accept_artifact_payload"}


def route_interaction(message: str, expected_stage_id: str) -> Dict[str, Any]:
    text = message.strip()
    if text in INTERACTION_ADAPTER_CONTRACT["vague_commands"]:
        return {"mutates_state": False, "route": "vague_non_mutating", "capability_id": None, "diagnostic": "Vague command rejected as non-mutating."}
    m = re.match(r"^Adopt ANDY Narrative: (.+)$", text, flags=re.DOTALL)
    if m:
        return {"mutates_state": bool(m.group(1).strip()), "route": "composite_adopt_narrative", "capability_id": "ANDY.CAP.ADOPT_NARRATIVE", "payload": m.group(1)}
    m = re.match(r"^Adopt ANDY Narrative from uploaded file: (.+)$", text, flags=re.DOTALL)
    if m:
        return {"mutates_state": bool(m.group(1).strip()), "route": "composite_adopt_narrative_from_file", "capability_id": "ANDY.CAP.ADOPT_NARRATIVE", "payload": m.group(1)}
    m = re.match(r"^Run stage (STG-[0-9]+) with prompt: (.+)$", text, flags=re.DOTALL) or re.match(r"^Submit and execute stage (STG-[0-9]+): (.+)$", text, flags=re.DOTALL)
    if m:
        if m.group(1) != expected_stage_id:
            return {"mutates_state": False, "route": "wrong_stage", "capability_id": None, "diagnostic": "Wrong stage."}
        return {"mutates_state": bool(m.group(2).strip()), "route": "composite_run_stage_to_review", "capability_id": "ANDY.CAP.RUN_STAGE_TO_REVIEW", "stage_id": m.group(1), "payload": m.group(2)}
    m = re.match(r"^Accept artifact with evidence for slot (SLOT-[0-9]+) in stage (STG-[0-9]+):(.+)$", text, flags=re.DOTALL)
    if m:
        if m.group(2) != expected_stage_id:
            return {"mutates_state": False, "route": "wrong_stage", "capability_id": None, "diagnostic": "Wrong stage."}
        parsed = parse_accept_artifact_payload(m.group(3))
        if not parsed["valid"]:
            return {"mutates_state": False, "route": "invalid_macro_payload", "capability_id": None, "diagnostic": parsed}
        payload = dict(parsed["fields"])
        payload["slot_id"] = m.group(1)
        return {"mutates_state": True, "route": "composite_accept_artifact_with_evidence", "capability_id": "ANDY.CAP.ACCEPT_ARTIFACT_WITH_EVIDENCE", "stage_id": m.group(2), "slot_id": m.group(1), "payload": payload}
    return {"mutates_state": False, "route": "unmatched_non_mutating", "capability_id": None, "diagnostic": "No registered route."}


def reopen_stage_as_new_version_state(state: Mapping[str, Any], stage_id: str, source_snapshot_id: Optional[str] = None, source_snapshot_digest: Optional[str] = None) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(st["current_state"] in {"CLOSED", "EXPORTED"}, "Reopen requires CLOSED or EXPORTED")
    _require(stage_id in st["stage_records"], "Unknown stage")
    if source_snapshot_id:
        _require(source_snapshot_id in st.get("snapshots", {}), "Source Snapshot missing")
        if source_snapshot_digest:
            _require(st["snapshots"][source_snapshot_id]["canonical_state_digest"] == source_snapshot_digest, "Source Snapshot digest mismatch")
    st["current_stage_id"] = stage_id
    st["stage_records"][stage_id]["stage_status"] = "stage_ready"
    st["stage_records"][stage_id]["review_status"] = "not_open"
    st["stage_records"][stage_id]["completion_confirmed"] = False
    st["reopen_record"] = {"stage_id": stage_id, "source_snapshot_id": source_snapshot_id, "source_snapshot_digest": source_snapshot_digest, "lineage_policy": "new_successor_version_preserve_history"}
    return _bump(st, "REOPENED", "ANDY.EVENT.STAGE_REOPENED_AS_NEW_VERSION", stage_id=stage_id)


def restore_as_new_version_state(state: Mapping[str, Any], source_snapshot_id: str, source_snapshot_digest: str) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    _require(source_snapshot_id in st.get("snapshots", {}), "Source Snapshot missing")
    snap = st["snapshots"][source_snapshot_id]
    _require(snap["canonical_state_digest"] == source_snapshot_digest, "Source Snapshot digest mismatch")
    restored = copy.deepcopy(snap["canonical_state"])
    restored["previous_state"] = st.get("current_state")
    restored["active_version"] = int(st.get("active_version", 1)) + 1
    restored["restore_record"] = {"source_snapshot_id": source_snapshot_id, "source_snapshot_digest": source_snapshot_digest, "lineage_policy": "restore_as_new_successor_version"}
    return _bump(restored, "STAGE_READY" if restored.get("current_stage_id") else "REOPENED", "ANDY.EVENT.SNAPSHOT_RESTORED_AS_NEW_VERSION", source_snapshot_id=source_snapshot_id)


def block_workflow_state(state: Mapping[str, Any], reason: str) -> Dict[str, Any]:
    st = copy.deepcopy(dict(state))
    st["workflow_status"] = "blocked"
    st["blocked_reason"] = reason
    return _bump(st, "BLOCKED", "ANDY.EVENT.WORKFLOW_BLOCKED", reason=reason)


class KernelCapabilityExecutor:
    """AWKA-compatible test harness adapter for alpha.7 enforcement proof.

    The real AWKA Kernel remains the normative executor. This adapter gives the
    Verification Suite a deterministic contract surface for authorization,
    concurrency, idempotency, event-contract, and snapshot checks when a direct
    AWKA execute_capability API is unavailable.
    """

    def __init__(self, model: Mapping[str, Any]):
        self.model = model
        self.invocations: Dict[str, Any] = {}

    def execute(self, state: Mapping[str, Any], capability_id: str, actor_roles: Sequence[str], payload: Mapping[str, Any], invocation_id: str, expected_active_version: Optional[int] = None) -> Dict[str, Any]:
        _require(capability_id in self.model["capabilities"], "Unknown Capability")
        cap = self.model["capabilities"][capability_id]
        _require(set(actor_roles).intersection(cap["authorization"]["roles"]), "Unauthorized actor")
        if invocation_id in self.invocations:
            prior = self.invocations[invocation_id]
            _require(prior["capability_id"] == capability_id and prior["payload_digest"] == _digest(payload), "Conflicting idempotent invocation")
            return copy.deepcopy(prior["result"])
        if cap["concurrency_requirement"].get("requires_active_version"):
            _require(expected_active_version == state.get("active_version"), "Stale active version")
        before = copy.deepcopy(dict(state))
        function_map: Dict[str, Callable[..., Dict[str, Any]]] = {
            "ANDY.CAP.SUBMIT_STAGE_PROMPT": lambda **kw: submit_stage_prompt_state(before, kw["stage_id"], kw["prompt_text"]),
            "ANDY.CAP.EXPORT_ARTIFACT_SET": lambda **kw: export_artifact_set_state(before, kw.get("output_reference", "ANDY_Final_Artifact_Set.txt"), kw.get("resolver_context")),
        }
        _require(capability_id in function_map, "Executor demo supports selected critical Capabilities only")
        result_state = function_map[capability_id](**dict(payload))
        emitted = [event["event_id"] if isinstance(event, Mapping) else event for event in result_state.get("events", [])]
        _require(any(event in emitted for event in cap["events_emitted"]), "Declared event not emitted")
        self.invocations[invocation_id] = {"capability_id": capability_id, "payload_digest": _digest(payload), "result": result_state}
        return result_state


if __name__ == "__main__":
    print(json.dumps(validate_model(), indent=2, sort_keys=True))
