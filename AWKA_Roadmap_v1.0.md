# AWKA Roadmap

**Document status:** Proposed architectural roadmap  
**Roadmap version:** 1.0  
**Date:** July 29, 2026  
**Scope:** AWKA Kernel, Constitution, Runtime, Verification, Domain activation, and domain runtimes such as LINDA

---

## 1. Purpose

This roadmap translates the accepted findings from an independent architectural review into a controlled evolution plan for AWKA.

AWKA should continue to be developed as a **deterministic governance kernel for activating and operating verified domain runtimes in an AI-assisted environment**. Its defining characteristics currently remain:

- governance before execution;
- strict separation between Kernel infrastructure and Domain behavior;
- executable admission control before activation;
- versioned and immutable runtime definitions;
- atomic activation and fail-closed behavior;
- capability-controlled mutation;
- explicit evidence, provenance, and artifact-integrity controls.

The roadmap adopts semantic relationships, graph introspection, declarative invariants, and stronger runtime interpretation where they improve traceability and extensibility. It does **not** replace the registries, capabilities, or deterministic workflow controls that currently provide AWKA's enforcement boundary, as proposed by the independent review.

---

## 2. Architectural Position

### 2.1 Target architecture

AWKA should evolve through additive layers:

```text
AWKA Constitution
        |
        v
Authoritative Definition Registries
        |
        +--> Typed Semantic Relationship Index
        |          |
        |          +--> dependency analysis
        |          +--> provenance traversal
        |          +--> impact analysis
        |          +--> architectural introspection
        |
        +--> Deterministic Runtime Interpreter
                   |
                   +--> capabilities
                   +--> guarded state transitions
                   +--> validators
                   +--> controlled mutations
                   +--> renderers and artifact receipts
```

### 2.2 Architectural boundary

The layers have distinct responsibilities:

- **Constitution:** Cross-domain architectural authority and machine-evaluable invariants.
- **Definition Registries:** Authoritative identity, namespace, version, publication, and locking of definitions.
- **Semantic Relationship Index:** A deterministic projection of accepted definitions and runtime provenance.
- **Runtime Interpreter:** Enforces capabilities, workflow guards, authority, validation, mutation permissions, and event emission.
- **Instance Stores:** Hold mutable workflow state only through registered capabilities.
- **Evidence and Provenance Stores:** Explain what supports each accepted fact and why it entered canonical state.
- **Artifact Receipt Store:** Attests to selected Snapshot, renderer, artifact digest, status, and export time.

---

## 3. Roadmap Principles

All initiatives should satisfy these principles:

1. **Determinism over emergence.** Runtime behavior must be explicit, reproducible, testable, and governed.
2. **Registries remain authoritative.** Graph and ontology structures may enrich definitions but cannot bypass activation, versioning, or locking.
3. **Validation precedes mutation.** Any capability that can mutate an Instance Store must identify and pass its required validators.
4. **Evidence is separate from definition and configuration.** Configuration cannot become business evidence merely because it is available to the runtime.
5. **Human authority remains explicit.** Consequential approvals and exceptions require authorized human actors.
6. **Fail closed.** Unsupported, ambiguous, stale, conflicting, or integrity-invalid operations do not silently proceed.
7. **Backward compatibility is intentional.** Migration, deprecation, and rollback must be declared rather than inferred.
8. **Semantic additions must be queryable.** New relationships must support introspection and impact analysis, not merely duplicate prose.
9. **Artifacts require proof of production.** A successful controlled export requires a post-hash Artifact Receipt.
10. **Natural language and declarative controls coexist.** Prose explains policy; machine-evaluable data enforces suitable invariants.

---

## 4. Workstreams and Priorities

## Workstream A: Current Architecture Hardening

**Priority:** Immediate  
**Objective:** Complete the operational controls needed before introducing a broader semantic architecture.

### A1. Configuration lifecycle

Create first-class distinctions among:

- release configuration;
- embedded generic templates;
- deployment or organization overrides;
- workflow evidence;
- canonical business state;
- secret references;
- presentation substitution.

**Required outcomes:**

