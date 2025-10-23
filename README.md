# AI Agents Project

## Setup

### Creating venv with uv
```bash
uv venv --python 3.11 .venv
.venv\Scripts\activate

# install and sync deps  
uv init
uv add [deps] 
# compile from pyproject.toml
uv pip compile pyproject.toml -o requirements.txt
```

## Database Setup

### Creating Database
Initialize the SQLite database using the schema defined in `src/db_schema.py`:

```bash
python src/db_schema.py
```

This will:
- Create the `database/database.db` file
- Set up the `findings` table with columns: id, topic, source_url, snippet, created_at
- Create indexes for optimal query performance
- Configure SQLite with WAL mode and foreign key constraints

## Project Structure

### Source Directory (`src/`)

The `src/` directory contains the core application code organized into several key areas:

#### Core Modules
- **`db_schema.py`** - Database schema and connection management
- **`llm.py`** - LLM integration using Groq API
- **`models.py`** - Pydantic models for data validation and state management

#### Tools (`src/tools/`)
- **`web_search.py`** - Web search functionality using Tavily API
- **`insert.py`** - Database insertion tools for research findings
- **`report.py`** - Report generation tools
- **`retrieve.py`** - Data retrieval tools

#### Labs (`src/labs/`)
Experimental implementations of different AI agent frameworks:

##### CrewAI Lab (`src/labs/crewai/`)
- **`crewai_lab.py`** - Multi-agent research system using CrewAI
- Features researcher and writer agents working collaboratively
- Implements task sequencing and callbacks

##### LangGraph Lab (`src/labs/langGraph/`)
- **`langGraph_lab.py`** - Workflow-based research system using LangGraph
- **`utils/`** - Supporting modules:
  - `build_workflow.py` - Workflow construction
  - `orchestrator.py` - Workflow orchestration
  - `researcher_worker.py` - Research worker implementation
  - `analyst_synthesizer.py` - Analysis and synthesis
  - `assign_research_workers.py` - Worker assignment logic

##### Lab 4 (`src/labs/lab4/`)
- **`main.py`** - Advanced research workflow with quality control
- **`utils/`** - Quality assurance modules:
  - `chief_researcher_node.py` - Chief researcher coordination
  - `evaluator_node.py` - Quality evaluation
  - `report_writer_node.py` - Report generation
  - `research_node.py` - Research execution
  - `route_after_evaluation.py` - Quality-based routing

### Key Features
- **Multi-framework support**: CrewAI, LangGraph implementations
- **Database persistence**: SQLite with optimized schema
- **Web search integration**: Tavily API for real-time information
- **Quality control**: Advanced evaluation and iteration systems
- **Modular design**: Reusable tools and components

