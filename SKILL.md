---
name: research-engineering-scaffold
description: Create or update a standardized, reproducible, auditable research-project engineering scaffold. Use when the user wants to start a new research project, scaffold project governance files, make a project transferable/reproducible/auditable, standardize Codex project memory, create data/analysis/figure/evidence registries, or adapt the mregTLS-NEXUS governance pattern to another project.
---

# Research Engineering Scaffold

Use this skill to turn a research idea into a durable project system. The repository, not chat history, is the long-term memory.

## Quick Start

When the user asks to start a new project or standardize an existing one, run:

```bash
python <skill_dir>/scripts/scaffold_research_engineering.py --project-dir <target_dir> --project-name "<name>" --title "<working title>" --domain "<domain>"
```

Optional parameters:

```bash
--primary-hypothesis "<hypothesis>"
--primary-data "<main data source>"
--primary-endpoint "<main endpoint>"
--remote-path "<server project path>"
--init-git
--commit
--overwrite
```

Use `--overwrite` only when the user explicitly wants existing Research Engineering Scaffold files refreshed.

## Workflow

1. Determine the target project directory and project name.
2. Run `scripts/scaffold_research_engineering.py` with project-specific parameters.
3. Run the generated validator:

```bash
python scripts/00_setup/validate_research_engineering_scaffold.py
```

4. If requested, initialize Git with `--init-git --commit`.
5. Customize project-specific files:
   - `docs/project_charter.md`
   - `docs/analysis_plan.md`
   - `config/datasets.yml`
   - `config/signatures.yml` or the domain equivalent
   - `config/endpoints.yml`
   - `registries/data_registry.tsv`
6. End by telling the user what was created, what was validated, and what still needs human scientific judgment.

## Required Operating Model

Every generated project should keep these responsibilities separate:

- Codex: execute, check, refactor, document, and update registries.
- Git repository: durable project memory.
- Issues/PR/CI: process and review control.
- Human owner: scientific judgment, endpoint acceptance, claim acceptance.

## Core Files

Generated projects include:

- `AGENTS.md`: standing Codex rules.
- `PROJECT_STATE.md`: project memory.
- `NEXT_ACTIONS.md`: task queue.
- `DECISIONS.md`: scientific and engineering decisions.
- `RISK_REGISTER.md`: risks, mitigations, and pivots.
- `docs/analysis_plan.md`: pre-specified analysis route.
- `docs/statistical_analysis_plan.md`: statistical guardrails.
- `registries/data_registry.tsv`: dataset provenance.
- `registries/evidence_ledger.tsv`: claim evidence chain.
- `registries/figure_manifest.tsv`: figure source tracking.
- `registries/ai_usage_log.tsv`: AI usage record.
- `scripts/00_setup/validate_research_engineering_scaffold.py`: scaffold validator.

## Customization Rules

Keep the standard scaffold intact unless the project truly needs a different rule.

For biomedical or clinical projects:

- Use `config/endpoints.yml` for endpoint definitions.
- Use `config/signatures.yml` for gene sets, biomarkers, scores, or feature definitions.
- Require data provenance before analysis.

For non-biomedical projects:

- Rename domain concepts only after preserving the same governance surfaces:
  - dataset registry
  - analysis plan
  - evidence ledger
  - figure/output manifest
  - decision log
  - risk register

For advanced adaptation guidance, read `references/customization.md`.

## Quality Gate

Before considering the scaffold complete:

```bash
python scripts/00_setup/validate_research_engineering_scaffold.py
```

The validator must pass. If Git was initialized, `git status --short` should be clean after the initial commit unless the user asked for uncommitted work.


