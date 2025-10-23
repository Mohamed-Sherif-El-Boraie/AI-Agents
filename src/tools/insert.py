from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]))

from langchain.tools import tool


from src.tools.web_search import web_search
from src.db_schema import insert_findings
from src.models import ResearchTask, GraphState

from config.logger import get_logger

log = get_logger("insert_tool")


def search_and_insert(state: GraphState, max_items: int = 1) -> GraphState:
    '''
    Search for relevant findings and insert them into the database.
    '''
    topic = state["topic"]
    task = ResearchTask(topic=topic, max_items=max_items)
    data = []
    for f in web_search(task.topic, task.max_items):
        data.append((f.topic, str(f.source_url) if f.source_url else None, f.snippet))
        log.info(f"Found snippet from {f.source_url}")

    count = insert_findings(data)
    log.info(f"Inserted {count} findings for topic='{task.topic}'.")
    try:
        return {"research_done": True, "data": data}
    except Exception as e:
        log.error(f"Error occurred while finalizing research for topic='{task.topic}': {e}")
        return {"research_done": False, "error": str(e)}


@tool
def researcher_tool(topic: str) -> str:
    """Search for relevant findings and insert them into the DB."""
    log.info(f"[Researcher] Gathering info for '{topic}'...")
    return search_and_insert({"topic": topic}, max_items=1)

# @tool
# def researcher_tool(topic: str) -> str:
#     """Search for relevant findings and insert them into the DB."""
#     log.info(f"[Researcher] Gathering info for '{topic}'...")
#     result = search_and_insert({"topic": topic}, max_items=1)
    
#     # Return a clear message the agent can understand
#     if result.get("research_done"):
#         return f"Successfully researched and stored {len(result.get('data', []))} findings about '{topic}' in the database."
#     else:
#         return f"Failed to research topic: {result.get('error', 'Unknown error')}"