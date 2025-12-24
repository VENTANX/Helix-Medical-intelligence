import re

class PHIRemover:
    """
    A class to remove Protected Health Information (PHI) from clinical text
    using regular expressions to simulate HIPAA compliance.
    """
    
    def __init__(self):
        # Compiled regex patterns for performance
        self.date_pattern = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b')
        # Matches capitalized words following Dr. or Mr./Ms./Mrs. 
        # This is a heuristic and might miss some names or over-capture, but suitable for simulation.
        self.name_pattern = re.compile(r'(?<=Dr\.\s)[A-Z][a-z]+|(?<=Mr\.\s)[A-Z][a-z]+|(?<=Ms\.\s)[A-Z][a-z]+|(?<=Mrs\.\s)[A-Z][a-z]+|(?<=Patient\s)[A-Z][a-z]+ [A-Z][a-z]+') 
        # Also try to catch names at start of sentences if they look like names (simple heuristic)
        # For this simulation, we'll stick to the specific context provided in the generator to be safer
        
        # ID pattern: Simple 5 digit number as generated in producer
        self.id_pattern = re.compile(r'\b\d{5}\b')
        # Specific pattern for "ID: <num>. <Name>" which was missed
        self.id_name_pattern = re.compile(r'ID:\s*\d+\.\s+([A-Z][a-z]+(\s[A-Z][a-z]+)?)')

    def deidentify(self, text):
        """
        Replaces PHI in the text with placeholder tags.
        """
        cleaned_text = text
        
        # Patch for "ID: 12345. Name ..." pattern
        # Must run BEFORE ID replacement because it relies on the number being present
        cleaned_text = self.id_name_pattern.sub(lambda m: m.group(0).replace(m.group(1), '[NAME]'), cleaned_text)

        # Replace Dates
        cleaned_text = self.date_pattern.sub('[DATE]', cleaned_text)
        
        # Replace IDs
        cleaned_text = self.id_pattern.sub('[ID]', cleaned_text)
        
        # Replace Names
        # Note: Name replacement is tricky with regex alone.
        # We'll use a slightly broader pattern for the simulation based on our generator's structure.
        # Capturing "Patient X" or "Dr. Y"
        
        # Specific replacements based on known prefixes in our synthetic data
        cleaned_text = re.sub(r'(?<=Patient\s)([A-Z][a-z]+(\s[A-Z][a-z]+)?)', '[NAME]', cleaned_text)
        cleaned_text = re.sub(r'(?<=Dr\.\s)([A-Z][a-z]+)', '[NAME]', cleaned_text)
        cleaned_text = re.sub(r'(?<=for\s)([A-Z][a-z]+(\s[A-Z][a-z]+)?)', '[NAME]', cleaned_text) # "Discharge summary for X"
        cleaned_text = re.sub(r'(?<=evaluated\s)([A-Z][a-z]+(\s[A-Z][a-z]+)?)', '[NAME]', cleaned_text) # "evaluated X"

        return cleaned_text

# Example usage for testing
if __name__ == "__main__":
    remover = PHIRemover()
    sample = "Patient John Doe seen on 12/05/2023. ID: 12345."
    print(f"Original: {sample}")
    print(f"Cleaned:  {remover.deidentify(sample)}")
