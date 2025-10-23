from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import QualityState
from src.labs.lab4.utils.chief_researcher_node import chief_researcher_node
from src.labs.lab4.utils.research_node import research_node
from src.labs.lab4.utils.report_writer_node import report_writer_node
from src.labs.lab4.utils.evaluator_node import evaluator_node
from src.labs.lab4.utils.route_after_evaluation import should_continue, route_next_agent
 
from langgraph.graph import StateGraph, START, END

from config.config import *
from config.logger import get_logger

log = get_logger("routing")


# Workflow 
def build_workflow():
    """Build workflow with Chief + quality control"""
    builder = StateGraph(QualityState)
    
    # Add all nodes
    builder.add_node("chief_researcher", chief_researcher_node)
    builder.add_node("research", research_node)
    builder.add_node("report_writer", report_writer_node)
    builder.add_node("evaluator", evaluator_node)
    
    # Start with Chief
    builder.add_edge(START, "chief_researcher")
    
    # Chief delegates or completes
    builder.add_conditional_edges("chief_researcher", should_continue,
        {"continue": "router", "end": END}
    )
    
    # Router distributes work
    builder.add_node("router", lambda s: s)
    builder.add_conditional_edges("router", route_next_agent,
        {
            "research": "research",
            "report_writer": "report_writer",
            "evaluator": "evaluator",
            "chief_researcher": "chief_researcher",
            "complete": END
        }
    )
    
    # Workers report to Chief
    builder.add_edge("research", "chief_researcher")
    builder.add_edge("report_writer", "chief_researcher")
    builder.add_edge("evaluator", "chief_researcher")
    
    workflow = builder.compile()
    return workflow

