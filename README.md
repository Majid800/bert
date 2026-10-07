# Asthma Clinical NER

## Overiew 

This project develops a custom clinical named entity recognition (NER)
pipeline for extracting predefined asthma features from free-text patient
language.

The system builds on the pretrained clinical NER model
`samrawal/bert-base-uncased_clinical-ner` and fine-tunes it using a custom
asthma-specific annotation schema.

The extracted entities are intended to be normalised into the structured
clinical features required by a downstream asthma treatment-prediction model.

## Motivation

My existing asthma treatment-prediction model requires predefined structured
clinical features such as symptom frequency, night waking, activity
limitation and exacerbation history.

Patients, however, naturally provide this information using unstructured
language rather than model-ready feature values.

An initial implementation in my wider healthcare AI project uses a
general-purpose LLM API with structured outputs to perform this extraction.

This project investigates a specialised alternative: adapting a pretrained
clinical NER model to recognise the asthma-specific entities required by the
downstream prediction system.

Rather than relying on a general-purpose LLM to directly produce the complete
structured patient representation, this project explores a narrower and
independently trainable clinical NLP pipeline consisting of entity extraction,
normalisation and structured feature generation.

## Development Approach

The NER system is being developed incrementally.

Each version introduces a controlled group of clinical entities so that
annotation quality, tokenisation, training behaviour and extraction
performance can be evaluated before increasing task complexity.

### Version 1

**Entities**

- `AGE`
- `SYMPTOM_FREQUENCY`
- `NIGHT_WAKING`

**Status:** In development

Version 1 is intended to establish the complete NER pipeline from manual
annotation through to model training and evaluation.

## Current Pipeline

Patient text
→ Manual annotation
→ BIO labels
→ Clinical tokenisation
→ Token-label alignment
→ Transformer fine-tuning
→ Entity extraction
→ Normalisation
→ Structured asthma features

## Current Status

Version 1 dataset annotation and model-development work is in progress.

## Disclaimer

This project is an educational and research proof of concept. It has not
been clinically validated and is not intended for real-world diagnosis,
prescribing, or treatment decisions.