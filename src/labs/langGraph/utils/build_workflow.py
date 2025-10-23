from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[4]))

from src.models import State
from src.labs.langGraph.utils.orchestrator import orchestrator
from src.labs.langGraph.utils.researcher_worker import researcher_worker
from src.labs.langGraph.utils.analyst_synthesizer import analyst_synthesizer
from src.labs.langGraph.utils.assign_research_workers import assign_research_workers

from langgraph.graph import StateGraph, START, END

from config.config import *
from config.logger import get_logger

log = get_logger("build_workflow")


def build_workflow():
    """Build and compile the orchestrator-worker workflow"""
    
    builder = StateGraph(State)
    
    # Add nodes
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("researcher_worker", researcher_worker)
    builder.add_node("analyst_synthesizer", analyst_synthesizer)
    
    # Add edges
    builder.add_edge(START, "orchestrator")
    builder.add_conditional_edges(
        "orchestrator",
        assign_research_workers,
        ["researcher_worker"]
    )
    builder.add_edge("researcher_worker", "analyst_synthesizer")
    builder.add_edge("analyst_synthesizer", END)
    
    # Compile
    workflow = builder.compile()
        
    return workflow