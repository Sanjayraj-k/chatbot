import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
import os
from PyPDF2 import PdfReader

llm = ChatGroq(model="llama3-8b-8192")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = Chroma(embedding_function=embeddings)

def load_texts(text_folder: str):
    documents = []
    for filename in os.listdir(text_folder):
        file_path = os.path.join(text_folder, filename)

        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                documents.append(Document(page_content=text, metadata={"source": filename}))

        elif filename.endswith(".pdf"):
            pdf_reader = PdfReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            documents.append(Document(page_content=text, metadata={"source": filename}))

    if not documents:
        raise ValueError(f"No documents found in the folder: {text_folder}")
    return documents


text_folder = "./pa"
docs = load_texts(text_folder)
print(f"Loaded {len(docs)} documents from {text_folder}.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)
if not all_splits:
    raise ValueError("Document splitting failed. Ensure documents contain content.")
print(f"Split into {len(all_splits)} chunks.")

valid_splits = [doc for doc in all_splits if doc.page_content.strip()]
if not valid_splits:
    raise ValueError("No valid document chunks found after splitting.")
_ = vector_store.add_documents(documents=valid_splits)
print("Document chunks added to vector store successfully.")


prompt = hub.pull("rlm/rag-prompt")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

st.title("Chatbot with Langchain and Streamlit")


question = st.text_input("Ask me anything:")

if question:
    try:
        
        response = graph.invoke({"question": question})
        st.write(f"Answer: {response['answer']}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
