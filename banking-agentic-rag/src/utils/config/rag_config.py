# rag_config.py
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.retrievers import BM25Retriever
from .llm_config import LLMConfig
from .memory_config import MemoryConfig
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class RAGConfig:
    _docs = None
    _chunks = None
    _vectorstore = None
    _vector_retriever = None
    _bm25_retriever = None
    _hybrid_retriever = None
    _compression_retriever = None
    _llm = None
    _conversational_rag = None

    @staticmethod
    def load_documents(path: str = "banking-agentic-rag/src/data/"):
        if RAGConfig._docs is None:
            loader = DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader)
            docs = loader.load()
            for doc in docs:
                fname = doc.metadata.get("source", "").lower()
                if "policy" in fname:
                    doc.metadata["doc_type"] = "Policy"
                elif "transaction" in fname:
                    doc.metadata["doc_type"] = "Transaction"
                elif "fee" in fname:
                    doc.metadata["doc_type"] = "Fee"
                elif "complaint" in fname or "dispute" in fname:
                    doc.metadata["doc_type"] = "Complaint"
                else:
                    doc.metadata["doc_type"] = "General"
            RAGConfig._docs = docs
            # print(f"{RAGConfig._docs}..._docs")
        return RAGConfig._docs

    @staticmethod
    def chunk_documents(chunk_size: int = 500, chunk_overlap: int = 50):
        if RAGConfig._chunks is None:
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            RAGConfig._chunks = splitter.split_documents(RAGConfig.load_documents())
            # print(f"{RAGConfig._chunks}...chunkjs")
        return RAGConfig._chunks

    @staticmethod
    def create_vectorstore():
        if RAGConfig._vectorstore is None:
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            RAGConfig._vectorstore = FAISS.from_documents(RAGConfig.chunk_documents(), embeddings)
        return RAGConfig._vectorstore

    @staticmethod
    def get_vector_retriever(k: int = 10):
        if RAGConfig._vector_retriever is None:
            RAGConfig._vector_retriever = RAGConfig.create_vectorstore().as_retriever(
                search_type="similarity", search_kwargs={"k": k}
            )
        return RAGConfig._vector_retriever

    @staticmethod
    def get_bm25_retriever(k: int = 10):
        try:
            if RAGConfig._bm25_retriever is None:
                bm25 = BM25Retriever.from_documents(RAGConfig.chunk_documents())
                bm25.k = k
                RAGConfig._bm25_retriever = bm25
            return RAGConfig._bm25_retriever
        except Exception as e:
            print(f"{e}...get_bm25_retriever")
    

    @staticmethod
    def get_hybrid_retriever(weights: tuple = (0.6, 0.4)):
        try:
            if RAGConfig._hybrid_retriever is None:
                RAGConfig._hybrid_retriever = EnsembleRetriever(
                    retrievers=[RAGConfig.get_vector_retriever(), RAGConfig.get_bm25_retriever()],
                    weights=weights
                )
            return RAGConfig._hybrid_retriever
        except Exception as e:
            print(f"{e}...get_hybrid_retriever")

    @staticmethod
    def get_compression_retriever():
        try:
            if RAGConfig._compression_retriever is None:
                model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
                reranker = CrossEncoderReranker(model=model, top_n=10)
                RAGConfig._compression_retriever = ContextualCompressionRetriever(
                    base_compressor=reranker,
                    base_retriever=RAGConfig.get_hybrid_retriever()
                )
            # print(f"{RAGConfig._compression_retriever}...get_compression_retriever")
            return RAGConfig._compression_retriever
        except Exception as e:
            print(f"{e}...get_compression_retriever")

    @staticmethod
    def get_llm():
        if RAGConfig._llm is None:
            RAGConfig._llm = LLMConfig.getLLM()
            print(f"{RAGConfig._llm}")
        return RAGConfig._llm

    @staticmethod
    def get_conversational_rag():
        print("inside conversational RAG")
        if RAGConfig._conversational_rag is None:
            # 1️⃣ System message template
            system_message = SystemMessagePromptTemplate.from_template("""
    You are a Banking Triage Assistant.
    Answer the user's question using ONLY the retrieved context.
    Do NOT add extra information, disclaimers, or unrelated content.
            """)

            # 2️⃣ Human message template
            human_message = HumanMessagePromptTemplate.from_template("""
    Context: {context}
    User question: {question}
            """)

            # 3️⃣ Combine into a ChatPromptTemplate
            prompt = ChatPromptTemplate.from_messages([system_message, human_message])

            RAGConfig._conversational_rag = ConversationalRetrievalChain.from_llm(
                llm=LLMConfig.getLLM(),
                retriever=RAGConfig.get_compression_retriever(),
                memory=MemoryConfig.get_memory(),
                return_source_documents=False,
                output_key="answer",
                combine_docs_chain_kwargs={"prompt": prompt} 
            )

        return RAGConfig._conversational_rag

