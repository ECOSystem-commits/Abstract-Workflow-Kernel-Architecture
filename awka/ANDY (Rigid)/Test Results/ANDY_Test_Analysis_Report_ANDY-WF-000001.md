# ANDY Test Analysis Report

**Workflow under test:** `ANDY-WF-000001`  
**ANDY runtime:** `1.0.0-alpha.7`  
**AWKA runtime:** `1.0.0-alpha.4`  
**Report type:** post-run behavioral analysis against expected ANDY/AWKA workflow behavior  
**Generated from:** inspection transcript, canonical workflow state, close result, and final artifact export

## 1. Executive Verdict

The workflow completed successfully at the runtime level. Activation was already successful, the domain was active, all five narrative stages reached a finalized state, five accepted dependency-eligible artifacts were exported, and the workflow closed cleanly.

However, the test should not be treated as a full production-quality pass. It is a strong **runtime/lifecycle PASS** with several **inspection findings** around evidence quality, transcript completeness, placeholder acceptance data, and digest lineage ambiguity in export receipts. The most important behavioral result is that the patched alpha.7 activation path appears to work under AWKA alpha.4: the Event Registry was not published as a first-class registry and the workflow proceeded to completion.

### High-level outcome

| Area | Expected behavior | Observed behavior | Verdict |
|---|---|---|---|
| Activation gate | ANDY alpha.7 active on AWKA alpha.4, tests PASS, event catalog projected into schema registry | Activation record reports PASS, 260/260, `event_catalog_present=true`, `event_registry_published=false` | PASS |
| Workflow lifecycle | Run new workflow, adopt narrative, execute stages, finalize, export, close | Workflow reached `CLOSED`, `workflow_status=closed`, active version 41, logical sequence 162 | PASS |
| Stage progression | Each stage must go through prompt, review, artifact acceptance, evaluation, confirmation, advance | All five stages advanced and all five required slots were satisfied | PASS |
| Fail-closed routing | Invalid shorthand or premature advance should not mutate canonical state | Invalid stage run and shorthand accept were non-mutating; premature advance was blocked | PASS with diagnostic note |
| Artifact lifecycle | Accepted artifacts must be evidenced, dependency eligible, body-resolved, and exported | Five artifacts accepted, evidence packet assigned, body resolution PASS, export QA PASS | PASS mechanically |
| Evidence quality | Evidence should carry concrete source inputs and meaningful acceptance statements | Evidence packets contain literal placeholders: `<source list>` and `<acceptance statement>` | FAIL for evidence substance |
| Export integrity | Export digest and QA should match final output | Final file SHA-256 equals recorded exported artifact digest | PASS |
| Snapshot receipt lineage | Receipt selected snapshot digest should be unambiguous and match selected snapshot record | Receipt selected snapshot digest differs from snapshot record canonical digest | CONCERN |
| Transcript completeness | Inspection transcript should include exact UI raw conversation if available | Transcript explicitly states it is partial for UI prose and reconstructed from runtime records | PARTIAL |

## 2. Source Files Inspected

- `ANDY_Workflow_ANDY-WF-000001_Inspection_Transcript.txt`  
  - Size: `513772` bytes  
  - SHA-256: `01c69cb6afc40af4aacb35a9ae749722ff3ad7df752828f186d784259288c48c`
- `ANDY_Workflow_ANDY-WF-000001_State (1).json`  
  - Size: `3321780` bytes  
  - SHA-256: `0e94ae9a7fccd5cfcebb1e2cac4de61ee59e94e6a473b8ada292fa3adf709c45`
- `ANDY_Workflow_ANDY-WF-000001_Close_Result.json`  
  - Size: `998` bytes  
  - SHA-256: `c0ad145b985277d834bed5f29cd3d388d3030e9d02e0d3b8e2eacb97a015312a`
- `ANDY_Final_Artifact_Set (1).txt`  
  - Size: `44288` bytes  
  - SHA-256: `6db76e943d47a12284d0d50d145d53bca59049f07f9aec5bb6cd6b65b977585a`

## 3. Observed Runtime Summary

