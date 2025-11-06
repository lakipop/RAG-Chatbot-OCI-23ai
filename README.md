# RAG Chatbot with OCI Generative AI and Oracle 23ai Vector Search

A complete, production-ready **Retrieval-Augmented Generation (RAG)** chatbot that answers questions about Oracle Cloud Infrastructure using OCI's Generative AI service and Oracle 23ai's Vector Search capabilities.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)
![OCI](https://img.shields.io/badge/OCI-Generative%20AI-red.svg)
![Oracle](https://img.shields.io/badge/Oracle-23ai-orange.svg)

---

## 🎯 Project Overview

This project demonstrates how to build an intelligent Q&A system that eliminates AI "hallucinations" by grounding responses in your own documents. It's a complete end-to-end implementation suitable for enterprise use cases.

### What is RAG? (Simple Analogy)

Think of RAG like an **"open-book exam"** for AI:

| Type | How it Works | Problem |
|------|--------------|---------|
| **Normal Chatbot** | Answers from memory (training data) | ❌ Can make up facts ("hallucinate") |
| **RAG Chatbot** | First looks up facts in your documents, THEN answers | ✅ Factual and verifiable |

**RAG = Retrieval-Augmented Generation**
- **Retrieval**: Find relevant information from your documents
- **Augmented**: Add that information to the question
- **Generation**: Generate an answer based on the retrieved facts

---

## 🏗️ Architecture & Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ASKS QUESTION                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Question → Vector Embedding (OCI Generative AI)         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Search for Similar Documents (Oracle 23ai Vector DB)    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Retrieve Top 3 Most Relevant Document Chunks            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Combine Question + Context → Send to LLM               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Generate Factual Answer (OCI Generative AI)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              DISPLAY ANSWER + SOURCES                        │
└─────────────────────────────────────────────────────────────┘
```

### Two-Phase Process

#### Phase 1: Data Ingestion (One-Time Setup)
**Script**: `ingest.py`

1. 📂 **Load**: Read `.txt` files from `./data` folder
2. ✂️ **Split**: Break documents into 1000-character chunks (with 200-char overlap)
3. 🧠 **Embed**: Convert each chunk to vector embeddings using OCI
4. 💾 **Store**: Save embeddings + text in Oracle 23ai Vector Database

#### Phase 2: Query & Retrieval (Runtime)
**Script**: `main_app.py`

1. 💬 **User** asks a question via Streamlit web UI
2. 🔍 **App** converts question to embedding and searches Oracle DB
3. 📚 **Retrieval** returns top 3 most similar document chunks
4. 🤖 **LLM** generates answer using only the retrieved context
5. ✅ **Display** answer + source citations

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **OCI Account** with Generative AI access
- **Oracle 23ai Database** (Autonomous Database or on-premise)
- **OCI API Keys** configured

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/lakipop/oci-rag-oracle-23ai.git
cd oci-rag-oracle-23ai
```

#### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
# Use your favorite text editor
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Required values in `.env`:**

```env
# OCI Authentication
OCI_USER_ID="ocid1.user.oc1..your_user_id"
OCI_TENANCY_ID="ocid1.tenancy.oc1..your_tenancy_id"
OCI_REGION="us-chicago-1"
OCI_KEY_FINGERPRINT="xx:xx:xx:..."
OCI_PRIVATE_KEY_PATH="C:/path/to/your/oci_api_key.pem"
COMPARTMENT_ID="ocid1.compartment.oc1..your_compartment_id"

# Oracle Database
DB_USER="ADMIN"
DB_PASSWORD="YourPassword123!"
DB_DSN="your_connection_string"
```

> 💡 **Tip**: Get your Oracle DB connection string from OCI Console → Autonomous Database → DB Connection

#### 5. Run Data Ingestion (ONE TIME ONLY)

```bash
python ingest.py
```

**Expected output:**
```
🚀 STARTING DATA INGESTION PIPELINE
📋 Step 1: Loading configuration...
✓ Configuration loaded successfully
📂 Step 2: Loading documents...
✓ Loaded 2 document(s)
✂️ Step 3: Splitting documents into chunks...
✓ Created 12 chunk(s) from 2 document(s)
🧠 Step 4: Initializing OCI Embeddings model...
✓ Using embedding model: cohere.embed-english-v3.0
💾 Step 8: Adding documents to vector store...
   ⏳ This may take 30-60 seconds...
✅ INGESTION COMPLETE!
```

#### 6. Launch the Chatbot

```bash
streamlit run main_app.py
```

**The app will open automatically in your browser at** `http://localhost:8501`

---

## 📖 Usage Guide

### Example Questions to Try

Once the app is running, try asking:

```
1. "What is Oracle Cloud Infrastructure?"
2. "What are the benefits of OCI Compute?"
3. "How does OCI ensure security?"
4. "What types of compute instances does OCI offer?"
5. "Tell me about OCI's pricing model"
```

### Understanding the Response

The app provides:

1. **📖 Answer**: The generated response based on your documents
2. **📚 Sources Used**: The exact document chunks that were used
   - Click to expand and see the full text
   - Verify the answer against the source material

---

## 📁 Project Structure

```
oci-rag-oracle-23ai/
├── .gitignore              # Git ignore rules (prevents committing secrets)
├── .env.example            # Template for environment variables
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── config_loader.py        # Loads secrets from .env securely
├── ingest.py              # Data ingestion script (run once)
├── main_app.py            # Streamlit chatbot application
└── data/                  # Your documents folder
    ├── oci_overview.txt   # Sample document about OCI
    └── oci_compute.txt    # Sample document about OCI Compute
```

### Key Files Explained

| File | Purpose | Run Frequency |
|------|---------|---------------|
| `config_loader.py` | Loads OCI & DB credentials from `.env` | Imported by other scripts |
| `ingest.py` | Ingests documents into vector database | Once (or when adding new docs) |
| `main_app.py` | Web UI for asking questions | Every time you want to use the chatbot |
| `data/*.txt` | Your knowledge base documents | Add/update as needed |

### Important Code Components

| File | Lines | Key Features |
|------|-------|--------------|
| `ingest.py` | 251 | Step-by-step ingestion, chunking strategy, error handling, progress indicators |
| `main_app.py` | 337 | Streamlit UI, caching, source citations, sidebar info, status indicators |
| `config_loader.py` | 95 | Secure credential loading, validation, standalone testing |

---

## 🛠️ Technical Details

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | LangChain | Chains together retrieval + generation |
| **Embeddings** | OCI Generative AI (Cohere) | Converts text to vectors |
| **LLM** | OCI Generative AI (Cohere Command-R-Plus) | Generates answers |
| **Vector Database** | Oracle 23ai Vector Search | Stores and searches embeddings |
| **Web Framework** | Streamlit | Provides the user interface |
| **Database Driver** | python-oracledb | Connects to Oracle Database |

### Why These Choices?

- **LangChain**: Industry-standard framework for LLM applications
- **OCI Generative AI**: Enterprise-grade, secure, and cost-effective
- **Oracle 23ai**: Native vector search without needing separate vector DB
- **Streamlit**: Rapid prototyping with minimal code

### Key Parameters

#### Chunking Strategy
```python
chunk_size=1000       # Characters per chunk
chunk_overlap=200     # Overlap to preserve context
```

#### Embedding Model
```python
model_id="cohere.embed-english-v3.0"
# Dimensions: 1024
# Language: English
```

#### LLM Configuration
```python
model_id="cohere.command-r-plus"
max_tokens=500        # Maximum answer length
temperature=0.3       # Low = more factual, high = more creative
```

#### Retrieval Settings
```python
k=3                   # Return top 3 most similar chunks
distance_strategy=COSINE  # Cosine similarity for vector comparison
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

#### 2. "Configuration Error: Missing required..."
```bash
# Check your .env file
# Ensure all variables are set (no empty values)
cat .env  # Linux/Mac
type .env # Windows
```

#### 3. "Database error: ORA-00942: table or view does not exist"
```bash
# You need to run ingestion first!
python ingest.py
```

#### 4. "Connection timeout" to OCI
```bash
# Check:
# 1. Your OCI credentials are correct
# 2. Your region matches your resources
# 3. Your API key file path is correct
# 4. You have network access to OCI
```

#### 5. "Authentication failed" for Oracle DB
```bash
# Verify:
# 1. DB_USER is correct (usually "ADMIN" for Autonomous DB)
# 2. DB_PASSWORD is correct
# 3. DB_DSN connection string is valid
# 4. Your IP is whitelisted (for Autonomous DB)
```

---

## 📝 Adding Your Own Documents

### Step 1: Add Documents

```bash
# Add .txt files to the data/ folder
cp your_document.txt ./data/
```

### Step 2: Re-run Ingestion

```bash
python ingest.py
```

### Tips for Document Preparation

- ✅ **Use plain text (.txt)** files for best results
- ✅ **Keep documents focused** on specific topics
- ✅ **Break large documents** into separate files by topic
- ✅ **Use clear headings** and structure
- ❌ Avoid very short documents (< 100 words)
- ❌ Avoid mixing multiple languages in one document

---

## 🎓 Learning Resources

### For Java Developers New to Python

This project uses Python concepts that might be unfamiliar:

| Python Concept | Java Equivalent | Used In |
|---------------|-----------------|---------|
| Virtual environments | Maven/Gradle dependencies | Setup |
| `dotenv` | `application.properties` | config_loader.py |
| Decorators (`@st.cache`) | Annotations (`@Cacheable`) | main_app.py |
| Dictionary unpacking | Varargs | config_loader.py |
| Context managers (`with`) | try-with-resources | ingest.py |

### Understanding RAG

- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Oracle 23ai Vector Search Docs](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/)
- [OCI Generative AI Service](https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm)

---

## 🔐 Security Best Practices

- ✅ **Never commit** `.env` file to Git (it's in `.gitignore`)
- ✅ **Use API keys** instead of user/password for OCI
- ✅ **Rotate credentials** regularly
- ✅ **Restrict compartment** permissions to minimum required
- ✅ **Use private endpoints** for Oracle Database in production
- ✅ **Enable audit logging** in OCI

---

## 🚀 Next Steps & Enhancements

### Potential Improvements

1. **Add More Document Types**: Support PDF, Word, Markdown
2. **Improve Chunking**: Use semantic chunking instead of fixed-size
3. **Add Chat History**: Implement conversation memory
4. **Deploy to Production**: Use OCI Container Instances or Kubernetes
5. **Add Authentication**: Implement user login and access control
6. **Monitor Usage**: Track questions, response times, and costs
7. **Fine-tune Prompts**: Customize system prompts for your domain
8. **Hybrid Search**: Combine vector search with keyword search

---

## 📄 License

This project is for educational and portfolio purposes. Feel free to use it as a template or Fork it for your own projects. Please do not use it for commercial purposes without permission.
If you find it useful, a star ⭐ on GitHub is appreciated!

---

## 👨‍💻 Author

**lakipop**
- GitHub: [@lakipop](https://github.com/lakipop)
- Course: OCI Generative AI Professional 

---

## 🙏 Acknowledgments

- **Oracle** for Oracle Cloud Infrastructure and 23ai Vector Search
- **LangChain** for the excellent RAG framework
- **Cohere** for the embedding and LLM models available on OCI
- **Streamlit** for making web UIs incredibly simple

---

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the heavily-commented code in `ingest.py` and `main_app.py`
3. Ensure all prerequisites are met
4. Verify your credentials in `.env`

---

**Built with ❤️ using LangChain, OCI Generative AI, and Oracle 23ai Vector Search**

*Last Updated: November 2025*
