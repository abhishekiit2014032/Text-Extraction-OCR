# Invoice Extraction System

This project is a Python-based system built to extract key fields from invoice images using two independent approaches and validate the results, as per the requirements.

## Dataset
**Kaggle:** [High Quality Invoice Images for OCR](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr)
The system expects 50 images from `batch_1 > batch_1 > batch1_1 > batch1-0331 to batch1-0381`.

## Approach
This system implements two distinct and modern approaches:
1. **Pipeline A (Prebuilt Structured Model): Azure AI Document Intelligence** 
   Uses Microsoft's prebuilt invoice extraction model which employs OCR combined with a robust deep learning structured extraction layer.
2. **Pipeline B (Multimodal LLM): Google Gemini 1.5 Flash API** 
   A state-of-the-art vision-language model approach, which consumes the raw image directly and returns structured JSON using instructions provided in the prompt.

### Extracted Fields
- Seller Name
- Seller Tax ID
- Client Name
- Client Tax ID
- Invoice Number
- Invoice Date
- Net Worth
- VAT
- Gross Worth

## Setup & Installation

1. **Clone/Navigate** to the project folder.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
   *Required Keys:*
   - `AZURE_ENDPOINT`: Your Azure AI Document Intelligence endpoint.
   - `AZURE_KEY`: Your Azure Document Intelligence access key.
   - `GEMINI_API_KEY`: Your Google Gemini API key (can be generated in Google AI Studio).

4. **Prepare Dataset:**
   Download the Kaggle dataset. Extract the specific 50 images (`batch1-0331` to `batch1-0381`) and place them in the `./images/` directory (or update `IMAGE_DIR` in `.env`).

## Running the Pipeline

Execute the main orchestrator script:
```bash
python main.py
```

## Deliverables Generated
- `output.csv`: The final extracted fields from both pipelines for all images.
- `comparison_report.csv`: A detailed comparison report mapping the fields side-by-side between Pipeline A and Pipeline B, along with match validation flags and a match rate metric.