| Field | Observed value |
|---|---|
| Workflow instance ID | `ANDY-WF-000001` |
| Final canonical state | `CLOSED` |
| Workflow status | `closed` |
| Active version | `41` |
| Logical sequence | `162` |
| Runtime event records | `135` |
| Snapshot records | `41` |
| Accepted artifacts | `5` |
| Artifact versions | `5` |
| Evidence packets | `5` |
| Artifact body resolution records | `5` |
| Artifact receipts | `5` |
| Artifact set receipts | `1` |
| Close result | `PASS` / `CLOSED` / `closed` |

## 4. Expected Behavior Model Used for Comparison

The expected behavior was inferred from the alpha.7 activation contract and the recorded ANDY workflow contract:

1. Kernel and domain must already be active before workflow creation.
2. `Run New ANDY Workflow` must create a workflow instance and initial snapshot.
3. Narrative adoption must load a five-stage linear workflow with five required artifact slots.
4. Stage execution must require an explicit prompt payload and must route through a registered capability path.
5. Draft artifacts must remain candidates until accepted with evidence.
6. Accepted artifacts must become dependency-eligible only after artifact registration, acceptance, evidence attachment, and dependency promotion succeed.
7. Stage completion must be evaluated before confirmation, and confirmation must occur before advancement.
8. Invalid shorthand, incomplete commands, or premature transitions must fail closed with no unauthorized mutation.
9. Finalization must occur only after all stages are complete and all required artifact slots are satisfied.
10. Export must include only accepted dependency-eligible artifacts and must emit receipts, body resolution records, QA records, and package digest.
11. Closing the workflow must occur only after export and must leave no next registered workflow command.
12. Auditability requires event records, snapshots, prompt route evidence, artifact lineage, evidence packets, and export receipts sufficient for inspection.

## 5. Activation Compatibility Assessment

The activation portion behaved as expected for the patched alpha.7 reissue. The inspection transcript records activation as `PASS`, with `declared_tests=260`, `executed_tests=260`, `required_failures=0`, `kernel_state=ACTIVE`, and `domain_state=DOMAIN_ACTIVE`. It also records `event_catalog_present=true` and `event_registry_published=false`, which is the expected AWKA alpha.4-compatible behavior after the Event Registry projection patch.

**Assessment:** PASS. The workflow would not have proceeded if the domain were not active. The completed workflow gives additional runtime evidence that the alpha.7 registry projection patch is viable in practice, not only in standalone verification.

## 6. Workflow Lifecycle Analysis

The lifecycle path matched the expected linear ANDY workflow sequence:

```text
Activation PASS
Run New ANDY Workflow
Adopt ANDY Narrative
STG-001 run -> accept -> evaluate -> confirm -> advance
STG-002 run -> accept -> evaluate -> confirm -> advance
STG-003 run -> accept -> evaluate -> confirm -> advance
STG-004 run -> accept -> evaluate -> confirm -> advance
STG-005 run -> accept -> evaluate -> confirm -> advance
Finalize workflow
Export artifact set
Close workflow
```

The final close result reports `previous_state=EXPORTED`, `current_state=CLOSED`, `closure_status=closed`, and `next_registered_workflow_command=null`, which is correct for a fully closed workflow.

## 7. Stage Completion Matrix

| Stage | Stage status | Review status | Completion confirmed | Slot | Slot disposition | Artifact version | Evidence packet | Body resolution |
|---|---|---|---:|---|---|---|---|---|
| `STG-001` | `stage_advanced` | `closed` | `True` | `SLOT-001` | `satisfied` | `ARTV-STG-001-SCOPE-BRIEF-001` | `EVD-STG-001-SCOPE-BRIEF-001` | `PASS` |
| `STG-002` | `stage_advanced` | `closed` | `True` | `SLOT-002` | `satisfied` | `ARTV-STG-002-TAXONOMY-001` | `EVD-STG-002-TAXONOMY-001` | `PASS` |
| `STG-003` | `stage_advanced` | `closed` | `True` | `SLOT-003` | `satisfied` | `ARTV-STG-003-INVARIANTS-001` | `EVD-STG-003-INVARIANTS-001` | `PASS` |
| `STG-004` | `stage_advanced` | `closed` | `True` | `SLOT-004` | `satisfied` | `ARTV-STG-004-AWKA-COMPARATIVE-001` | `EVD-STG-004-AWKA-COMPARATIVE-001` | `PASS` |
| `STG-005` | `stage_advanced` | `closed` | `True` | `SLOT-005` | `satisfied` | `ARTV-STG-005-FINAL-SYNTHESIS-001` | `EVD-STG-005-FINAL-SYNTHESIS-001` | `PASS` |

