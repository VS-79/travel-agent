# ✈️ AI Travel Planning Agent

An intelligent travel planning agent powered by Claude AI that helps users plan personalized 2-day trips to any city. Built with FastAPI, LangChain, Redis, and a multi-hop RAG pipeline.

🌐 **Live Demo**: [https://stirring-puppy-b6863f.netlify.app/](https://stirring-puppy-b6863f.netlify.app/)  
🔗 **API**: [https://travel-agent-vgw3.onrender.com](https://travel-agent-vgw3.onrender.com)  
📖 **API Docs**: [https://travel-agent-vgw3.onrender.com/docs](https://travel-agent-vgw3.onrender.com/docs)

---

## 🌟 Features

- **Intelligent Planning** — Automatically breaks down travel requests into sub-tasks using a Plan-and-Execute agent
- **Real-time Weather** — Fetches live weather forecasts for any destination
- **Real Hotel Data** — Live hotel listings via SerpAPI Google Hotels with price and rating filters
- **Web Search** — AI-optimized travel search via Tavily
- **Multi-hop RAG** — Retrieves detailed travel knowledge from a Wikipedia knowledge base (311 chunks across 5 cities)
- **Short-term Memory** — Remembers conversation context within a session (Redis)
- **Long-term Memory** — Remembers user preferences across sessions (Redis + TF-IDF)
- **Pet-friendly Support** — Toggle pet-friendly mode for specialized recommendations
- **Multilingual Support** — Responds in the user's language automatically
- **Budget Filters** — Budget, moderate, and luxury options

---

## 🏗️ Architecture

```
User (Netlify Frontend)
         ↓
FastAPI REST API (Render)
         ↓
    Agent Core
   ┌─────────────────────────────┐
   │  Planner → Executor         │
   │  (Plan-and-Execute pattern) │
   └─────────────────────────────┘
         ↓
   ┌─────┬──────┬────────┬─────┐
   │Weather│Search│Hotels │ RAG │
   └─────┴──────┴────────┴─────┘
         ↓
   Claude Sonnet (LLM)
         ↓
   ┌──────────────────┐
   │  Redis (Upstash) │
   │  - Short-term    │
   │  - Long-term     │
   └──────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude Sonnet (claude-sonnet-4-5) |
| API Framework | FastAPI |
| Orchestration | LangChain |
| Short-term Memory | Redis (Upstash) |
| Long-term Memory | Redis + TF-IDF (scikit-learn) |
| RAG Pipeline | Wikipedia + TF-IDF Vector Search |
| Web Search | Tavily Search API |
| Weather | OpenWeatherMap API |
| Hotels | SerpAPI Google Hotels |
| Frontend | HTML + marked.js |
| Backend Deploy | Render (Docker) |
| Frontend Deploy | Netlify |

---

## 📁 Project Structure

```
travel-agent/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Settings via pydantic-settings
│   ├── dependencies.py            # Shared dependency injection
│   ├── api/
│   │   ├── schemas.py             # Request/response models
│   │   └── routes/
│   │       ├── chat.py            # POST /api/chat
│   │       ├── health.py          # GET /health
│   │       └── trips.py           # GET /api/preferences/{user_id}
│   ├── agent/
│   │   ├── agent.py               # TravelAgent orchestrator
│   │   ├── planner.py             # Goal → sub-task decomposition
│   │   ├── executor.py            # Sub-task → tool execution
│   │   ├── prompts.py             # System prompts
│   │   └── preference_extractor.py # Extract preferences from conversations
│   ├── tools/
│   │   ├── weather.py             # OpenWeatherMap tool
│   │   ├── search.py              # Tavily search tool
│   │   ├── hotels.py              # SerpAPI Google Hotels tool
│   │   └── rag_retriever.py       # TF-IDF knowledge base tool
│   ├── memory/
│   │   ├── short_term.py          # Redis conversation buffer
│   │   ├── long_term.py           # Redis + TF-IDF preference store
│   │   └── session_store.py       # Session metadata
│   └── rag/
│       ├── indexer.py             # Wikipedia fetcher and chunker
│       ├── retriever.py           # Multi-hop retrieval logic
│       └── vector_store.py        # TF-IDF vectorizer and search
├── scripts/
│   └── ingest_data.py             # Build RAG knowledge base (run once)
├── data/
│   └── faiss_index/               # Persisted TF-IDF index files
├── frontend/
│   └── index.html                 # Single-page chat UI
├── tests/
│   ├── test_tools.py              # Tool unit tests
│   ├── test_memory.py             # Memory unit tests
│   └── test_agent.py              # Agent unit tests
├── Dockerfile                     # Docker container config
├── render.yaml                    # Render deployment config
└── requirements.txt               # Python dependencies
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/VS-79/travel-agent.git
cd travel-agent
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:
```env
ANTHROPIC_API_KEY=sk-ant-...
OPENWEATHER_API_KEY=...
TAVILY_API_KEY=tvly-...
SERPAPI_KEY=...
REDIS_URL=rediss://default:...@...upstash.io:6379
```

### 5. Get API Keys

| Service | URL | Free Tier |
|---|---|---|
| Anthropic | https://console.anthropic.com | Pay-as-you-go |
| OpenWeatherMap | https://openweathermap.org/api | 1000 calls/day |
| Tavily | https://app.tavily.com | 1000 searches/month |
| SerpAPI | https://serpapi.com | 250 searches/month |
| Upstash Redis | https://upstash.com | 10k commands/day |

### 6. Build the RAG knowledge base
```bash
python scripts/ingest_data.py
```

This fetches Wikipedia articles for Tokyo, Paris, Singapore, London and Bangkok and builds a TF-IDF index. Run this once before starting the server.

### 7. Start the server
```bash
uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`

### 8. Test the API
Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### 9. Open the frontend
Open `frontend/index.html` in your browser or use Live Server in VS Code.

---

## 🔌 API Reference

### POST /api/chat
Send a message to the travel agent.

**Request:**
```json
{
  "user_id": "user123",
  "message": "Plan a 2 day trip to Tokyo",
  "pet_friendly": false,
  "budget": "moderate"
}
```

**Response:**
```json
{
  "user_id": "user123",
  "reply": "Here's your personalized Tokyo itinerary..."
}
```

### GET /api/preferences/{user_id}
Retrieve stored preferences for a user.

**Response:**
```json
{
  "user_id": "user123",
  "preferences": [
    "loves Japanese food",
    "prefers budget hotels",
    "interested in cultural sites"
  ]
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🐳 Docker

Build and run locally with Docker:

```bash
docker build -t travel-agent .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your-key \
  -e OPENWEATHER_API_KEY=your-key \
  -e TAVILY_API_KEY=your-key \
  -e SERPAPI_KEY=your-key \
  -e REDIS_URL=your-redis-url \
  travel-agent
```

---

## ☁️ Deployment

### Backend (Render)
1. Push code to GitHub
2. Connect repo to Render
3. Set runtime to Docker
4. Add environment variables
5. Deploy — auto-deploys on every push

### Frontend (Netlify)
1. Connect repo to Netlify
2. Set publish directory to `frontend`
3. Deploy — auto-deploys on every push

> **Note:** Render free tier spins down after 15 minutes of inactivity. First request may take 30-60 seconds.

---

## 💡 Usage Examples

**Plan a basic trip:**
```
Plan a 2 day trip to Tokyo
```

**Plan with budget constraint:**
```
Plan a budget-friendly 2 day trip to Paris
```

**Plan a luxury trip:**
```
Plan a luxury 2 day trip to Singapore
```

**Pet-friendly trip:**
Toggle the 🐾 Pet-friendly button ON, then:
```
Plan a 2 day trip to London
```

**Multilingual:**
```
计划一次去东京的2天旅行 (Plan a trip to Tokyo in Chinese)
சிங்கப்பூருக்கு 2 நாள் பயணம் (Plan a trip to Singapore in Tamil)
```

---

## 🧠 How Memory Works

**Short-term memory** stores your conversation history in Redis with a 1-hour TTL. This lets Claude remember context within a session — say "make it budget-friendly" after asking about Tokyo and it knows you mean Tokyo.

**Long-term memory** extracts your travel preferences after each conversation using Claude and stores them in Redis. Next time you chat, your preferences are automatically loaded and applied — even for a different city.

---

## 📚 How RAG Works

1. `ingest_data.py` fetches Wikipedia articles for 5 cities (20 articles, 311 chunks)
2. Chunks are vectorized using TF-IDF and saved to disk
3. When planning a trip, the RAG tool retrieves the 3 most relevant chunks
4. Multi-hop: first retrieval enriches the query for a second, deeper retrieval
5. Retrieved knowledge is injected into Claude's context for more accurate responses

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-city`)
3. Add your changes
4. Run tests (`pytest tests/ -v`)
5. Push and open a Pull Request

---

## 📄 License

MIT License — feel free to use this project as a reference or starting point.

---

*Built for Hipster Pte. Ltd. AI/ML Engineer Assessment — Task 2*