- A configuration classification schema.
- Explicit rules governing whether configuration is required, optional, or embedded.
- A rule that configuration does not become Job Report evidence.
- Separate activation-time and artifact-time placeholder policies.
- Audit events for accepted deployment overrides.
- No external configuration file unless a Domain release explicitly declares one as a component.

### A2. Signed release trust model

Extend component hashing into publisher-authenticated releases.

**Required outcomes:**

- Signed Manifest support.
- Trusted publisher-key registry.
- Signature algorithm and key-rotation policy.
- Revocation and compromised-key procedures.
- Distinction between byte integrity and publisher authenticity.
- Activation rejection for invalid, revoked, or untrusted signatures when signature enforcement is enabled.

### A3. Migration and compatibility framework

Define how Domains and Snapshots evolve across releases.

**Required outcomes:**

- Schema migration definitions.
- Field addition, deprecation, replacement, and removal policies.
- Snapshot compatibility declarations.
- Domain rollback rules.
- Historical execution against the original Domain version.
- Renderer-version capture for artifact reproducibility.
- Migration verification tests and reversible-migration rules where feasible.

### A4. Runtime recovery and concurrency

Strengthen behavior during interruptions and competing operations.

**Required outcomes:**

- Durable operation identifiers and idempotency handling.
- Lock acquisition, expiry, renewal, and abandoned-lock recovery.
- Stale-write rejection through version and digest tokens.
- Restart-safe activation and artifact generation.
- Cleanup of incomplete artifacts without issuing success receipts.
- Concurrent Workflow Instance isolation tests.
- Recovery runbooks and executable fault-injection tests.

### A5. Artifact reproducibility and receipt verification

Make artifact integrity independently verifiable.

**Required outcomes:**

- Receipt schema with Snapshot ID and digest, artifact digest, renderer ID and version, selected version, active version, timestamp, QA result, and export status.
- Receipt verification command and API.
- Re-render comparison policy.
- Clear definition of reproducible versus presentation-equivalent artifacts.
- Closure gates requiring an eligible final artifact and valid receipt.

### Exit criteria for Workstream A

- Configuration lifecycle is unambiguous and executable.
- Releases can be authenticated, not merely hashed.
- Domain and Snapshot migrations are declared and tested.
- Interrupted operations recover without partial success claims.
- Artifact receipts can be independently verified.

---

## Workstream B: Runtime-Driven Behavior

**Priority:** High  
**Objective:** Move from verified declarations toward a generic interpreter that directly enforces those declarations.

### B1. Definition-to-runtime coverage map

For every declarative contract, classify its enforcement level:

```text
Declared only
Loaded and queryable
Runtime enforced
Executable conformance proven
```

**Required outcomes:**

- Coverage report for every Capability, Validator, Workflow Transition, Renderer, Tool Binding, and Rule.
- No installation-critical rule may remain merely declarative without an explicit exception.
- Verification tests must distinguish structural presence from actual runtime enforcement.

### B2. Generic capability interpreter

Implement a runtime execution pipeline driven by registered Capability definitions.

**Pipeline:**

```text
Resolve capability
-> authenticate actor
-> validate authority
-> validate current state
-> validate concurrency token
-> resolve required validators
-> execute validators in order
-> authorize permitted mutations
-> commit atomically
-> emit declared events
-> create successor Snapshot when required
```

### B3. Guarded state-transition interpreter

Formalize existing workflows as deterministic state graphs.

Each transition must declare:

- source state;
- destination state;
- invoking Capability;
- guard conditions;
- required authority;
- required validators;
- permitted mutations;
- emitted events;
- failure effect;
- idempotency policy;
- concurrency requirement.

The current state and transition registries remain authoritative. The graph representation provides traversal and formal validation.

### B4. Executable behavior conformance

Expand Verification Suites beyond definition checks.

**Required test categories:**

- positive path;
- unauthorized actor;
- invalid state;
- stale concurrency token;
- missing evidence;
- ambiguous evidence;
- validator failure;
- mutation outside permitted stores;
- duplicate invocation;
- event mismatch;
- failed transaction rollback;
- incorrect Snapshot lineage.

### Exit criteria for Workstream B

- Registered Capability contracts drive the standard execution pipeline.
- Workflow transitions are enforced as guarded graph edges.
- Runtime enforcement coverage is measurable.
- Critical behavior is proven through executable negative and positive tests.

