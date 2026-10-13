# Asthma Clinical NER — Annotation Guidelines

## 1. Purpose

This document defines the annotation guidelines for the custom asthma clinical Named Entity Recognition (NER) dataset.

The NER system is designed to identify clinically relevant information from free-text patient language.

Extracted entities will later pass through a separate normalisation and resolution stage that determines whether the extracted information:

1. can be converted directly into the structured value required by the downstream system; or
2. is relevant but insufficiently precise and therefore requires clarification.

The project is being developed incrementally.

These guidelines currently describe **Version 1** of the NER schema.

---

# 2. Version 1 Entity Schema

Version 1 contains three entities:

| Entity | Meaning |
|---|---|
| `AGE` | Information establishing the patient's current age |
| `SYMPTOM_FREQUENCY` | Information describing how frequently general asthma symptoms occur |
| `NIGHT_WAKING` | Information describing how frequently asthma causes night waking |

The eventual BIO label set is:

```text
O

B-AGE
I-AGE

B-SYMPTOM_FREQUENCY
I-SYMPTOM_FREQUENCY

B-NIGHT_WAKING
I-NIGHT_WAKING
```

In Label Studio, annotate using:

```text
AGE
SYMPTOM_FREQUENCY
NIGHT_WAKING
```

BIO conversion will occur later during preprocessing.

---

# 3. Core Annotation Philosophy

The NER model is responsible for identifying **clinically relevant information**.

It is not responsible for deciding whether that information can already be converted into the final numerical feature required by the downstream machine-learning model.

The pipeline is:

```text
Patient text
      ↓
NER
      ↓
Relevant clinical span
      ↓
Normaliser / Resolver
      ↓
Can the information be converted to an exact value?
      │
   ┌──┴──┐
   │     │
  YES    NO
   │     │
   ↓     ↓
value   clarification required
   │     │
   └──┬──┘
      ↓
Structured patient state
```

Therefore:

> **Relevant but ambiguous information should still be annotated.**

For example:

```text
My asthma wakes me three nights a week.
```

Annotate:

```text
[three nights a week]
→ NIGHT_WAKING
```

The normaliser can later resolve this to:

```text
3
```

However:

```text
My asthma wakes me occasionally.
```

should also be annotated:

```text
[occasionally]
→ NIGHT_WAKING
```

The normaliser should not invent a number for `occasionally`.

Instead:

```text
occasionally
      ↓
NIGHT_WAKING
      ↓
exact value unavailable
      ↓
clarification required
```

---

# 4. General Annotation Boundary Rule

Annotate the **smallest contiguous span that preserves the complete clinically relevant meaning of the target feature**.

This replaces a strict "frequency value only" rule.

For straightforward expressions, the entity will usually remain narrow.

Example:

```text
My asthma wakes me [twice a week].
                    NIGHT_WAKING
```

The surrounding words:

```text
My asthma wakes me
```

provide context to the transformer but are not required inside the entity span.

However, some grammatical constructions require a larger span.

Example:

```text
I generally have [two asthma-related night wakings each week].
                 NIGHT_WAKING
```

The quantity:

```text
two
```

and time period:

```text
each week
```

are separated by clinically relevant words.

Because BIO NER represents contiguous spans, annotate:

```text
two asthma-related night wakings each week
```

rather than creating disconnected entities.

The goal is therefore:

> **Use the smallest single contiguous span that preserves the complete relevant meaning.**

---

# 5. Exact, Ambiguous and Missing Information

Version 1 deliberately distinguishes three situations.

## 5.1 Exact / Resolvable Information

Example:

```text
Asthma wakes me [three nights a week].
                 NIGHT_WAKING
```

NER result:

```text
three nights a week
```

Normalisation:

```text
3
```

---

## 5.2 Relevant but Ambiguous Information

Example:

```text
Asthma wakes me [occasionally].
                 NIGHT_WAKING
```

NER successfully identifies relevant information.

However:

```text
occasionally ≠ exact 0–7 value
```

The normaliser should therefore mark the feature as requiring clarification.

