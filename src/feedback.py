from typing import List
from .ai_providers import ai_provider
from .prompts import get_system_prompt

async def generate_feedback(query: str, num_questions: int = 3) -> List[str]:
    """Generate follow-up questions to clarify research direction"""
    
    prompt = f"""Given the following query from the user, ask some follow up questions to clarify the research direction. Return a maximum of {num_questions} questions, but feel free to return less if the original query is clear: <query>{query}</query>"""
    
    schema = {
        "questions": {
            "type": "array",
            "items": {"type": "string"},
            "description": f"Follow up questions to clarify the research direction, max of {num_questions}"
        }
    }
    
    result = ai_provider.generate_object(get_system_prompt(), prompt, schema)
    questions = result.get("questions", [])[:num_questions]
    
    return questions