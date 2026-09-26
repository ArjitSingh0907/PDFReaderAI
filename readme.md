<div align="center">

# 📚 StudyBuddy — Multi-PDF RAG Chatbot

**Ask anything. From any PDF. Instantly.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

> A **Retrieval-Augmented Generation (RAG)** powered chatbot that ingests multiple PDFs, builds a semantic vector index, and answers your questions with context-aware, conversation-history-aware responses — all running locally with zero OpenAI costs.

</div>

---

## 🧠 What is RAG? (Retrieval-Augmented Generation)

Traditional LLMs have two big problems:
- They **don't know** about your private documents
- They **hallucinate** when they don't know something

**RAG solves both.** Instead of relying purely on what the model "memorized" during training, RAG:

1. 📄 **Retrieves** the most relevant chunks from your documents at query time
2. 💬 **Augments** the LLM prompt with that retrieved context
3. 🤖 **Generates** an answer grounded in your actual documents

Think of it as giving the LLM an open-book exam instead of a closed-book one.

---

## 🏗️ System Architecture

StudyBuddy operates in two distinct phases: **Indexing** (happens when you click Process) and **Querying** (happens when you ask a question).

### Phase 1 — Document Indexing Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                     INDEXING PHASE (One-time)                        │
└─────────────────────────────────────────────────────────────────────┘

  📄 PDF Files
       │
       ▼
  ┌─────────────┐
  │   PyPDF2    │  ← Reads each page, extracts raw text
  │ PdfReader() │     Handles multi-page, multi-PDF inputs
  └─────────────┘
       │
       │  raw_text (one giant string)
       ▼
  ┌──────────────────────────┐
  │  CharacterTextSplitter   │  ← Splits text into overlapping chunks
  │  chunk_size    = 1000    │     chunk_size: max chars per chunk
  │  chunk_overlap = 200     │     chunk_overlap: shared chars between
  │  separator     = "\n"    │     adjacent chunks (preserves context)
  └──────────────────────────┘
       │
       │  text_chunks[] (list of strings)
       ▼
  ┌────────────────────────────────┐
  │  HuggingFace Embeddings        │  ← Converts each chunk into a
  │  model: all-MiniLM-L6-v2      │     384-dimensional float vector
  │  (runs 100% locally, free)    │     Semantically similar text →
  └────────────────────────────────┘     similar vectors (cosine proximity)
       │
       │  embeddings[] (list of 384-dim vectors)
       ▼
  ┌───────────────────────────────┐
  │  FAISS Vector Store           │  ← Facebook AI Similarity Search
  │  FAISS.from_texts()           │     Indexes all vectors in memory
  │  (in-memory, lightning fast)  │     Supports ANN (Approx Nearest
  └───────────────────────────────┘     Neighbour) search in O(log n)
       │
       ▼
  ✅  vectorstore.as_retriever()  →  Stored in st.session_state
```

---

### Phase 2 — Query & Generation Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                    QUERYING PHASE (Every question)                    │
└─────────────────────────────────────────────────────────────────────┘

  👤 User types a question
       │
       ▼
  ┌────────────────────────────────┐
  │  HuggingFace Embeddings        │  ← Same model as indexing phase
  │  model: all-MiniLM-L6-v2      │     Converts question → 384-dim vector
  └────────────────────────────────┘
       │
       │  query_vector (384-dim)
       ▼
  ┌───────────────────────────────────────────┐
  │  FAISS Similarity Search                  │
  │  retriever.invoke(user_question)          │  ← Finds Top-K chunks
  │                                           │     whose vectors are
  │  [cosine similarity across all chunks]    │     closest to query
  └───────────────────────────────────────────┘
       │
       │  docs[] (top-k most relevant chunks)
       ▼
  ┌─────────────────────────┐
  │   format_docs(docs)     │  ← Joins chunk texts with "\n\n"
  │   context = str         │     into a single context string
  └─────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────┐
  │  ChatPromptTemplate (LangChain)                     │
  │                                                     │
  │  SYSTEM: "You are an assistant. Use the following   │
  │           retrieved context to answer. If you       │
  │           don't know, say so. Keep it concise."    │
  │           + {context}   ← injected here             │
  │                                                     │
  │  HISTORY: {chat_history}  ← HumanMessage/AIMessage  │
  │                              list (multi-turn aware) │
  │                                                     │
  │  HUMAN:   {input}  ← the actual question            │
  └─────────────────────────────────────────────────────┘
       │
       │  formatted prompt string
       ▼
  ┌──────────────────────────────────┐
  │  Groq LLM                        │
  │  model: openai/gpt-oss-20b       │  ← Ultra-fast inference via
  │  temperature: 0                  │     Groq's LPU hardware
  └──────────────────────────────────┘     (deterministic: temp=0)
       │
       │  answer (string)
       ▼
  ┌──────────────────────┐
  │  StrOutputParser()   │  ← Extracts plain text from LLM response
  └──────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────┐
  │  Chat History Update                     │
  │  HumanMessage(content=user_question)     │  ← Appended to
  │  AIMessage(content=answer)               │     session_state
  └──────────────────────────────────────────┘
       │
       ▼
  💬  Rendered in Streamlit UI with custom HTML templates
```

