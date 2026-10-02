# AI-Assisted Letter of Credit Document Examination

## PE6201 End-of-Course Project

This project explores an AI-assisted workflow for Letter of Credit (LC) document examination.

The system combines three complementary components:

1. Compliance classification
2. Retrieval of LC-specific information
3. Structured discrepancy extraction

## Problem

Letter of Credit document examination requires trade-finance staff to compare submitted documents against LC terms, identify discrepancies, and record outcomes consistently. The task combines classification, document retrieval, and structured information extraction, so a single AI technique is not sufficient.

## System Overview

The project is implemented through three connected experiments:

- `PE6201_Part1_Classifier_vs_API.ipynb`  
  Compares a traditional TF-IDF classifier with a foundation-model API for classifying LC cases as compliant or discrepant.

- `PE6201_Part2_Retrieval.ipynb`  
  Builds a retrieval system for LC-specific facts and evaluates retrieval failures and grounding.

- `PE6201_Part3_Prompt_Evaluation.ipynb`  
  Evaluates structured discrepancy extraction using L1 structural checks and L2 semantic judgement.

## Main Results

### Classification
- Majority baseline accuracy: 60.0%
- Local classifier accuracy: 81.0%
- Foundation-model API accuracy: 100.0% on the 21-item test set
- Classifier latency: 0.07 ms/item
- API latency: 1246 ms/item

### Retrieval
- 16 domain documents
- 26 chunks
- Main documented failure: retrieval confused semantically similar LC documents

### Prompt Evaluation
- Version 1: L1 90%, L2 70%
- Version 2: L1 100%, L2 70%

The 100% API accuracy was measured on a small 21-item test set and should not be interpreted as production-level perfect accuracy.

## Requirements

Python 3.11+ is recommended.

Main packages used:
- openai
- scikit-learn
- sentence-transformers
- numpy

## API Key

The notebooks use an OpenRouter API key.

Do not store the key directly in the repository. Set it as an environment variable instead:

```bash
OPENROUTER_API_KEY=your_key_here
``` 
## Limitations

This project is a prototype using a small synthetic LC dataset.

Important limitations include:
- small evaluation sets
- retrieval errors between semantically similar LC documents
- API latency
- structured outputs may be valid in format but still semantically incorrect
- human review remains important for higher-risk trade-finance decisions
