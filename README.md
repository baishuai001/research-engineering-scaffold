# Research Engineering Scaffold

**Research Engineering Scaffold** is a reusable Codex skill for creating a standardized engineering foundation for research projects.

中文名：**科研工程底座**

It turns a research idea into a reproducible, transferable, and auditable project repository by generating the files and conventions needed to track:

- project state
- decisions
- risks
- data provenance
- analysis plans
- statistical rules
- evidence chains
- figure/source-data traceability
- AI usage
- validation checks

It is not an automated research system. It is a governance scaffold: Codex helps execute, organize, check, and document work; humans remain responsible for scientific judgment.

## Why This Exists

Research projects often become hard to audit once ideas, datasets, code, literature, clinical endpoints, figures, AI conversations, and version history start to mix.

This skill provides a consistent project structure so each new project starts with the same operational baseline instead of being rebuilt through repeated ad hoc conversations.

## What It Generates

A scaffolded project includes:

```text
AGENTS.md
PROJECT_STATE.md
NEXT_ACTIONS.md
DECISIONS.md
RISK_REGISTER.md
config/
docs/
registries/
hypotheses/
scripts/
data/
results/
notebooks/
manuscript/
references/
.github/
```

Key governance surfaces:

- `AGENTS.md`: standing instructions for Codex and other AI agents
- `PROJECT_STATE.md`: durable project memory
- `DECISIONS.md`: scientific and engineering decision log
- `RISK_REGISTER.md`: project risks and mitigation routes
- `registries/data_registry.tsv`: dataset/source provenance
- `registries/evidence_ledger.tsv`: claim-to-evidence tracking
- `registries/figure_manifest.tsv`: figure/source-data traceability
- `registries/ai_usage_log.tsv`: AI assistance log
- `scripts/00_setup/validate_research_engineering_scaffold.py`: scaffold validation script

## Installation

Clone this repository into your Codex skills directory.

Windows:

```powershell
git clone https://github.com/baishuai001/research-engineering-scaffold.git `
  "$env:USERPROFILE\.codex\skills\research-engineering-scaffold"
```

macOS/Linux:

```bash
git clone https://github.com/baishuai001/research-engineering-scaffold.git \
  ~/.codex/skills/research-engineering-scaffold
```

Restart Codex, or open a new Codex thread, so the skill can be discovered.

## Usage

In Codex, ask:

```text
Use $research-engineering-scaffold to scaffold a new research project.
Project name: MyProject
Project directory: E:\Codex\MyProject
Domain: biomedical oncology
Working title: ...
Primary hypothesis: ...
Primary data: ...
Primary endpoint: ...
Initialize Git and create the first commit.
```

The skill will use:

```text
scripts/scaffold_research_engineering.py
```

to generate the project scaffold.

## Direct Script Usage

You can also run the scaffolding script directly.

```powershell
python C:\Users\<USER>\.codex\skills\research-engineering-scaffold\scripts\scaffold_research_engineering.py `
  --project-dir E:\Codex\MyProject `
  --project-name "MyProject" `
  --title "Working title" `
  --domain "biomedical oncology" `
  --primary-hypothesis "Primary working hypothesis" `
  --primary-data "Primary dataset or source" `
  --primary-endpoint "Primary endpoint or outcome" `
  --init-git `
  --commit
```

After scaffolding, validate the generated project:

```powershell
cd E:\Codex\MyProject
python scripts/00_setup/validate_research_engineering_scaffold.py
```

## Updating

If installed from GitHub:

```powershell
cd "$env:USERPROFILE\.codex\skills\research-engineering-scaffold"
git pull
```

If you improve the skill locally:

```powershell
cd "$env:USERPROFILE\.codex\skills\research-engineering-scaffold"
git status
git add .
git commit -m "Improve scaffold behavior"
git push
```

Before pushing substantial changes, validate the skill:

```powershell
python C:\Users\<USER>\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
```

## Design Principle

The repository is the project memory.

Chat history is useful for reasoning, but not reliable as the source of truth. Project assumptions, analysis standards, data provenance, results, figures, and claims should be recorded in versioned files.
