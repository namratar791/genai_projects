# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever, CachedRetriever
# from langchain_community.cross_encoders import CrossEncoderReranker
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain.storage import InMemoryStore
# from utils.config.llm_configimport getLLM
# from langchain_community.retrievers import BM25Retriever
# # 1. Load multiple text files
# loader = DirectoryLoader("data/", glob="*.txt", loader_cls=TextLoader)
# docs = loader.load()

# # 2. Chunking
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# chunks = splitter.split_documents(docs)

# # 3. Vector store
# embeddings = OpenAIEmbeddings()
# vectorstore = FAISS.from_documents(chunks, embeddings)
# vector_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":10})

# # 4. Keyword retriever (BM25)
# bm25_retriever = BM25Retriever.from_documents(chunks)
# bm25_retriever.k = 10

# # 5. Hybrid retriever
# hybrid_retriever = EnsembleRetriever(
#     retrievers=[vector_retriever, bm25_retriever],
#     weights=[0.6,0.4]
# )

# # 6. Re-ranker
# reranker = CrossEncoderReranker(model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=5)

# # 7. Compression retriever
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=reranker,
#     base_retriever=hybrid_retriever
# )

# # 8. Caching
# cache_store = InMemoryStore()
# cached_retriever = CachedRetriever(compression_retriever, storage=cache_store)

# # 9. Conversation memory for multi-agent session
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# # 10. LLM
# llm =getLLM()

# conversational_rag = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=cached_retriever,
#         memory=memory,
#         return_source_documents=True
#     )

# # 11. Conversational RAG Chain
# def getConversationalRag(user_query: str):
#     result = conversational_rag.invoke({"question": user_query})
#     return result



# # 🔍 Example Query
# # query1 = "What is the process for disputing a credit card charge?"
# # result1 = conversational_rag.invoke({"question": query1})
# # print(result1["answer"])

# # # Next turn, multi-agent can still access previous context
# # query2 = "And what are the associated fees?"
# # result2 = conversational_rag.invoke({"question": query2})
# # print(result2["answer"])


