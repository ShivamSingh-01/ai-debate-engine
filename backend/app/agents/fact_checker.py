from tavily import TavilyClient
import re
from ..schemas.debate import FactCheckResult
class FactChecker:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)
    
    async def check_claims(self, text: str) -> list[FactCheckResult]:
        claims = self._extract_claims(text)
        results = []
        
        for claim in claims[:5]:
            try:
                search_result = self.client.search(
                    query=claim,
                    max_results=2
                )
                
                sources = [r.get("url", "") for r in search_result.get("results", [])]
                
                verified = len(sources) > 0
                details = self._generate_verification_details(verified, search_result)
                
                results.append(FactCheckResult(
                    claim=claim,
                    is_verified=verified,
                    verification_details=details,
                    sources=sources
                ))
            except Exception as e:
                results.append(FactCheckResult(
                    claim=claim,
                    is_verified=False,
                    verification_details=f"Could not verify claim: {str(e)}",
                    sources=[]
                ))
        
        return results
    
    def _extract_claims(self, text: str) -> list[str]:
        sentences = re.split(r'[.!?]+', text)
        claims = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 30 and any(word in sentence.lower() for word in [
                "percent", "studies show", "research", "according to", 
                "data", "statistics", "evidence", "fact", "proven"
            ]):
                claims.append(sentence)
        
        return claims[:5]
    
    def _generate_verification_details(self, verified: bool, search_result: dict) -> str:
        if verified:
            results = search_result.get("results", [])
            if results:
                return f"Found {len(results)} source(s) supporting this claim"
        return "No verification sources found"