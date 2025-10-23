from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3]))

from src.labs.langGraph.utils.build_workflow import build_workflow

from config.config import *
from config.logger import get_logger

log = get_logger("langGraph_main")



if __name__ == "__main__":
    log.info("\nHi! I'm langGraph.")
    log.info("Type the topic you want me to research and summarize.")
    
    topic = input("\nEnter research topic: ").strip()
    
    if not topic:
        log.error("No topic provided. Exiting.")
        sys.exit(1)
    
    # Build workflow
    workflow = build_workflow()
    
    # Execute workflow
    log.info(f"\n[Starting] Research workflow for topic: '{topic}'\n")
    
    try:
        result = workflow.invoke({"topic": topic})
        
        # Display results
        log.info("\nFINAL SUMMARY")
        log.info(result['final_summary'])

        
    except Exception as e:
        log.error(f"Error during workflow execution: {e}")
        import traceback
        log.error(traceback.format_exc())