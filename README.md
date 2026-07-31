# AWKA

## Abstract Workflow Kernel Architecture

_A microkernel architecture for governed Large Language Model (LLM) applications._

## Overview

AWKA is an architectural research project exploring whether complex LLM applications should be governed by **software architecture** rather than increasingly sophisticated prompts.

Instead of embedding workflow logic, validation, authorization, state management, evidence handling, and artifact governance directly into prompts, AWKA separates these concerns into a reusable architectural kernel.

The result is a layered architecture in which:

- the **AWKA Kernel** provides domain-independent architectural services;
- **Domain Runtimes** provide business semantics;
- **Workflow Instances** represent individual operational sessions;
- **Canonical State** represents authoritative workflow truth;
- **Snapshots** preserve immutable state history;
- **Artifact Receipts** attest to controlled exports.

AWKA is not a chatbot, prompt library, or agent framework.

It is an architectural kernel for governed AI-assisted applications.

## Positioning

AWKA does **not** challenge the current direction of the AI application ecosystem.

Modern frameworks are rapidly improving:

- agent orchestration;
- multi-agent workflows;
- tool and function calling;
- memory and persistence;
- human-in-the-loop control;
- observability;
- external data and tool connectivity.

**AWKA would not have been possible without this evolution.**

The emergence of capable AI agent platforms revealed a new architectural problem: once AI systems can coordinate actions, call tools, persist memory, generate artifacts, and participate in multi-step workflows, the critical question is no longer only how to make them more capable. The critical question becomes when their outputs, actions, or conclusions are allowed to become authoritative state.

AWKA exists because current AI systems are powerful enough to require a governance boundary.

Agent frameworks and AI application platforms provide increasingly sophisticated execution capabilities. They help systems reason, plan, coordinate, retrieve information, call tools, and produce outputs. AWKA assumes those capabilities exist. It does not attempt to replace them.

Instead, AWKA addresses the architectural layer that appears after those capabilities become useful:

> When should an AI-assisted operation be admitted into governed workflow state?

In this sense, AWKA is best understood as a **governance boundary** for consequential AI-assisted workflows.

Where agent frameworks ask:

> How should agents reason, coordinate, call tools, and execute workflows?

AWKA asks:

> When is an AI-assisted operation allowed to become authoritative workflow state?

AWKA is therefore complementary to modern AI agent platforms. It depends on their progress, but separates their generative, probabilistic, and tool-using behavior from the deterministic act of admitting state, evidence, artifacts, and workflow transitions into an authoritative system of record.

## Research Motivation

Prompt engineering has enabled remarkable progress in controlling LLM behavior.

As systems become increasingly complex, however, prompts often begin to assume responsibilities traditionally associated with software architecture, including:

- workflow orchestration;
- validation;
- authorization;
- state management;
- evidence tracking;
- version control;
- auditability;
- artifact generation;
- tool governance;
- failure handling.

AWKA explores an alternative hypothesis:

> Complex LLM applications may become more maintainable when governance is expressed through architecture rather than prompt composition.

The project investigates whether AI-assisted systems can remain flexible and probabilistic at the reasoning layer while becoming deterministic and verifiable at the governance layer.

## Core Design Principles

AWKA is built around several architectural principles.

- **Architecture precedes behavior**
- **Domain-independent kernel**
- **Behavior defined through registered Capabilities**
- **Canonical State as the authoritative operational state**
- **Validation before mutation**
- **Evidence before assertion**
- **Immutable Snapshots**
- **Pure Renderers**
- **Atomic state transitions**
- **Executable conformance verification**
- **Runtime immutability after Domain activation**
- **Tool and model output treated as data until admitted**
- **Artifacts as projections, not sources of truth**
- **Conversation as expression, not authority**
- **Fail-closed governance under ambiguity**

## Architecture

```text
                   User
                    |
            Natural Language
                    |
       +------------------------+
       |      AWKA Kernel       |
       +------------------------+
          Constitution
          Runtime
          Verification
                    |
       Domain Runtime Activation
                    |
       +------------------------+
       |    Domain Runtime      |
       +------------------------+
          Entities
          Capabilities
          Validators
          Workflows
          Renderers
          Policies
          Tool Bindings
                    |
             Workflow Instance
                    |
   Evidence -> Candidate Facts -> Canonical State
                    |
               Snapshots
                    |
             Pure Renderers
                    |
               Artifacts
                    |
            Artifact Receipts
```

## Execution Model

AWKA operates in three intentionally separate stages.

