# Asthma Clinical NER

## Overiew 

This project develops a custom clinical named entity recognition (NER)
pipeline for extracting predefined asthma features from free-text patient language.

The system builds on the pretrained clinical NER model
`samrawal/bert-base-uncased_clinical-ner` and fine-tunes it using a custom asthma-specific annotation schema.

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

## 4. Objectives

The main objectives of this project are to:

- define a custom asthma-specific clinical NER schema;
- establish consistent annotation guidelines;
- create a diverse synthetic clinical-language dataset;
- manually annotate training examples using Label Studio;
- fine-tune `samrawal/bert-base-uncased_clinical-ner` for the custom entity schema;
- evaluate extraction performance using entity-level precision, recall and F1;
- analyse false positives, false negatives and entity-boundary errors;
- iteratively improve the training dataset based on observed model failures;
- progressively introduce additional asthma entities;
- develop a normalisation layer that converts extracted text spans into canonical structured feature values;
- eventually integrate the extractor with the downstream asthma treatment-prediction pipeline.



## 5. System Architecture

The intended architecture is:

```text
Patient free text
        ↓
Clinical tokenizer
        ↓
Pretrained clinical NER model
samrawal/bert-base-uncased_clinical-ner
        ↓
Fine-tuning on custom asthma annotations
        ↓
Asthma-specific token classifier
        ↓
BIO entity predictions
        ↓
Entity reconstruction
        ↓
Clinical value normalisation
        ↓
Structured asthma features
        ↓
Patient state / validation
        ↓
Downstream asthma treatment model
```

The NER and normalisation stages are deliberately separated.

For example:

```text
NER:

"twice a week"
→ NIGHT_WAKING

        ↓

Normalisation:

"twice a week"
→ 2

        ↓

Structured feature:

night_waking_nights_per_week = 2
```

---

# Asthma Clinical NER

A custom clinical Named Entity Recognition (NER) pipeline for extracting structured asthma information from free-text patient language.

> **Status:** Version 1 — Discovery inference & error analysis

## Overview

Asthma treatment-prediction models require structured clinical features, while patients naturally describe their symptoms using free text.

This project explores a specialised NLP approach for bridging that gap by fine-tuning:

`samrawal/bert-base-uncased_clinical-ner`

on a custom asthma-specific NER schema.

The extracted information is intended to pass through a later normalisation and clarification layer before being converted into structured features for a downstream asthma treatment-prediction model.

```text
Patient text
     ↓
Clinical NER
     ↓
Extracted clinical information
     ↓
Normalisation / clarification
     ↓
Structured asthma features
     ↓
Treatment-prediction model
```

The project is being developed incrementally so that extraction performance can be evaluated before additional clinical entities are introduced.

---

## Version 1

Version 1 currently focuses on three entities:

| Entity | Description |
|---|---|
| `AGE` | Current patient age |
| `SYMPTOM_FREQUENCY` | Frequency of general asthma symptoms |
| `NIGHT_WAKING` | Frequency of asthma-related night waking |

Both exact and ambiguous frequency information can be extracted.

For example:


"Asthma wakes me three nights a week."
→ NIGHT_WAKING["three nights a week"]
→ normalise to 3


while:

```text
"Asthma wakes me occasionally."
→ NIGHT_WAKING["occasionally"]
→ clarification required
```

This keeps entity recognition separate from downstream clinical-value normalisation.

---

## Development Progress

| Stage |
|---|---|
| V1 entity schema | ✅ Complete |
| Annotation guidelines | ✅ Complete |
| Initial synthetic dataset | ✅ Complete |
| Manual Label Studio annotation | ✅ Complete |
| BIO/token preprocessing | ✅ Complete |
| V1 baseline fine-tuning | ✅ Complete |
| Fixed benchmark evaluation | ✅ Complete |
| 500-sentence discovery pool inference | ✅ Complete |
| Prediction audit / error analysis | 🚧 Current |
| Targeted active-learning annotation | ⏳ Next |
| V1.1 retraining | ⏳ Planned |
| Final V1 evaluation | ⏳ Planned |

### Current Focus

Rather than scaling labelled data indiscriminately, the current V1 baseline is being run against a larger unlabelled discovery pool.

Model predictions will be audited to identify failure patterns such as false positives, missed entities, entity confusion and boundary errors.

High-value failure cases will then be selectively annotated and added to the training data for the next model iteration.

```text
V1 Baseline
     ↓
500 unseen discovery sentences
     ↓
Inference
     ↓
Prediction audit
     ↓
Identify failure patterns
     ↓
Select informative examples
     ↓
Manual annotation
     ↓
Targeted retraining
     ↓
V1.1
```

---

## Current Results

### V1 Baseline

The baseline model was trained using an initial manually annotated synthetic dataset and subsequently evaluated against a fixed unseen benchmark.

| Precision | Recall | F1 |
|---:|---:|---:|
| 0.601 | 0.759 | **0.671** |

The lower precision relative to recall motivates the current error-discovery stage, with particular attention to false positives and contextual discrimination.

Future iterations will be evaluated against the same fixed benchmark to measure whether targeted annotation improves performance.

| Model | Development Stage | Benchmark F1 |
|---|---|---:|
| V1 Baseline | Initial training | **0.671** |
| V1 AL-01 | First active-learning iteration | TBD |
| V1 AL-02 | Further refinement if required | TBD |

---

## Dataset

Development currently uses synthetic patient and clinical-language examples containing no real patient records.

The data includes:

- positive entity examples;
- linguistic and paraphrase variation;
- ambiguous frequency descriptions;
- negation and explicit absence;
- hard negatives;
- competing frequency expressions;
- clinical shorthand;
- informal patient language;
- age, medication and frequency distractors.

Manual annotations are created using **Label Studio**.

---

## Repository Structure


asthma-clinical-ner/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/
│   ├── annotation_guidelines.md
│   ├── dataset_design.md
│   └── experimentation.md
│
├── data/
│   ├── raw/
│   ├── annotations/
│   └── processed/
│
├── notebooks/
├── models/
├── results/
└── src/


---

## Documentation

More detailed technical documentation is kept outside the main README:

- **[Annotation Guidelines](docs/annotation_guidelines.md)**  
  Entity definitions, annotation boundaries, ambiguous language, negation and difficult annotation cases.

- **[Dataset Design](docs/dataset_design.md)**  
  Synthetic data methodology, linguistic diversity, hard negatives, competing frequencies and the roles of training, benchmark and discovery datasets.

- **[Experimentation](docs/experimentation.md)**  
  Model training, Google Colab experiments, baseline evaluation, benchmark methodology, discovery-pool inference, prediction auditing, error analysis and active-learning iterations.

---

## Next Steps

1. Audit and categorise model predictions.
2. Select high-value failure cases for manual annotation.
3. Add targeted examples to the training data.
4. Retrain as `V1 AL-01`.
5. Evaluate against the same fixed benchmark.
6. Repeat targeted refinement if required.
7. Stabilise Version 1 before introducing additional asthma entities.

---

## Limitations

- Current development data is synthetic.
- Version 1 currently covers only three entities.
- The normalisation/clarification layer is not yet complete.
- Performance on synthetic data does not establish real-world clinical performance.
- The system has not been clinically validated.

---

## Disclaimer

This project is an educational and research-oriented proof of concept.

It is not a medical device, has not been clinically validated, and is not intended for real-world diagnosis, prescribing or treatment decisions.