<img width="1919" height="933" alt="image" src="https://github.com/user-attachments/assets/2dcd8805-d3ad-4852-a8b9-ccb7e1985172" />

# Helix Intelligence: Medical NER & Analytics System
**Architected by Oussama Aslouj**

## 1. The Challenge: Unstructured & Sensitive Clinical Data
In the modern healthcare landscape, over **80% of medical data is unstructured**—locked away in free-text clinical notes, discharge summaries, and doctor's logs. This data contains vital information about patient health, disease patterns, and treatment efficacy, but it faces two major hurdles:
1.  **Privacy (HIPAA/GDPR)**: Clinical notes utilize Personally Identifiable Information (PII/PHI), making them virtually impossible to share or analyze at scale without rigorous de-identification.
2.  **Inaccessibility**: unstructured text cannot be easily queried, graphed, or used for population health analytics.

## 2. The Solution: A Real-Time, Privacy-First Pipeline
**Helix Intelligence** is an end-to-end engineered solution designed to bridge this gap. It simulates a hospital data stream, automatically strips sensitive data, extracts structured medical entities using State-of-the-Art NLP, and visualizes the results in a real-time command center.

### Core Capabilities
- **De-identification at Source**: Uses a custom regex-based engine to scrub names, IDs, and dates *before* the data leaves the secure environment.
- **Deep Medical Understanding**: Leverages **ClinicalBERT**, a transformer model fine-tuned on biomedical text, to identify Diseases, Medications, and Dosages with high precision.
- **Live Intelligence Dashboard**: A futuristic, glassmorphism-styled "Doctor's Workbench" that provides real-time alerts, population health heatmaps, and patient search capabilities.

---

## 3. Technical Architecture
The system is built as a microservices-style pipeline:

### 🏥 A. Data Stream (RabbitMQ)
- **Component**: `src/streaming/rabbitmq_producer.py`
- **Function**: Simulates a hospital Electronic Health Record (EHR) system.
- **Logic**: Generates synthetic clinical notes using a massive vocabulary of **150+ medical conditions and treatments** (Oncology, Cardiology, Psychiatry, etc.) to stress-test the system. Messages are published to a local RabbitMQ queue.

### 🛡️ B. Privacy & Inference Node
- **Component**: `src/ner/inference.py`
- **Function**: The "Brain" of the operation.
- **Workflow**:
    1.  **Ingestion**: Consumes raw notes from RabbitMQ.
    2.  **PHI Scrubbing**: `src/deidentification/phi_removal.py` replaces names (`[NAME]`) and IDs (`[ID]`) to ensure privacy.
    3.  **Entity Extraction**: `src/ner/clinicalbert.py` runs the text through the Hugging Face `d4data/biomedical-ner-all` model. It handles subword token merging (e.g., `##tension`) and filters generic noise (e.g., "symptoms").
    4.  **Storage**: Appends structured JSON results to `data/processed_notes.jsonl`.

### 💻 C. Helix Dashboard (Streamlit)
- **Component**: `src/dashboard/app.py`
- **Function**: The User Interface.
- **Features**:
    - **Ops Center**: Live feed of incoming notes with color-coded entity badges.
    - **Intel Core**: Real-time analytics including **Treatment Correlation Heatmaps** and **Patient Velocity Trends**.
    - **Visuals**: "Ultra-Premium" dark UI with glassmorphism, floating particles, and FontAwesome icons.

---

## 4. Installation & Usage

### Prerequisites
- Python 3.8+
- RabbitMQ Server (Running locally)
- Dependencies: `pip install transformers torch streamlit pika faker pandas altair`

### System Launch Sequence
Open 3 separate terminal windows to spin up the grid:

**Terminal 1: The Pulse (Data Generator)**
```bash
python src/streaming/rabbitmq_producer.py
```

**Terminal 2: The Brain (Inference Engine)**
```bash
python src/ner/inference.py
```

**Terminal 3: The View (Dashboard)**
```bash
streamlit run src/dashboard/app.py
```

---

## 5. Credits
**Architect & Lead Developer**: Oussama Aslouj
*Built with Python, Hugging Face Transformers, and Streamlit.*