---

## 5.3 Missing Information

Example:

```text
I'm 24 and currently use an inhaler.
```

There is no information about symptom frequency or night waking.

Therefore:

```text
AGE → present
SYMPTOM_FREQUENCY → no entity
NIGHT_WAKING → no entity
```

The downstream system may later interpret the absent features as:

```text
Unknown
```

Do not invent annotations when the text contains no relevant information.

---

# 6. AGE

## 6.1 Definition

`AGE` represents information establishing the **current age of the patient being assessed**.

The downstream structured feature is:

```text
age
```

---

## 6.2 Simple Age

Example:

```text
I'm [24].
    AGE
```

Annotate:

```text
24
```

---

## 6.3 Age Introduced by "aged"

Example:

```text
Patient aged [46] reports asthma symptoms.
             AGE
```

Following the value-focused approach, annotate:

```text
46
```

The word `aged` provides contextual information but is not required in the entity.

---

## 6.4 Hyphenated Age Expressions

Example:

```text
[18-year-old] patient with asthma.
AGE
```

Annotate the complete expression:

```text
18-year-old
```

because the age descriptor is structurally joined to the number.

---

## 6.5 Compact Age Expressions

Example:

```text
[26yo] with asthma.
AGE
```

Annotate:

```text
26yo
```

---

## 6.6 Written Ages

Example:

```text
I'm [twenty-four].
    AGE
```

Annotate:

```text
twenty-four
```

---

## 6.7 Disease Duration Is Not AGE

Example:

```text
I've had asthma for 15 years.
```

Do not annotate:

```text
15 years
```

as `AGE`.

This represents disease duration.

---

## 6.8 Historical Age Is Not Current AGE

Example:

```text
I'm [49] and was diagnosed when I was 13.
    AGE
```

Do not annotate:

```text
13
```

The patient is currently 49.

---

## 6.9 Another Person's Age

Example:

```text
My 16-year-old brother has asthma, but I'm [28].
                                            AGE
```

Do not annotate:

```text
16-year-old
```

because it refers to another person.

---

# 7. SYMPTOM_FREQUENCY

## 7.1 Definition

`SYMPTOM_FREQUENCY` represents information describing **how frequently the patient experiences general asthma symptoms**.

The eventual downstream feature is:

```text
symptom_days_per_week
```

The NER model identifies the relevant information.

The normaliser determines whether it can be converted into a value from:

```text
0–7
```

or whether clarification is required.

---

## 7.2 Exact Weekly Frequency

Example:

```text
My asthma symptoms occur [four days a week].
                          SYMPTOM_FREQUENCY
```

Normalisation:

```text
4
```

---

## 7.3 Other Exact Expressions

Examples:

```text
Symptoms occur [three days per week].
                 SYMPTOM_FREQUENCY
```

```text
Symptoms occur [five days out of seven].
                 SYMPTOM_FREQUENCY
```

```text
I experience symptoms [twice weekly].
                       SYMPTOM_FREQUENCY
```

---

## 7.4 Everyday Symptoms

Example:

```text
I experience asthma symptoms [every day].
                              SYMPTOM_FREQUENCY
```

Normalisation can later resolve:

```text
every day → 7
```

---

## 7.5 Explicit Zero

Explicit absence is clinically meaningful.

Example:

```text
I [don't get asthma symptoms during a normal week].
   SYMPTOM_FREQUENCY
```

Annotate the smallest contiguous span that preserves the complete zero-frequency meaning.

The normaliser may resolve this to:

```text
0
```

This is different from the patient saying nothing about symptom frequency.

---

# 8. Ambiguous Symptom Frequency

Real patients may not provide exact numerical frequencies.

These expressions should still be annotated when they clearly describe symptom frequency.

Examples include:

```text
most days
fairly often
sometimes
occasionally
frequently
now and then
intermittently
```

Example:

```text
My asthma bothers me [most days].
                      SYMPTOM_FREQUENCY
```

Annotate:

```text
most days
```

Do not arbitrarily normalise:

```text
most days = 5
```

