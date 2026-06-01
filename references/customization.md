# Research Engineering Scaffold Customization

Use this reference when adapting the scaffold beyond the default biomedical-style template.

## Minimal Invariant

Every project should preserve these surfaces:

| Surface | Purpose |
|---|---|
| Project state | Durable memory across Codex sessions |
| Decision log | Why scientific or engineering choices were made |
| Risk register | Known failure modes and planned pivots |
| Data registry | Provenance, access, licensing, sample scope |
| Analysis plan | Pre-specified route before results are known |
| Statistical plan | Modeling and interpretation guardrails |
| Evidence ledger | Claim-to-result traceability |
| Figure manifest | Output-to-code/source-data traceability |
| AI usage log | Transparent AI assistance record |
| Validator | Fast consistency check |

## Domain Adaptation

Biomedical projects usually need:

- `config/signatures.yml`
- `config/endpoints.yml`
- sample inclusion/exclusion fields
- clinical endpoint caveats
- source-data tables for figures

Computational-method projects usually need:

- benchmark registry
- metric dictionary
- baseline model registry
- train/test split registry
- hardware/runtime log

Literature-review projects usually need:

- search strategy registry
- screening decision log
- inclusion/exclusion table
- evidence grading table
- citation verification status

Wet-lab projects usually need:

- protocol registry
- reagent and batch registry
- sample manifest
- experimental run log
- deviation log

## Naming

Prefer stable IDs:

- datasets: `D001`, or short machine IDs such as `tcga_luad`
- claims: `C001`
- figures: `F1A`
- tasks: `T001`
- decisions: `D001`
- risks: `R001`

## Guardrails

- Do not make chat history the source of truth.
- Do not store credentials.
- Do not use unregistered data for manuscript claims.
- Do not accept AI-generated citations without source verification.
- Do not silently change endpoints, cutoffs, signatures, metrics, or statistical models after seeing results.


