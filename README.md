# AI-Assisted Letter of Credit Document Examination

## PE6201 End-of-Course Project

This project explores an AI-assisted workflow for Letter of Credit (LC) document examination. It combines compliance classification, LC-specific retrieval, structured discrepancy extraction, validation, and human review.

## Persona

**Primary user:** a trade-finance document examiner who reviews Letter of Credit presentations and needs support identifying discrepancies consistently and efficiently.

## Problem

Letter of Credit document examination requires trade-finance staff to compare submitted documents against LC terms, identify discrepancies, and record outcomes consistently. The task combines classification, document retrieval, and structured information extraction, so a single AI technique is not sufficient.

## Input

The system accepts:

- an LC examiner note or document-related case description;
- LC-specific reference information contained in the retrieval knowledge base.

## Output

The system produces:

- a `compliant` / `discrepant` classification;
- retrieved LC evidence with similarity scores;
- structured discrepancy output containing:
  - `lc_reference`
  - `document_type`
  - `discrepancy_category`
  - `severity`
  - `recommended_action`
- a final human-review step for higher-risk or ambiguous cases.

## Product Architecture

Input LC document / examiner note  
→ Compliance Classification  
→ LC-specific Evidence Retrieval  
→ Structured Discrepancy Extraction  
→ Validation / Human Review

![AI-Assisted LC Document Examination Workflow](docs/AI_Assisted_LC_Document_Examination_Workflow.png)

## Repository Structure

- `app.py` — end-to-end working demo
- `PE6201_Part1_Classifier_vs_API.ipynb` — classifier vs foundation-model API experiment
- `PE6201_Part2_Retrieval.ipynb` — retrieval, grounding, and retrieval-failure experiment
- `PE6201_Part3_Prompt_Evaluation.ipynb` — structured-output prompt evaluation
- `data/README.md` — data provenance and location explainer
- `evals/README.md` — evaluation design and metrics explainer
- `docs/` — product architecture documentation
- `requirements.txt` — Python dependencies

## System Components

### Part 1 — Classification

Compares a traditional TF-IDF + logistic-regression classifier with a foundation-model API for classifying LC cases as compliant or discrepant.

### Part 2 — Retrieval

Builds a retrieval system for LC-specific facts and evaluates grounding, breaker cases, and a documented cross-LC retrieval failure.

### Part 3 — Structured Output Evaluation

Evaluates free-text examiner-note conversion into structured discrepancy output using L1 structural checks and L2 semantic judgement.

## Metrics

### Metrics Targeted

- classification accuracy
- precision, recall, and F1
- inference latency
- API cost per item
- retrieval relevance and failure behaviour
- grounding behaviour for absent information
- L1 structural pass rate
- L2 semantic pass rate

### Metrics Reached

#### Classification
- Majority baseline accuracy: **60.0%**
- Local classifier accuracy: **81.0%**
- Foundation-model API accuracy: **100.0%** on the 21-item held-out test set
- Classifier latency: **0.07 ms/item**
- API latency: **1246 ms/item**

#### Retrieval
- **16 domain documents**
- **26 chunks**
- Main documented failure: a semantically similar chunk from the wrong LC was ranked first with similarity **0.796**

#### Prompt Evaluation
- Version 1: **L1 90%, L2 70%**
- Version 2: **L1 100%, L2 70%**

The 100% API accuracy was measured on a small 21-item test set and should not be interpreted as production-level perfect accuracy.

## Data and Evals

The project uses synthetic LC data only; no real customer, bank, or confidential trade-finance information is included.

See:

- [`data/README.md`](data/README.md) for data provenance, purpose, and where the data is defined.
- [`evals/README.md`](evals/README.md) for the evaluation sets, breaker tests, metrics, and reported results.

## Requirements

Python 3.11+ is recommended.

Install dependencies with:

```bash
pip install -r requirements.txt
```

Main packages:

- openai
- scikit-learn
- sentence-transformers
- numpy
- pandas

## API Key

The notebooks and demo use an OpenRouter API key. Do not store the key directly in the repository.

Set it as an environment variable before running the demo.

**Windows PowerShell:**

```powershell
$env:OPENROUTER_API_KEY="your_key_here"
```

**macOS / Linux:**

```bash
export OPENROUTER_API_KEY="your_key_here"
```

## Run the Demo

```bash
python app.py
```

Example input:

```text
The bill of lading shows one transshipment at Hong Kong although LC-2026-0114 prohibits transshipment.
```

Expected pipeline behaviour:

1. classify the note as `discrepant`;
2. retrieve LC-2026-0114 as the strongest evidence;
3. return structured JSON describing the discrepancy;
4. present the result for human review.

## Limitations and Rough Edges

This project is a prototype using small synthetic datasets and evaluation sets.

Important limitations include:

- the 21-item classification test set is too small to establish production-level accuracy;
- semantically similar LC documents can cause cross-document retrieval errors;
- API inference is substantially slower than the local classifier;
- structurally valid JSON can still contain semantic errors;
- the current fixed schema handles one main discrepancy category at a time;
- human review remains important when evidence conflicts or semantic uncertainty remains.

## Future Work

Potential next steps include:

- expanding the held-out evaluation set;
- adding LC-reference metadata filtering or reranking before semantic retrieval;
- supporting multiple discrepancies in one structured output;
- adding confidence thresholds and human-in-the-loop escalation;
- testing on anonymised real-world trade-finance documents.

## Author

Feng Jingjing  
PE6201 Emerging AI Technologies