```text
Bootstrap Kernel
        |
        v
Activate Domain Runtime
        |
        v
Create Workflow Instance
```

These stages remain separate by design.

- **Kernel Bootstrap** initializes the domain-independent governance environment.
- **Domain Activation** verifies and freezes business definitions.
- **Workflow Instance Creation** begins an operational business session.

Activating a Domain Runtime prepares the execution environment but does **not** create business data.

## Architectural Layers

```text
Layer 1
AWKA Kernel
        |
        v
Layer 2
Domain Runtime
        |
        v
Layer 3
Workflow Instance
```

This separation allows multiple domains to share the same architectural kernel.

The Kernel contains no business knowledge.

Domain behavior belongs to Domain Runtime Definitions.

## Project Structure

```text
AWKA/
├── paper/
│   └── Research paper and architectural analysis
│
├── awka/
│   └── Kernel Constitution, Runtime, Verification, and guides
│
├── linda/
│   └── Reference Domain Runtime
│
├── andy/
│   └── Narrative workflow Domain Runtime
│
├── docs/
│   └── User guides, roadmap, handoff documents, and analysis reports
│
└── examples/
    └── Demonstration materials and test fixtures
```

## Repository Components

### AWKA Kernel

The Kernel provides reusable architectural services.

It contains:

- Constitution;
- Runtime;
- Verification Suite;
- Bootstrap Directive;
- User Guide.

The Kernel is domain-independent and contains **no business knowledge**.

The Kernel is responsible for:

- lifecycle management;
- Definition Registry initialization and locking;
- Domain Runtime activation;
- Capability dispatch;
- Validator execution;
- Canonical State management;
- Snapshot management;
- event and audit services;
- renderer dispatch;
- artifact receipt support;
- atomic transaction behavior;
- optimistic concurrency controls.

### LINDA

LINDA, the **Language Intake and Narrative Documentation Authority**, is the current reference Domain Runtime.

It demonstrates how a complete business workflow can be implemented without modifying the AWKA Kernel.

LINDA contributes:

- Domain entities;
- controlled workflow definitions;
- business rules;
- Capabilities;
- Validators;
- Renderers;
- Tool Bindings;
- presentation policies;
- executable verification.

The current implementation models a controlled language-services Job Report workflow.

LINDA is a reference domain, not the AWKA Kernel itself.

### ANDY

ANDY, the **Adopted Narrative Directional Yielder**, is a narrative workflow Domain Runtime for AWKA.

ANDY demonstrates how AWKA can govern an AI-assisted narrative or procedural workflow without allowing prompt text, draft artifacts, model output, tool output, or informal conversation to become authoritative state directly.

ANDY contributes:

- narrative workflow entities;
- one controlled narrative procedure workflow;
- primitive and composite Capabilities;
- validation-before-mutation controls;
- final export projection integrity;
- artifact-set export governance;
- artifact body resolution;
- runtime state serialization consistency;
- Artifact Receipt and Artifact Set Receipt digest controls;
- adapter routing rules for approved workflow commands;
- AWKA alpha.4-compatible Event Registry Catalog projection;
- executable conformance verification.

ANDY is a Domain Runtime, not the AWKA Kernel itself.

Activation publishes and freezes ANDY definitions, but does **not** create a workflow instance or business data.

## ANDY v1.0.0-alpha.7: Rigid Governance Runtime

ANDY v1.0.0-alpha.7 is a **rigid governance** version of ANDY.

Rigid means that workflow mutation is constrained by registered Capability routes, Validator gates, state preconditions, stage rules, required artifact slots, Evidence Packet requirements, and explicit user-confirmed transitions.

The user may request action, but the user cannot bypass the active workflow contract with vague language, shorthand commands, conversational approval, or premature advancement.

The first alpha.7 workflow test demonstrated this property:

- incomplete stage execution did not mutate state;
- shorthand `Accept` did not accept an artifact;
- an attempted evaluate-and-advance command evaluated the stage but blocked advancement until explicit completion confirmation occurred;
- artifact acceptance did not imply stage completion;
- stage completion did not imply advancement;
- finalization, export, and closure remained separate governed operations.

This is intentional. ANDY alpha.7 shows that even an authorized user must operate through the governance workflow.

## Current Baseline

### AWKA Kernel

- Version: `1.0.0-alpha.4`
- Status: Research Prototype
- Executable conformance: `17/17 PASS`

The current AWKA Kernel baseline uses a three-file bootstrap package:

```text
001_AWKA_Constitution_v1.0.0-alpha.4.json
002_AWKA_Runtime_v1_0_0_alpha_4.py
003_AWKA_Verification_v1_0_0_alpha_4.py
```

