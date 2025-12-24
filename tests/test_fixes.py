
import sys
import os
import unittest

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.deidentification.phi_removal import PHIRemover
from src.ner.clinicalbert import NERModel

class TestFixes(unittest.TestCase):
    def test_deid_name_pattern(self):
        remover = PHIRemover()
        # The specific pattern that was failing based on producer template:
        # "ID: 12345. Tyler Benson complains of..."
        text = "ID: 12345. Tyler Benson complains of worsening asthma."
        cleaned = remover.deidentify(text)
        print(f"Original: {text}")
        print(f"Cleaned:  {cleaned}")
        
        self.assertIn("[NAME]", cleaned)
        self.assertNotIn("Tyler Benson", cleaned)
        self.assertIn("[ID]", cleaned)
        
    def test_ner_subword_merging(self):
        # We can't easily force the model to split "hypertension" without knowing the specific tokenizer behavior 
        # that caused it, but we can test the logic if we mock the output or just test with a known word.
        # However, to be integration test style, let's try the word 'hypertension' and 'cardiovascular'.
        
        model = NERModel()
        # Mocking the pipeline output to simulate split tokens if the real model behaves perfectly on this input
        # This ensures our Logic works regardless of the model doing it or not.
        
        # Manually invoke merge logic by passing a "fake" pipeline result if we were unit testing the function 
        # but here we are testing the wrapper. 
        # Let's trust the integration test first. 
        
        text = "Patient has hypertension."
        entities = model.extract_entities(text)
        print("Entities found:", entities)
        
        # Check if we have one entity 'hypertension' (or similar) and not broken ones
        # If the model splits it, our code should join it.
        # If the model doesn't split it, this test passes trivially but doesn't prove the fix.
        # Let's try to inject a manual split test case.
        
        # We will subclass to mock just for this test
        class MockNER(NERModel):
            def __init__(self):
                pass 
                
        mock_ner = MockNER()
        mock_results = [
            {'entity_group': 'DISEASE_DISORDER', 'score': 0.99, 'word': 'hyper', 'start': 12, 'end': 17},
            {'entity_group': 'DISEASE_DISORDER', 'score': 0.98, 'word': '##tension', 'start': 17, 'end': 24}
        ]
        
        # We need to copy the extract_entities method or bind it. 
        # Actually easier to just call the method on the real object but mock the pipeline.
        model.pipeline = lambda x: mock_results
        
        merged = model.extract_entities("Patient has hypertension.")
        print("Merged Entities:", merged)
        
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]['entity'], 'hypertension')
        self.assertEqual(merged[0]['label'], 'Target: Disease')

if __name__ == '__main__':
    unittest.main()
