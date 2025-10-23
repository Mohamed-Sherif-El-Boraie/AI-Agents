from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import QualityState

from config.config import *
from config.logger import get_logger

log = get_logger("routing")

# Routing Logic
def route_after_evaluation(state: QualityState) -> str:
    """
    Route based on evaluation results.
    Implements the evaluator-optimizer routing pattern.
    """
    approved = state.get("approved", False)
    iteration = state.get("iteration_count", 0)
    max_iterations = state.get("max_iterations", 3)
    
    if approved:
        log.info("[Router] Report approved! Moving to completion.")
        return "approved"
    elif iteration >= max_iterations:
        log.warning(f"[Router] Max iterations ({max_iterations}) reached. Accepting current report.")
        return "max_iterations_reached"
    else:
        log.info(f"[Router] Report needs improvement. Iteration {iteration}/{max_iterations}. Going back to research.")
        return "needs_improvement"


def route_next_agent(state: QualityState) -> str:
    """Route based on Chief's decision"""
    return state.get("current_agent", "chief_researcher")

def should_continue(state: QualityState) -> str:
    """Check if workflow should continue"""
    if state.get("current_agent") == "complete":
        return "end"
    return "continue"
