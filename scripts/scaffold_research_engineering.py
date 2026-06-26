from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import textwrap
from datetime import date
from pathlib import Path


DIRS = [
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "config",
    "docs",
    "registries",
    "hypotheses",
    "data/raw",
    "data/processed",
    "data/metadata",
    "data/external",
    "scripts/00_setup",
    "scripts/01_data_download",
    "scripts/02_qc",
    "scripts/03_annotation",
    "scripts/04_analysis",
    "scripts/05_clinical_or_outcome_analysis",
    "scripts/06_figures",
    "results/tables",
    "results/figures",
    "results/logs",
    "results/reports",
    "notebooks",
    "manuscript",
    "references",
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "research-project"


def dedent(value: str) -> str:
    return textwrap.dedent(value).lstrip()


def render(template: str, context: dict[str, str]) -> str:
    value = dedent(template)
    for key, replacement in context.items():
        value = value.replace("{{" + key + "}}", replacement)
    return value


def write_file(path: Path, content: str, overwrite: bool, written: list[str], kept: list[str]) -> None:
    if path.exists() and not overwrite:
        kept.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    written.append(str(path))


def write_empty(path: Path, overwrite: bool, written: list[str], kept: list[str]) -> None:
    if path.exists() and not overwrite:
        kept.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8", newline="\n")
    written.append(str(path))


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=str(cwd), check=True)