---

## Workstream C: Typed Semantic Relationship Layer

**Priority:** High after Workstreams A and B foundations  
**Objective:** Make architectural relationships first-class and queryable without displacing authoritative registries.

### C1. Semantic edge model

Introduce typed, versioned relationships such as:

```text
Field --validated_by--> Validator
Field --supported_by--> Candidate Fact
Candidate Fact --extracted_from--> Evidence Source
Candidate Fact --maps_to--> Field
Capability --permitted_in--> Workflow State
Capability --requires_authority--> Role
Capability --invokes--> Validator
Capability --mutates--> Instance Store
Transition --invoked_by--> Capability
Snapshot --rendered_by--> Renderer
Renderer --invokes--> Tool Binding
Artifact Receipt --attests_to--> Artifact
Artifact Receipt --references--> Snapshot
```

Each edge must include:

- stable relationship ID;
- source and target IDs;
- relationship type;
- version applicability;
- authority source;
- activation status;
- optional evidence or derivation reference.

### C2. Deterministic graph projection

The initial graph must be generated from accepted definitions rather than maintained as a competing source of truth.

**Rules:**

- Registries are authoritative.
- Graph generation is deterministic.
- Graph digest is recorded.
- Orphaned targets, invalid edge types, and prohibited cycles block activation.
- Rebuilding from the same definitions produces the same graph digest.

### C3. Architectural introspection APIs

Add read-only APIs for:

- dependency traversal;
- reverse dependency lookup;
- impact analysis;
- orphan detection;
- cycle detection;
- provenance paths;
- definition ownership;
- transition justification;
- validator coverage;
- artifact lineage.

Representative questions:

```text
Why is this field blocked?
Which validators protect this Capability?
What definitions depend on this field?
What permits this transition?
Which evidence supports this canonical value?
Which Snapshot produced this artifact?
```

### C4. Graph security and authority

Prevent semantic relationships from becoming a bypass.

**Required controls:**

- No edge may grant authority not present in a registered definition.
- No inferred edge may authorize mutation.
- Derived edges must identify their deterministic derivation rule.
- Query results must respect access classifications.
- Sensitive provenance may be summarized while the restricted record remains external.

### Exit criteria for Workstream C

- Relationships are queryable and versioned.
- The graph is reproducible from registries.
- Impact and provenance traversal are available.
- Semantic data cannot authorize execution independently.

---

## Workstream D: First-Class Knowledge and Provenance Model

**Priority:** Medium  
**Objective:** Represent definition, evidence, canonical state, and provenance without collapsing their authority boundaries.

### D1. Four-layer knowledge separation

Implement separate but connected models:

1. **Definition graph:** What objects and relationships are valid.
2. **Evidence graph:** What sources support proposed assertions.
3. **Canonical-state graph:** What the active workflow currently accepts.
4. **Provenance graph:** Why an accepted value exists and which action admitted it.

### D2. Assertion lifecycle

A proposed assertion must progress through explicit states:

```text
Extracted
-> Classified
-> Reviewed
-> Accepted or Rejected
-> Incorporated into Canonical State
-> Superseded or Retained
```

No graph relationship alone makes an assertion canonical.

### D3. Provenance completeness

Every populated canonical field must resolve to at least one permitted origin:

- approved evidence;
- authorized human entry;
- registered controlled default;
- registered deterministic derivation.

### D4. Explainability services

Provide deterministic explanations derived from provenance records, including:

- why a value was accepted;
- why a value remains unresolved;
- which conflict blocked finalization;
- which actor approved an exception;
- which rule produced a deterministic derivation.

### Exit criteria for Workstream D

- Knowledge assertions retain explicit authority status.
- Canonical state cannot be confused with extracted or inferred information.
- Every accepted value has a traversable provenance path.

---

## Workstream E: Declarative Constitutional Invariants

**Priority:** Medium  
**Objective:** Convert suitable architectural prose into machine-evaluable rules while preserving clear human explanations.

### E1. Invariant schema

A constitutional invariant should support:

