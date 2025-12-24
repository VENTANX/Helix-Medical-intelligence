
from transformers import pipeline

def test_medication():
    nlp = pipeline("ner", model="d4data/biomedical-ner-all", aggregation_strategy="simple")
    text = "Plan: Start Metformin 500 mg."
    results = nlp(text)
    print("Results for 'Metformin':")
    for r in results:
        print(r)

if __name__ == "__main__":
    test_medication()
