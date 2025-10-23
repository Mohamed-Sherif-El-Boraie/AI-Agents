from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[4]))

from src.models import State, ResearchQuery

from config.config import *
from config.logger import get_logger

log = get_logger("orchestrator")

def orchestrator(state: State) -> dict:
    """
    Orchestrator that creates a single research query.
    """
    topic = state["topic"]
    
    log.info(f"[Orchestrator] Planning research for topic: '{topic}'")
    
    # Create a single query directly
    query = ResearchQuery(
        query=topic,
        focus=f"General information about {topic}"
    )
        
    return {"queries": [query]}