unless a future clinically justified mapping explicitly defines this.

Instead:

```text
most days
      ↓
SYMPTOM_FREQUENCY
      ↓
not sufficiently precise
      ↓
clarification required
```

---

# 9. Variable Symptom Frequency

Some patients describe frequency as changing substantially between weeks.

Example:

```text
My symptoms [come and go; some weeks they're frequent and other weeks I barely notice them].
            SYMPTOM_FREQUENCY
```

In this case, annotating only:

```text
frequent
```

would lose important information.

The complete meaning is that symptom frequency varies between weeks.

Therefore annotate the smallest contiguous span that preserves this variability:

```text
come and go; some weeks they're frequent and other weeks I barely notice them
```

The downstream resolver should recognise:

```text
Relevant symptom-frequency information? YES

Exact 0–7 value available? NO

Action → clarification required
```

---

# 10. Approximation Words

Expressions such as:

```text
about
around
roughly
approximately
```

may accompany otherwise resolvable frequencies.

Example:

```text
Symptoms occur about [four days a week].
                      SYMPTOM_FREQUENCY
```

Annotate:

```text
four days a week
```

when the approximation word is not necessary to preserve the core frequency value.

The normaliser may still resolve this approximately to:

```text
4
```

Maintain this boundary convention consistently.

---

# 11. Medication Frequency Is Not SYMPTOM_FREQUENCY

Example:

```text
I use my inhaler three times a week.
```

Do not annotate:

```text
three times a week
```

as `SYMPTOM_FREQUENCY`.

Medication use and symptom occurrence are different concepts.

---

# 12. Exercise Frequency Is Not SYMPTOM_FREQUENCY

Example:

```text
I exercise four days a week.
```

Do not annotate:

```text
four days a week
```

as `SYMPTOM_FREQUENCY`.

---

# 13. Other Frequency Distractors

Do not annotate unrelated frequencies.

Examples:

```text
I work three days a week.

I take vitamin D every day.

I go swimming twice weekly.

I attend university four days a week.
```

These should remain `O` for Version 1.

---

# 14. NIGHT_WAKING

## 14.1 Definition

`NIGHT_WAKING` represents information describing **how frequently asthma or asthma-related symptoms wake the patient during the night**.

The downstream feature is:

```text
night_waking_nights_per_week
```

The NER model identifies the relevant information.

The normaliser determines whether the expression can be converted to:

```text
0–7
```

or requires clarification.

---

## 14.2 Exact Frequency

Example:

```text
My asthma wakes me [twice a week].
                    NIGHT_WAKING
```

Normalisation:

```text
2
```

---

## 14.3 Explicit Night Frequency

Example:

```text
My asthma wakes me [three nights a week].
                    NIGHT_WAKING
```

Normalisation:

```text
3
```

---

## 14.4 Other Exact Expressions

Examples:

```text
Asthma wakes me [twice weekly].
                 NIGHT_WAKING
```

```text
Asthma wakes me [four nights out of seven].
                 NIGHT_WAKING
```

```text
I wake because of asthma [once each week].
                          NIGHT_WAKING
```

---

## 14.5 Every Night

Example:

```text
Asthma wakes me [every night].
                 NIGHT_WAKING
```

Normalisation:

```text
7
```

---

# 15. Explicit Zero Night Waking

Explicit absence of night waking should be annotated.

Example:

```text
My asthma [never] wakes me at night.
           NIGHT_WAKING
```

Normalisation:

```text
0
```

Another example:

```text
My asthma [doesn't wake me at night].
           NIGHT_WAKING
```

Here `doesn't` alone does not preserve what is being negated.

Therefore annotate:

```text
doesn't wake me at night
```

The general rule is:

> Annotate the smallest contiguous span that preserves the complete zero-frequency meaning.

---

# 16. Ambiguous Night Waking

Relevant but vague night-waking expressions should still be annotated.

Example:

```text
My asthma [sometimes] wakes me at night.
           NIGHT_WAKING
```

Example:

```text
Asthma wakes me [occasionally].
                 NIGHT_WAKING
```

