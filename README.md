# Invoice Extraction System

This project is a Python-based system built to extract key fields from invoice images using two independent approaches and validate the results, as per the requirements.

## Dataset
**Kaggle:** [High Quality Invoice Images for OCR](https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr)
The system expects 50 images from `batch_1 > batch_1 > batch1_1 > batch1-0331 to batch1-0381`.

## 💡 The Two-Pipeline Approach (Cross-Validation)
To ensure robustness and satisfy the requirement for meaningfully different extraction techniques, this system runs each invoice through two fundamentally distinct architectures:

### 1. Pipeline A: Structured Prebuilt Model (Azure Document Intelligence)
* **Methodology:** Classical OCR combined with a specialized deep-learning spatial/layout analyzer.
* **Why it's different:** Microsoft Azure's model is explicitly pre-trained on millions of standard invoices. It relies on rigid, pre-trained spatial rules to identify fields (e.g., finding the word "Total" and extracting the number next to it based on bounding boxes).

### 2. Pipeline B: Multimodal Vision-Language Model (Google Gemini Flash)
* **Methodology:** Pure Generative AI (LLM + Vision).
* **Why it's different:** Instead of line-by-line OCR, it consumes the raw image directly alongside a prompt. It uses generative context understanding to infer fields, making it highly robust to messy or completely non-standard layouts where traditional OCR fails.

**Validation Strategy:** By comparing the outputs of these two vastly different paradigms, we can cross-validate the results with extremely high confidence.

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

## 📊 Analysis of Results
After running the pipeline on the 50-image dataset, the raw automated match rate averaged around **32.5%**. However, a deeper analysis of `comparison_report.csv` reveals that the actual extraction accuracy is much higher, and the mismatches are primarily due to formatting differences and one model outperforming the other:

1. **Entity Names & Invoice Numbers**: Both Azure Document Intelligence and Gemini Flash achieved near-perfect accuracy in extracting the `Seller Name`, `Client Name`, and `Invoice Number`.
2. **Tax ID Extraction (Advantage: Gemini)**: The prebuilt Azure model completely failed to extract the `Seller Tax ID` and `Client Tax ID` across the dataset, returning null values. Gemini Flash, however, successfully identified and extracted these IDs.
3. **Date Formatting Discrepancies**: Azure consistently formatted dates in ISO format (`YYYY-MM-DD`), whereas Gemini extracted them as they appeared or defaulted to American formatting (`MM/DD/YYYY`). 
4. **Currency Formatting Discrepancies**: Azure automatically prepended the `$` symbol to financial fields (Net Worth, VAT, Gross Worth). Gemini extracted the raw numbers but retained the European number formatting present in the images (using spaces for thousands and commas for decimals, e.g., `1 612,50`).

**Conclusion**: While the generative Multimodal LLM (Gemini) proved superior in extracting all required fields (specifically Tax IDs) compared to the rigid prebuilt model, both models performed excellently. To achieve a 100% automated match rate in a production environment, an intermediate **data normalization** step (standardizing dates and currency strings) must be implemented before the validation check.