def templates() -> dict[str, str]:
    return {
        "README.md": """
        # {{project_name}}

        {{title}}

        This repository is the durable memory and audit surface for the project. Chat threads are useful for reasoning, but they are not the source of truth. Scientific assumptions, data provenance, analysis plans, code, figures, and conclusions must be recorded here.

        ## Operating Principle

        Codex executes, checks, refactors, and documents work inside this repository.
        Git tracks project memory.
        Issues, pull requests, CI, registries, and logs track process.
        Humans make the scientific judgment calls.

        ## Start Every Codex Session

        Read:

        1. `AGENTS.md`
        2. `PROJECT_STATE.md`
        3. `NEXT_ACTIONS.md`
        4. `DECISIONS.md`
        5. `RISK_REGISTER.md`
        6. `docs/project_charter.md`
        7. `docs/analysis_plan.md`
        8. `registries/data_registry.tsv`
        9. `registries/evidence_ledger.tsv`
        10. `registries/figure_manifest.tsv`

        End each meaningful work session by updating the relevant state, decision, registry, and log files.

        ## Remote Compute

        {{remote_path}}
        """,
        "AGENTS.md": """
        # AGENTS.md

        This file is the standing instruction set for Codex and any AI-assisted coding agent working on {{project_name}}.

        ## Prime Directive

        Do not rely on chat memory for project state. The repository is the project memory. Before acting, read the context files. After acting, update the files that changed project state, decisions, risks, evidence, figures, or next actions.

        ## Required Context Pack

        1. `PROJECT_STATE.md`
        2. `NEXT_ACTIONS.md`
        3. `DECISIONS.md`
        4. `RISK_REGISTER.md`
        5. `docs/project_charter.md`
        6. `docs/analysis_plan.md`
        7. `docs/statistical_analysis_plan.md`
        8. `registries/data_registry.tsv`
        9. `registries/evidence_ledger.tsv`
        10. `registries/figure_manifest.tsv`

        ## Scientific Reliability Rules

        - No dataset enters primary analysis until it has a row in `registries/data_registry.tsv`.
        - No endpoint, metric, signature, score, cutoff, or threshold is hard-coded in analysis scripts. Put definitions in `config/`.
        - No major claim is manuscript-ready until it has a row in `registries/evidence_ledger.tsv`.
        - No figure is manuscript-ready until it has a row in `registries/figure_manifest.tsv` with source data, script, and claim linkage.
        - Negative, weak, or contradictory results must be logged.
        - Treat AI-generated scientific statements as hypotheses until independently verified.
        - Human scientific review is required before accepting any result as a conclusion.

        ## Engineering Rules

        - Keep scripts modular, deterministic, and rerunnable.
        - Use relative project paths from the repository root.
        - Write logs to `results/logs/`.
        - Write generated tables to `results/tables/`.
        - Write generated figures to `results/figures/`.
        - Keep raw data under `data/raw/` or external mounted storage. Do not commit raw large data.
        - Prefer configuration-driven analysis over script-local constants.

        ## Session Closeout

        Update `PROJECT_STATE.md`, `NEXT_ACTIONS.md`, `DECISIONS.md`, and relevant registries. State what was verified and what remains uncertain.

        ## Security

        Never commit passwords, tokens, SSH keys, browser cookies, raw controlled-access data, or personal identifiers.
        """,
        "PROJECT_STATE.md": """
        # Project State

        Last updated: {{today}}

        ## Current Phase

        Phase 0: research engineering scaffold.

        ## Project

        Project name: {{project_name}}

        Domain: {{domain}}

        Working title:

        {{title}}

        Core hypothesis:

        {{primary_hypothesis}}

        ## Completed

        - Created standardized Research Engineering Scaffold.

        ## Active Questions

        - Which datasets or source materials are usable?
        - Which definitions, endpoints, signatures, or metrics must be locked before analysis?
        - Which result would justify expanding the project?

        ## Current Blockers

        - Dataset/source availability has not yet been independently verified.
        - Analysis environment has not yet been locked.

        ## Next Milestone

        Feasibility Gate 1: verify data/source availability, lock first definitions, run the smallest meaningful analysis, and write a short feasibility report.
        """,
        "NEXT_ACTIONS.md": """
        # Next Actions

        Last updated: {{today}}

        ## Immediate

        - [ ] Fill mandatory fields in `registries/data_registry.tsv`.
        - [ ] Define primary endpoints, metrics, signatures, or feature sets in `config/`.
        - [ ] Run `python scripts/00_setup/validate_research_engineering_scaffold.py`.
        - [ ] Record the initial software environment.

        ## Feasibility Gate 1

        - [ ] Verify primary data/source access.
        - [ ] Create first minimal analysis script.
        - [ ] Produce `results/reports/feasibility_gate_1.md`.
        - [ ] Update `registries/evidence_ledger.tsv`.
        """,
        "DECISIONS.md": """
        # Decisions

        ## Template

        ```text
        ID:
        Date:
        Status: proposed | accepted | superseded
        Decision:
        Rationale:
        Alternatives considered:
        Consequences:
        Evidence:
        ```

        ## D001: Repository Is the Project Memory

        Date: {{today}}
        Status: accepted

        Decision:
        Use the repository as the durable project memory. Chat conversations may assist reasoning, but project state, decisions, analysis definitions, evidence, and figure provenance must be recorded in versioned files.
        """,
        "RISK_REGISTER.md": """
        # Risk Register

        Last updated: {{today}}

        | Risk ID | Risk | Likelihood | Impact | Mitigation | Owner | Status |
        |---|---|---:|---:|---|---|---|
        | R001 | Primary data/source is not usable | Medium | High | Verify access before analysis expansion | Human + Codex | Open |
        | R002 | Definitions drift after seeing results | Medium | High | Lock definitions in `config/` and record decisions | Human + Codex | Open |
        | R003 | Codex context loss causes inconsistent standards | High | Medium | Use `AGENTS.md`, registries, and state logs | Codex | Mitigated |
        | R004 | Claims become disconnected from evidence | Medium | High | Require evidence ledger rows for all claims | Codex | Open |
        | R005 | Figures become disconnected from source data | Medium | High | Require figure manifest rows for all panels | Codex | Open |
        """,
        ".gitignore": """
        .env
        .Renviron
        *.pem
        *.key
        id_rsa*
        known_hosts
        .Rhistory
        .RData
        .Ruserdata
        renv/library/
        renv/staging/
        __pycache__/
        *.py[cod]
        .pytest_cache/
        .venv/
        venv/
        data/raw/**
        data/processed/**
        data/external/**
        results/figures/**
        results/tables/**
        results/logs/**
        results/reports/**
        !data/raw/.gitkeep
        !data/processed/.gitkeep
        !data/external/.gitkeep
        !data/metadata/.gitkeep
        !results/figures/.gitkeep
        !results/tables/.gitkeep
        !results/logs/.gitkeep
        !results/reports/.gitkeep
        .DS_Store
        Thumbs.db
        .vscode/
        .idea/
        """,
        ".gitattributes": """
        *.md text eol=lf
        *.R text eol=lf
        *.py text eol=lf
        *.yml text eol=lf
        *.yaml text eol=lf
        *.tsv text eol=lf
        *.csv text eol=lf
        *.sh text eol=lf
        *.ps1 text eol=crlf
        """,
        "docs/project_charter.md": """
        # Project Charter

        ## Project Name

        {{project_name}}

        ## Working Title

        {{title}}

        ## Domain

        {{domain}}

        ## Primary Hypothesis

        {{primary_hypothesis}}

        ## Primary Data or Source

        {{primary_data}}

        ## Primary Endpoint or Outcome

        {{primary_endpoint}}

        ## Success Criteria

        - Data/source provenance is auditable.
        - Definitions are locked before inferential analysis.
        - Every major claim links to data, code, output, and review status.
        - Negative or contradictory results are logged.

        ## Pivot Criteria

        Define project-specific conditions that would change the main framing.
        """,
        "docs/analysis_plan.md": """
        # Analysis Plan

        ## Primary Route

        1. Verify data/source availability.
        2. Lock definitions, endpoints, metrics, signatures, or feature sets in `config/`.
        3. Run the smallest meaningful feasibility analysis.
        4. Compare against baseline or alternative definitions.
        5. Record outputs in registries before making claims.

        ## Minimum Viable Analysis

        Feasibility Gate 1:

        - Can the primary data/source be used?
        - Can the core concept be measured?
        - Is there enough signal or structure to justify expansion?

        ## Prohibited Practices

        - Choosing cutoffs after inspecting outcome association without recording the decision.
        - Dropping negative validation results without logging them.
        - Treating exploratory results as final claims.
        """,
        "docs/statistical_analysis_plan.md": """
        # Statistical Analysis Plan

        ## General Principles

        - Predefine contrasts before running outcome tests.
        - Report effect sizes, uncertainty, and sample sizes.
        - Separate discovery from validation.
        - Correct for multiple testing where families of hypotheses are tested.
        - Log all tested models, including null and negative results.

        ## Reporting Requirements

        For each model or quantitative comparison, record:

        - Dataset ID.
        - Script.
        - Outcome.
        - Predictors or features.
        - Covariates where applicable.
        - Sample inclusion.
        - Effect estimate.
        - Confidence interval or standard error where applicable.
        - P value or adjusted P value where applicable.
        - Sensitivity analysis status.
        """,
        "docs/codex_workflow.md": """
        # Codex Workflow

        ## Standard Work Cycle

        1. Read context pack.
        2. State task objective.
        3. Confirm expected artifact.
        4. Make scoped changes.
        5. Run validation or explain why it could not run.
        6. Update state files and registries.
        7. Report changed files and residual risk.

        ## Role Boundary

        Codex executes and audits. Humans accept scientific claims.
        """,
        "docs/data_governance.md": """
        # Data Governance

        Every dataset or source must have an entry in `registries/data_registry.tsv` before use.

        ## Access States

        - `candidate`: mentioned in planning but not verified.
        - `verified_source`: source and access route verified.
        - `downloaded`: raw data present locally or on server.
        - `processed`: processed data generated reproducibly.
        - `analysis_ready`: metadata, QC, and format are sufficient for analysis.
        - `excluded`: not used, with reason recorded.
        """,
        "docs/figure_blueprint.md": """
        # Figure Blueprint

        Every figure panel must map to data, code, and a claim.

        ## Candidate Main Figures

        1. Project map and data/source overview.
        2. Core measurement or reference definition.
        3. Primary association or mechanism result.
        4. Validation or sensitivity analysis.
        5. Outcome or translational relevance.

        ## Figure Readiness Criteria

        A figure is not ready until `registries/figure_manifest.tsv` records figure ID, panel ID, claim ID, dataset ID, source data, script, output path, and review status.
        """,
        "docs/reproducibility_protocol.md": """
        # Reproducibility Protocol

        Each analysis run should capture date, Git commit, machine, software versions, input files, config files, output files, and log file.

        Run:

        ```bash
        python scripts/00_setup/validate_research_engineering_scaffold.py
        ```
        """,
        "docs/review_checklist.md": """
        # Review Checklist

        ## Data

        - [ ] Dataset/source is registered.
        - [ ] Access route is verified.
        - [ ] License or terms are recorded.

        ## Analysis

        - [ ] Script is versioned.
        - [ ] Config values are versioned.
        - [ ] Model or comparison is documented.
        - [ ] Negative results are logged.

        ## Claim

        - [ ] Evidence ledger row exists.
        - [ ] Claim wording is proportional to evidence.
        - [ ] Human review status is recorded.
        """,
        "docs/ai_usage_policy.md": """
        # AI Usage Policy

        AI tools may help with code, documentation, triage, and review.

        AI tools may not be treated as primary evidence, final scientific judgment, or a place to store credentials.

        Record meaningful AI-assisted work in `registries/ai_usage_log.tsv`.
        """,
        "docs/glossary.md": """
        # Glossary

        | Term | Working definition | Status |
        |---|---|---|
        | Core concept | TODO | Draft |
        | Primary endpoint | {{primary_endpoint}} | Draft |
        """,
        "config/project_profile.yml": """
        project:
          name: "{{project_name}}"
          id: "{{project_id}}"
          title: "{{title}}"
          domain: "{{domain}}"
          primary_hypothesis: "{{primary_hypothesis}}"
          primary_data: "{{primary_data}}"
          primary_endpoint: "{{primary_endpoint}}"
          remote_path: "{{remote_path_raw}}"
          created: "{{today}}"
        """,
        "config/datasets.yml": """
        datasets:
          - dataset_id: primary_source
            short_name: "{{primary_data}}"
            role: primary
            status: candidate
            verification_status: to_verify
            notes: Replace with verified source details before analysis.
        """,
        "config/signatures.yml": """
        signatures_or_feature_sets:
          core_feature_set_v0:
            status: draft
            source: planning
            features:
              - TODO
            notes: Replace with project-specific signatures, biomarkers, metrics, or feature definitions.
        """,
        "config/endpoints.yml": """
        endpoints_or_outcomes:
          primary_endpoint:
            status: draft
            name: "{{primary_endpoint}}"
            definition: TODO
            allowed_values:
              - TODO
            caveats: Define before analysis.
        """,
        "config/thresholds.yml": """
        thresholds:
          default_high_low_split:
            status: draft
            method: median
            allowed_use: exploratory_only
            notes: Outcome-optimized cutoffs require pre-specification and validation.
        """,
        "config/compute.yml": """
        compute:
          remote_project_path: "{{remote_path_raw}}"
          preferred_log_dir: results/logs
          preferred_table_dir: results/tables
          preferred_figure_dir: results/figures
          notes: Do not store credentials in this file.
        """,
        "registries/data_registry.tsv": "dataset_id\tshort_name\tsource_url_or_reference\taccess_route\tmodality_or_source_type\tdomain_or_population\tsample_count_or_scope\tendpoints_or_outcomes\tlicense_or_terms\tverification_status\tplanned_role\tlocal_or_remote_path\tnotes\nprimary_source\t{{primary_data}}\tTODO\tTODO\tTODO\t{{domain}}\tTODO\t{{primary_endpoint}}\tTODO\tcandidate\tprimary\tTODO\tVerify before analysis.\n",
        "registries/evidence_ledger.tsv": "claim_id\tclaim_text\tstatus\tdataset_id\tanalysis_script\tresult_table\tfigure_panel\tevidence_strength\thuman_review\treviewer\tnotes\nC001\tCore concept can be measured with predefined definitions.\tproposed\tprimary_source\tTODO\tTODO\tTODO\tnot_started\tpending\tTODO\tFeasibility Gate 1.\n",
        "registries/figure_manifest.tsv": "figure_id\tpanel_id\tclaim_id\tdataset_id\tsource_data\tanalysis_script\tfigure_path\tstatus\treviewer\tnotes\nF1\tA\tC001\tprimary_source\tTODO\tTODO\tTODO\tplanned\tTODO\tProject overview.\n",
        "registries/analysis_task_registry.tsv": "task_id\ttask_name\tstatus\tdataset_id\tinputs\tconfigs\tscript\toutputs\tlog_path\towner\tnotes\nT001\tValidate Research Engineering Scaffold\tready\tNA\tNA\tNA\tscripts/00_setup/validate_research_engineering_scaffold.py\tresults/reports/research_engineering_scaffold_validation.txt\tresults/logs/research_engineering_scaffold_validation.log\tCodex\tRun before handoff.\n",
        "registries/claims_registry.tsv": "claim_id\tclaim_family\tclaim_text\tallowed_strength\tcurrent_status\trequired_evidence\tnotes\nC001\tmethod\tCore concept can be measured with predefined definitions.\tdescriptive\tproposed\tReference or source validation\tNo manuscript claim until checked.\n",
        "registries/validation_matrix.tsv": "analysis_component\tdiscovery_dataset\tvalidation_dataset\tsensitivity_analysis\tstatus\tnotes\ncore_measurement\tprimary_source\tTODO\talternative_definition\tnot_started\tDefine project-specific validation.\n",
        "registries/ai_usage_log.tsv": "date\ttool\ttask\tfiles_changed\thuman_review_status\tnotes\n{{today}}\tCodex\tScaffold Research Engineering project\trepository_scaffold\tpending\tInitial standardized scaffold.\n",
        "registries/data_access_log.tsv": "date\tdataset_id\taction\tuser_or_tool\tpath_or_url\tstatus\tnotes\n{{today}}\tNA\tcreate_project_scaffold\tCodex\tlocal\tcomplete\tNo data downloaded.\n",
        "registries/literature_evidence_table.tsv": "reference_id\tcitation_or_title\tclaim_supported\tsource_type\tverification_status\turl_or_doi\tnotes\nL001\tTODO\tProject rationale\tprimary_source_or_review\tto_verify\tTODO\tVerify before citing.\n",
        "hypotheses/H01_core_measurement.md": """
        # H01: Core Measurement

        ## Hypothesis

        {{primary_hypothesis}}

        ## Required Evidence

        - Source verified.
        - Definitions locked.
        - Sensitivity analysis planned.

        ## Pass Criteria

        Define project-specific pass criteria.

        ## Fail or Pivot Criteria

        Define conditions for changing the project framing.
        """,
        "scripts/00_setup/validate_research_engineering_scaffold.py": VALIDATOR_TEMPLATE,
        "scripts/00_setup/bootstrap_project.R": """
        project_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), "..", ".."), mustWork = TRUE)
        setwd(project_root)

        dirs <- c(
          "data/raw", "data/processed", "data/metadata", "data/external",
          "results/tables", "results/figures", "results/logs", "results/reports"
        )

        for (d in dirs) {
          dir.create(d, recursive = TRUE, showWarnings = FALSE)
        }

        message("Project bootstrap complete: ", project_root)
        """,
        "scripts/00_setup/session_info.R": """
        project_root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), "..", ".."), mustWork = TRUE)
        log_dir <- file.path(project_root, "results", "logs")
        dir.create(log_dir, recursive = TRUE, showWarnings = FALSE)

        stamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
        out <- file.path(log_dir, paste0("session_info_", stamp, ".txt"))

        sink(out)
        cat("Project root:", project_root, "\\n")
        cat("Time:", as.character(Sys.time()), "\\n")
        cat("R version:", R.version.string, "\\n\\n")
        print(sessionInfo())
        sink()

        message("Wrote session info to ", out)
        """,
        ".github/pull_request_template.md": """
        # Summary

        ## Type

        - [ ] Governance/documentation
        - [ ] Data registration
        - [ ] Analysis code
        - [ ] Figure/source data
        - [ ] Manuscript text
        - [ ] Refactor

        ## Checks

        - [ ] I read `AGENTS.md`.
        - [ ] I updated state files or explain why not.
        - [ ] I updated relevant registries.
        - [ ] I ran `python scripts/00_setup/validate_research_engineering_scaffold.py`.
        - [ ] I did not commit secrets or raw controlled data.
        """,
        ".github/ISSUE_TEMPLATE/analysis_task.yml": """
        name: Analysis task
        description: Track a reproducible research analysis task.
        title: "[Analysis]: "
        labels: ["analysis"]
        body:
          - type: textarea
            id: objective
            attributes:
              label: Objective
            validations:
              required: true
          - type: textarea
            id: expected
            attributes:
              label: Expected artifacts
            validations:
              required: true
        """,
        ".github/ISSUE_TEMPLATE/data_request.yml": """
        name: Data request
        description: Register or verify a dataset/source before analysis.
        title: "[Data]: "
        labels: ["data"]
        body:
          - type: input
            id: dataset_id
            attributes:
              label: Dataset ID
            validations:
              required: true
          - type: textarea
            id: source
            attributes:
              label: Source and access route
            validations:
              required: true
        """,
        ".github/workflows/research-engineering-scaffold-check.yml": """
        name: research-engineering-scaffold-check

        on:
          pull_request:
          push:
            branches:
              - main

        jobs:
          validate:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-python@v5
                with:
                  python-version: "3.12"
              - name: Validate Research Engineering Scaffold
                run: python scripts/00_setup/validate_research_engineering_scaffold.py
        """,
    }


