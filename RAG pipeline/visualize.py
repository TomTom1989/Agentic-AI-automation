import os
import glob
import numpy as np
from dotenv import load_dotenv
from sklearn.manifold import TSNE
import plotly.graph_objects as go
import plotly.io as pio

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# === CONFIGURATION ===
MODEL = "gpt-4o-mini"
db_name = "vector_db"

# === FORCE PLOTLY TO OPEN IN BROWSER ===
pio.renderers.default = 'browser'

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

# === VISUALIZATION DATA ===
result = vectorstore._collection.get(include=['embeddings', 'documents', 'metadatas'])
vectors = np.array(result['embeddings'])
documents = result['documents']
metadatas = result['metadatas']
doc_types = [metadata['doc_type'] for metadata in metadatas]

unique_doc_types = list(set(doc_types))
color_palette = ['blue', 'green', 'red', 'orange', 'purple', 'gray']
color_map = {doc_type: color_palette[i % len(color_palette)] for i, doc_type in enumerate(unique_doc_types)}
colors = [color_map[t] for t in doc_types]

# === 2D PLOT ===
tsne_2d = TSNE(n_components=2, random_state=42)
reduced_2d = tsne_2d.fit_transform(vectors)
fig2d = go.Figure(data=[go.Scatter(
    x=reduced_2d[:, 0],
    y=reduced_2d[:, 1],
    mode='markers',
    marker=dict(size=5, color=colors, opacity=0.8),
    text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
    hoverinfo='text')])
fig2d.update_layout(title='2D Vector Visualization', width=800, height=600)
fig2d.show()

# === 3D PLOT ===
tsne_3d = TSNE(n_components=3, random_state=42)
reduced_3d = tsne_3d.fit_transform(vectors)
fig3d = go.Figure(data=[go.Scatter3d(
    x=reduced_3d[:, 0],
    y=reduced_3d[:, 1],
    z=reduced_3d[:, 2],
    mode='markers',
    marker=dict(size=5, color=colors, opacity=0.8),
    text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(doc_types, documents)],
    hoverinfo='text')])
fig3d.update_layout(title='3D Vector Visualization', width=900, height=700)
fig3d.show()

# === SAVE VECTORSTORE FOR LATER USE ===
# Chroma persists to disk; no need to export
print("\nChroma vectorstore is ready and visualized.")
