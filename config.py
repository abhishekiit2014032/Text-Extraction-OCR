import os
from dotenv import load_dotenv

load_dotenv()

# Azure Document Intelligence config
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")
AZURE_KEY = os.getenv("AZURE_KEY", "")

# Google Generative AI config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Application config
IMAGE_DIR = os.getenv("IMAGE_DIR", "images/")
OUTPUT_FILE = "output.csv"
COMPARISON_FILE = "comparison_report.csv"
