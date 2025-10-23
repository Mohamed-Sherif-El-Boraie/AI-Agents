from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, TypedDict , Literal
from typing_extensions import TypedDict, Annotated
import operator
from langchain.messages import AnyMessage

# Core Tools Models
class ResearchTask(BaseModel):
    topic: str  # Research topic
    max_items: int = Field(default=1) # Max findings to retrieve

class Finding(BaseModel):
    topic: str 
    source_url: Optional[HttpUrl] = None
    snippet: str

class GraphState(TypedDict, total=False):
    topic: str
    research_done: bool # Flag indicating if research is complete
    report_text: str # Final report text
    
    
# LangGraph Lab State Definitions
class ResearchQuery(BaseModel):
    """A specific research query to investigate"""
    query: str = Field(
        description="A specific search query to research about the topic"
    )
    focus: str = Field(
        description="What aspect of the topic this query focuses on"
    )

class State(TypedDict):
    """Main graph state"""
    topic: str  # Main research topic
    queries: List[ResearchQuery]  # Planned research queries
    completed_research: Annotated[list, operator.add]  # Results from all workers
    final_summary: str  # Final synthesized summary

class WorkerState(TypedDict):
    """Individual worker state"""
    query: ResearchQuery
    topic: str
    completed_research: Annotated[list, operator.add]


# Lab 4 State Definitions
class QualityState(TypedDict):
    """State with quality control"""
    topic: str # Research topic
    messages: Annotated[list, operator.add] # Conversation history
    current_agent: str  # Active agent
    research_complete: bool # Flag indicating if research is complete
    report_complete: bool  # Flag indicating if report is complete
    report_text: str # Final report text
    quality_grade: str # Quality grade
    feedback: str # Feedback for improvement
    approved: bool # Approval status
    iteration_count: int # Number of iterations
    max_iterations: int # Max allowed iterations
    

class TaskDelegation(BaseModel):
    """Task delegation from Chief Researcher"""
    next_agent: Literal["research", "report_writer", "evaluator", "complete"] = Field(
        description="Next agent to delegate to"
    ) # Next agent to delegate to
    instructions: str = Field(description="Instructions for the agent") # Instructions for the agent
    reasoning: str = Field(description="Why this agent was chosen") # Reasoning for the choice


class ReportQuality(BaseModel):
    """Quality assessment of a research report"""
    grade: Literal["excellent", "good", "needs_improvement"] = Field(
        description="Overall quality grade of the report"
    ) # Overall quality grade
    completeness_score: int = Field(
        description="Score from 1-10 for how complete the research is",
        ge=1, le=10
    ) # Completeness score
    feedback: str = Field(
        description="Specific feedback on what needs improvement (if any)"
    ) # Feedback for improvement
    approved: bool = Field(
        description="Whether the report meets quality standards"
    ) # Approval status











# For Other Versions of State Dictionaries
  

    
# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], operator.add] 
#     topic: str
#     llm_calls: int

# class TeamState(TypedDict):
#     """Shared state for the collaborative team"""
#     topic: str  # Research topic
#     messages: Annotated[list, operator.add]  # Conversation history
#     research_complete: bool  # Flag: has search been done?
#     report_complete: bool  # Flag: has report been written?
#     current_agent: str  # Track which agent is active
#     final_report: str  # Final output
