from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, image_path: str) -> Dict[str, Any]:
        """
        Extract fields from an invoice image.
        Returns a dictionary with the required fields:
        - Seller Name
        - Seller Tax ID
        - Client Name
        - Client Tax ID
        - Invoice Number
        - Invoice Date
        - Net Worth
        - VAT
        - Gross Worth
        """
        pass