Example:

```text
Asthma wakes me [most nights].
                 NIGHT_WAKING
```

These are relevant `NIGHT_WAKING` expressions.

However, the normaliser should not invent exact values.

Instead:

```text
NER
      ↓
NIGHT_WAKING found
      ↓
exact value unavailable
      ↓
clarification required
```

---

# 17. Variable Night Waking

Some patients describe substantial week-to-week variation.

Example:

```text
[Some weeks I wake several times with asthma and other weeks not at all].
NIGHT_WAKING
```

The entire span is annotated because the complete statement is necessary to preserve the frequency meaning.

Annotating only:

```text
several times
```

would incorrectly remove the information that:

```text
other weeks → no waking
```

Therefore:

```text
Relevant night-waking information? YES

Exact weekly value? NO

Action → clarification required
```

---

# 18. Uncertain Night Waking

Example:

```text
18-year-old patient says asthma [sometimes] wakes them at night but cannot estimate how often.
                               NIGHT_WAKING
```

Annotations:

```text
18-year-old
→ AGE

sometimes
→ NIGHT_WAKING
```

Do not annotate:

```text
cannot estimate how often
```

as a second `NIGHT_WAKING` entity.

It provides contextual evidence that the value is uncertain, but `sometimes` is the frequency-bearing expression.

---

# 19. Another Ambiguous Example

Example:

```text
Patient aged 46 says night waking happens [occasionally], although they are unsure how many nights per week.
                                          NIGHT_WAKING
```

Annotations:

```text
46
→ AGE

occasionally
→ NIGHT_WAKING
```

Do not annotate:

```text
how many nights per week
```

because it does not provide a frequency value.

---

# 20. Context Determines Entity Type

The same surface frequency expression can represent different concepts.

Example:

```text
My asthma wakes me [twice a week].
                    NIGHT_WAKING
```

But:

```text
I experience asthma symptoms [twice a week].
                              SYMPTOM_FREQUENCY
```

And:

```text
I use my inhaler twice a week.
```

contains no Version 1 frequency entity.

Therefore:

```text
"twice a week"
```

does not have a fixed label.

Its label depends on the surrounding context.

This contextual discrimination is one of the central learning objectives of the model.

---

# 21. Competing Frequencies

A sentence may contain multiple frequency expressions describing different concepts.

Example:

```text
I use my inhaler twice a day, get symptoms [four days a week],
and asthma wakes me [three nights weekly].
```

Annotations:

```text
twice a day
→ O

four days a week
→ SYMPTOM_FREQUENCY

three nights weekly
→ NIGHT_WAKING
```

Do not annotate every frequency expression simply because it contains a number and time period.

---

# 22. Multiple Target Entities

A sentence may contain several Version 1 entities.

Example:

```text
I'm [31], get asthma symptoms [four days a week],
and asthma wakes me [two nights a week].
```

Annotations:

```text
31
→ AGE

four days a week
→ SYMPTOM_FREQUENCY

two nights a week
→ NIGHT_WAKING
```

Annotate all relevant target entities independently.

---

# 23. Shared Negation / Complex Grammar

Some sentences contain grammatical structures where one negation applies to multiple clinical concepts.

Example:

```text
I'm 67 and asthma doesn't bother me during the day or wake me overnight.
```

The word:

```text
doesn't
```

applies to both:

```text
daytime symptoms
```

and:

```text
night waking
```

Simple BIO span annotation does not naturally represent every shared or discontinuous semantic relationship.

During Version 1 dataset development, prefer clearer constructions where possible:

```text
I'm 67. Asthma doesn't bother me during the day and it doesn't wake me overnight.
```

This produces cleaner independent annotations.

More complex coordinated negation should later be included deliberately in challenge/evaluation data to assess model robustness.

Do not invent overlapping BIO annotations without first updating the annotation schema.

---

# 24. Unknown Is Not an Entity

`Unknown` is a downstream state value.

It is not an NER label.

Example:

```text
I'm 30 and my asthma has been troublesome recently.
```

