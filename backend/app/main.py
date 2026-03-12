from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid
from datetime import datetime
from .config import settings
from .schemas.debate import (
    DebateTopic, DebateSession, DebateResponse, 
    Round, Argument, FactCheckResult, JudgeEvaluation
)
from .agents.debate_agent import DebateAgent
from .agents.fact_checker import FactChecker
from .agents.judge import DebateJudge
debate_sessions: dict[str, DebateSession] = {}
agents: dict = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    global agents
    agents["debate"] = DebateAgent(settings.groq_api_key, settings.model_name)
    agents["fact_checker"] = FactChecker(settings.tavily_api_key)
    agents["judge"] = DebateJudge(settings.groq_api_key, settings.model_name)
    yield
app = FastAPI(title="AI Debate Engine", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/debate/start", response_model=DebateResponse)
async def start_debate(topic: DebateTopic):
    session_id = str(uuid.uuid4())
    
    session = DebateSession(
        session_id=session_id,
        topic=topic.topic,
        created_at=datetime.now()
    )
    debate_sessions[session_id] = session
    
    return DebateResponse(
        session_id=session_id,
        message=f"Debate started on topic: {topic.topic}",
        is_complete=False
    )
@app.post("/api/debate/{session_id}/round", response_model=DebateResponse)
async def execute_round(session_id: str):
    if session_id not in debate_sessions:
        return DebateResponse(
            session_id=session_id,
            message="Session not found",
            is_complete=True
        )
    
    session = debate_sessions[session_id]
    current_round = len(session.rounds) + 1
    
    if current_round > settings.debate_rounds:
        return DebateResponse(
            session_id=session_id,
            message="All rounds complete",
            is_complete=True
        )
    
    debate_agent = agents["debate"]
    fact_checker = agents["fact_checker"]
    
    if current_round == 1:
        pro_arg = await debate_agent.generate_argument(
            session.topic, "pro", None
        )
    else:
        last_round = session.rounds[-1]
        pro_arg = await debate_agent.generate_argument(
            session.topic, "pro", last_round.con_argument.content
        )
    
    pro_fact_checks = await fact_checker.check_claims(pro_arg)
    pro_argument = Argument(
        agent="Pro",
        content=pro_arg,
        fact_checks=pro_fact_checks
    )
    
    con_arg = await debate_agent.generate_argument(
        session.topic, "con", pro_argument.content
    )
    con_fact_checks = await fact_checker.check_claims(con_arg)
    con_argument = Argument(
        agent="Con",
        content=con_arg,
        fact_checks=con_fact_checks
    )
    
    round_obj = Round(
        round_number=current_round,
        pro_argument=pro_argument,
        con_argument=con_argument
    )
    session.rounds.append(round_obj)
    
    return DebateResponse(
        session_id=session_id,
        message=f"Round {current_round} complete",
        current_round=round_obj,
        is_complete=False
    )
@app.post("/api/debate/{session_id}/judge", response_model=DebateResponse)
async def get_judgment(session_id: str):
    if session_id not in debate_sessions:
        return DebateResponse(
            session_id=session_id,
            message="Session not found",
            is_complete=True
        )
    
    session = debate_sessions[session_id]
    
    if not session.rounds:
        return DebateResponse(
            session_id=session_id,
            message="No rounds to judge",
            is_complete=True
        )
    
    judge = agents["judge"]
    evaluation = await judge.evaluate_debate(session.topic, session.rounds)
    
    session.judge_evaluation = evaluation
    session.status = "completed"
    
    return DebateResponse(
        session_id=session_id,
        message="Debate complete",
        judge_evaluation=evaluation,
        is_complete=True
    )
@app.get("/api/debate/{session_id}")
async def get_debate(session_id: str):
    if session_id not in debate_sessions:
        return {"error": "Session not found"}
    
    return debate_sessions[session_id]