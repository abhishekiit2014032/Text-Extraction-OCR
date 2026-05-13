from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from .base import BaseExtractor
import config

class AzureExtractor(BaseExtractor):
    def __init__(self):
        if not config.AZURE_ENDPOINT or not config.AZURE_KEY:
            raise ValueError("Azure credentials not provided in .env (AZURE_ENDPOINT, AZURE_KEY).")
        self.client = DocumentAnalysisClient(
            endpoint=config.AZURE_ENDPOINT, 
            credential=AzureKeyCredential(config.AZURE_KEY)
        )

    def extract(self, image_path: str) -> dict:
        result = {
            "Seller Name": None,
            "Seller Tax ID": None,
            "Client Name": None,
            "Client Tax ID": None,
            "Invoice Number": None,
            "Invoice Date": None,
            "Net Worth": None,
            "VAT": None,
            "Gross Worth": None
        }
        
        try:
            with open(image_path, "rb") as f:
                poller = self.client.begin_analyze_document(
                    "prebuilt-invoice", document=f
                )
            
            invoices = poller.result()
            
            if invoices.documents:
                doc = invoices.documents[0]
                fields = doc.fields
                
                def get_val(key):
                    field = fields.get(key)
                    if field:
                        return str(field.value) if field.value is not None else field.content
                    return None

                result["Seller Name"] = get_val("VendorName")
                result["Seller Tax ID"] = get_val("VendorTaxId")
                result["Client Name"] = get_val("CustomerName")
                result["Client Tax ID"] = get_val("CustomerTaxId")
                result["Invoice Number"] = get_val("InvoiceId")
                
                # Handling date specially
                date_val = get_val("InvoiceDate")
                result["Invoice Date"] = str(date_val) if date_val else None
                
                # Financials
                result["Net Worth"] = get_val("SubTotal")
                result["VAT"] = get_val("TotalTax")
                result["Gross Worth"] = get_val("InvoiceTotal")
                
        except Exception as e:
            print(f"Azure Extraction Error for {image_path}: {e}")

        return result
