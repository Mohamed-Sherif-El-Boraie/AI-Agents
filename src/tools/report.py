from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))

from langchain.tools import tool

from src.llm import groq_chat
from src.db_schema import read_findings
from src.models import GraphState

from config.logger import get_logger

log = get_logger("report_tool")


def report(state: GraphState) -> GraphState:
    '''Read findings from DB and summarize them.'''
    data = read_findings(state["topic"], limit=10)
    context = "\n\n".join(x[3] for x in data)
    messages = [
        {"role": "system", "content": "You are a precise technical report analyst."},
        {"role": "user", "content": f"Summarize the following into concise bullets:\n{context}"}
    ]
    
    # Generate the report using Groq
    text = groq_chat(messages)
    log.info(f"Generated report for topic='{state['topic']}'.")
    try:
        return {"research_done": True, "report_text": text}
    except Exception as e:
        log.error(f"Error occurred while generating report for topic='{state['topic']}': {e}")
        return {"research_done": False, "report_text": "Error occurred while generating report."}



@tool
def analyst_tool(topic: str) -> str:
    """Read findings from DB and summarize them."""
    log.info(f"[Analyst] Summarizing findings for '{topic}'...")
    return report({"topic": topic}) 