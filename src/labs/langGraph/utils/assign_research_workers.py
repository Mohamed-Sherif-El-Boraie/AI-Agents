from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[4]))

from typing import List
from src.models import State

from langgraph.types import Send

from config.config import *
from config.logger import get_logger

log = get_logger("assign_research_workers")

# Conditional Edge Function
def assign_research_workers(state: State) -> List[Send]:
    """
    Assign a researcher worker to query in the plan.
    Each query gets its own worker.
    """
    
    # Create a worker for each research query
    return [
        Send("researcher_worker", {"query": q, "topic": state["topic"]})  #Send: A message or packet to send to a specific node in the graph
        for q in state["queries"]
    ]
