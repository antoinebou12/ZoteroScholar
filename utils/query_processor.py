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
            qdrant_host = os.getenv('QDRANT_HOST', 'localhost')
            qdrant_port = int(os.getenv('QDRANT_PORT', '6333'))
            qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
            qdrant = Qdrant(
                client=qdrant_client,
                collection_name=self.collection_name,
                embeddings=GPT4AllEmbeddings(),
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
        ollama_host = os.getenv('OLLAMA_HOST', 'localhost')
        ollama_port = int(os.getenv('OLLAMA_PORT', '11434'))
        model = ChatOllama(
            model=self.model_name,
            base_url=f"http://{ollama_host}:{ollama_port}",
        )
        prompt = ChatPromptTemplate.from_template(template)
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