```yaml
invariant_id: AWKA.INVARIANT.VALIDATION_BEFORE_MUTATION
applies_to: capability
condition:
  permitted_mutations:
    not_empty: true
requires:
  validator_ids:
    minimum_count: 1
severity: blocking
human_explanation: Mutation requires prior validation.
```

### E2. Suitable rules for declarative conversion

Prioritize:

- validation before mutation;
- namespace ownership;
- registry locking after activation;
- atomic activation;
- capability-only Instance Store mutation;
- required digest and signature checks;
- no Workflow Instance creation during Domain activation;
- required authority for consequential decisions;
- post-hash receipt requirements.

### E3. Rules retained in prose

Keep nuanced policy in natural language when formal conversion would create false precision. Each prose-only policy must identify:

- responsible interpreter or validator;
- test coverage;
- reason it is not yet declarative.

### Exit criteria for Workstream E

- High-value structural invariants are machine-evaluable.
- Human explanations remain available.
- Declarative rules are covered by executable tests.

---

## Workstream F: Affordance Metadata

**Priority:** Medium to low  
**Objective:** Improve discovery and introspection without replacing executable Capabilities.

Affordances may express that an object can participate in an operation:

```text
Snapshot --may_be_rendered_through--> Export Artifact Capability
Historical Snapshot --may_be_restored_through--> Restore Capability
Source Packet --may_be_approved_through--> Approve Source Capability
```

Affordances are descriptive only. The referenced Capability remains responsible for:

- authority;
- inputs;
- preconditions;
- validators;
- state guards;
- permitted mutations;
- events;
- failure effects;
- idempotency.

### Exit criteria for Workstream F

- Affordances improve discoverability.
- No affordance directly authorizes or performs mutation.
- Every executable affordance resolves to a registered Capability.

---

## Workstream G: Executable Ontology Research Track

**Priority:** Long-term research  
**Objective:** Explore richer domain representation after deterministic semantic infrastructure is proven.

This track may investigate Domains as executable ontologies, subject to strict constraints:

- Definition Registries remain authoritative.
- Ontology relationships cannot bypass Capabilities.
- Runtime interpretation rules are explicit and versioned.
- The same accepted ontology produces the same executable plan and digest.
- Inference cannot create authority, evidence, approval, or canonical facts.
- Every derived behavior is traceable to a registered rule.
- Activation and conformance testing remain mandatory.

### Research gates

Proceed only if:

- Workstreams A through E meet their exit criteria;
- graph projection is deterministic;
- runtime behavior is already definition-driven;
- ontology interpretation can be tested without weakened governance;
- a rollback path to conventional registered definitions exists.

---

## 5. Delivery Sequence

### Release Horizon 1: Governance hardening

- Configuration lifecycle.
- Signed releases.
- Migration and compatibility contracts.
- Recovery and concurrency controls.
- Artifact Receipt verification.
- Runtime enforcement coverage inventory.

### Release Horizon 2: Generic interpretation

- Capability execution pipeline.
- Guarded state-transition graph.
- Positive and negative executable behavior tests.
- Runtime coverage reporting.

### Release Horizon 3: Semantic introspection

- Typed relationship schema.
- Deterministic graph projection.
- Dependency, impact, and provenance APIs.
- Graph validation during activation.

### Release Horizon 4: Knowledge and constitutional enrichment

- Four-layer knowledge model.
- Assertion lifecycle.
- Explainability services.
- Declarative constitutional invariants.
- Affordance metadata.

### Release Horizon 5: Ontology research

- Controlled executable-ontology prototypes.
- Determinism and governance benchmarks.
- Formal decision on production adoption.

---

## 6. Success Measures

AWKA roadmap progress should be measured through objective controls:

- Percentage of critical contracts enforced by the generic runtime.
- Percentage of constitutional invariants that are machine-evaluable.
- Percentage of populated canonical fields with complete provenance paths.
- Number of unresolved or orphan semantic relationships at activation: target zero.
- Reproducibility rate for graph and Snapshot digests: target 100%.
- Failed-operation rollback rate without partial mutation: target 100%.
- Artifact exports with valid post-hash receipts: target 100%.
- Releases with authenticated publisher signatures: target 100% after signature enforcement.
- Migration suites with verified forward and declared rollback behavior.
- Concurrency and interruption scenarios covered by executable tests.

