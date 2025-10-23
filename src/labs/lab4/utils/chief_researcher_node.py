from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import QualityState
from src.models import TaskDelegation
from src.llm import model as llm

from langchain.messages import HumanMessage, SystemMessage, AIMessage


from config.config import *
from config.logger import get_logger

log = get_logger("chief_researcher")

def chief_researcher_node(state: QualityState) -> dict:
    """Chief Researcher manages workflow"""
    topic = state["topic"]
    research_complete = state.get("research_complete", False)
    report_complete = state.get("report_complete", False)
    approved = state.get("approved", False)
    
    log.info(f"[Chief Researcher] Evaluating status")
    log.info(f"  Research: {research_complete} | Report: {report_complete} | Approved: {approved}")
    
    if not research_complete:
        context = "Need research"
        available = ["research"]
    elif not report_complete:
        context = "Need report"
        available = ["report_writer"]
    elif not approved:
        context = "Need quality check"
        available = ["evaluator"]
    else:
        context = "Complete"
        available = ["complete"]
    
    decision = chief_planner.invoke([
        SystemMessage(content=f"Choose next agent from: {available}. Context: {context}"),
        HumanMessage(content=f"What's next for '{topic}'?")
    ])
    
    log.info(f"[Chief] Decision: {decision.next_agent}")
    log.info(f"[Chief] Reasoning: {decision.reasoning}")
    
    return {
        "messages": [AIMessage(content=f"[Chief → {decision.next_agent}]")],
        "current_agent": decision.next_agent
    }
    
# Chief Planner LLM
chief_planner = llm.with_structured_output(TaskDelegation)