---

## 🔬 RAG Concepts Explained In-Depth

### 1. 📄 Document Ingestion — `get_pdf_text()`

```python
pdf_reader = PdfReader(pdf)
for page in pdf_reader.pages:
    text += page.extract_text()
```

**What happens:** PyPDF2 opens each uploaded PDF, iterates over every page, and extracts the raw text content. Multiple PDFs are concatenated into one large string.

**Why this matters:** The quality of text extraction directly affects retrieval quality. Clean, machine-readable PDFs work best. Scanned image-PDFs require OCR (not implemented here — a future enhancement).

---

### 2. ✂️ Text Chunking — `get_text_chunks()`

```python
CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)
```

**Why chunk at all?** LLMs have a context window limit. You can't stuff an entire 200-page PDF into a prompt. More importantly, embedding a huge document into a single vector loses granularity — you need fine-grained chunks to retrieve *precisely* relevant content.

**Why overlap?** If an answer spans the boundary between two chunks, `chunk_overlap=200` ensures those boundary characters appear in *both* chunks — preventing the retriever from missing cross-boundary information.

```
  Chunk 1: [============================]
  Chunk 2:                   [============================]
                             |←  200 char overlap  →|
```

---

### 3. 🔢 Embedding Generation — `HuggingFaceEmbeddings`

```python
HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

**What is an embedding?** A mathematical representation of text as a fixed-size vector of floating-point numbers (384 dimensions for MiniLM). The key property: **semantically similar text produces geometrically close vectors.**

```
  "What is machine learning?"   → [0.21, -0.43, 0.87, ... ]  ← 384 numbers
  "Explain ML to me"            → [0.19, -0.41, 0.85, ... ]  ← very close!
  "My cat likes tuna"           → [0.92,  0.11, -0.33, ... ] ← far away
```

**Why MiniLM-L6-v2?** It's a distilled Sentence-BERT model — fast, lightweight (80MB), runs locally with no API calls, and produces high-quality semantic embeddings ideal for retrieval tasks.

---

### 4. 🗄️ Vector Store — FAISS

```python
vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
retriever   = vectorstore.as_retriever()
```

**What is FAISS?** Facebook AI Similarity Search — a library for efficient similarity search over dense vectors. It stores all chunk embeddings and can find the nearest neighbours to any query vector at blazing speed.

**How similarity search works:**

```
  Query vector Q = [0.21, -0.43, 0.87, ...]

  FAISS computes cosine similarity between Q and every stored chunk vector:
  
  Chunk 1 similarity: 0.92  ← most relevant ✅
  Chunk 2 similarity: 0.87  ← relevant ✅
  Chunk 3 similarity: 0.21  ← not relevant ❌
  Chunk 4 similarity: 0.19  ← not relevant ❌
  ...
  
  Returns Top-K (default: 4) most similar chunks
