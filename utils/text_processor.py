import logging
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

logger = logging.getLogger(__name__)

class TextProcessor:
    @staticmethod
    def process_text(papers: List[str]) -> str:
        # Since 'papers' is already a list of strings, you can directly join them
        full_text = ' '.join(papers)
        if not full_text.strip():
            logger.error("Extracted text is empty. Possibly due to PDF format issues.")
            raise ValueError("Extracted text is empty, possibly due to PDF format issues.")
        logger.info("Text processed successfully.")
        return full_text

    @staticmethod
    def split_text(full_text: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        paper_chunks = text_splitter.create_documents([full_text])
        if not paper_chunks:
            logger.error("Failed to process text into chunks, possibly due to formatting issues.")
            raise ValueError("Failed to process text into chunks, possibly due to formatting issues.")
        logger.info("Text split into chunks successfully.")
        return paper_chunks
