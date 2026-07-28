#!/usr/bin/env python3
"""Executable LINDA Generic Domain Runtime verification v1.0.0-alpha.6.

This suite verifies the LINDA Manifest and executable Domain Model against the
AWKA v1.0.0-alpha.4 Constitution and Runtime. It introduces no business
behavior and writes no test data into an active operational Workflow Instance.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import py_compile
import sys
from typing import Any, Callable, Dict, List, Mapping

VERSION = "1.0.0-alpha.6"
AWKA_VERSION = "1.0.0-alpha.4"
SUITE_ID = "LINDA-GENERIC-DOMAIN-ACTIVATION-CONFORMANCE"

CONSTITUTION_FILE = "001_AWKA_Constitution_v1.0.0-alpha.4.json"
AWKA_RUNTIME_FILE = "002_AWKA_Runtime_v1_0_0_alpha_4.py"
MANIFEST_FILE = "001_LINDA_Generic_Manifest_v1.0.0-alpha.6.json"
MODEL_FILE = "002_LINDA_Generic_Model_v1_0_0_alpha_6.py"

EXPECTED_TEST_IDS = [
    "LINDA-MODEL-001",
    "LINDA-MODEL-002",
    "LINDA-MODEL-003",
    "LINDA-CAP-001",
    "LINDA-CAP-002",
    "LINDA-WF-001",
    "LINDA-WF-002",
    "LINDA-VAL-001",
    "LINDA-RENDER-001",
    "LINDA-RENDER-002",
    "LINDA-TOOL-001",
    "LINDA-BEHAVIOR-001",
    "LINDA-BEHAVIOR-002",
    "LINDA-BEHAVIOR-003",
    "LINDA-BEHAVIOR-004",
    "LINDA-BEHAVIOR-005",
    "LINDA-BEHAVIOR-006",
    "LINDA-BEHAVIOR-007",
    "LINDA-BEHAVIOR-008",
    "LINDA-ACT-001",
    "LINDA-ACT-002",
    "LINDA-ACT-003",
    "LINDA-DELIVERY-001",
    "LINDA-DELIVERY-002",
    "LINDA-DATASET-001",
    "LINDA-DATASET-002",
    "LINDA-DATASET-003",
    "LINDA-DATASET-004",
    "LINDA-HARDEN-001",
    "LINDA-HARDEN-002",
    "LINDA-HARDEN-003",
    "LINDA-HARDEN-004",
    "LINDA-HARDEN-005",
    "LINDA-HARDEN-006",
    "LINDA-HARDEN-007",
    "LINDA-HARDEN-008",
    "LINDA-GENERIC-001",
    "LINDA-GENERIC-002",
    "LINDA-GENERIC-003",
    "LINDA-GENERIC-004",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def file_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def result(test_id: str, function: Callable[[], Any]) -> Dict[str, Any]:
    try:
        evidence = function()
        return {"test_id": test_id, "passed": True, "evidence": evidence}
    except Exception as error:
        return {
            "test_id": test_id,
            "passed": False,
            "evidence": f"{type(error).__name__}: {error}",
        }


def run(package_dir: Path) -> Dict[str, Any]:
    constitution_path = package_dir / CONSTITUTION_FILE
    runtime_path = package_dir / AWKA_RUNTIME_FILE
    manifest_path = package_dir / MANIFEST_FILE
    model_path = package_dir / MODEL_FILE

    constitution = json.loads(constitution_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    py_compile.compile(str(runtime_path), doraise=True)
    py_compile.compile(str(model_path), doraise=True)
    runtime = load_module("awka_runtime_for_linda_generic_a6", runtime_path)
    model = load_module("linda_generic_model_for_verification_a6", model_path)
    results: List[Dict[str, Any]] = []

    def new_ready_kernel():
        kernel = runtime.AWKAKernel(constitution)
        kernel.bootstrap()
        require(kernel.kernel_state == "READY", "Kernel did not reach READY")
        return kernel

    def candidate_runtime():
        kernel = new_ready_kernel()
        candidate = kernel.build_candidate_registries()
        model.populate_candidate_registries(kernel, candidate)
        return kernel, candidate

    def activated_runtime():
        kernel, candidate = candidate_runtime()
        kernel.activate_domain(
            candidate,
            verifier=lambda registries: None,
            domain_descriptor=model.domain_descriptor(),
            correlation_id="CORR-LINDA-ACTIVATE",
        )
        return kernel

    def model_001():
        summary = model.validate_model()
        fields = model.MODEL["canonical_model"]["fields"]
        require(summary["fields"] == 84, "Expected 84 fields")
        require(len({item["field_id"] for item in fields}) == 84, "Duplicate field IDs")
        require(len({item["section_id"] for item in fields}) == 4, "Expected four sections")
        return {"fields": 84, "sections": 4, "unique_field_ids": 84}

    results.append(result("LINDA-MODEL-001", model_001))

    def model_002():
        entities = model.MODEL["entities"]
        require(len(entities) == 6, "Expected six entities")
        require("LINDA.ENTITY.JOB_REPORT" in entities, "Aggregate root missing")
        relationships = entities["LINDA.ENTITY.JOB_REPORT"].get("relationships", {})
        for target in relationships.values():
            if target == "AWKA.SNAPSHOT":
                continue
            require(target in entities, f"Missing entity relationship target: {target}")
        return {"entities": len(entities), "relationship_targets_valid": True}

    results.append(result("LINDA-MODEL-002", model_002))

    def model_003():
        namespaces = manifest["namespace_contract"]
        declared = manifest["declared_definition_ids"]
        mapping = {
            "entities": "entities",
            "capabilities": "capabilities",
            "validators": "validators",
            "renderers": "renderers",
            "workflows": "workflows",
            "tools": "tools",
            "rules": "rules",
        }
        for category, namespace_key in mapping.items():
            prefix = namespaces[namespace_key] + "."
            for identifier in declared[category]:
                require(identifier.startswith(prefix), f"Namespace violation: {identifier}")
        return "All declared definition IDs use the LINDA namespace contract"

    results.append(result("LINDA-MODEL-003", model_003))

    def cap_001():
        capabilities = model.MODEL["capabilities"]
        require(len(capabilities) == 10, "Expected ten Capabilities")
        required = {
            "version", "purpose", "inputs", "outputs", "preconditions",
            "postconditions", "permitted_mutations", "validator_ids",
            "authorization", "events_emitted", "failure_effect", "idempotency"
        }
        for capability_id, definition in capabilities.items():
            missing = required - set(definition)
            require(not missing, f"{capability_id} missing {sorted(missing)}")
        return {"capabilities": 10, "complete_contracts": True}

    results.append(result("LINDA-CAP-001", cap_001))

    def cap_002():
        capabilities = model.MODEL["capabilities"]
        validators = set(model.MODEL["validator_definitions"])
        permitted_stores = {
            "workflow_instance_store", "canonical_state_store", "evidence_store",
            "event_store", "snapshot_store", "artifact_receipt_store"
        }
        for capability_id, definition in capabilities.items():
            missing = set(definition["validator_ids"]) - validators
            require(not missing, f"{capability_id} missing validators {sorted(missing)}")
            invalid = set(definition["permitted_mutations"]) - permitted_stores
            require(not invalid, f"{capability_id} has invalid stores {sorted(invalid)}")
        return "Validator and permitted-Instance-Store references are complete"

    results.append(result("LINDA-CAP-002", cap_002))

    def wf_001():
        workflow = model.MODEL["workflow_definitions"]["LINDA.WF.JOB_REPORT"]
        states = set(workflow["states"])
        capabilities = set(model.MODEL["capabilities"])
        require(workflow["initial_state"] in states, "Initial state missing")
        adjacency = {state: set() for state in states}
        for transition in workflow["transitions"]:
            require(transition["from_state"] in states, "Missing from_state")
            require(transition["to_state"] in states, "Missing to_state")
            require(transition["capability_id"] in capabilities, "Missing transition Capability")
            adjacency[transition["from_state"]].add(transition["to_state"])
        reached = {workflow["initial_state"]}
        frontier = [workflow["initial_state"]]
        while frontier:
            state = frontier.pop()
            for target in adjacency[state]:
                if target not in reached:
                    reached.add(target); frontier.append(target)
        require(reached == states, f"Unreachable states: {sorted(states-reached)}")
        return {"states": len(states), "transitions": len(workflow["transitions"]), "reachable": True}

    results.append(result("LINDA-WF-001", wf_001))

    def wf_002():
        workflow = model.MODEL["workflow_definitions"]["LINDA.WF.JOB_REPORT"]
        from_closed = [item for item in workflow["transitions"] if item["from_state"] == "CLOSED"]
        require(len(from_closed) == 1, "CLOSED must have exactly one outgoing transition")
        transition = from_closed[0]
        require(transition["to_state"] == "REOPENED", "CLOSED may only restore to REOPENED")
        require(transition["capability_id"] == "LINDA.CAP.RESTORE_AS_NEW_VERSION", "Wrong restore Capability")
        return "CLOSED is controlled; restoration creates REOPENED successor state"

    results.append(result("LINDA-WF-002", wf_002))

    def val_001():
        validators = model.MODEL["validator_definitions"]
        require(len(validators) == 9, "Expected nine validators")
        orders = [item["order"] for item in validators.values()]
        require(len(orders) == len(set(orders)), "Validator orders are not unique")
        require(validators["LINDA.VAL.CANDIDATE_FACT"]["order"] < validators["LINDA.VAL.BUSINESS"]["order"], "Candidate review must precede business validation")
        require(validators["LINDA.VAL.PRESENTATION"]["order"] < validators["LINDA.VAL.ARTIFACT"]["order"], "Presentation must precede artifact validation")
        return {"validators": 9, "ordered": True}

    results.append(result("LINDA-VAL-001", val_001))

    def render_001():
        renderers = model.MODEL["renderer_definitions"]
        tools = set(model.MODEL["tool_bindings"])
        require(len(renderers) == 5, "Expected five renderers")
        for renderer_id, definition in renderers.items():
            require(definition.get("purity") is True, f"{renderer_id} is not pure")
            require(not (set(definition.get("tool_ids", [])) - tools), f"{renderer_id} has missing tool")
        return {"renderers": 5, "pure": True, "tool_bindings_complete": True}

    results.append(result("LINDA-RENDER-001", render_001))

    def render_002():
        draft = model.MODEL["renderer_definitions"]["LINDA.RENDER.DRAFT"]
        presentation = model.MODEL["presentation_contract"]
        require(draft["required_banner"] == "DRAFT EXPORT - Not approved for final filing", "Draft banner mismatch")
        require(draft["banner_scope"] == "every_page", "Draft banner not required on every page")
        require(presentation["standard_profile"]["show_field_id"] is False, "Standard profile exposes Field IDs")
        require(presentation["standard_profile"]["allow_machine_status_codes"] is False, "Standard profile exposes machine codes")
        return "Draft renderer and standard presentation controls are correct"

    results.append(result("LINDA-RENDER-002", render_002))

    def tool_001():
        binding = model.MODEL["tool_bindings"]["LINDA.TOOL.FILE_RENDERER"]
        required = {
            "tool_binding_id", "tool_id", "invoked_by", "input_contract",
            "output_contract", "side_effects", "network_access",
            "data_classification_allowed", "required_authority", "timeout_policy",
            "retry_policy", "failure_mapping"
        }
        require(not (required - set(binding)), "Tool binding contract incomplete")
        require(binding["network_access"] is False, "File Renderer may not use network access")
        return "Tool binding is allowlisted, contract-bound, and network-disabled"

    results.append(result("LINDA-TOOL-001", tool_001))

    def behavior_001():
        capability = model.MODEL["capabilities"]["LINDA.CAP.CREATE_JOB_REPORT"]
        require("source registered" in capability["postconditions"], "Source registration postcondition missing")
        require("controlled fields unchanged" in capability["postconditions"], "Preapproval mutation guard missing")
        return "Create Job Report requires source registration and no preapproval field population"

    results.append(result("LINDA-BEHAVIOR-001", behavior_001))

    def behavior_002():
        capability = model.MODEL["capabilities"]["LINDA.CAP.APPROVE_SOURCE"]
        require("exact command names Source Packet" in capability["preconditions"], "Exact Source Packet command missing")
        require("ambiguous candidates remain unaccepted" in capability["postconditions"], "Ambiguous Candidate guard missing")
        return "Source approval is exact-targeted and does not accept ambiguous candidates"

    results.append(result("LINDA-BEHAVIOR-002", behavior_002))

    def behavior_003():
        rule = next(item for item in model.MODEL["business_rules"] if item["rule_id"] == "LINDA.RULE.VISUAL_AMBIGUITY")
        require(rule["effect"] == "value null and status coordinator_review", "Visual ambiguity effect drifted")
        require("blocking_error" in rule["severity"], "Visual ambiguity violation is not blocking")
        return "Ambiguous visual selections remain null under coordinator review"

    results.append(result("LINDA-BEHAVIOR-003", behavior_003))

    def behavior_004():
        rule = next(item for item in model.MODEL["business_rules"] if item["rule_id"] == "LINDA.RULE.DURATION")
        require("JR-S1-022" in rule["effect"], "Duration is not mapped to revised duration field")
        require("do not infer a scheduled end time" in rule["effect"], "Scheduled end-time prohibition missing")
        return "Explicit duration maps to revised duration control without inferring an end time"

    results.append(result("LINDA-BEHAVIOR-004", behavior_004))

    def behavior_005():
        rule = next(item for item in model.MODEL["business_rules"] if item["rule_id"] == "LINDA.RULE.END_CLIENT")
        require("Client Account candidate" in rule["effect"], "Client Account candidate handling missing")
        require("never map to End User" in rule["effect"], "End User prohibition missing")
        return "End Client remains a review candidate and does not establish End User"

    results.append(result("LINDA-BEHAVIOR-005", behavior_005))

    def behavior_006():
        rule = next(item for item in model.MODEL["business_rules"] if item["rule_id"] == "LINDA.RULE.LANGUAGE_DIRECTION")
        require("preserve exact names" in rule["effect"], "Exact language preservation missing")
        require("under review" in rule["effect"], "Language review status missing")
        return "Undirected language names remain exact and under review"

    results.append(result("LINDA-BEHAVIOR-006", behavior_006))

    def behavior_007():
        capability = model.MODEL["capabilities"]["LINDA.CAP.EXPORT_ARTIFACT"]
        require("snapshot digest valid" in capability["preconditions"], "Snapshot digest precondition missing")
        require("snapshot unchanged" in capability["postconditions"], "Snapshot immutability postcondition missing")
        require("receipt created after final hashing" in capability["postconditions"], "Receipt timing missing")
        return "Artifact export requires digest, immutability, and post-hash receipt"

    results.append(result("LINDA-BEHAVIOR-007", behavior_007))

    def behavior_008():
        contract = model.MODEL["presentation_contract"]
        require(contract["standard_profile"]["allow_machine_status_codes"] is False, "Machine codes allowed")
        require(len(contract["forbidden_standard_tokens"]) >= 6, "Leakage scan token set incomplete")
        return "Standard artifact presentation suppresses internal status codes"

    results.append(result("LINDA-BEHAVIOR-008", behavior_008))

    def act_001():
        summary = model.validate_model()
        declared = manifest["declared_definition_counts"]
        require(summary["entities"] == declared["entities"], "Entity count mismatch")
        require(summary["capabilities"] == declared["capabilities"], "Capability count mismatch")
        require(summary["validators"] == declared["validators"], "Validator count mismatch")
        require(summary["renderers"] == declared["renderers"], "Renderer count mismatch")
        require(summary["fields"] == declared["controlled_fields"], "Field count mismatch")
        return "Manifest declarations match executable Model"

    results.append(result("LINDA-ACT-001", act_001))

    def act_002():
        kernel, candidate = candidate_runtime()
        counts = {name: len(values) for name, values in candidate.items()}
        expected = {
            "capability_registry": 10, "validator_registry": 9,
            "renderer_registry": 5, "workflow_registry": 1,
            "entity_registry": 6, "tool_registry": 1,
            "schema_registry": 1, "policy_registry": 10,
        }
        require(counts == expected, f"Candidate Registry count mismatch: {counts}")
        kernel.activate_domain(candidate, lambda registries: None, model.domain_descriptor(), "CORR-ACT-002")
        require(kernel.definition_registries_locked, "Definition Registries not frozen")
        try:
            kernel.register_definition_after_activation("capability_registry", "LINDA.CAP.LATE", {})
        except runtime.RegistryLocked:
            return {"registry_counts": counts, "definition_lock": True}
        raise AssertionError("Dynamic registration remained enabled")

    results.append(result("LINDA-ACT-002", act_002))

    def act_003():
        kernel, candidate = candidate_runtime()
        try:
            kernel.activate_domain(
                candidate,
                verifier=lambda registries: (_ for _ in ()).throw(runtime.ValidationError("synthetic activation failure")),
                domain_descriptor=model.domain_descriptor(),
                correlation_id="CORR-ACT-003",
            )
        except runtime.ValidationError:
            require(kernel.kernel_state == "READY", "Kernel did not return READY")
            require(all(not values for values in kernel.definition_registries.values()), "Candidate definitions leaked")
            require(kernel.active_domain_descriptor is None, "Failed Domain remained active")
            return "Failed activation discarded temporary definitions and returned Kernel to READY"
        raise AssertionError("Synthetic activation failure did not reject")

    results.append(result("LINDA-ACT-003", act_003))

    def delivery_001():
        contract = model.release_contract()
        require(
            contract["activation_directive_delivery"] == "current_user_message",
            "Activation directive must be delivered as the current user message",
        )
        require(
            contract["activation_directive_is_file_component"] is False,
            "Activation directive must not be treated as an uploaded component",
        )
        require(
            contract["activation_directive_requires_sha256"] is False,
            "Message-delivered activation directive must not require a file digest",
        )
        require(
            len(contract["uploaded_components"]) == 3,
            "Exactly three LINDA files must be uploaded",
        )
        return "Activation directive is message-delivered and excluded from file-component hashing"

    results.append(result("LINDA-DELIVERY-001", delivery_001))

    def delivery_002():
        contract = model.release_contract()
        require(
            contract["hashed_components"] == [MODEL_FILE, Path(__file__).name],
            "Only the executable Model and Verification files are hashed components",
        )
        require(
            manifest["activation_rules"]["workflow_creation_during_activation"] is False,
            "Domain Activation must not create a Workflow Instance",
        )
        # The preliminary Manifest may still contain pending component hashes,
        # but activation cannot succeed until a finalized Manifest is supplied.
        pending = [
            component
            for component in manifest.get("component_contracts", [])
            if component.get("digest_status") != "verified"
        ]
        require(
            manifest["activation_rules"]["all_component_digests_required_before_activation"] is True,
            "Manifest must require final component digests before activation",
        )
        return {
            "hashed_components": contract["hashed_components"],
            "pending_manifest_components": [item.get("component_id") for item in pending],
            "activation_blocked_until_manifest_finalized": bool(pending),
        }

    results.append(result("LINDA-DELIVERY-002", delivery_002))

    def dataset_001():
        fields = model.MODEL["canonical_model"]["fields"]
        counts = {
            section: sum(item["section_id"] == section for item in fields)
            for section in ("section_1", "section_2", "section_3", "section_4")
        }
        require(counts == {"section_1": 37, "section_2": 17, "section_3": 18, "section_4": 12}, f"Section counts drifted: {counts}")
        require(manifest["field_model_contract"]["flat_core_field_count"] == 84, "Manifest core count mismatch")
        return {"core_fields": 84, "section_counts": counts}

    results.append(result("LINDA-DATASET-001", dataset_001))

    def dataset_002():
        schemas = model.MODEL["canonical_model"]["repeatable_record_schemas"]
        expected = {
            "LINDA.RECORD.LANGUAGE_COMBINATION",
            "LINDA.RECORD.TEAM_COMPOSITION",
            "LINDA.RECORD.PREPARATION_MATERIAL",
            "LINDA.RECORD.ASSIGNED_INTERPRETER",
            "LINDA.RECORD.ASSIGNMENT_EVENT_EXCEPTION",
            "LINDA.RECORD.FEEDBACK",
            "LINDA.RECORD.RELATED_CONTROLLED_RECORD",
        }
        require(set(schemas) == expected, "Repeatable-record schema set drifted")
        require(all(schemas[key] for key in expected), "A repeatable-record schema is empty")
        return {"repeatable_record_types": 7, "schema_ids": sorted(expected)}

    results.append(result("LINDA-DATASET-002", dataset_002))

    def dataset_003():
        boundaries = set(model.MODEL["canonical_model"]["external_record_boundaries"])
        required = {
            "resource_qualification_record",
            "interpreting_protocol",
            "incident_or_corrective_action_record",
            "accounting_record",
            "restricted_wellbeing_follow_up_record",
            "awka_technical_and_audit_stores",
        }
        require(boundaries == required, "External record boundaries drifted")
        require(manifest["supporting_record_contract"]["job_report_must_reference_not_duplicate_sensitive_or_master_data"] is True, "Reference-not-duplicate rule missing")
        return "Sensitive, financial, qualification, protocol, and AWKA metadata remain outside the Job Report"

    results.append(result("LINDA-DATASET-003", dataset_003))

    def dataset_004():
        presentation = model.MODEL["presentation_contract"]["section_rendering"]
        require(presentation["active_stage_fields_individual"] is True, "Active fields are not rendered individually")
        require(presentation["collapse_entire_section_to_generic_pending_row"] is False, "Section collapsing remains allowed")
        require(presentation["repeatable_records_render_as_child_tables"] is True, "Repeatable records are not child tables")
        for renderer_id, renderer in model.MODEL["renderer_definitions"].items():
            require("never use broken bullet glyphs or collapse a section" in renderer["section_rendering_rule"], f"{renderer_id} lacks hardened rendering rule")
        return "Renderers expose stage-relevant controls individually and keep linked records reference-only"

    results.append(result("LINDA-DATASET-004", dataset_004))

    def harden_001():
        fields = {item["field_id"]: item for item in model.MODEL["canonical_model"]["fields"]}
        require(fields["JR-S1-028"]["label"] == "Interpreter Rate Record", "Hardened rate field missing")
        require(fields["JR-S3-016"]["label"] == "Actual Work Units Record", "Hardened work-unit field missing")
        contract = model.MODEL["canonical_model"]["pricing_and_work_units_contract"]
        require(contract["financial_calculation_permitted"] is False, "Financial calculation remains permitted")
        forbidden = set(contract["forbidden_outputs"])
        require({"extended_cost", "invoice_total", "tax", "amount_payable", "rate_times_days", "rate_times_hours"} <= forbidden, "Forbidden financial outputs incomplete")
        return "Exact interpreter rates and work units are retained while all financial calculations are prohibited"
    results.append(result("LINDA-HARDEN-001", harden_001))

    def harden_002():
        assigned = model.MODEL["canonical_model"]["repeatable_record_schemas"]["LINDA.RECORD.ASSIGNED_INTERPRETER"]
        for key in ("daily_rate_exact", "hourly_rate_exact", "currency_and_units_exact"):
            require(key in assigned, f"Missing exact rate attribute: {key}")
        related = model.MODEL["canonical_model"]["repeatable_record_schemas"]["LINDA.RECORD.RELATED_CONTROLLED_RECORD"]
        for key in ("interpreter_or_resource_id", "total_days_worked_exact", "total_hours_worked_exact"):
            require(key in related, f"Missing exact work-unit attribute: {key}")
        return "Per-interpreter exact rates and exact days/hours worked are structurally supported"
    results.append(result("LINDA-HARDEN-002", harden_002))

    def harden_003():
        contract = model.MODEL["hardening_contract"]
        require(contract["human_ai_identity_separation"] is True, "Human/AI identity separation disabled")
        human_fields = set(model.MODEL["canonical_model"]["human_identity_fields"])
        require({"JR-S1-008", "JR-S2-002", "JR-S2-009", "JR-S4-001", "JR-S4-003"} <= human_fields, "Human operational field set incomplete")
        authority = model.MODEL["validator_definitions"]["LINDA.VAL.AUTHORITY"]["purpose"]
        require("AI/tool identities" in authority, "Authority Validator lacks identity-separation duty")
        return "AI and tool identities cannot populate human operational fields"
    results.append(result("LINDA-HARDEN-003", harden_003))

    def harden_004():
        presentation = model.MODEL["presentation_contract"]
        standard = presentation["standard_profile"]
        require(standard["allow_replacement_glyphs"] is False, "Replacement glyphs allowed")
        require(standard["list_marker_policy"] == "verified_glyph_or_ascii_hyphen", "Unsafe list-marker policy")
        forbidden = set(presentation["forbidden_standard_tokens"])
        require("�" in forbidden and "■" in forbidden and "□" in forbidden, "Glyph leakage tokens incomplete")
        return "Standard artifacts reject replacement glyphs, black squares, and broken bullets"
    results.append(result("LINDA-HARDEN-004", harden_004))

    def harden_005():
        presentation = model.MODEL["presentation_contract"]
        require(presentation["standard_profile"]["allow_cleartext_secrets"] is False, "Cleartext secrets allowed")
        policy = presentation["secret_field_policy"]
        require("JR-S1-032" in policy["fields"], "Remote-access field lacks secret policy")
        require(policy["display"] == "controlled_reference_only", "Secrets do not render as references")
        require({"password", "access_code", "token", "restricted_link"} <= set(policy["prohibited_cleartext_types"]), "Secret types incomplete")
        return "Meeting credentials, access codes, tokens, and restricted links are reference-only"
    results.append(result("LINDA-HARDEN-005", harden_005))

    def harden_006():
        business = model.MODEL["validator_definitions"]["LINDA.VAL.BUSINESS"]["purpose"]
        require("cross-field reconciliation" in business, "Cross-field reconciliation missing")
        finalize = model.MODEL["capabilities"]["LINDA.CAP.FINALIZE_JOB_REPORT"]["preconditions"]
        for item in ("human operational identities valid", "financial calculations absent", "cross-field reconciliation passes", "secret minimization passes", "presentation glyph safety passes", "external record boundaries pass"):
            require(item in finalize, f"Finalization hardening precondition missing: {item}")
        return "Finalization fails closed unless identity, calculation, reconciliation, secret, glyph, and boundary checks pass"
    results.append(result("LINDA-HARDEN-006", harden_006))

    def harden_007():
        boundaries = set(model.MODEL["canonical_model"]["external_record_boundaries"])
        required = {"resource_qualification_record", "interpreting_protocol", "incident_or_corrective_action_record", "accounting_record", "restricted_wellbeing_follow_up_record", "awka_technical_and_audit_stores"}
        require(boundaries == required, "External-record boundary drift")
        for renderer_id, renderer in model.MODEL["renderer_definitions"].items():
            require(renderer["linked_record_rule"] == "Sensitive and master records render as references only.", f"{renderer_id} leaks linked records")
        return "Sensitive, financial, qualification, protocol, wellbeing, and AWKA data remain reference-only"
    results.append(result("LINDA-HARDEN-007", harden_007))

    def harden_008():
        export = model.MODEL["capabilities"]["LINDA.CAP.EXPORT_ARTIFACT"]
        require("snapshot digest valid" in export["preconditions"], "Snapshot digest check missing")
        require("presentation glyph safety passes" in export["preconditions"], "Glyph safety export gate missing")
        require("cleartext secrets absent from standard artifact" in export["preconditions"], "Secret export gate missing")
        require("receipt created after final hashing" in export["postconditions"], "Post-hash receipt missing")
        artifact_purpose = model.MODEL["validator_definitions"]["LINDA.VAL.ARTIFACT"]["purpose"]
        require("fail-closed export behavior" in artifact_purpose, "Artifact Validator is not fail-closed")
        return "Final export requires Snapshot integrity, safe presentation, artifact hashing, and post-hash receipt"
    results.append(result("LINDA-HARDEN-008", harden_008))

    def generic_001():
        contract = manifest["genericization_contract"]
        require(contract["generic_release"] is True, "Generic release marker missing")
        require(contract["company_specific_values_allowed_in_definition_files"] is False, "Company-specific values remain permitted")
        require(contract["placeholder_syntax"] == "[UPPER_SNAKE_CASE]", "Placeholder syntax drifted")
        require(len(contract["required_placeholders"]) == 12, "Expected twelve organization placeholders")
        require(contract["unresolved_required_placeholder_blocks_activation"] is False, "Generic template placeholders should not block Domain activation")
        return {"generic_release": True, "required_placeholders": 12, "three_file_activation": True}
    results.append(result("LINDA-GENERIC-001", generic_001))

    def generic_002():
        template = model.organization_configuration_template()
        require(len(template) == 12, "Model configuration template count drifted")
        template_validation = model.validate_organization_configuration(template)
        require(template_validation["status"] == "VALID_GENERIC_TEMPLATE", "Embedded generic template did not validate")
        require(template_validation["template_mode"] is True, "Template mode not detected")
        configured = {key: f"Configured value for {key}" for key in template}
        validation = model.validate_organization_configuration(configured)
        require(validation["status"] == "VALID_AUTHORIZED_OVERRIDE", "Authorized organization override did not validate")
        require(validation["required_keys"] == 12, "Configuration validation key count drifted")
        require(validation["job_report_evidence"] is False, "Configuration became Job Report evidence")
        return "The embedded generic template activates within the three-file package; authorized overrides remain optional and non-evidentiary"
    results.append(result("LINDA-GENERIC-002", generic_002))

    def generic_003():
        manifest_text = json.dumps(manifest, ensure_ascii=False)
        model_text = model_path.read_text(encoding="utf-8")
        required = set(manifest["genericization_contract"]["required_placeholders"].values())
        for placeholder in required:
            require(placeholder in manifest_text or placeholder in model_text, f"Required generic placeholder missing: {placeholder}")
        require(manifest["runtime_identity"]["author"] == "[IMPLEMENTING_ORGANIZATION_NAME]", "Manifest author is not generic")
        branding = model.MODEL["presentation_contract"]["organization_branding_policy"]
        require(branding["organization_name"] == "[IMPLEMENTING_ORGANIZATION_NAME]", "Organization placeholder missing")
        require(branding["unresolved_placeholder_display_permitted"] is False, "Unresolved placeholders may render")
        return "Generic Manifest and Model use only controlled organization placeholders for organization identity and branding"
    results.append(result("LINDA-GENERIC-003", generic_003))

    def generic_004():
        configuration = model.MODEL["organization_configuration_contract"]
        require(configuration["configuration_values_may_not_populate_job_facts_without_evidence"] is True, "Configuration can improperly establish Job facts")
        require(configuration["configuration_values_may_supply_branding_and_controlled_defaults"] is True, "Branding configuration disabled")
        require(configuration["secret_values_prohibited"] is True, "Secrets remain permitted in organization configuration")
        require(manifest["organization_configuration_contract"]["restricted_values_use_controlled_references_only"] is True, "Restricted configuration values may render directly")
        descriptor = model.domain_descriptor()
        require(descriptor["workflow_instance_type"] == "LINDA-GENERIC-JOB-REPORT-HARDENED-REV3", "Generic workflow instance type drifted")
        release = model.release_contract()
        require(release["uploaded_components"] == [MANIFEST_FILE, MODEL_FILE, Path(__file__).name], "Generic release filenames drifted")
        return "Generic configuration is branding-only, non-evidentiary, secret-free, reference-controlled, and release-consistent"
    results.append(result("LINDA-GENERIC-004", generic_004))

    executed_ids = [item["test_id"] for item in results]
    require(executed_ids == EXPECTED_TEST_IDS, "Test order or count drifted")
    failures = [item for item in results if not item["passed"]]
    return {
        "verification_suite": SUITE_ID,
        "version": VERSION,
        "awka_version": AWKA_VERSION,
        "declared_tests": len(EXPECTED_TEST_IDS),
        "executed_tests": len(results),
        "required_failures": len(failures),
        "status": "PASS" if not failures else "FAIL",
        "model_sha256": file_digest(model_path),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", default=".")
    parser.add_argument("--output", default="LINDA_Generic_Verification_Result_v1.0.0-alpha.6.json")
    args = parser.parse_args()
    report = run(Path(args.package_dir))
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("version", "awka_version", "declared_tests", "executed_tests", "required_failures", "status")}, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
