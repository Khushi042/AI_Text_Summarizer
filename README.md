# 🧠 IntelliSummary AI

An AI-powered text and PDF summarization web application built using FastAPI, React, and Hugging Face Transformers.

The application allows users to:
- Summarize large blocks of text
- Upload and summarize PDF documents
- Ask questions from uploaded PDFs using a basic RAG (Retrieval-Augmented Generation) pipeline

---

# 🚀 Features

## ✅ Text Summarization
Users can paste long text and generate concise summaries instantly.

## ✅ PDF Summarization
Users can upload PDF files and receive summarized content extracted from the document.

## ✅ AI Question Answering (RAG)
Users can upload PDFs and ask questions based on document content.

## ✅ Modern Frontend UI
Built with React and custom CSS for a clean and responsive interface.

---

# 🛠️ Tech Stack

## Frontend
- React.js
- HTML
- CSS
- JavaScript

## Backend
- FastAPI
- Python

## AI / NLP
- Hugging Face Transformers
- Facebook BART Large CNN
- Google FLAN-T5
- FAISS Vector Store
- Sentence Transformers

---

# 📂 Project Structure

```bash
Project4/
│
├── backend/
│   ├── main.py
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
```

---

## 2️⃣ Backend Setup

Navigate to backend folder:

```bash
cd backend
```

Install dependencies:

```bash
pip install fastapi uvicorn transformers torch PyPDF2 langchain-community sentence-transformers faiss-cpu python-multipart
```

Run backend server:

```bash
uvicorn main:app --reload
```

Backend runs at:

```bash
http://127.0.0.1:8000
```

---

## 3️⃣ Frontend Setup

Navigate to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start React app:

```bash
npm start
```

Frontend runs at:

```bash
http://localhost:3000
```

---

# 🧪 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/summarize` | POST | Summarize text |
| `/summarize-pdf` | POST | Summarize PDF |
| `/upload-pdf-chat` | POST | Upload PDF for Q&A |
| `/ask` | POST | Ask questions from PDF |

---

# 🧠 AI Models Used

## Facebook BART Large CNN
Used for:
- Text summarization
- PDF summarization

## Google FLAN-T5
Used for:
- Context-based question answering

---

# 🔥 Future Improvements

- Better RAG pipeline
- Chat-style interface
- Authentication system
- Cloud deployment
- OCR support for scanned PDFs
- Multi-document querying

---
