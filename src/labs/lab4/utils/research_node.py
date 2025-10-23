from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import QualityState
from src.tools.insert import search_and_insert

from langchain.messages import HumanMessage, SystemMessage, AIMessage


from config.config import *
from config.logger import get_logger

log = get_logger("researcher_node")

def research_node(state: QualityState) -> dict:
    """
    Researcher: Searches and stores data.
    Can be called multiple times based on evaluator feedback.
    """
    topic = state["topic"]
    iteration = state.get("iteration_count", 0)
    feedback = state.get("feedback", "")
    
    if iteration > 0:
        log.info(f"[Researcher] Iteration {iteration}: Addressing feedback")
        log.info(f"  Feedback: {feedback}")
    else:
        log.info(f"[Researcher] Starting initial research on '{topic}'")
    
    # Perform search (increase max_items if reiteration based on feedback)
    max_items = 1 if iteration == 0 else 2
    result = search_and_insert({"topic": topic}, max_items=max_items)
    
    research_done = result.get("research_done", False)
    
    log.info(f"[Researcher] Research completed. Items found: {len(result.get('data', []))}")
    
    return {
        "research_complete": research_done,
        "iteration_count": iteration + 1,
        "messages": [AIMessage(content=f"[Research] Completed")],
        "current_agent": "chief_researcher" 
    }