---

## 7. Governance and Change Control

Every roadmap initiative must include:

- an Architecture Decision Record;
- constitutional impact assessment;
- backward-compatibility analysis;
- threat and failure-mode analysis;
- registry and namespace impact;
- executable conformance tests;
- migration and rollback plan;
- documentation update;
- release Manifest changes;
- explicit approval authority.

No semantic, graph, ontology, or affordance feature may be activated dynamically after Domain activation unless AWKA introduces and verifies a constitutionally governed extension mechanism.

---

## 8. Accepted Ideas Registry

### ACC-001: Preserve Kernel and Domain separation

**Decision:** Accepted as a permanent architectural principle.  
**Reason:** It keeps the Kernel domain-independent and allows independently verified Domain Runtimes.

### ACC-002: Governance before execution

**Decision:** Accepted.  
**Reason:** Bootstrap, verification, activation, and only then execution materially reduce ambiguity and partial publication.

### ACC-003: Executable conformance before activation

**Decision:** Accepted and expanded.  
**Reason:** Architectural correctness should be demonstrated through executable admission control, including behavior tests rather than structural checks alone.

### ACC-004: Explicit semantic relationships

**Decision:** Accepted as an additive layer.  
**Reason:** Typed relationships improve provenance, dependency analysis, introspection, and change-impact assessment.

### ACC-005: First-class knowledge model

**Decision:** Accepted with authority boundaries.  
**Reason:** Definition, evidence, canonical state, and provenance should be connected but must remain distinct.

### ACC-006: Graph-based workflow representation

**Decision:** Accepted as formalization of existing states and transitions.  
**Reason:** The current workflow is already graph-like; guarded transition semantics and traversal make it more explicit without replacing deterministic tables.

### ACC-007: Declarative constitutional invariants

**Decision:** Accepted where practical.  
**Reason:** Machine-evaluable invariants reduce interpretive variance while human-readable explanations preserve governance clarity.

### ACC-008: Architectural introspection APIs

**Decision:** Accepted.  
**Reason:** Dependency, provenance, transition, and impact queries improve maintainability and auditability.

### ACC-009: Affordance metadata

**Decision:** Accepted as non-executable metadata.  
**Reason:** Affordances improve discovery, provided registered Capabilities retain all enforcement responsibilities.

### ACC-010: Executable ontology exploration

**Decision:** Accepted as a gated research track.  
**Reason:** Richer semantics may improve expressiveness, but production adoption requires proven determinism, traceability, and governance preservation.

---

## 9. Declined Ideas Registry

The entries below are declined in their original or unrestricted form. Some have an accepted, narrower alternative elsewhere in this roadmap.

### DEC-001: Replace Definition Registries with a semantic graph

**Status:** Declined.  
**Reason:** Registries provide authoritative identity, namespaces, version control, atomic publication, duplicate protection, and post-activation locking. A graph does not inherently provide those controls.  
**Accepted alternative:** Preserve registries as authoritative and derive a deterministic Semantic Relationship Index from them.

### DEC-002: Replace the registry-based architecture with an ontology-based architecture

**Status:** Declined as a wholesale replacement.  
**Reason:** An ontology is a representation model, while registries are an enforcement and publication boundary. Replacing registries would risk weakening activation and immutability.  
**Accepted alternative:** Add ontology-like semantics incrementally and retain registries, capabilities, and verification as governance controls.

### DEC-003: Replace procedural workflows entirely with a new graph interpreter

**Status:** Declined as stated.  
**Reason:** Existing workflow states and transitions already constitute a directed graph. Replacing them would add migration risk without first addressing missing guards, authority, validation, and introspection metadata.  
**Accepted alternative:** Formalize existing workflows as guarded state-transition graphs interpreted through registered definitions.

### DEC-004: Replace Capabilities with affordances

**Status:** Declined.  
**Reason:** Affordances do not express sufficient enforcement detail, including actor authority, required inputs, validators, permitted mutations, event emission, failure effects, concurrency, and idempotency.  
**Accepted alternative:** Use affordances as discovery relationships that resolve to registered Capabilities.

