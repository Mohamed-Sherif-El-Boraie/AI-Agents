from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.models import QualityState
from src.models import ReportQuality
from src.llm import model as llm
from langchain.messages import HumanMessage, SystemMessage, AIMessage


from config.config import *
from config.logger import get_logger

log = get_logger("evaluator_node")

def evaluator_node(state: QualityState) -> dict:
    """
    Quality Evaluator: Assesses report quality and provides feedback.
    Implements the evaluator pattern from documentation.
    """
    topic = state["topic"]
    report = state["report_text"]
    iteration = state.get("iteration_count", 1)
    
    log.info(f"[Evaluator] Assessing report quality (Iteration {iteration})")
    
    # Evaluate the report
    evaluation = quality_evaluator.invoke([
        SystemMessage(
            content="""You are a Quality Evaluator for research reports. Assess:
1. Completeness: Does it cover the topic thoroughly?
2. Structure: Is it well-organized with clear sections?
3. Insights: Does it provide meaningful analysis?
4. Sources: Are findings properly referenced?

Grade as: excellent, good, or needs_improvement
Approve if grade is excellent or good."""
        ),
        HumanMessage(content=f"Topic: {topic}\n\nReport:\n{report}\n\nEvaluate this report.")
    ])
    
    log.info(f"[Evaluator] Grade: {evaluation.grade}")
    log.info(f"[Evaluator] Completeness: {evaluation.completeness_score}/10")
    log.info(f"[Evaluator] Approved: {evaluation.approved}")
    
    if not evaluation.approved:
        log.info(f"[Evaluator] Feedback: {evaluation.feedback}")
    
    return {
        "quality_grade": evaluation.grade,
        "feedback": evaluation.feedback,
        "approved": evaluation.approved,
        "research_complete": evaluation.approved,  
        "report_complete": evaluation.approved,  
        "messages": [AIMessage(content=f"[Evaluator] Grade: {evaluation.grade}")],  
        "current_agent": "chief_researcher" 
    }
#  Quality Evaluator LLM
quality_evaluator = llm.with_structured_output(ReportQuality)