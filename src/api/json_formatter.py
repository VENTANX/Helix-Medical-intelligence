import json

def format_ner_output(data):
    """
    Formats the raw inference output for display.
    """
    formatted_output = {
        "timestamp": data.get("timestamp"),
        "text": data.get("original_text_masked"),
        "entities": []
    }
    
    for entity in data.get("entities", []):
        formatted_output["entities"].append({
            "Label": entity["label"],
            "Text": entity["entity"],
            "Confidence": f"{entity['score']:.2%}"
        })
        
    return formatted_output
