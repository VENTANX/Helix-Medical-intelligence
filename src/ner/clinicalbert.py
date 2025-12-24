from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

class NERModel:
    """
    Wrapper for a ClinicalBERT-based NER model.
    """
    def __init__(self, model_name="d4data/biomedical-ner-all"):
        """
        Initializes the NER pipeline.
        We use 'd4data/biomedical-ner-all' as a proxy for a fine-tuned ClinicalBERT 
        since it has good coverage of medical entities out-of-the-box for this demo.
        """
        self.pipeline = pipeline("ner", model=model_name, tokenizer=model_name, aggregation_strategy="simple")

    def extract_entities(self, text):
        """
        Runs NER on the input text and returns structured entities.
        Focuses on Disease, Medication, Dosage.
        """
        results = self.pipeline(text)
        
        # 1. Group entities by aggregation strategy handled by pipeline, 
        # but we need to double check for subword fragmentation if the pipeline didn't merge them perfectly
        # or if we want to enforce specific logic.
        # The 'simple' aggregation strategy in pipeline usually handles B- I- tags.
        # However, "hyper" and "##tension" might still appear if the model isn't predicting B- I- correctly
        # or if it's just raw tokens. 
        # Since we used 'simple' aggregation, 'results' should already be words. 
        # If we are seeing "##tension", it means the tokenizer split it and the model treated them as separate entities 
        # not strongly linked. Let's merge manually.
        
        merged_entities = []
        current_entity = None
        
        for entity in results:
            word = entity['word']
            label = entity['entity_group']
            score = float(entity['score'])
            start = entity['start']
            end = entity['end']
            
            # Normalize Label
            normalized_label = label
            if label in ['DIAGNOSTIC_PROCEDURE', 'DISEASE_DISORDER', 'Sign_symptom']:
                normalized_label = 'Target: Disease'
            elif label in ['MEDICATION', 'Medication']:
                normalized_label = 'Target: Medication'
            elif label in ['DOSAGE', 'Dosage']:
                normalized_label = 'Target: Dosage'
            
            # Filter non-targets
            if "Target:" not in normalized_label:
                continue
                
            # Filter generic words that pollute the dashboard
            clean_word_check = word.lower().strip(".,;:!?")
            if clean_word_check in ['symptoms', 'diagnosis', 'history', 'plan', 'medications', 'date', 'id']:
                continue
                
            # Merge Logic
            if current_entity and (start == current_entity['end'] or word.startswith("##")):
                # Merge with previous
                clean_word = word.replace("##", "")
                current_entity['entity'] += clean_word
                current_entity['end'] = end
                # Average score (simple approx)
                current_entity['score'] = (current_entity['score'] + score) / 2
            else:
                # Discard orphan subwords (e.g. starting with ## but no current_entity)
                if word.startswith("##"):
                    continue

                # Append previous if exists
                if current_entity:
                    merged_entities.append(current_entity)
                
                # Start new
                current_entity = {
                    "entity": word,
                    "label": normalized_label,
                    "score": score,
                    "start": start,
                    "end": end
                }
        
        # Append last
        if current_entity:
            merged_entities.append(current_entity)
            
        return merged_entities

if __name__ == "__main__":
    # Test the model
    model = NERModel()
    text = "Patient has hypertension and is taking Lisinopril 10 mg."
    print(model.extract_entities(text))