### DEC-005: Allow behavior to emerge from semantic relationships

**Status:** Declined for production.  
**Reason:** Unbounded emergent behavior conflicts with AWKA's deterministic governance objective. Relationships alone must not create executable authority or mutation rights.  
**Accepted alternative:** Permit only behavior produced by explicit, versioned, deterministic interpretation rules and proven by executable conformance tests.

### DEC-006: Treat graph relationships as knowledge or truth by default

**Status:** Declined.  
**Reason:** A relationship can be declared, extracted, inferred, disputed, or canonical. Treating all edges as truth would collapse definition, evidence, state, and provenance boundaries.  
**Accepted alternative:** Use separate Definition, Evidence, Canonical-State, and Provenance graphs with explicit authority status.

### DEC-007: Infer missing relationships during activation

**Status:** Declined.  
**Reason:** Activation-time inference could create undeclared dependencies or authority and make identical releases behave differently.  
**Accepted alternative:** Allow only registered deterministic derivations that produce reproducible edges and digests.

### DEC-008: Convert the entire Constitution into machine-only declarative data

**Status:** Declined.  
**Reason:** Some constitutional principles require nuanced explanation, and premature formalization can create false precision or omit important context.  
**Accepted alternative:** Pair machine-evaluable invariants with human-readable explanations and retain prose for rules not yet safely formalized.

### DEC-009: Treat organization configuration as Job Report evidence

**Status:** Declined.  
**Reason:** Configuration identifies deployment branding and controlled defaults; it does not prove facts about a specific assignment.  
**Accepted alternative:** Require approved evidence, authorized human entry, controlled default, or registered deterministic derivation for business fields.

### DEC-010: Require an external organization-configuration file for every generic Domain activation

**Status:** Declined.  
**Reason:** It unnecessarily expands the package and confuses release components with deployment overrides. Generic activation can use an embedded template while final artifacts enforce placeholder resolution.  
**Accepted alternative:** Three-file generic package with an embedded activation-valid template and optional authorized overrides.

### DEC-011: Permit unresolved generic placeholders in final artifacts

**Status:** Declined.  
**Reason:** Final customer-facing artifacts must not expose installation placeholders or appear incomplete.  
**Accepted alternative:** Allow placeholders for Domain activation but require resolved branding or deliberate omission before final export.

### DEC-012: Use SHA-256 alone as proof of trusted publisher identity

**Status:** Declined.  
**Reason:** A digest proves integrity relative to a known value but does not authenticate who published the Manifest.  
**Accepted alternative:** Retain SHA-256 for component integrity and add signed Manifests with trusted publisher keys.

### DEC-013: Claim successful export before final artifact hashing and receipt creation

**Status:** Declined.  
**Reason:** A pre-hash success claim cannot attest to the final bytes delivered to the user.  
**Accepted alternative:** Create the Artifact Receipt only after final hashing and require it for controlled final export.

### DEC-014: Allow semantic or ontology layers to bypass Capability-controlled mutation

**Status:** Declined.  
**Reason:** This would create an alternate mutation path outside authority, validation, concurrency, event, and rollback controls.  
**Accepted alternative:** Semantic layers remain read-only for execution purposes and resolve operations through registered Capabilities.

### DEC-015: Prioritize ontology conversion before runtime enforcement coverage

**Status:** Declined.  
**Reason:** Richer representation does not compensate for definitions that are not yet directly enforced by the generic Runtime.  
**Accepted alternative:** Complete the enforcement coverage map and generic interpreters before production ontology work.

---

## 10. Final Direction

AWKA's next stage should enrich representation without compromising enforcement.

The governing direction is:

> Preserve authoritative registries, atomic activation, registered Capabilities, guarded workflows, executable verification, and immutable Snapshots. Add a deterministic semantic relationship layer for dependency, provenance, knowledge separation, and introspection. Convert suitable constitutional rules into machine-evaluable invariants. Explore executable ontology behavior only after the runtime directly enforces definitions and only where interpretation remains explicit, reproducible, auditable, and subordinate to AWKA governance.

This approach advances AWKA from a strongly governed activation runtime toward a semantically richer execution platform while retaining the architectural discipline that distinguishes it.
