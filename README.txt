================================================================================
                    SECUREBOT - NETWORK SECURITY TUTOR BOT
                          Project Documentation
================================================================================

PROJECT OVERVIEW
----------------
SecureBot is an AI-powered chatbot designed to assist students in learning 
network security concepts. It features a Tutor Agent for Q&A and a Quiz Agent 
for generating practice questions from PDF lecture materials.


REQUIRED ENVIRONMENT
--------------------
- Operating System: Windows 10/11 (tested on Windows)
- Python Version: 3.10 or higher
- RAM: Minimum 8GB (16GB recommended for faster processing)
- Storage: At least 2GB free space for models and dependencies


ADOPTED LIBRARIES
-----------------
Core Libraries:
- streamlit: Web interface for the chatbot
- google-generativeai: Gemini LLM for response generation
- langchain-community: PDF loading and document processing
- langchain-chroma: Vector database for embeddings storage
- langchain-huggingface: Embedding model integration
- sentence-transformers: Text embeddings (all-MiniLM-L6-v2)

Supporting Libraries:
- requests: Web search functionality
- beautifulsoup4: Web scraping for external queries
- pypdf: PDF parsing
- numpy<2: Numerical operations (version constraint for compatibility)
- torch>=2.1.0: PyTorch for ML models
- torchvision>=0.16.0: Computer vision utilities


FLOW OF EXECUTION
------------------
1. PDF Ingestion Phase:
   - Load PDF files from data/pdfs/ directory
   - Split documents into chunks (1000 chars, 200 overlap)
   - Generate embeddings using sentence-transformers
   - Store embeddings in ChromaDB vector database

2. Query Classification:
   - User submits a query through Streamlit interface
   - LLM classifies if query is network security related
   - Decision: Search PDFs or use web search

3. Retrieval Phase (if network security query):
   - Query embeddings generated
   - Similarity search in ChromaDB (top 4 chunks)
   - Context compiled from retrieved chunks
   - If insufficient context (<100 chars), fallback to web search

4. Web Search Phase (if non-network security query):
   - DuckDuckGo API search for relevant information
   - Extract snippets from search results
   - Compile web context for LLM

5. Response Generation:
   - Context + conversation history sent to Gemini LLM
   - LLM generates comprehensive response
   - Sources/Web references appended to response

6. Logging:
   - All interactions logged to logs/ directory
   - JSON format with timestamp, query, chunks, sources, response


COMMANDS TO RUN THE CODE
-------------------------
1. Install Dependencies:
   pip install -r requirements.txt

2. Ingest PDF Files (First Time Setup):
   python rag_pipeline.py
   Note: This takes 5-15 minutes depending on number of PDFs

3. Run the Application:
   streamlit run app.py
   
4. Access the Application:
   Open browser and navigate to: http://localhost:8501

5. Clear Python Cache (if experiencing import issues):
   rmdir /s /q __pycache__


PROJECT STRUCTURE
-----------------
CS5342-Security-Tutor-Bot-Group7/
├── app.py                      # Main Streamlit application
├── app_enhanced.py             # Alternative UI
├── securebot_experimental.py   # Experimental features (not used)
├── chat_utils.py               # Core chat logic and LLM integration
├── tutor_agent.py              # Tutor agent interface
├── quiz_agent.py               # Quiz generation interface
├── rag_pipeline.py             # PDF ingestion and vector DB setup
├── logger_utils.py             # Logging functionality
├── web_search_utils.py         # Web search integration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── data/
│   ├── pdfs/                   # Place PDF lecture files here
│   └── chroma_db/              # Vector database (auto-generated)
└── logs/                       # Query logs (auto-generated)


ISSUES EXPERIENCED & SOLUTIONS
-------------------------------
Issue 1: Document Embedding and Vector Database Training
Problem: 
During the initial PDF ingestion phase, the system encountered performance 
bottlenecks when processing 26 lecture PDF files. The sentence-transformers 
model (all-MiniLM-L6-v2) required significant computational resources to 
generate 384-dimensional embeddings for each text chunk. The process took 
10-15 minutes on standard hardware, and the ChromaDB vector database grew 
to over 2GB in size. Additionally, the embedding model needed to be 
downloaded (~400MB) on first run, causing delays.

Technical Details:
- Text chunking: 1000 characters per chunk with 200-character overlap
- Embedding dimension: 384 (sentence-transformers/all-MiniLM-L6-v2)
- Total chunks generated: ~2000-3000 from 26 PDFs
- Vector similarity search: Cosine similarity with k=4 retrieval

Solution:
Optimized the ingestion pipeline by implementing batch processing and 
ensuring the embedding model is cached locally after first download. The 
vector database is persisted to disk, so ingestion only needs to run once 
unless new PDFs are added. For production deployment, pre-computed embeddings 
can be distributed with the application to eliminate initial setup time.

Issue 2: Source Attribution and Context Mapping
Problem:
The system initially failed to properly map retrieved document chunks back 
to their source PDFs and page numbers in the response. When users asked 
questions, the bot would provide answers but not display the "Sources:" 
section at the end. This occurred because the retrieval logic was bypassing 
the local PDF database for certain queries, triggering web search instead, 
which resulted in an empty docs list. The source attribution logic only 
checked the docs list, not the web_references list, causing missing citations.

Technical Details:
- ChromaDB returns Document objects with metadata (source, page)
- Metadata extraction: doc.metadata.get("source", "Unknown Source")
- Source deduplication: set() to remove duplicate PDF references
- Conditional logic: if use_web_search vs if docs for citation display

Solution:
Implemented a dual-path citation system that properly handles both local 
PDF sources and web references. The logic now correctly identifies whether 
the response came from the vector database or web search, and appends the 
appropriate citations. For PDF sources, it displays "Sources: Lecture_X.pdf" 
with deduplicated file names. For web queries, it displays "Web References:" 
with clickable URLs. Additionally, implemented LLM-based query classification 
to ensure network security questions always check the PDF database first 
before falling back to web search, improving source mapping accuracy.


SUGGESTIONS & FEEDBACK & OBSERVATIONS
------------------------
Strengths:
+ Successfully retrieves relevant information from PDF knowledge base
+ Intelligent fallback to web search for non-security topics
+ Comprehensive logging for debugging and analysis
+ Mixed-format quiz generation (T/F, MCQ, Open-ended)
+ Clean separation of concerns (agents, utils, pipeline)

Areas for Enhancement:
- Initial PDF ingestion is time-consuming (unavoidable with embeddings)
- Web search could be more reliable with paid APIs
- LLM classification adds latency (~1-2 seconds per query)
- No persistent conversation memory across sessions
- Limited error handling for network failures

TROUBLESHOOTING
---------------
Problem: "ModuleNotFoundError"
Solution: Ensure all dependencies installed: pip install -r requirements.txt

Problem: "No such file or directory: logs/"
Solution: Directory auto-created on first run, or manually: mkdir logs

Problem: "ChromaDB not found"
Solution: Run PDF ingestion first: python rag_pipeline.py

Problem: Slow response times
Solution: First query is slow (model loading), subsequent queries faster

Problem: No sources displayed
Solution: Ensure PDFs are ingested and chroma_db exists

Problem: Web search not working
Solution: Check internet connection, DuckDuckGo may be rate-limiting


================================================================================
                            END OF DOCUMENTATION
================================================================================
