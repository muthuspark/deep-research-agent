import asyncio
from typing import List, Dict, Any, Optional, NamedTuple
from dataclasses import dataclass
from .ai_providers import ai_provider
from .prompts import get_system_prompt
from .firecrawl_client import firecrawl

@dataclass
class ResearchResult:
    learnings: List[str]
    visited_urls: List[str]

class SerpQuery(NamedTuple):
    query: str
    research_goal: str

async def generate_serp_queries(
    query: str, 
    num_queries: int = 3, 
    learnings: Optional[List[str]] = None
) -> List[SerpQuery]:
    """Generate SERP queries for research"""
    
    learnings_text = ""
    if learnings:
        learnings_text = f"\n\nHere are some learnings from previous research, use them to generate more specific queries: {' '.join(learnings)}"
    
    prompt = f"""Given the following prompt from the user, generate a list of SERP queries to research the topic. Return a maximum of {num_queries} queries, but feel free to return less if the original prompt is clear. Make sure each query is unique and not similar to each other: <prompt>{query}</prompt>{learnings_text}"""
    
    schema = {
        "queries": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SERP query"
                    },
                    "research_goal": {
                        "type": "string",
                        "description": "First talk about the goal of the research that this query is meant to accomplish, then go deeper into how to advance the research once the results are found, mention additional research directions. Be as specific as possible, especially for additional research directions."
                    }
                },
                "required": ["query", "research_goal"]
            },
            "description": f"List of SERP queries, max of {num_queries}"
        }
    }
    
    result = ai_provider.generate_object(get_system_prompt(), prompt, schema)
    queries = result.get("queries", [])[:num_queries]
    
    print(f"Created {len(queries)} queries: {[q['query'] for q in queries]}")
    
    return [SerpQuery(q["query"], q["research_goal"]) for q in queries]

async def process_serp_result(
    query: str,
    search_result: Dict[str, Any],
    num_learnings: int = 3,
    num_follow_up_questions: int = 3
) -> Dict[str, Any]:
    """Process search results to extract learnings and follow-up questions"""
    
    # Extract markdown content from results
    contents = []
    for item in search_result.get("data", []):
        if item.get("markdown"):
            # Trim content to reasonable size
            content = ai_provider.trim_prompt(item["markdown"], 25000)
            contents.append(content)
    
    print(f"Ran {query}, found {len(contents)} contents")
    
    if not contents:
        return {"learnings": [], "follow_up_questions": []}
    
    contents_text = "\n".join([f"<content>\n{content}\n</content>" for content in contents])
    
    prompt = f"""Given the following contents from a SERP search for the query <query>{query}</query>, generate a list of learnings from the contents. Return a maximum of {num_learnings} learnings, but feel free to return less if the contents are clear. Make sure each learning is unique and not similar to each other. The learnings should be concise and to the point, as detailed and information dense as possible. Make sure to include any entities like people, places, companies, products, things, etc in the learnings, as well as any exact metrics, numbers, or dates. The learnings will be used to research the topic further.

<contents>{contents_text}</contents>"""
    
    schema = {
        "learnings": {
            "type": "array",
            "items": {"type": "string"},
            "description": f"List of learnings, max of {num_learnings}"
        },
        "follow_up_questions": {
            "type": "array",
            "items": {"type": "string"},
            "description": f"List of follow-up questions to research the topic further, max of {num_follow_up_questions}"
        }
    }
    
    result = ai_provider.generate_object(get_system_prompt(), ai_provider.trim_prompt(prompt), schema)
    learnings = result.get("learnings", [])
    follow_up_questions = result.get("follow_up_questions", [])
    
    print(f"Created {len(learnings)} learnings: {learnings}")
    
    return {
        "learnings": learnings,
        "follow_up_questions": follow_up_questions
    }

