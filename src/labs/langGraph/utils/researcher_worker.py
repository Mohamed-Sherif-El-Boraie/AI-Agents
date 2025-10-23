from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[4]))

from src.models import WorkerState , ResearchQuery
from src.tools.insert import search_and_insert
from src.llm import model as llm


from config.config import *
from config.logger import get_logger

log = get_logger("researcher_worker")


def researcher_worker(state: WorkerState) -> dict:
    """
    Worker that executes a single research query.
    Searches the web and stores findings in the database.
    """
    query = state["query"]
    topic = state["topic"]
    
    log.info(f"[Researcher Worker] Researching: '{query.query}'")
    
    # Execute the search and insert
    result = search_and_insert({"topic": topic}, max_items=1)
    
    # Format the result for the completed research
    research_result = {
        "query": query.query,
        "focus": query.focus,
        "success": result.get("research_done", False),
        "findings_count": len(result.get("data", []))
    }
    
    log.info(f"[Researcher Worker] Completed: {query.focus} - {research_result['findings_count']} findings")
    
    return {"completed_research": [research_result]}


# LLM with structured output for planning
planner = llm.with_structured_output(ResearchQuery)
