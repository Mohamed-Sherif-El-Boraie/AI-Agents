from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))

from langchain.tools import tool


from src.db_schema import read_findings
from src.models import ResearchTask, GraphState

from config.logger import get_logger

log = get_logger("insert_tool")


@tool
def retrieve_findings(topic: str) -> str:
    """Search the database for findings about the topic"""
    log.info(f"[Analyst] Retrieving findings for '{topic}'...")
    records = read_findings(topic, limit=10)
    if not records:
        return f"Database search complete. No findings found for topic '{topic}'."
    
    findings_text = f"Database search complete. Found {len(records)} finding(s) for '{topic}':\n\n"
    for i, record in enumerate(records, 1):
        snippet = record[3]
        source = record[2]
        findings_text += f"{i}. {snippet}\n   Source: {source}\n\n"
        log.info(f"Retrieved snippet: {record[1]} from {source}")
    
    findings_text += "Now summarize these findings into concise bullets."
    return findings_text
    
    
# def retrieve_findings(state: GraphState, max_items: int = 1) -> GraphState:
#     '''
#     Search for relevant topic from DB
#     '''
#     topic = state["topic"]
#     data = []
#     records = read_findings(topic, limit=max_items)
#     for record in records:
#         data.append({
#             "topic": record[1],
#             "source_url": record[2],
#             "snippet": record[3]
#         })
#         log.info(f"Retrieved snippet: {record[1]} from {record[2]}")

#     try:
#         return {"research_done": True, "data": data}
#     except :
#         log.warning(f"Error occurred while finalizing research for topic='{topic}")
#         return {"research_done": False, "Didn't find relevant data about topic": topic}


# @tool
# def retrieve_tool(topic: str) -> str:
#     """Search for relevant findings from DB."""
#     log.info(f"[Researcher] Gathering info for '{topic}'...")
#     return retrieve_findings({"topic": topic}, max_items=1)
