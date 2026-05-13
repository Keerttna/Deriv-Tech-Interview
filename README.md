# Funnel Friction Intelligence Pipeline

## Overview

This project implements a deterministic onboarding-funnel analytics pipeline that:

* ingests onboarding event streams
* reconstructs user sessions
* computes deterministic funnel and segment metrics
* identifies friction points
* computes lift potential deterministically
* generates grounded friction hypotheses
* produces an A/B-test backlog with deterministic sample-size calculations
* generates final reporting and validation artifacts

The pipeline is replayable, reproducible, and designed to operate on evaluator-provided event streams that follow the same schema.

---

# Core Design Principles

## Deterministic Analytics

All analytics computations are implemented in code:

* funnel conversion metrics
* segment metrics
* lift potential
* ranking
* sample-size calculations

LLMs are never used to compute metrics.

---

## Staged Pipeline Architecture

The pipeline executes in explicit stages:

```text
INIT
 -> EVENTS_LOADED
 -> DATASET_EXTENDED_OR_VALIDATED
 -> SESSIONS_RECONSTRUCTED
 -> FUNNEL_AGGREGATED
 -> SEGMENTS_AGGREGATED
 -> HYPOTHESES_GENERATED
 -> LIFT_POTENTIAL_COMPUTED
 -> RANKINGS_CRITIQUED
 -> EXPERIMENTS_GENERATED
 -> SAMPLE_SIZES_COMPUTED
 -> REPORT_GENERATED
 -> OPTIONAL_CHECKS_COMPLETE
 -> VALIDATION_COMPLETE
 -> RESULTS_FINALISED
```

---

## Replayability

The evaluator may:

* delete generated artifacts
* replace `events.json`
* rerun the repository from a clean checkout

The pipeline regenerates all outputs deterministically.

---

# Funnel Stages

Configured in:

```text
src/utils/constants.py
```

Pipeline funnel order:

```text
landing
signup_form
email_verify
kyc_doc_upload
kyc_review
first_deposit
first_trade
```

---

# Repository Structure

```text
project/
│
├── data/
│   └── events.json
│
├── outputs/
│   ├── funnel.json
│   ├── segments.json
│   ├── sampled_traces.json
│   ├── hypotheses.json
│   ├── ranked_hypotheses.json
│   ├── experiments.json
│   ├── friction_report.md
│   ├── llm_calls.jsonl
│   └── ...
│
├── src/
│   ├── analytics/
│   ├── llm/
│   ├── pipeline/
│   ├── reporting/
│   ├── utils/
│   └── validation/
│
├── tests/
├── pipeline.py
├── validate.py
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repo_url>
cd <repo_name>
```

---

## 2. Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

If execution is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# Running the Pipeline

Execute the full pipeline:

```powershell
python pipeline.py
```

Expected stages:

```text
Generating synthetic dataset...
Reconstructing sessions...
Computing funnel metrics...
Computing segment metrics...
Sampling representative traces...
Generating hypotheses...
Ranking hypotheses...
Generating experiments...
Generating final report...
```

---

# Validation

Run:

```powershell
python validate.py
```

Expected:

```text
PASS artifact existence
PASS JSON validity
PASS experiment validation

ALL VALIDATIONS PASSED
```

---

# Synthetic Dataset Extension

The pipeline extends the provided seed fixture into:

* ~600 sessions
* ~4000–6000 events
* realistic funnel progression
* realistic segment variation

Segment dimensions:

* country
* device
* language

---

# Seed Friction Patterns Injected

## Signup Form Friction

Affected segment:

```text
BR + mobile_android + pt-BR
```

Behavior:

* elevated signup dropoff
* invalid phone validation errors
* localized formatting friction

Error:

```text
invalid_country_code
```

---

## KYC Upload Friction

Affected segment:

```text
NG
```

Behavior:

* elevated KYC upload dropoff
* unsupported document formats

Error:

```text
document_format_unsupported
```

---

## KYC Review Latency

Behavior:

* elevated review latency
* long-tail p90 delays
* abandonment during review stage

---

# Deterministic Funnel Metrics

Generated artifact:

```text
outputs/funnel.json
```

