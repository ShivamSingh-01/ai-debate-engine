from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DebateTopic(BaseModel):
    topic: str
    rounds: int = 3

class FactCheckResult(BaseModel):
    claim: str
    is_verified: bool
    verification_details: str
    sources: List[str] = []

class Argument(BaseModel):
    agent: str
    content: str
    fact_checks: List[FactCheckResult] = []

class Round(BaseModel):
    round_number: int
    pro_argument: Argument
    con_argument: Argument

class JudgeEvaluation(BaseModel):
    winner: str
    pro_score: float
    con_score: float
    reasoning: str
    feedback: List[str] = []

class DebateSession(BaseModel):
    session_id: str
    topic: str
    rounds: List[Round] = []
    judge_evaluation: Optional[JudgeEvaluation] = None
    status: str = "in_progress"
    created_at: Optional[datetime] = None

class DebateResponse(BaseModel):
    session_id: str
    message: str
    current_round: Optional[Round] = None
    judge_evaluation: Optional[JudgeEvaluation] = None
    is_complete: bool = False