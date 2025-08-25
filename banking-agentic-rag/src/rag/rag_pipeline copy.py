# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import CrossEncoderReranker
# from sentence_transformers import CrossEncoder
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.memory import ConversationBufferMemory
# from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
# from langchain.cache import InMemoryCache
# from langchain_community.retrievers import BM25Retriever
# from typing import Optional, Dict
# from utils.config.llm_config import getLLM

# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# class RAGPipeline:
#     _instance = None
#     def __init__(self, data_path: str = "banking-agentic-rag/src/data/", chunk_size: int = 500, chunk_overlap: int = 50,
#                  vector_k: int = 10, bm25_k: int = 10, hybrid_weights: tuple = (0.6, 0.4),
#                  reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", reranker_top_n: int = 5):

#         if RAGPipeline._instance is not None:
#             self.vectorstore = RAGPipeline._instance.vectorstore
#             self.chain = RAGPipeline._instance.chain
#             self.docs = RAGPipeline._instance.docs
#             self.chunks = RAGPipeline._instance.chunks
#             self.lmm = RAGPipeline._instance.llm
#             self.conversational_rag = RAGPipeline._instance.conversational_rag
#             return



#         # Load & chunk docs
#         self.docs = self.load_documents(data_path)
#         self.chunks = self.chunk_documents(self.docs, chunk_size, chunk_overlap)

#         # VectorStore
#         self.vectorstore = self.create_vectorstore(self.chunks)
#         self.vector_k = vector_k
#         self.vector_retriever = self.create_vector_retriever(self.vectorstore, vector_k)

#         # BM25 retriever
#         self.bm25_retriever = self.create_bm25_retriever(self.chunks, bm25_k)

#         # Hybrid retriever
#         self.hybrid_retriever = EnsembleRetriever(
#             retrievers=[self.vector_retriever, self.bm25_retriever],
#             weights=hybrid_weights
#         )

#         # Re-ranker + Compression

#         model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
#         self.reranker = CrossEncoderReranker(model=model, top_n=10)     

#         # Pass to the reranker
#         # reranker = CrossEncoderReranker(model=lc_cross_encoder, top_n=5)
#         self.compression_retriever = ContextualCompressionRetriever(
#             base_compressor=self.reranker,
#             base_retriever=self.hybrid_retriever
#         )

        

#         # Conversation memory
#         self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#         # LLM
#         self.llm =  getLLM()

#         # In-memory cache
#         self.cache = InMemoryCache()

#         # Conversational RAG chain with caching
#         self.conversational_rag = ConversationalRetrievalChain.from_llm(
#             llm=self.llm,
#             retriever=self.compression_retriever,
#             memory=self.memory,
#             return_source_documents=False,
#             output_key="answer" 
#         )
#         # self.conversational_rag.cache = self.cache  # <-- Add caching here

#     # ---------------- Document Loading & Metadata ----------------
#     @staticmethod
#     def load_documents(path: str):
#         print(os.listdir("banking-agentic-rag/src/data")) 
#         loader = DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader)
#         docs = loader.load()
#         for doc in docs:
#             fname = doc.metadata.get("source", "").lower()
#             if "policy" in fname:
#                 doc.metadata["doc_type"] = "Policy"
#             elif "transaction" in fname:
#                 doc.metadata["doc_type"] = "Transaction"
#             elif "fee" in fname:
#                 doc.metadata["doc_type"] = "Fee"
#             elif "complaint" in fname or "dispute" in fname:
#                 doc.metadata["doc_type"] = "Complaint"
#             else:
#                 doc.metadata["doc_type"] = "General"
#         return docs

#     @staticmethod
#     def chunk_documents(docs, chunk_size: int, chunk_overlap: int):
#         splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#         return splitter.split_documents(docs)

#     @staticmethod
#     def create_vectorstore(chunks):
#         embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,)
#         return FAISS.from_documents(chunks, embeddings)

#     def create_vector_retriever(self, vectorstore, k: int):
#         return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

#     @staticmethod
#     def create_bm25_retriever(chunks, k: int):
#         bm25 = BM25Retriever.from_documents(chunks)
#         bm25.k = k
#         return bm25

#     # ---------------- Query ----------------
#     def query(self, user_query: str, filter_metadata: Optional[Dict[str, str]] = None):
#         # Apply filter to vector retriever dynamically
#         if filter_metadata:
#             self.vector_retriever.search_kwargs["filter"] = filter_metadata
#         result = self.conversational_rag.invoke({"question": user_query})
#         return result




# # query1 = "Where is the Eiffel Tower?"
# # print("Answer 1:", result1["answer"])
    
# # query = "Explain the process of opening a savings account"
# # rag_pipe = RAGPipeline()
# # result = rag_pipe.query("What documents are required for a savings account?")
# # print("Answer:\n", result["answer"])