**Assessment:** PASS. All five expected stages are present, all five required slots are satisfied, all five artifacts are accepted dependency-eligible, and all five body resolution records pass.

## 8. Routing, Precondition, and Fail-Closed Behavior

The test included useful negative-path behavior:

- `Run stage STG-001` without an explicit prompt payload was rejected as `REJECTED_NON_MUTATING`.
- `Accept` shorthand during STG-003 review was rejected as `REJECTED_NON_MUTATING`.
- `Evaluate stage completion for STG-002, then advance to STG-003` produced a partial pass for evaluation but blocked the advance attempt with `BLOCKED_PRECONDITION`, because advance requires `STAGE_COMPLETE_CONFIRMED`.

These are good behavioral signals. The runtime did not silently coerce ambiguous instructions into mutating operations. It forced explicit registered command forms and preserved stage preconditions.

**Assessment:** PASS. This validates the design principle that language proposes, but registered capability routes mutate.

**Diagnostic note:** The canonical `rejection_records` object in the state file is empty even though the transcript records non-mutating rejections. This may be by design if route-level non-mutating diagnostics are not canonical rejection records. If the expected behavior is that all rejected user commands become canonical rejection records, this is a defect. If only failed mutating capability attempts are recorded there, this is acceptable but should be documented.

## 9. Event and Snapshot Analysis

| Event type | Count |
|---|---:|
| `ANDY.EVENT.ADAPTER_ROUTE_EVIDENCE_RECORDED` | `5` |
| `ANDY.EVENT.ARTIFACT_ACCEPTED_PENDING_EVIDENCE` | `5` |
| `ANDY.EVENT.ARTIFACT_BODY_RESOLVED` | `5` |
| `ANDY.EVENT.ARTIFACT_DEPENDENCY_ELIGIBLE` | `5` |
| `ANDY.EVENT.ARTIFACT_REGISTERED` | `5` |
| `ANDY.EVENT.ARTIFACT_SET_EXPORTED` | `1` |
| `ANDY.EVENT.ARTIFACT_SET_RECEIPT_CREATED` | `1` |
| `ANDY.EVENT.COMPOSITE_OPERATION_COMMITTED` | `11` |
| `ANDY.EVENT.COMPOSITE_OPERATION_STARTED` | `11` |
| `ANDY.EVENT.EVIDENCE_PACKET_ATTACHED` | `5` |
| `ANDY.EVENT.NARRATIVE_LOADED` | `1` |
| `ANDY.EVENT.NARRATIVE_VALIDATED` | `1` |
| `ANDY.EVENT.NEXT_STAGE_READY` | `4` |
| `ANDY.EVENT.SNAPSHOT_CREATED` | `41` |
| `ANDY.EVENT.STAGE_ADVANCED` | `5` |
| `ANDY.EVENT.STAGE_COMPLETION_CONFIRMED` | `5` |
| `ANDY.EVENT.STAGE_COMPLETION_EVALUATED` | `5` |
| `ANDY.EVENT.STAGE_EXECUTED` | `5` |
| `ANDY.EVENT.STAGE_PROMPT_SUBMITTED` | `5` |
| `ANDY.EVENT.STAGE_REVIEW_OPENED` | `5` |
| `ANDY.EVENT.WORKFLOW_CLOSED` | `1` |
| `ANDY.EVENT.WORKFLOW_COMPLETE` | `1` |
| `ANDY.EVENT.WORKFLOW_FINALIZED` | `1` |
| `ANDY.EVENT.WORKFLOW_INSTANCE_CREATED` | `1` |

