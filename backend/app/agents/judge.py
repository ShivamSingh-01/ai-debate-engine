from langchain_groq import ChatGroq
from ..schemas.debate import Round, JudgeEvaluation
class DebateJudge:
    def __init__(self, api_key: str, model_name: str):
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0.3
        )
    
    async def evaluate_debate(self, topic: str, rounds: list[Round]) -> JudgeEvaluation:
        debate_text = self._format_debate(topic, rounds)
        
        prompt = f"""{debate_text}
You are an impartial debate judge. Evaluate this debate on the topic: "{topic}"
Provide your evaluation in the following format:
1. Winner: [Pro/Con/Tie]
2. Pro Score: [0-10]
3. Con Score: [0-10]
4. Reasoning: [Your detailed analysis]
5. Feedback: [3 specific points for improvement, one per line]
Be fair and objective. Consider:
- Quality of arguments
- Use of evidence and logic
- Ability to counter opponent's points
- Persuasiveness"""
        response = self.llm.invoke(prompt)
        return self._parse_evaluation(response.content)
    
    def _format_debate(self, topic: str, rounds: list[Round]) -> str:
        text = f"DEBATE TOPIC: {topic}\n\n"
        
        for round_obj in rounds:
            text += f"--- Round {round_obj.round_number} ---\n\n"
            text += f"PRO: {round_obj.pro_argument.content}\n\n"
            text += f"CON: {round_obj.con_argument.content}\n\n"
        
        return text
    
    def _parse_evaluation(self, response: str) -> JudgeEvaluation:
        lines = response.strip().split('\n')
        
        winner = "Tie"
        pro_score = 5.0
        con_score = 5.0
        reasoning = response
        feedback = []
        
        for line in lines:
            if line.startswith("Winner:"):
                winner = line.split(":", 1)[1].strip()
            elif line.startswith("Pro Score:"):
                try:
                    pro_score = float(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("Con Score:"):
                try:
                    con_score = float(line.split(":", 1)[1].strip())
                except:
                    pass
            elif line.startswith("Feedback:") or line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
                clean_line = line.lstrip("0123456789. ").strip()
                if clean_line and len(feedback) < 3:
                    feedback.append(clean_line)
        
        return JudgeEvaluation(
            winner=winner,
            pro_score=pro_score,
            con_score=con_score,
            reasoning=reasoning,
            feedback=feedback
        )