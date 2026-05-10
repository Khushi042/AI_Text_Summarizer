from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import PyPDF2

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

qa_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Load model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# Request models
class TextRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

vector_store = None

def split_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

@app.get("/")
def home():
    return {"message": "API is running"}


#  TEXT SUMMARIZATION
@app.post("/summarize")
def summarize_text(request: TextRequest):
    try:
        chunks = split_text(request.text)
        summaries = []

        for chunk in chunks:
            result = summarizer(
                "Summarize this in a concise and original way: " + chunk,
                max_length=90,
                min_length=25,
                do_sample=True,
                temperature=0.8,
                top_p=0.95,
                repetition_penalty=1.2
            )
            summaries.append(result[0]["summary_text"])

        return {"summary": " ".join(summaries)}

    except Exception as e:
        return {"error": str(e)}


#  PDF SUMMARIZATION
@app.post("/summarize-pdf")
def summarize_pdf(file: UploadFile = File(...)):
    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""

        for page in pdf_reader.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + " "

        
        if not text.strip():
            return {"error": "No readable text found in PDF"}

        chunks = split_text(text)

        
        if len(chunks) == 0:
            return {"error": "Could not split PDF text properly"}

        summaries = []

        for chunk in chunks:

            
            if len(chunk.split()) < 20:
                continue

            result = summarizer(
                "Summarize this in a concise and original way: " + chunk,
                max_length=90,
                min_length=25,
                do_sample=True,
                temperature=0.8,
                top_p=0.95,
                repetition_penalty=1.2
            )

            summaries.append(result[0]["summary_text"])

        
        if len(summaries) == 0:
            return {"error": "PDF content too small to summarize"}

        return {"summary": " ".join(summaries)}

    except Exception as e:
        return {"error": str(e)}



@app.post("/upload-pdf-chat")
def upload_pdf_chat(file: UploadFile = File(...)):
    global vector_store

    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            return {"error": "No readable text found"}

        texts = split_text(text)
        
        embeddings = HuggingFaceEmbeddings()
        
        vector_store = FAISS.from_texts(texts, embeddings)

        return {"message": "PDF ready for chat"}

    except Exception as e:
        return {"error": str(e)}


#  Ask questions from PDF
@app.post("/ask")
def ask_question(request: QueryRequest):
    global vector_store

    try:
        if vector_store is None:
            return {"error": "Upload a PDF first"}

        docs = vector_store.similarity_search(request.query, k=3)
        
        context = docs[0].page_content[:1000]

        result = qa_model(
            f"""
Answer the question clearly and concisely using ONLY the given context.

Context:
{context}

Question:
{request.query}

Answer:
""",
            max_length=120
        )

        return {"answer": result[0]["generated_text"]}

    except Exception as e:
        return {"error": str(e)}