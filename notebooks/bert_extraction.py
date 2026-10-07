from transformers import pipeline

print("Loading local BioBERT model...")

# Initialize token classification pipeline
# 'aggregation_strategy="simple"' handles subword stitching automatically
ner_extractor = pipeline(
    task="token-classification",
    model="d4data/biomedical-ner-all",
    aggregation_strategy="simple"
)

# Sample MPharm clinical case notes to experiment with
test_cases = [
    "Patient uses Ventolin two puffs as needed. Reports waking up coughing at night twice a week.",
    "Prescribed Clenil Modulite 100mcg 1 puff BD. Patient experiences mild shortness of breath during exercise.",
    "72yo male taking Salbutamol 100mcg PRN. Peak flow measured at 350 L/min. No nocturnal awakenings."
]

print("\n================ STARTING EXTRACTION TEST ================\n")

for i, note in enumerate(test_cases, 1):
    print(f"--- Case Scenario {i} ---")
    print(f"Input Note: \"{note}\"\n")
    
    # Run model extraction
    entities = ner_extractor(note)
    
    # Format and display extracted entities
    if not entities:
        print("  [!] No entities detected.")
    else:
        for entity in entities:
            word = entity["word"]
            label = entity["entity_group"]
            confidence = entity["score"]
            start, end = entity["start"], entity["end"]
            
            print(f"  • Extracted Span: '{word:<25}' | Entity Category: {label:<20} | Confidence: {confidence:.2f}")
            
    print("-" * 75 + "\n")