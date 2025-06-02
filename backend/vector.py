from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Paths
pdf_dir = "./grosafe_kb_pdfs"
db_location = "./chroma_langchain_db"

# Embeddings
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Flag to determine whether to ingest documents
add_documents = not os.path.exists(db_location)

# Only ingest if DB folder doesn't exist
if add_documents:
    documents = []
    doc_id = 0

    # Split PDFs into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=384, chunk_overlap=64)

    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_dir, filename))
            chunks = text_splitter.split_documents(loader.load())

            for i, chunk in enumerate(chunks):
                content = chunk.page_content.strip()
                metadata = {
                    "source": filename,
                    "chunk_index": i,
                    "page_number": chunk.metadata.get("page", "unknown"),
                    "preview": content[:100]  # Optional: helpful for debugging
                }

                documents.append(Document(
                    page_content=content,
                    metadata=metadata,
                    id=str(doc_id)
                ))
                doc_id += 1

# Initialize the vector store
vector_store = Chroma(
    collection_name="agency_documents",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add documents to vector store if required
if add_documents:
    vector_store.add_documents(documents)
    print(f"vector.py: Added {len(documents)} documents to the new vector store.")

# Create retriever with top-k filtering (optionally use MMR)
retriever = vector_store.as_retriever(search_kwargs={"k": 6})
