# Data Explainer

## Overview

This project uses **synthetic Letter of Credit (LC) data** created for the PE6201 project. No real customer, bank, or confidential trade-finance data is used.

## Data Used

The project contains three main forms of data:

1. **Part 1 classification examples**  
   Labelled examples for classifying LC cases as `compliant` or `discrepant`.

2. **Part 2 retrieval corpus**  
   LC-specific domain documents and supporting trade-finance notes used to test retrieval and grounding. The current experiment contains 16 domain documents split into 26 chunks.

3. **End-to-end demo knowledge base**  
   A small synthetic LC knowledge base embedded directly in `app.py` for the working demo.

## Location

- Classification examples: `PE6201_Part1_Classifier_vs_API.ipynb`
- Retrieval corpus: `PE6201_Part2_Retrieval.ipynb`
- Demo knowledge base: `app.py`

## Example Synthetic LC References

- `LC-2026-0091`
- `LC-2026-0114`
- `LC-2026-0158`

These identifiers, amounts, dates, organisations, and case outcomes are synthetic and exist only for this coursework prototype.

## Purpose

The data was designed to test:

- compliant vs discrepant classification;
- date, amount, tolerance, and document reasoning;
- retrieval of LC-specific facts;
- cross-LC retrieval errors;
- structured discrepancy extraction.

## Limitations

The corpus is deliberately small and synthetic. Results should therefore be interpreted as prototype evidence rather than production-level performance.