VALIDATOR_TEMPLATE = r'''
from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "PROJECT_STATE.md",
    "NEXT_ACTIONS.md",
    "DECISIONS.md",
    "RISK_REGISTER.md",
    "docs/project_charter.md",
    "docs/analysis_plan.md",
    "docs/statistical_analysis_plan.md",
    "docs/codex_workflow.md",
    "docs/data_governance.md",
    "docs/figure_blueprint.md",
    "config/project_profile.yml",
    "config/datasets.yml",
    "config/endpoints.yml",
    "config/thresholds.yml",
    "registries/data_registry.tsv",
    "registries/evidence_ledger.tsv",
    "registries/figure_manifest.tsv",
    "registries/analysis_task_registry.tsv",
    "registries/ai_usage_log.tsv",
]

TSV_SCHEMAS = {
    "registries/data_registry.tsv": [
        "dataset_id",
        "short_name",
        "source_url_or_reference",
        "access_route",
        "modality_or_source_type",
        "domain_or_population",
        "sample_count_or_scope",
        "endpoints_or_outcomes",
        "license_or_terms",
        "verification_status",
        "planned_role",
        "local_or_remote_path",
        "notes",
    ],
    "registries/evidence_ledger.tsv": [
        "claim_id",
        "claim_text",
        "status",
        "dataset_id",
        "analysis_script",
        "result_table",
        "figure_panel",
        "evidence_strength",
        "human_review",
        "reviewer",
        "notes",
    ],
    "registries/figure_manifest.tsv": [
        "figure_id",
        "panel_id",
        "claim_id",
        "dataset_id",
        "source_data",
        "analysis_script",
        "figure_path",
        "status",
        "reviewer",
        "notes",
    ],
}


def read_header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        return next(reader)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")

    for rel, expected_header in TSV_SCHEMAS.items():
        path = ROOT / rel
        if path.exists():
            actual_header = read_header(path)
            if actual_header != expected_header:
                errors.append(
                    f"schema mismatch in {rel}: expected {expected_header}, got {actual_header}"
                )

    forbidden_patterns = ["password=", "passwd=", "token=", "api_key=", "secret=", "bearer "]
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.exists() or path.suffix.lower() not in {".md", ".yml", ".tsv"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for pattern in forbidden_patterns:
            if pattern in text and rel != "AGENTS.md":
                errors.append(f"possible secret pattern `{pattern}` found in {rel}")

    if errors:
        print("Research Engineering Scaffold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Research Engineering Scaffold validation passed.")
    print(f"Checked {len(REQUIRED_FILES)} required files and {len(TSV_SCHEMAS)} TSV schemas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a standardized research engineering project.")
    parser.add_argument("--project-dir", required=True, help="Target project directory.")
    parser.add_argument("--project-name", required=True, help="Human-readable project name.")
    parser.add_argument("--title", default="", help="Working project or manuscript title.")
    parser.add_argument("--domain", default="research", help="Research domain.")
    parser.add_argument("--primary-hypothesis", default="", help="Primary working hypothesis.")
    parser.add_argument("--primary-data", default="TODO", help="Primary dataset or source.")
    parser.add_argument("--primary-endpoint", default="TODO", help="Primary endpoint, outcome, or metric.")
    parser.add_argument("--remote-path", default="", help="Optional remote project path.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing scaffold files.")
    parser.add_argument("--init-git", action="store_true", help="Initialize Git if needed.")
    parser.add_argument("--commit", action="store_true", help="Create an initial commit. Implies --init-git.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_dir = Path(args.project_dir).expanduser().resolve()
    project_id = slugify(args.project_name)
    today = date.today().isoformat()
    title = args.title.strip() or f"{args.project_name}: reproducible research project"
    primary_hypothesis = args.primary_hypothesis.strip() or "TODO: write the primary hypothesis before analysis."
    remote_path = args.remote_path.strip()
    remote_path_block = f"Server or remote path: `{remote_path}`" if remote_path else "Remote compute path: TODO"

    context = {
        "project_name": args.project_name.strip(),
        "project_id": project_id,
        "title": title,
        "domain": args.domain.strip(),
        "primary_hypothesis": primary_hypothesis,
        "primary_data": args.primary_data.strip(),
        "primary_endpoint": args.primary_endpoint.strip(),
        "remote_path": remote_path_block,
        "remote_path_raw": remote_path or "TODO",
        "today": today,
    }

    project_dir.mkdir(parents=True, exist_ok=True)
    for directory in DIRS:
        (project_dir / directory).mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    kept: list[str] = []
    for rel_path, template in templates().items():
        write_file(project_dir / rel_path, render(template, context), args.overwrite, written, kept)

    for rel_path in [
        "data/raw/.gitkeep",
        "data/processed/.gitkeep",
        "data/metadata/.gitkeep",
        "data/external/.gitkeep",
        "results/tables/.gitkeep",
        "results/figures/.gitkeep",
        "results/logs/.gitkeep",
        "results/reports/.gitkeep",
    ]:
        write_empty(project_dir / rel_path, args.overwrite, written, kept)

    if args.init_git or args.commit:
        if not (project_dir / ".git").exists():
            run(["git", "init", "-b", "main"], cwd=project_dir)
        if args.commit:
            run(["git", "add", "."], cwd=project_dir)
            run(["git", "commit", "-m", "Initialize Research Engineering Scaffold"], cwd=project_dir)

    print(f"Research Engineering Scaffold created at: {project_dir}")
    print(f"Files written: {len(written)}")
    print(f"Existing files kept: {len(kept)}")
    print("Next: run `python scripts/00_setup/validate_research_engineering_scaffold.py` from the project root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
