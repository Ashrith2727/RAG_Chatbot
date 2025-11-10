# SecureBot - Network Security Tutor & Quiz Bot

## 📋 Project Description

SecureBot is an AI-powered intelligent tutoring system designed to assist students in learning **Network Security** concepts. The system leverages Retrieval-Augmented Generation (RAG) architecture to provide accurate, citation-backed responses from course materials. It features two specialized AI agents:

- **Tutor Agent** – Interactive Q&A system that answers network security questions using local PDF knowledge base with automatic web search fallback
- **Quiz Agent** – Generates comprehensive practice quizzes with mixed question formats (True/False, Single Correct MCQ, Multiple Correct MCQ, and Open-Ended questions)

The system combines local document retrieval with cloud-based LLM inference to provide accurate, contextual responses while maintaining comprehensive logging for educational analytics.

---

## 📚 Documentation

### System Components
- **RAG Pipeline**: Vector-based document retrieval using ChromaDB
- **LLM Integration**: Google Gemini 2.5 Flash for response generation
- **Web Search Fallback**: DuckDuckGo integration for non-security queries
- **Logging System**: Comprehensive trace data for all interactions
- **Streamlit UI**: User-friendly web interface

### Key Features
- Semantic search across 26 lecture PDFs
- Intelligent query classification (LLM-based)
- Dual-path citation system (PDF sources + Web references)
- Mixed-format quiz generation
- Real-time response with source attribution
- Conversation history management

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Web Interface                  │
│                           (app.py)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│  Tutor Agent   │       │   Quiz Agent   │
│(tutor_agent.py)│       │(quiz_agent.py) │
└───────┬────────┘       └───────┬────────┘
        │                        │
        └────────┬───────────────┘
                 │
        ┌────────▼────────┐
        │   Chat Utils    │
        │ (chat_utils.py) │
        │  - LLM calls    │
        │  - Classification│
        └────┬───────┬────┘
             │       │
    ┌────────▼──┐ ┌─▼──────────┐
    │ RAG       │ │ Web Search │
    │ Pipeline  │ │   Utils    │
    └────┬──────┘ └─────┬──────┘
         │              │
    ┌────▼──────┐  ┌────▼──────┐
    │ ChromaDB  │  │DuckDuckGo │
    │ Vector DB │  │    API    │
    └───────────┘  └───────────┘
         │
    ┌────▼──────────┐
    │ Logger Utils  │
    │ (JSON logs)   │
    └───────────────┘
```

### Data Flow
1. **User Query** → Streamlit Interface
2. **Query Classification** → LLM determines if network security related
3. **Retrieval Phase**:
   - Network Security Query → ChromaDB vector search (top 4 chunks)
   - General Query → DuckDuckGo web search
4. **Context Compilation** → Chunks/snippets aggregated
5. **LLM Generation** → Gemini generates response with context
6. **Citation Appending** → Sources/Web references added
7. **Logging** → Trace data saved to JSON
8. **Response Display** → Formatted output to user

---

## 🎥 Video Demonstration

[Project Demo Video Link - To be added]

---

## ⚙️ Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python Version**: 3.10 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 2GB free space for models and dependencies
- **Internet**: Required for initial setup and web search features

### Required Accounts
- Google Cloud account with Gemini API access (API key required)

---

## 📦 Requirements

### Core Dependencies
```
streamlit                    # Web interface
google-generativeai          # Gemini LLM
langchain-community>=0.0.20  # Document loaders
langchain-chroma>=0.1.0      # Vector database
langchain-huggingface>=0.0.1 # Embeddings
sentence-transformers>=2.2.0 # Text embeddings
pypdf>=3.0.0                 # PDF parsing
requests                     # HTTP requests
beautifulsoup4               # Web scraping
```

### Supporting Libraries
```
numpy<2                      # Numerical operations
torch>=2.1.0                 # PyTorch
torchvision>=0.16.0          # Computer vision
langchain-core>=0.1.0        # LangChain core
langchain-text-splitters>=0.0.1  # Text processing
```

Full requirements available in `requirements.txt`

---

## 🚀 Step-by-Step Execution Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/jatinmallarapu/CS5342-Security-Tutor-Bot-Group7.git
cd CS5342-Security-Tutor-Bot-Group7
```

### Step 2: Set Up Python Environment
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Prepare Training Data
```bash
# Place your PDF lecture files in the data/pdfs/ directory
# Ensure PDFs are named appropriately (e.g., Lecture_1.pdf, Lecture_2.pdf)
```

### Step 5: Ingest PDF Documents
```bash
python rag_pipeline.py
```
**Note**: This process takes 10-15 minutes. It will:
- Load all PDFs from `data/pdfs/`
- Split documents into chunks
- Generate embeddings using sentence-transformers
- Store vectors in ChromaDB (`data/chroma_db/`)

### Step 6: Run the Application
```bash
streamlit run app.py
```

### Step 7: Access the Interface
- Open browser and navigate to: `http://localhost:8501`
- Select **Tutor Agent** or **Quiz Agent** from sidebar
- Start interacting with SecureBot!

---

## ✨ Features

### Tutor Agent Features
- ✅ **Semantic Search**: Vector-based retrieval from PDF knowledge base
- ✅ **Intelligent Classification**: LLM determines query relevance
- ✅ **Web Search Fallback**: Automatic external search for non-security topics
- ✅ **Source Citations**: PDF references with page numbers
- ✅ **Conversation History**: Multi-turn dialogue support
- ✅ **Chat Management**: Create, switch, and delete conversations