- Event sequence range: `1` to `162`.
- Runtime event records present: `135`.
- Missing numeric event sequence values: `27` values: `[9, 10, 12, 21, 22, 29, 30, 40, 49, 50, 57, 58, 68, 77, 78, 85, 86, 96, 105, 106, 113, 114, 124, 133, 134, 141, 142]`.
- Snapshot records: `41`.
- Snapshot-created event to snapshot-record digest mismatches: `0`.

**Interpretation:** The event list is not numerically contiguous because the logical sequence appears to include non-event records, such as composite operation run start and completion records. This is not automatically a defect. The important sanity check is that every `ANDY.EVENT.SNAPSHOT_CREATED` event payload matched the corresponding snapshot record digest, and that check passed.

## 10. Artifact Lifecycle and Export Analysis

| Receipt | Artifact version | Accepted artifact | Body resolution | Export QA | Source artifact digest | Final projection digest |
|---|---|---|---|---|---|---|
| `RCPT-ANDY-WF-000001-0001` | `ARTV-STG-001-SCOPE-BRIEF-001` | `ACC-ARTV-STG-001-SCOPE-BRIEF-001` | `PASS` | `PASS` | `ab590e59c5177a0fb837b7849bccde45598eea644c7c001daffdbbeaeeb5edc5` | `74d8d1f925099e545c1e451e00c1548fc4876b4cc7f65de3b954cc5ed5a943a6` |
| `RCPT-ANDY-WF-000001-0002` | `ARTV-STG-002-TAXONOMY-001` | `ACC-ARTV-STG-002-TAXONOMY-001` | `PASS` | `PASS` | `f2762c2fb0982dba7928336d46e7613d5ee617f4a974dbec80d70ab488845a04` | `1ce1b36232a526f1d04258d7a7e83f156b3f84840c875775dfccdff3e4e03bb6` |
| `RCPT-ANDY-WF-000001-0003` | `ARTV-STG-003-INVARIANTS-001` | `ACC-ARTV-STG-003-INVARIANTS-001` | `PASS` | `PASS` | `d9ab2cfde1cebb0cd0c31c1da42e64727feeb203f7fa96dc683923148b911c2c` | `9085a99123abb2ec44963681fe49ddab109fea7f15a4326953aac1fc4f211316` |
| `RCPT-ANDY-WF-000001-0004` | `ARTV-STG-004-AWKA-COMPARATIVE-001` | `ACC-ARTV-STG-004-AWKA-COMPARATIVE-001` | `PASS` | `PASS` | `188bf859e90a969b2da0a3dff8dbce3455c827ae22845574a3a9f93f7bdc0405` | `6893e90c265df7c626a0c9a50c27149de813aa827ec157b548280e9c494f184e` |
| `RCPT-ANDY-WF-000001-0005` | `ARTV-STG-005-FINAL-SYNTHESIS-001` | `ACC-ARTV-STG-005-FINAL-SYNTHESIS-001` | `PASS` | `PASS` | `ed1e4323acfe006bf66c8f5624bad9c97d95aa553d51f40760479a1d0cb99249` | `80cc43c66598a6df38b670531279cf82262602dd6a77fa7db645a2b01a579d61` |

The export QA record reports:

- QA status: `PASS`
- Body rewrite policy: `PASS`
- Forbidden phrase scan: `PASS`
- Lifecycle projection: `PASS`
- Required lineage fields present: `PASS`
- Visible status match: `PASS`
- Exported artifact digest: `6db76e943d47a12284d0d50d145d53bca59049f07f9aec5bb6cd6b65b977585a`
- Actual final export SHA-256: `6db76e943d47a12284d0d50d145d53bca59049f07f9aec5bb6cd6b65b977585a`
- Digest match: `True`

**Assessment:** PASS for export mechanics. The final export file digest matches the recorded exported artifact digest, all member receipts are present, and all body resolution records passed.

## 11. Evidence Quality Analysis

This is the largest substantive issue in the test result. All evidence packets are mechanically present and marked valid, but their contents are placeholders rather than concrete evidence records.