Possible annotation:

```text
30
→ AGE
```

If the sentence provides no usable information about symptom frequency or night waking:

```text
SYMPTOM_FREQUENCY → no entity
NIGHT_WAKING → no entity
```

The downstream system may interpret these missing entities as:

```text
Unknown
```

---

# 25. Important Distinction: Missing vs Ambiguous

The system must eventually distinguish:

## Missing

```text
"I'm 24 and use an inhaler."
```

No night-waking information exists.

Result:

```text
NIGHT_WAKING → not detected
```

Downstream:

```text
Unknown
```

---

## Ambiguous

```text
"Asthma wakes me occasionally."
```

Relevant information exists.

Result:

```text
occasionally
→ NIGHT_WAKING
```

But:

```text
exact value unavailable
```

Downstream:

```text
needs clarification
```

---

## Exact

```text
"Asthma wakes me three nights a week."
```

Result:

```text
three nights a week
→ NIGHT_WAKING
```

Normalisation:

```text
3
```

This distinction is central to the Version 1 architecture.

---

# 26. Hard Negatives

Hard-negative examples deliberately resemble target entities but should not receive target labels.

Examples:

```text
I use my inhaler twice a week.
```

```text
I exercise four days a week.
```

```text
I work three nights a week.
```

```text
I've had asthma for 15 years.
```

These examples discourage shortcut learning such as:

```text
<number> + week
→ SYMPTOM_FREQUENCY
```

or:

```text
<number> + nights
→ NIGHT_WAKING
```

or:

```text
<number> + years
→ AGE
```

---

# 27. Annotation Decision Process

When annotating each example, follow this sequence.

## Step 1 — Identify the Patient

Determine whose information is being described.

Do not annotate another person's information as belonging to the patient.

---

## Step 2 — Check AGE

Ask:

> Does the text establish the patient's current age?

If yes:

```text
AGE
```

---

## Step 3 — Check SYMPTOM_FREQUENCY

Ask:

> Does the text provide any clinically relevant information about how frequently general asthma symptoms occur?

If yes:

```text
SYMPTOM_FREQUENCY
```

This applies even if the information is vague or variable.

---

## Step 4 — Check NIGHT_WAKING

Ask:

> Does the text provide any clinically relevant information about how frequently asthma wakes the patient at night?

If yes:

```text
NIGHT_WAKING
```

This applies even if the information is vague or variable.

---

## Step 5 — Determine the Boundary

Ask:

> What is the smallest contiguous span that preserves the complete relevant meaning?

For exact expressions, this will usually be narrow.

For ambiguous or variable descriptions, a larger span may be necessary.

---

## Step 6 — Check Distractors

Verify that frequency expressions do not instead describe:

- medication use;
- exercise;
- employment;
- university attendance;
- unrelated sleep patterns;
- another person's symptoms;
- disease duration;
- historical age;
- another non-target concept.

---

# 28. Quality-Control Checklist

Before completing an annotation, check:

- [ ] Did I annotate the patient's current age rather than another number?
- [ ] Did I distinguish current age from age at diagnosis?
- [ ] Did I distinguish current age from disease duration?
- [ ] Does `SYMPTOM_FREQUENCY` actually describe asthma symptoms?
- [ ] Does `NIGHT_WAKING` actually describe asthma-related night waking?
- [ ] Did I avoid medication-frequency distractors?
- [ ] Did I avoid exercise/work-frequency distractors?
- [ ] Did I annotate relevant ambiguous language?
- [ ] Did I avoid inventing an exact value for vague language?
- [ ] Did I distinguish explicit zero from missing information?
- [ ] Did I use the smallest contiguous span that preserves the complete meaning?
- [ ] Did I preserve variability when the patient describes different frequencies across time?
- [ ] Are my boundaries consistent with the annotation guidelines?
- [ ] Did I annotate every relevant Version 1 entity?

---

# 29. Example Summary

