import os
import glob
import numpy as np
from dotenv import load_dotenv
import gradio as gr
from sklearn.manifold import TSNE
import plotly.graph_objects as go

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.callbacks import StdOutCallbackHandler

# === CONFIGURATION ===
MODEL = "gpt-4o-mini"
db_name = "vector_db"

# === LOAD ENV VARS ===
load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')

# === LOAD DOCUMENTS ===
folders = glob.glob("knowledge-base/*")
text_loader_kwargs = {'encoding': 'utf-8'}

documents = []
for folder in folders:
    doc_type = os.path.basename(folder)
    loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    folder_docs = loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
    documents.extend(folder_docs)

# === SPLIT DOCUMENTS ===
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Total chunks: {len(chunks)}")
print(f"Document types: {set(doc.metadata['doc_type'] for doc in documents)}")

# === EMBEDDINGS + VECTORSTORE ===
embeddings = OpenAIEmbeddings()
if os.path.exists(db_name):
    Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
print(f"Vectorstore created with {vectorstore._collection.count()} documents")


# === RAG PIPELINE ===
llm = ChatOpenAI(temperature=0.7, model_name=MODEL)
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 25})
conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory, callbacks=[StdOutCallbackHandler()])



print("\nChat History:")
for msg in memory.chat_memory.messages:
    print(f"{msg.type.upper()}: {msg.content}")

# === GRADIO CHAT ===
def chat(question, history):
    result = conversation_chain.invoke({"question": question})
    return result["answer"]

view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True)
