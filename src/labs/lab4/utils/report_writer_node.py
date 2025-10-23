from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import QualityState
from src.llm import model as llm
from src.db_schema import read_findings

from langchain.messages import HumanMessage, SystemMessage, AIMessage


from config.config import *
from config.logger import get_logger

log = get_logger("report_writer")


def report_writer_node(state: QualityState) -> dict:
    """
    Report Writer: Creates report from database.
    Uses feedback from evaluator to improve.
    """
    topic = state["topic"]
    feedback = state.get("feedback", "")
    iteration = state.get("iteration_count", 1)
    
    log.info(f"[Report Writer] Creating report (Iteration {iteration})")
    
    # Retrieve findings from database
    records = read_findings(topic, limit=20)
    
    if not records:
        return {
            "report_text": f"No findings found for '{topic}'.",
            "approved": False
        }
    
    # Build context
    context = "\n\n".join([
        f"Finding {i+1}:\n{record[3]}\nSource: {record[2]}" 
        for i, record in enumerate(records)
    ])
    
    # Create prompt with feedback if available
    if feedback:
        system_content = f"""You are a Report Writer. Create a comprehensive research report.

Previous feedback to address:
{feedback}

Improve the report based on this feedback."""
    else:
        system_content = "You are a Report Writer. Create a comprehensive, well-structured research report with clear sections, key findings, and insights."
    
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=f"Topic: {topic}\n\nFindings:\n{context}\n\nWrite a professional report.")
    ]
    
    result = llm.invoke(messages)
    report = result.content
    
    log.info(f"[Report Writer] Report generated ({len(report)} characters)")
    
    return {
        "report_text": report,
        "report_complete": True, 
        "messages": [AIMessage(content=f"[Report Writer] Done")], 
        "current_agent": "chief_researcher"
    }