```

---

### 5. 🧩 Prompt Engineering — `ChatPromptTemplate`

```python
ChatPromptTemplate.from_messages([
    ("system", "...context: {context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])
```

**Three-part prompt structure:**

| Part | Role | Content |
|------|------|---------|
| `system` | Sets AI behaviour | Instructions + retrieved context injected here |
| `chat_history` | Multi-turn memory | All previous Human+AI messages |
| `human` | Current query | The user's latest question |

**Why separate context from system prompt?** It keeps the instructions clean and makes the context block easy to swap or update without breaking the instruction logic.

---

### 6. 🤖 LLM — Groq + LPU Inference

```python
ChatGroq(model="openai/gpt-oss-20b", temperature=0)
```

**Why Groq?** Groq runs inference on custom LPU (Language Processing Unit) hardware — purpose-built for transformer inference. This gives 5–10× faster responses than GPU-based APIs, with generous free tier limits.

**Why `temperature=0`?** Temperature controls randomness. At 0, the model is deterministic and picks the highest-probability token every time — ideal for factual Q&A where you want consistent, accurate answers, not creative variation.

---

### 7. 🔗 LangChain Chain — LCEL (LangChain Expression Language)

```python
chain = prompt | llm | StrOutputParser()
```

**What is LCEL?** The `|` pipe operator chains components like Unix pipes. Data flows left → right:

```
  prompt  ──|──►  llm  ──|──►  StrOutputParser
    ↑                                ↓
  Formats the                  Extracts plain
  input dict into              text from the
  a ChatPromptValue            AIMessage object
```

This is cleaner, more composable, and easier to debug than legacy `LLMChain`.

---

### 8. 💬 Conversation Memory — `st.session_state`

```python
st.session_state.chat_history.append(HumanMessage(content=question))
st.session_state.chat_history.append(AIMessage(content=answer))
```

**How multi-turn memory works:** After every Q&A pair, both messages are appended to `chat_history`. On the next question, this entire history is injected into `MessagesPlaceholder("chat_history")` in the prompt — giving the LLM full conversation context.

**Why Streamlit session_state?** Streamlit reruns the entire script on every interaction. `session_state` persists data across reruns, acting as the application's memory store.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Web UI, file upload, chat interface |
| **PDF Parsing** | PyPDF2 | Extract text from uploaded PDFs |
| **Text Splitting** | LangChain `CharacterTextSplitter` | Chunk documents with overlap |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` | Convert text → semantic vectors |
| **Vector DB** | FAISS (in-memory) | Store & search embedding vectors |
| **Orchestration** | LangChain (LCEL) | Chain prompt → LLM → parser |
| **LLM** | Groq (`openai/gpt-oss-20b`) | Generate context-aware answers |
| **Env Management** | python-dotenv | Load API keys from `.env` |
| **UI Templates** | Custom HTML/CSS | Styled chat bubbles with SVG avatars |

---

## 📁 Project Structure

```
StudyBuddy/
│
├── app.py                 # Main application — all RAG logic lives here
│   ├── get_pdf_text()     # Phase 1: PDF ingestion
│   ├── get_text_chunks()  # Phase 1: Text splitting
│   ├── get_vectorstore()  # Phase 1: Embedding + FAISS indexing
│   ├── get_qa_chain()     # Phase 2: Prompt + LLM chain setup
│   └── handle_userinput() # Phase 2: Retrieval + generation + history
│
├── htmlTemplates.py       # Custom HTML/CSS for chat UI
│   ├── css               # Chat bubble styling
│   ├── bot_template       # Siri-style aurora SVG avatar + message
│   └── user_template      # Dotted person SVG avatar + message
│
├── .env                   # API keys (never commit this!)
│   ├── GROQ_API_KEY       # From console.groq.com
│   └── GOOGLE_API_KEY     # (Optional) From aistudio.google.com
│
├── requirements.txt       # Python dependencies
├── .gitignore             # Excludes venv/, .env, __pycache__
└── README.md              # You are here 📍
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com/keys)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/StudyBuddy.git
cd StudyBuddy
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install sentence-transformers langchain-groq
```

**4. Create your `.env` file**
```env
GROQ_API_KEY=gsk_your_key_here
```

**5. Run the app**
```bash
streamlit run app.py
```

**6. Use it**
- Upload one or more PDFs in the sidebar
- Click **Process**
- Ask any question in the chat input

---

## 🔮 How the Full Flow Connects (End-to-End)

```
User uploads PDF(s)
        │
        ▼
[PyPDF2] Extract all text
        │
        ▼
[CharacterTextSplitter] → ~N chunks of ≤1000 chars, 200-char overlap
        │
        ▼
[HuggingFace MiniLM] → N × 384-dim embedding vectors
        │
        ▼
[FAISS] Index all vectors → in-memory vector store
        │
        ▼
User asks: "What is X?"
        │
        ▼
[HuggingFace MiniLM] Embed the question → 384-dim query vector
        │
        ▼
[FAISS] Cosine similarity search → Top-4 most relevant chunks
        │
        ▼
[ChatPromptTemplate] Assemble: System + Context + History + Question
        │
        ▼
[Groq LLM @ temp=0] Generate grounded answer
        │
        ▼
[StrOutputParser] Extract plain text
        │
        ▼
[session_state] Append HumanMessage + AIMessage to history
        │
        ▼
[Streamlit] Render styled chat bubbles ✅
```

---

## 🚀 Future Enhancements

- [ ] **Persistent vector store** — Save FAISS index to disk (avoid reprocessing on reload)
- [ ] **OCR support** — Handle scanned/image-based PDFs via Tesseract
- [ ] **Source citation** — Show which PDF page each answer came from
- [ ] **Multiple retrieval strategies** — MMR (Maximal Marginal Relevance) for diversity
- [ ] **Streaming responses** — Stream LLM tokens as they're generated
- [ ] **Re-ranking** — Cross-encoder re-ranking of retrieved chunks for precision

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

Built with ❤️ using LangChain, Groq, FAISS, and Streamlit

⭐ Star this repo if you found it helpful!

</div>