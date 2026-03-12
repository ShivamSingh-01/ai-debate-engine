from langchain_groq import ChatGroq
class DebateAgent:
    def __init__(self, api_key: str, model_name: str):
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0.7
        )
    
    async def generate_argument(self, topic: str, side: str, context: str = None) -> str:
        if side == "pro":
            prompt = self._pro_prompt(topic, context)
        else:
            prompt = self._con_prompt(topic, context)
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def _pro_prompt(self, topic: str, context: str = None) -> str:
        base = f"""You are a debate agent arguing FOR the topic: "{topic}"
        
Your goal is to present strong, logical arguments supporting this position.
Use evidence, reasoning, and compelling points to make your case.
Keep your response focused and persuasive."""
        if context:
            base += f"\n\nThe opposing side said:\n{context}\n\nProvide a counter-response that addresses their points while strengthening your argument."
        
        base += "\n\nProvide your argument (2-3 paragraphs):"
        return base
    
    def _con_prompt(self, topic: str, context: str = None) -> str:
        base = f"""You are a debate agent arguing AGAINST the topic: "{topic}"
Your goal is to present strong, logical arguments opposing this position.
Use evidence, reasoning, and compelling points to challenge the topic.
Keep your response focused and persuasive."""
        if context:
            base += f"\n\nThe supporting side said:\n{context}\n\nProvide a counter-argument that directly addresses their points."
        base += "\n\nProvide your argument (2-3 paragraphs):"
        return base