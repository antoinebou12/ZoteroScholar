import logging
from typing import List

from langchain.vectorstores import Qdrant
from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain.embeddings import GPT4AllEmbeddings
from langchain.schema import Document

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Question(BaseModel):
    __root__: str

class QueryProcessor:
    def __init__(
        self,
        paper_chunks: List[Document],
        question_text: str,
        qdrant_path: str = "./tmp/local_qdrant",
        collection_name: str = "zotero_papers",
        model_name: str = "llama2:7b-chat",
    ):
        self.paper_chunks = paper_chunks
        self.question_text = question_text
        self.qdrant_path = qdrant_path
        self.collection_name = collection_name
        self.model_name = model_name
        self.qdrant = self._create_vector_store()
        self.chain = self._build_chain()

    def _create_vector_store(self) -> Qdrant:
        try:
            qdrant = Qdrant.from_documents(
                documents=self.paper_chunks,
                embedding=GPT4AllEmbeddings(),
                path=self.qdrant_path,
                collection_name=self.collection_name,
            )
            logger.info("Qdrant vector store created successfully.")
            return qdrant
        except Exception as e:
            logger.error(f"Error creating Qdrant vector store: {e}")
            raise

    def _build_chain(self):
        retriever = self.qdrant.as_retriever()
        template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
        prompt = ChatPromptTemplate.from_template(template)
        model = ChatOllama(model=self.model_name)
        chain = (
            RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
            | prompt
            | model
            | StrOutputParser()
        ).with_types(input_type=Question)
        logger.info("Chain built successfully.")
        return chain

    def process_query(self) -> str:
        try:
            result = self.chain.invoke(self.question_text)
            return result
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"Failed to process query: {e}"
