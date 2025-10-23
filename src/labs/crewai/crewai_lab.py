from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from crewai import Agent, Task, Crew, LLM

from src.tools.insert import search_and_insert
from src.tools.report import report 

from config.config import *
from config.logger import get_logger

log = get_logger("crew_ai")

llm = LLM(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    base_url=GROQ_URL
)


researcher = Agent(
    role="Researcher",
    goal="Collect factual snippets for a given topic and persist them.",
    backstory="A detail-oriented research analyst who writes to a shared DB.",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Writer",
    goal="Read persisted snippets and summarize into bullet points.",
    backstory="A technical writer.",
    llm=llm,
    verbose=True,
)

if __name__ == "__main__":
    log.info("\nHi! I'm crewai.")
    log.info("Type the topic you want me to research and summarize.")
    topic = input("Topic:").strip()

    if not topic:
        log.warning("No topic provided. Exiting.")
        sys.exit(1)

    # Define Tasks
    t1 = Task(description=f"Gather and store findings about this topic: '{topic}'",
            agent=researcher,
            expected_output="Facts Inserted into DB.",
            callback=lambda _: search_and_insert({"topic": topic}, max_items=1))

    t2 = Task(description=f"Summarize findings from the DB on the topic: '{topic}'",
            agent=writer,
            expected_output="A bullet list summary.",
            context=[t1],  # sequencing
            callback=lambda _: report({"topic": topic}))

    # Define the Crew with agents and tasks
    crew = Crew(agents=[researcher, writer], tasks=[t1, t2], verbose=True)

    # Kickoff the Crew
    result = crew.kickoff()
    log.info("\n✅ Done. Here's your summary:\n")
    log.info(result)