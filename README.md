# AI Debate Engine


**AI Debate Engine** is a multi-agent GenAI application where two AI agents debate a topic (Pro vs Con), verify claims using web search, and a third AI agent acts as a judge to evaluate the debate.

It demonstrates a practical **LLM orchestration system with fact-checking and evaluation.**

---

## Features

* **AI Debate Agents** – Pro and Con agents argue different sides of a topic
* **Fact Checking** – Claims verified using Tavily web search
* **AI Judge** – Evaluates debate quality and selects a winner
* **Multiple Rounds** – Arguments evolve across several debate rounds
* **Interactive UI** – Users can start debates on any topic

---

## Tech Stack

**Backend**

* FastAPI
* LangChain
* Groq LLM (Llama-3)
* Tavily Search API

**Frontend**

* React
* Vite
* Tailwind CSS

**DevOps**

* Docker
* Docker Compose

---

## Architecture

```id="x5a2sk"
User
  ↓
React UI
  ↓
FastAPI Backend
  ↓
Pro Agent → Fact Check
  ↓
Con Agent → Fact Check
  ↓
Multiple Debate Rounds
  ↓
AI Judge Evaluation
```

---

## Project Structure

```id="n29p4e"
ai-debate-engine
│
├── backend
│   ├── app
│   │   ├── agents
│   │   ├── schemas
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── src
│   ├── package.json
│   └── vite.config.js
│
└── docker-compose.yml
```

---

## Local Setup

### 1️⃣ Backend

```id="d9h4ml"
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```id="3kk0zj"
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
```

Run backend:

```id="ztyo7u"
uvicorn app.main:app --reload
```

---

### 2️⃣ Frontend

```id="3j2hfd"
cd frontend
npm install
npm run dev
```

Open:

```id="r2hndx"
http://localhost:5173
```

---

## Run with Docker

Run the entire system with one command:

```id="n6fjpt"
docker compose up --build
```

---

## Example Topics

* Should AI replace teachers?
* Is remote work better than office work?
* Should social media be regulated?
* Is cryptocurrency the future of finance?

---

## Author

**Shivam Singh**

---

## License

MIT License
