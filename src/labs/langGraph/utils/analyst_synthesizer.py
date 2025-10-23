from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[4]))

from src.llm import model as llm
from src.models import State

from langchain.messages import HumanMessage, SystemMessage


from src.db_schema import read_findings

from config.config import *
from config.logger import get_logger

log = get_logger("analyst_synthesizer")


# Analyst Synthesizer Function
def analyst_synthesizer(state: State) -> dict:
    """
    Synthesizer that combines all research findings into a final summary.
    Retrieves data from database and generates comprehensive summary.
    """
    topic = state["topic"]
    completed_research = state["completed_research"]
    
    log.info(f"[Analyst] Synthesizing {len(completed_research)} research results for '{topic}'")
    
    # Retrieve all findings from database
    records = read_findings(topic, limit=20)
    
    if not records:
        summary = f"No findings were stored for topic '{topic}'."
        log.warning(f"[Analyst] No findings found in database")
    else:
        # Build comprehensive context from all findings
        context = "\n\n".join([
            f"Finding {i+1}:\n{record[3]}\nSource: {record[2]}"  # 3 Snippet and 2 Source URL
            for i, record in enumerate(records)
        ])
        
        # Generate research summary
        research_summary = "\n".join([
            f"- {r['focus']}: {r['findings_count']} findings" 
            for r in completed_research
        ])
        
        log.info(f"[Analyst] Retrieved {len(records)} total findings from database")
        
        # Create final summary using LLM
        messages = [
            SystemMessage(
                content="""You are a research analyst. Create a comprehensive summary 
                of the research findings. Organize the information logically with 
                bullet points and include key insights. Use markdown formatting."""
            ),
            HumanMessage(
                content=f"""Topic: {topic}

Research completed:
{research_summary}

All findings:
{context}

Create a well-organized summary of these findings."""
            )
        ]
        
        result = llm.invoke(messages)
        summary = result.content
        log.info(f"[Analyst] Generated final summary for '{topic}'")
    
    return {"final_summary": summary}