### Quiz Agent Features
- ✅ **Mixed Question Types**: T/F, Single MCQ, Multiple MCQ, Open-Ended
- ✅ **Topic-Based Generation**: Specify topics or generate random quizzes
- ✅ **10-Question Format**: Comprehensive assessment coverage
- ✅ **Source Attribution**: Shows which PDFs questions came from
- ✅ **Sample Answers**: Provides expected answers for open-ended questions

### System Features
- ✅ **Comprehensive Logging**: JSON logs with trace data
- ✅ **Real-time Processing**: Fast response times (1-3 seconds after initial load)
- ✅ **Error Handling**: Graceful fallbacks and error messages
- ✅ **Scalable Architecture**: Easy to add more PDFs or features

---

## 📊 Training Data & Data Formats

### Training Data Description
- **Source**: CS5342 Network Security course lecture slides
- **Format**: PDF documents
- **Quantity**: 26 lecture files
- **Topics Covered**:
  - Cryptography (AES, DES, RSA, ECC)
  - Hash Functions (MD5, SHA, HMAC)
  - Key Exchange (Diffie-Hellman)
  - Network Protocols (SSL/TLS, TCP/IP)
  - Authentication & Authorization
  - Blockchain & Digital Signatures
  - Security Attacks & Vulnerabilities

### Data Processing Pipeline
1. **PDF Loading**: PyPDFLoader extracts text from PDFs
2. **Text Chunking**: RecursiveCharacterTextSplitter
   - Chunk size: 1000 characters
   - Overlap: 200 characters
3. **Embedding Generation**: sentence-transformers/all-MiniLM-L6-v2
   - Dimension: 384
   - Model size: ~400MB
4. **Vector Storage**: ChromaDB with cosine similarity
5. **Metadata Preservation**: Source file, page number, content

### Data Formats

#### Input Format (PDFs)
```
data/pdfs/
├── Lecture_1_slides.pdf
├── Lecture_2_slides.pdf
├── ...
└── Lecture_26_slides.pdf
```

#### Vector Database Format (ChromaDB)
```json
{
  "id": "chunk_uuid",
  "embedding": [0.123, -0.456, ...],  // 384-dim vector
  "metadata": {
    "source": "data/pdfs/Lecture_15_slides.pdf",
    "page": 12
  },
  "document": "Hash functions are cryptographic algorithms..."
}
```

#### Log Format (JSON)
```json
{
  "timestamp": "2025-11-09T16:11:59.678208",
  "agent_type": "tutor",
  "user_query": "What is AES encryption?",
  "retrieval_info": {
    "total_chunks_retrieved": 4,
    "sources": ["Lecture_6.pdf", "Lecture_7.pdf"],
    "chunks": [
      {
        "chunk_id": 0,
        "source": "Lecture_6.pdf",
        "page": 11,
        "content_preview": "AES is a symmetric...",
        "content_length": 327
      }
    ]
  },
  "llm_info": {
    "context_sent": 4,
    "total_context_length": 1330,
    "response_length": 1445
  },
  "bot_response_preview": "AES (Advanced Encryption Standard)..."
}
```

---

## 🐛 Known Issues & Solutions

### Issue 1: Document Embedding Performance
**Problem**: Initial PDF ingestion takes 10-15 minutes
**Solution**: One-time process; embeddings are cached. Pre-computed embeddings can be distributed for production.

### Issue 2: Source Attribution Mapping
**Problem**: Sources not displaying for certain queries
**Solution**: Implemented dual-path citation system with LLM-based classification to ensure proper routing.

---

## 🔮 Future Enhancements

- [ ] GPU acceleration for faster embeddings
- [ ] Multi-language support
- [ ] Interactive quiz mode with scoring
- [ ] User authentication and progress tracking
- [ ] Export conversations and quizzes to PDF
- [ ] Voice input/output capabilities
- [ ] Mobile-responsive design
- [ ] Advanced analytics dashboard

---

## 🧪 Testing

Functional tests verify:
- ✅ Answer accuracy and citation validity (Tutor Agent)
- ✅ Question quality and format compliance (Quiz Agent)
- ✅ Retrieval accuracy from vector database
- ✅ Web search fallback functionality
- ✅ Logging completeness and accuracy

## Contributors


| Name                              | R#        | Email                                       |
| --------------------------------- | --------- | ------------------------------------------- |
| **Brahmanya Asrit Sudulagunta**   | R11955267 | [bsudulag@ttu.edu](mailto:bsudulag@ttu.edu) |
| **Nithin Kumar Jada**             | R11969019 | [njada@ttu.edu](mailto:njada@ttu.edu)       |
| **Rakesh Ponugumati**             | R11965486 | [rponugum@ttu.edu](mailto:rponugum@ttu.edu) |
| **Venkata Sai Karthik Matha**     | R11944417 | [vmatha@ttu.edu](mailto:vmatha@ttu.edu)     |
| **Jatin Mallarapu**               | R11955268 | [jmallara@ttu.edu](mailto:jmallara@ttu.edu) |
| **Renuka Mantena**                | R11949084 | [remanten@ttu.edu](mailto:remanten@ttu.edu) |
| **Nikhil Chakravarthy Chappalli** | R11976478 | [nchappal@ttu.edu](mailto:nchappal@ttu.edu) |
| **Ramya Samala**                  | R11926730 | [ramsamal@ttu.edu](mailto:ramsamal@ttu.edu) |