Metrics computed per funnel stage:

* entries
* completions
* dropoffs
* conversion_rate
* dropoff_rate
* median_time_spent_seconds
* p90_time_spent_seconds

Each metric includes explicit numerators and denominators.

---

# Segment Aggregation

Generated artifact:

```text
outputs/segments.json
```

Segment stratifications:

* country
* device
* language
* country × device
* device × language
* country × language

---

# Session Trace Sampling

Generated artifact:

```text
outputs/sampled_traces.json
```

Each sampled trace includes:

* session_id
* segment attributes
* ordered steps reached
* validation errors
* durations
* final step reached
* conversion outcome

Approximately 50 representative traces are sampled deterministically.

---

# Hypothesis Generation

Generated artifact:

```text
outputs/hypotheses.json
```

Hypotheses are generated from:

* funnel metrics
* segment metrics
* sampled traces

Each hypothesis contains:

* affected step
* affected segment
* suspected cause
* supporting evidence
* confidence level

---

# Lift Potential Ranking

Generated artifact:

```text
outputs/ranked_hypotheses.json
```

Lift potential is computed deterministically using:

```text
lift_potential =
impacted_segment_volume *
max(0,
segment_dropoff_rate - baseline_dropoff_rate)
```

Hypotheses are ranked by computed lift potential.

---

# Experiment Backlog

Generated artifact:

```text
outputs/experiments.json
```

Each experiment includes:

* experiment_id
* hypothesis
* intervention
* primary metric
* guardrail metric
* target segment
* minimum detectable effect
* baseline conversion rate
* sample size per arm
* runtime estimate
* success criteria

Every experiment includes a guardrail metric.

---

# Sample Size Model

Generated artifact:

```text
outputs/sample_size_model.md
```

Statistical assumptions:

* Power = 0.8
* Alpha = 0.05
* Two-sided test

Implementation uses:

* `statsmodels.stats.power.NormalIndPower`
* `statsmodels.stats.proportion.proportion_effectsize`

---

# Final Reporting

Generated artifact:

```text
outputs/friction_report.md
```

The report includes:

* Executive Summary
* Funnel Overview
* Segment-Level Findings
* Top Friction Hypotheses
* Lift Potential Ranking
* Causal-Plausibility Notes
* A/B-Test Backlog
* Confidence and Caveats

---

# Counterfactual Checks

Generated artifact:

```text
outputs/counterfactual_check.json
```

Alternative explanations considered:

* instrumentation issues
* traffic quality shifts
* localization mismatch
* browser/device bugs

---

# Localization Insights

Generated artifact:

```text
outputs/localisation_insights.json
```

Localization-driven friction patterns are identified from segment-level analytics.

---

# Sequential Experiment Planning

Generated artifact:

```text
outputs/sequential_test_plan.md
```

Includes:

* experiment ordering
* dependency rationale
* interaction-risk mitigation
* cooldown recommendations
* rollout gates

---

# LLM Call Logging

Generated artifact:

```text
outputs/llm_calls.jsonl
```

Every LLM stage is logged separately.

Each record contains:

* stage
* timestamp
* provider
* model
* prompt hash
* input artifacts
* output artifact

---

# Testing

Available validation tests:

```powershell
python -m tests.test_phase2_foundation
python -m tests.test_funnel_metrics
python -m tests.test_segment_metrics
python -m tests.test_trace_sampling
python -m tests.test_phase5_intelligence
```

---

# Key Technical Constraints Satisfied

## Deterministic Code

Implemented deterministically:

* funnel math
* segment metrics
* lift potential
* sample-size computation
* ranking

---

## LLM Usage Constraints

LLMs are used only for:

* hypothesis generation
* causal critique
* experiment ideation
* reporting support

LLMs never compute metrics.

---

# Technologies Used

* Python 3.12
* pandas
* numpy
* scipy
* statsmodels
* JSON
* Markdown

---

# Author Notes

This repository was designed for replayable evaluation under clean-checkout execution constraints.

The architecture prioritizes:

* deterministic analytics
* modular orchestration
* reproducibility
* evaluator transparency
* explicit validation
