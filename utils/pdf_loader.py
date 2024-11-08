import logging
import os
from typing import List

from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

class PDFLoader:
    def __init__(self, dirpath: str):
        self.dirpath = dirpath

    def load_pdfs(self) -> List[str]:
        all_papers = []
        for root, _, files in os.walk(self.dirpath):
            for filename in files:
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, filename)
                    try:
                        reader = PdfReader(pdf_path)
                        text_pages = []
                        for page in reader.pages:
                            text = page.extract_text()
                            if text:
                                text_pages.append(text)
                        if text_pages:
                            all_papers.append(' '.join(text_pages))
                            logger.info(f"Loaded {filename} successfully.")
                        else:
                            logger.warning(f"No text found in {filename}.")
                    except Exception as e:
                        logger.error(f"Error loading {filename}: {e}")
                        # Optionally, continue to the next file or re-raise the exception
                        continue
        if not all_papers:
            logger.error("No papers were loaded. Check if the directory contains valid PDF files.")
            raise FileNotFoundError("No valid PDFs found in the directory.")
        return all_papers
