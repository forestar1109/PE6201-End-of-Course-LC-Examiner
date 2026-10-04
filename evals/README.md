# Evaluation Explainer

## Overview

The project evaluates three different capabilities: classification, retrieval/grounding, and structured-output reliability.

## Part 1 — Classification Evaluation

A held-out test set of **21 examples** compares:

- majority-class baseline;
- TF-IDF + logistic-regression classifier;
- foundation-model API.

### Metrics

- accuracy
- precision
- recall
- F1
- latency
- API token cost

### Results

- Baseline accuracy: **60.0%**
- Local classifier accuracy: **81.0%**
- Foundation-model API accuracy: **100.0%** on the 21-item test set
- Classifier latency: **0.07 ms/item**
- API latency: **1246 ms/item**

The API result is based on a small held-out set and should not be interpreted as proof of production-level perfect accuracy.

## Part 2 — Retrieval and Grounding Evaluation

Five document-specific questions test whether retrieval supplies facts that are not reliably available from general model knowledge.

Additional breaker tests cover:

- vocabulary mismatch;
- questions requiring multiple pieces of evidence;
- distractor documents;
- absent but plausible information.

### Documented Failure

For an LC-2026-0158 question about presentation period and expiry date, the top-ranked chunk came from the wrong LC with similarity **0.796**. This demonstrates that semantic similarity does not guarantee factual identity.

Grounding is also tested with an out-of-scope question; the expected safe response is `The notes do not say.`

## Part 3 — Prompt Evaluation

The evaluation set contains **10 cases**:

- 5 typical;
- 3 edge;
- 2 adversarial.

### Evaluation Levels

- **L1:** automatic structural checks such as valid JSON and expected schema
- **L2:** semantic judgement of whether the output is substantively correct

### Results

- Version 1: **L1 90%, L2 70%**
- Version 2: **L1 100%, L2 70%**

The v2 prompt fixed the structural JSON failure without improving the overall L2 semantic pass rate. This illustrates why schema validation alone is insufficient.

## Evaluation Limitations

- small test sets;
- synthetic data;
- LLM-as-judge behaviour can itself require human spot-checking;
- semantic edge cases and multiple-discrepancy notes remain challenging.