| Patient Text | Entity | Expected Downstream Handling |
|---|---|---|
| `I'm 24.` | `24 → AGE` | `24` |
| `14-year-old patient` | `14-year-old → AGE` | `14` |
| `Symptoms four days a week` | `four days a week → SYMPTOM_FREQUENCY` | `4` |
| `Symptoms every day` | `every day → SYMPTOM_FREQUENCY` | `7` |
| `Symptoms most days` | `most days → SYMPTOM_FREQUENCY` | Clarification |
| `Asthma wakes me twice weekly` | `twice weekly → NIGHT_WAKING` | `2` |
| `Asthma wakes me every night` | `every night → NIGHT_WAKING` | `7` |
| `Asthma never wakes me` | `never → NIGHT_WAKING` | `0` |
| `Asthma wakes me occasionally` | `occasionally → NIGHT_WAKING` | Clarification |
| `I use my inhaler twice weekly` | No V1 frequency entity | Ignore |
| `I exercise four days weekly` | No V1 frequency entity | Ignore |
| No mention of night waking | No `NIGHT_WAKING` entity | `Unknown` |

---

# 30. Relationship to Normalisation

NER extraction and clinical-value normalisation are separate stages.

## Exact Example

```text
"twice a week"
        ↓
NIGHT_WAKING
        ↓
normaliser
        ↓
2
```

---

## Zero Example

```text
"never"
        ↓
NIGHT_WAKING
        ↓
normaliser
        ↓
0
```

---

## Ambiguous Example

```text
"occasionally"
        ↓
NIGHT_WAKING
        ↓
normaliser
        ↓
cannot resolve safely
        ↓
clarification required
```

---

## Missing Example

```text
No night-waking information
        ↓
no NIGHT_WAKING entity
        ↓
Unknown
        ↓
conversation logic may request information
```

---

# 31. Relationship to Conversation Logic

The long-term system will use NER and normalisation results to determine whether follow-up questions are necessary.

Conceptually:

```text
Patient text
      ↓
NER
      ↓
Relevant feature detected?
     / \
   YES  NO
    │    │
    │    └────────────→ Missing / Unknown
    ↓
Normaliser
    ↓
Exact value?
   /     \
 YES      NO
  ↓        ↓
0–7     clarification required
  │        │
  └────┬───┘
       ↓
Patient state
       ↓
Conversation logic
```

The NER model should therefore not discard relevant ambiguous information simply because it cannot immediately be converted into the final model feature.

---

# 32. Dataset Status

The Version 1 dataset is synthetic and contains no real patient records.

It is being manually annotated using Label Studio.

The dataset deliberately includes:

- exact frequency expressions;
- ambiguous frequency expressions;
- variable frequency descriptions;
- explicit zero/negation;
- missing information;
- multiple target entities;
- hard negatives;
- competing frequencies;
- medication-frequency distractors;
- exercise/work-frequency distractors;
- age and disease-duration distractors;
- clinical shorthand;
- conversational patient language.

The purpose is to encourage contextual extraction rather than superficial pattern matching.

---

# 33. Versioning

These guidelines correspond to:

```text
NER Schema Version: 1
```

Current entities:

```text
AGE
SYMPTOM_FREQUENCY
NIGHT_WAKING
```

The annotation guidelines are considered part of the model specification.

If an annotation rule changes:

1. update this document;
2. document why the rule changed;
3. review previously annotated examples affected by the change;
4. record the change in Git;
5. avoid silently mixing different annotation conventions within the same dataset version.

---

# 34. Current Version 1 Annotation Principle

The current guiding principle can be summarised as:

> **Annotate text whenever it provides clinically relevant information about a Version 1 feature, even when that information is ambiguous. Use the smallest contiguous span that preserves the complete relevant meaning. Exact expressions can later be normalised to structured values; ambiguous expressions should be passed to clarification logic rather than assigned arbitrary numerical values.**

This produces three downstream outcomes:

```text
EXACT INFORMATION
→ NER
→ normalise
→ structured value

AMBIGUOUS INFORMATION
→ NER
→ cannot safely normalise
→ clarification

NO INFORMATION
→ no entity
→ Unknown
→ information may need to be requested
```