| Evidence packet | Field | Observed value |
|---|---|---|
| `EVD-STG-001-SCOPE-BRIEF-001` | `source_inputs` | `<source list>` |
| `EVD-STG-001-SCOPE-BRIEF-001` | `approval_statement` | `<acceptance statement>` |
| `EVD-STG-002-TAXONOMY-001` | `source_inputs` | `<source list>` |
| `EVD-STG-002-TAXONOMY-001` | `approval_statement` | `<acceptance statement>` |
| `EVD-STG-003-INVARIANTS-001` | `source_inputs` | `<source list>` |
| `EVD-STG-003-INVARIANTS-001` | `approval_statement` | `<acceptance statement>` |
| `EVD-STG-004-AWKA-COMPARATIVE-001` | `source_inputs` | `<source list>` |
| `EVD-STG-004-AWKA-COMPARATIVE-001` | `approval_statement` | `<acceptance statement>` |
| `EVD-STG-005-FINAL-SYNTHESIS-001` | `source_inputs` | `<source list>` |
| `EVD-STG-005-FINAL-SYNTHESIS-001` | `approval_statement` | `<acceptance statement>` |

**Expected behavior:** An evidence packet should identify actual source inputs and meaningful acceptance rationale. For research workflows, this should include source references, source anchor resolution, or at minimum a concrete evidence statement that can be inspected later.

**Observed behavior:** Every evidence packet contains `source_inputs=<source list>` and `approval_statement=<acceptance statement>`. The runtime nevertheless accepted these packets as `validation_status=valid` and promoted the artifacts to `dependency_eligible`.

**Assessment:** FAIL for evidence substance, PASS for evidence lifecycle plumbing. The runtime proves that evidence attachment works structurally, but this test does not prove that evidence quality is enforced.

**Recommended patch or test addition:** Add a validator that rejects placeholder evidence values. At minimum, reject exact literals such as `<source list>`, `<acceptance statement>`, empty strings, and generic unresolved placeholders. Require either concrete source identifiers or a policy-approved evidence-free acceptance mode marked explicitly as such.

## 12. Digest and Snapshot Lineage Analysis

Most digest checks are good: artifact body resolution digests match expected digests, final export digest matches the QA record, and snapshot-created events match snapshot records.

One digest lineage ambiguity requires investigation:

| Field | Value |
|---|---|
| Artifact set selected snapshot ID | `ANDY-WF-000001-SNAP-000039` |
| Receipt selected snapshot digest | `fc941b3091e11cf0624b61ef028a992c40d1c9a18e54f85d635f4a3d4e8b027f` |
| Snapshot record canonical digest | `274d3cb81c9db58fa791d8e3d16a1729be1ba02cbe1f493b5dde3d352ae461b2` |
| Digests match | `False` |

**Assessment:** CONCERN. The selected snapshot ID points to `ANDY-WF-000001-SNAP-000039`, but the selected snapshot digest stored in artifact receipts and the artifact set receipt does not equal that snapshot record canonical digest. There may be a legitimate second digest type, such as a digest over the exported snapshot projection rather than the canonical state, but the field name does not make the distinction clear.

**Recommended patch or documentation:** Rename or split the receipt fields so they distinguish:

- `selected_snapshot_canonical_state_digest`
- `selected_snapshot_projection_digest`
- `selected_snapshot_record_digest`

Then add verification that each digest is computed from a declared object and that the object identity is inspectable.

## 13. Transcript Completeness Analysis

The inspection transcript is valuable and mostly sufficient for runtime analysis, but it is not a complete raw UI conversation transcript. It explicitly states that it is reconstructed from runtime state, result receipts, exported artifact set, and available file records, and that exact UI-level assistant prose was not persisted.

**Assessment:** PARTIAL. The transcript is complete for recorded runtime records and result files, but not complete for all human-facing conversational text. This is acceptable for a runtime state audit, but not for a full agent behavior audit.

**Recommended patch or test addition:** If full conversation inspection is a required artifact, ANDY should persist immutable conversation-turn records with:

- turn ID
- actor
- raw text
- route decision
- whether the turn was mutating or non-mutating
- linked capability invocation or rejection diagnostic
- digest of the raw message
- snapshot or state version affected, if any