### LINDA Generic Hardened Domain Runtime

- Version: `1.0.0-alpha.6`
- Status: Reference Domain Runtime

The current LINDA Generic baseline uses a three-file Domain Runtime package:

```text
001_LINDA_Generic_Manifest_v1.0.0-alpha.6.json
002_LINDA_Generic_Model_v1_0_0_alpha_6.py
003_LINDA_Generic_Verification_v1_0_0_alpha_6.py
```

### ANDY Domain Runtime

- Version: `1.0.0-alpha.7`
- Status: Rigid Narrative Workflow Domain Runtime
- Compatible Kernel: `AWKA v1.0.0-alpha.4`
- Executable conformance: `260/260 PASS`
- Release theme: Rigid Governance Workflow and AWKA Alpha.4 Event Registry Projection Compatibility Release

The current ANDY baseline uses a three-file Domain Runtime package:

```text
001_ANDY_Manifest_v1.0.0-alpha.7.json
002_ANDY_Model_v1_0_0_alpha_7.py
003_ANDY_Verification_v1_0_0_alpha_7.py
```

ANDY activation is message-delivered and is not a fourth release component.

Activation verifies the Manifest, Model, Verification Suite, Definition Registry population, conformance report, Event Registry Catalog projection, and Kernel activation boundary before freezing the Domain Runtime definitions.

The installation or activation directive is message-delivered and is not a fourth release component unless a future release explicitly declares otherwise.

## Current Reference Runtimes

### Generic LINDA

The generic LINDA reference implementation demonstrates:

- evidence registration;
- Candidate Fact extraction;
- human approval;
- Canonical State population;
- immutable Snapshots;
- controlled exports;
- executable conformance verification;
- organization configuration as non-evidentiary deployment data;
- artifact generation with post-hash Artifact Receipts.

Generic LINDA uses an embedded organization template that is valid for Domain activation.

Organization-specific overrides are optional, auditable, and non-evidentiary.

Final customer-facing artifacts must not display unresolved placeholders.

### ANDY Narrative Workflow

ANDY demonstrates a governed narrative workflow under the same AWKA Kernel boundary used by other Domain Runtimes.

The alpha.7 implementation emphasizes:

- separation between Domain activation and workflow creation;
- no workflow instance creation during activation;
- no Canonical State, Snapshot, Artifact Receipt, or governed instance data created as an activation side effect;
- AWKA alpha.4-compatible Event Registry Catalog projection through `schema_registry`;
- no first-class `event_registry` publication under AWKA alpha.4;
- composite Capabilities built from primitive Capability sequences;
- preservation of the primitive artifact lifecycle under composite operations;
- explicit adapter routing for payload-bearing commands;
- rejection of vague, incomplete, shorthand, or wrong-state commands as non-mutating or precondition-blocked;
- rigid governance where even an authorized user cannot bypass the workflow sequence;
- final export projection QA that prevents draft-status language from leaking into final exports;
- Artifact Receipts that record both source artifact digests and exported projection digests;
- Artifact Set Receipts that record package digests;
- artifact body resolution records for exported member artifacts;
- runtime serialization consistency between Canonical State and Snapshot views.

The current ANDY activation milestone is:

```text
ANDY Domain Runtime v1.0.0-alpha.7 activated on AWKA v1.0.0-alpha.4.
Executable conformance: 260/260 PASS.
Rigid governance workflow enabled.
Event Registry Catalog projection active for AWKA alpha.4 compatibility.
Awaiting workflow command: Run New ANDY Workflow.
```

## Example Lifecycle

```text
Source Packet
        |
        v
Source Evidence
        |
        v
Candidate Facts
        |
        v
Review / Approval
        |
        v
Registered Capability
        |
        v
Validation
        |
        v
Canonical State
        |
        v
Snapshot
        |
        v
Renderer
        |
        v
Artifact
        |
        v
Artifact Receipt
```

Only committed Canonical State represents workflow truth.

A generated artifact is a projection of a Snapshot.

A final controlled export is not complete until the final artifact bytes are hashed and an Artifact Receipt or Artifact Set Receipt is created.

## Why "Microkernel"?

The architecture intentionally resembles a microkernel operating system.

The Kernel provides stable infrastructure.

Business behavior is supplied by loadable Domain Runtimes.

```text
Kernel
  |
  v
Domain Runtime
  |
  v
Workflow Instance
```

The Kernel should not change when a new business domain is introduced.

