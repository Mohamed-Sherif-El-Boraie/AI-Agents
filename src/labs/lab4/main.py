from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from typing import List, Annotated, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from src.llm import model as llm
from src.models import QualityState, TaskDelegation, ReportQuality
from src.tools.insert import search_and_insert
from src.db_schema import read_findings

from src.labs.lab4.utils.chief_researcher_node import chief_researcher_node
from src.labs.lab4.utils.research_node import research_node
from src.labs.lab4.utils.report_writer_node import report_writer_node
from src.labs.lab4.utils.evaluator_node import evaluator_node
from src.labs.lab4.utils.route_after_evaluation import should_continue, route_next_agent
from src.labs.lab4.utils.build_workflow import build_workflow
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from config.config import *
from config.logger import get_logger

log = get_logger("research_with_quality_control")



if __name__ == "__main__":
    
    log.info("Multi-Agent System with Quality Control")
    topic = input("\nEnter research topic: ").strip()
    
    if not topic:
        log.error("No topic provided. Exiting.")
        sys.exit(1)
    
    max_iterations = int(input("Max quality iterations (default 3): ").strip() or "3")
    
    # Build workflow
    workflow = build_workflow()
    
    # Initialize state
    initial_state = {
        "topic": topic,
        "messages": [HumanMessage(content=f"Research: {topic}")], 
        "current_agent": "chief_researcher", 
        "research_complete": False,
        "report_complete": False, 
        "report_text": "",
        "quality_grade": "",
        "feedback": "",
        "approved": False,
        "iteration_count": 0,
        "max_iterations": max_iterations
    }
    
    # Execute workflow
    log.info(f"\n[Starting] Quality-controlled research on: '{topic}'\n")
    
    try:
        result = workflow.invoke(initial_state)
        

        log.info("RESEARCH COMPLETE")
        log.info(f"Topic: {result['topic']}")
        log.info(f"Final Grade: {result['quality_grade']}")
        log.info(f"Approved: {result['approved']}")
        log.info(f"Iterations: {result['iteration_count']}/{result['max_iterations']}")

        if result.get('feedback') and not result['approved']:
            log.info(f"Final Feedback: {result['feedback']}")

        log.info("FINAL REPORT")
        log.info(result['report_text'])

        
    except Exception as e:
        log.error(f"Error during workflow execution: {e}")
        import traceback
        log.error(traceback.format_exc())