## 14. Final Artifact Content Quality

The final exported artifact set is coherent and aligned with the research narrative. It integrates all five stages into a final synthesis about abstract kernels as reusable governance cores, and it correctly positions AWKA as a domain-independent LLM workflow kernel with proof-kernel discipline and microkernel-style mechanism/policy separation.

Substantive content strengths:

- The final output preserves the stage lineage from scope, taxonomy, invariants, comparative evaluation, and synthesis.
- It consistently maintains authority/expression separation as the central design claim.
- It identifies concrete architectural principles and risks.
- It produces follow-up research questions that are useful for future AWKA work.

Content limitations:

- Source anchors are described as preliminary, but the final export does not provide a concrete bibliography or resolvable citation map.
- Evidence packets do not contain concrete source lists.
- Acceptance statements are placeholders.
- The output is suitable as a concept synthesis, but not yet as source-auditable research.

## 15. Defects, Concerns, and Recommendations

### Blocking defects

None found for runtime lifecycle completion. The workflow closed successfully.

### Major concerns

1. **Evidence placeholders accepted as valid.**
   - Impact: weakens source-as-data discipline and artifact trust.
   - Recommendation: add placeholder evidence rejection validator.

2. **Snapshot digest ambiguity in export receipts.**
   - Impact: receipt lineage cannot be interpreted unambiguously from field names alone.
   - Recommendation: split canonical digest, projection digest, and receipt digest fields.

3. **Transcript is not raw UI-complete.**
   - Impact: cannot fully audit agent prose or user-facing behavior.
   - Recommendation: persist raw conversation-turn records as digest-addressed non-authoritative evidence.

### Minor concerns

1. `DRAFT-ART-001.txt` is reused as the artifact body reference for multiple stages. The artifact version digests disambiguate the bodies, but the reference string alone is ambiguous.
2. `demo_inline_cache` is used as body resolution method. This is acceptable for alpha testing, but should be replaced or explicitly bounded for non-demo use.
3. `rejection_records` is empty even though non-mutating rejections are visible in transcript records. The expected persistence policy should be clarified.

## 16. Recommended Additional Tests

1. **Evidence placeholder rejection test**
   - Attempt artifact acceptance with `<source list>` and `<acceptance statement>`.
   - Expected result: rejection or non-dependency-eligible artifact.

2. **Concrete evidence acceptance test**
   - Accept artifact with a concrete evidence source list and acceptance statement.
   - Expected result: dependency eligible and evidence packet marked valid.

3. **Source anchor resolution test**
   - Require source anchors to resolve to stored source records or citation registry entries.
   - Expected result: unresolved source anchors block evidence validation.

4. **Receipt digest semantics test**
   - Verify every digest field by recomputing it from its declared object.
   - Expected result: no ambiguous digest fields and no mismatches.

5. **Raw transcript persistence test**
   - Require every UI turn to be stored as a non-authoritative message record.
   - Expected result: transcript can be generated without reconstruction caveats.

6. **Non-mutating rejection persistence test**
   - Send invalid shorthand and incomplete commands.
   - Expected result: route diagnostics persist in a defined diagnostic record class.

7. **Artifact reference uniqueness test**
   - Ensure each stage draft has a unique body reference or explicit stage-scoped namespace.
   - Expected result: no ambiguity from repeated `DRAFT-ART-001.txt` references.

## 17. Final Assessment

```text
Runtime lifecycle:              PASS
AWKA alpha.4 compatibility:     PASS
Stage progression:              PASS
Fail-closed command routing:    PASS
Artifact export mechanics:      PASS
Final workflow closure:         PASS
Evidence substance:             FAIL
Snapshot receipt digest clarity: CONCERN
Transcript raw completeness:     PARTIAL
Overall test classification:     PASS WITH INSPECTION FINDINGS
```

The correct architectural conclusion is that alpha.7 is functionally viable under the patched AWKA alpha.4 activation path, and the first workflow execution validates the core lifecycle. The next hardening target should not be stage progression. It should be evidence quality, digest semantics, and raw transcript persistence.