A new domain should be supplied as a verified Domain Runtime, activated through the Kernel, and frozen through Definition Registries before operational use.

## Compatibility With Existing AI Frameworks

AWKA is compatible with existing AI application frameworks because it operates at a different architectural layer.

| Existing direction | What it provides | AWKA relationship |
|---|---|---|
| Agent orchestration frameworks | Agent execution, coordination, memory, durability, and workflow patterns | AWKA can govern whether agent outputs or actions become Canonical State |
| Function and plugin systems | Model-to-function integration and API exposure | AWKA can register functions as Tool Bindings or Capability implementations |
| Tool protocols such as MCP | Standardized access to tools, resources, prompts, and external systems | AWKA can treat external outputs as data, evidence, or Candidate Facts until admitted |
| Multi-agent governance research | Risk analysis, staged testing, benchmarking, and red teaming | AWKA provides runtime governance objects and mutation boundaries |

AWKA does not replace these systems.

It can complement these systems by adding a deterministic governance boundary around consequential workflow operations.

## Execution Witness Direction

A proposed future Kernel service is the **Execution Witness**.

The Execution Witness would produce exactly one immutable **Execution Observation** for each governed Capability invocation, including committed, rejected, rolled-back, failed, and idempotent outcomes.

The Witness must not:

- authorize operations;
- validate business rules;
- infer meaning;
- interpret policy;
- mutate business state;
- call an LLM;
- decide whether an operation succeeds.

It would only attest to the lifecycle and result determined by the Kernel.

An Execution Observation is audit evidence.

It is **not** Source Evidence and must never populate business fields merely because it records that processing occurred.

## Research Goals

The project explores several research questions.

- Can architectural kernels improve LLM governance?
- Can prompts become transport rather than behavioral authority?
- Can business behavior be isolated into reusable Domain Runtimes?
- Can narrative workflows be governed without allowing draft artifacts or prompt text to bypass architectural authority?
- Can executable architectural verification improve reliability?
- Can deterministic workflow governance coexist with probabilistic reasoning?
- Can artifacts become verifiable projections rather than informal outputs?
- Can multi-agent risk be reduced by separating proposal, evidence, validation, and Canonical State?
- Can rigid workflow governance improve reliability without eliminating useful AI-assisted generation?

These questions remain open and are intended to encourage discussion.

## Roadmap

Planned directions include:

- evidence quality validation hardening;
- placeholder evidence rejection;
- raw conversation-turn persistence for inspection-grade transcript generation;
- receipt digest semantics clarification;
- configuration lifecycle hardening;
- signed Manifests and trusted release support;
- migration and compatibility framework;
- recovery, concurrency, and interruption handling;
- independently verifiable Artifact Receipts;
- Definition-to-Runtime enforcement coverage mapping;
- generic Capability execution pipeline;
- guarded workflow transition interpreter;
- deterministic semantic relationship projection;
- provenance and impact-analysis APIs;
- declarative constitutional invariants;
- Execution Witness prototype;
- additional Domain Runtimes;
- SDK for Domain Runtime development;
- empirical evaluation against existing agent frameworks.

The roadmap intentionally prioritizes runtime enforcement before ontology or semantic-graph expansion.

## Current Status

Current maturity:

```text
AWKA
Version: 1.0.0-alpha.4
Status: Research Prototype

LINDA Generic Hardened Domain Runtime
Version: 1.0.0-alpha.6
Status: Reference Domain Runtime

ANDY Domain Runtime
Version: 1.0.0-alpha.7
Status: Rigid Narrative Workflow Domain Runtime
```

The project is currently intended for:

- architectural research;
- prompt engineering research;
- software architecture exploration;
- executable specification experiments;
- AI workflow governance;
- domain-runtime modeling;
- conformance and verification experiments.

It is **not** production software.

A production implementation would require additional controls such as durable transactional storage, authentication integration, tenant isolation, distributed locking, secure tool execution, signed releases, recovery procedures, monitoring, and independent security review.

## Contributing

This repository is currently an architectural research project.

Suggestions, critiques, discussions, and architectural feedback are welcome.

Useful contributions include:

- architectural review;
- conformance test design;
- negative-path scenario design;
- Domain Runtime experiments;
- narrative workflow governance experiments, including ANDY scenarios;
- documentation improvements;
- runtime hardening proposals;
- failure-mode analysis;
- comparisons with existing agent and workflow frameworks.

Please preserve the core governance boundary:

> Semantic richness may explain execution. It must not bypass authority.

> Behavior is a consequence of architecture.