async def deep_research(
    query: str,
    breadth: int,
    depth: int,
    learnings: Optional[List[str]] = None,
    visited_urls: Optional[List[str]] = None
) -> ResearchResult:
    """Perform deep research on a topic"""
    
    if learnings is None:
        learnings = []
    if visited_urls is None:
        visited_urls = []
    
    print(f"Starting research with breadth={breadth}, depth={depth}")
    
    # Generate search queries
    serp_queries = await generate_serp_queries(query, breadth, learnings)
    
    # Process all queries concurrently
    tasks = []
    for serp_query in serp_queries:
        task = process_single_query(serp_query, breadth, depth, learnings, visited_urls)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Combine results
    all_learnings = set(learnings)
    all_urls = set(visited_urls)
    
    for result in results:
        if isinstance(result, Exception):
            print(f"Error in research: {result}")
            continue
        
        if isinstance(result, ResearchResult):
            all_learnings.update(result.learnings)
            all_urls.update(result.visited_urls)
    
    return ResearchResult(
        learnings=list(all_learnings),
        visited_urls=list(all_urls)
    )

async def process_single_query(
    serp_query: SerpQuery,
    breadth: int,
    depth: int,
    learnings: List[str],
    visited_urls: List[str]
) -> ResearchResult:
    """Process a single search query"""
    
    try:
        # Perform search
        search_result = await firecrawl.search(serp_query.query, limit=5)
        
        # Extract URLs
        new_urls = []
        for item in search_result.get("data", []):
            if item.get("url"):
                new_urls.append(item["url"])
        
        # Process results
        processed_result = await process_serp_result(
            serp_query.query,
            search_result,
            num_follow_up_questions=max(1, breadth // 2)
        )
        
        current_learnings = learnings + processed_result["learnings"]
        current_urls = visited_urls + new_urls
        
        # If we have more depth, continue research
        if depth > 1:
            new_breadth = max(1, breadth // 2)
            new_depth = depth - 1
            
            print(f"Researching deeper, breadth: {new_breadth}, depth: {new_depth}")
            
            # Create next query from follow-up questions
            next_query = f"""
            Previous research goal: {serp_query.research_goal}
            Follow-up research directions: {' '.join(processed_result['follow_up_questions'])}
            """.strip()
            
            return await deep_research(
                next_query,
                new_breadth,
                new_depth,
                current_learnings,
                current_urls
            )
        else:
            return ResearchResult(
                learnings=current_learnings,
                visited_urls=current_urls
            )
    
    except Exception as e:
        print(f"Error processing query {serp_query.query}: {e}")
        return ResearchResult(learnings=learnings, visited_urls=visited_urls)

async def write_final_report(
    prompt: str,
    learnings: List[str],
    visited_urls: List[str]
) -> str:
    """Generate final research report"""
    
    learnings_text = "\n".join([f"<learning>\n{learning}\n</learning>" for learning in learnings])
    
    report_prompt = f"""Given the following prompt from the user, write a final report on the topic using the learnings from research. Make it as detailed as possible, aim for 3 or more pages, include ALL the learnings from research:

<prompt>{prompt}</prompt>

Here are all the learnings from previous research:

<learnings>
{learnings_text}
</learnings>"""
    
    schema = {
        "report_markdown": {
            "type": "string",
            "description": "Final report on the topic in Markdown"
        }
    }
    
    result = ai_provider.generate_object(
        get_system_prompt(),
        ai_provider.trim_prompt(report_prompt),
        schema
    )
    
    report = result.get("report_markdown", "")
    
    # Add sources section
    sources_section = f"\n\n## Sources\n\n" + "\n".join([f"- {url}" for url in visited_urls])
    
    return report + sources_section

async def write_final_answer(
    prompt: str,
    learnings: List[str]
) -> str:
    """Generate final concise answer"""
    
    learnings_text = "\n".join([f"<learning>\n{learning}\n</learning>" for learning in learnings])
    
    answer_prompt = f"""Given the following prompt from the user, write a final answer on the topic using the learnings from research. Follow the format specified in the prompt. Do not yap or babble or include any other text than the answer besides the format specified in the prompt. Keep the answer as concise as possible - usually it should be just a few words or maximum a sentence. Try to follow the format specified in the prompt (for example, if the prompt is using Latex, the answer should be in Latex. If the prompt gives multiple answer choices, the answer should be one of the choices).

<prompt>{prompt}</prompt>

Here are all the learnings from research on the topic that you can use to help answer the prompt:

<learnings>
{learnings_text}
</learnings>"""
    
    schema = {
        "exact_answer": {
            "type": "string",
            "description": "The final answer, make it short and concise, just the answer, no other text"
        }
    }
    
    result = ai_provider.generate_object(
        get_system_prompt(),
        ai_provider.trim_prompt(answer_prompt),
        schema
    )
    
    return result.get("exact_answer", "")