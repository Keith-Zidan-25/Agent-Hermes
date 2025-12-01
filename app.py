import os, sys
import dotenv
import logging

from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from google.adk.plugins import LoggingPlugin
from google.adk.agents import SequentialAgent, Agent
from google.adk.runners import InMemoryRunner

from agents.prioritizer import prioritizerAgent
from agents.harvester import harvesterAgent
from agents.classifier import classifierAgent

dotenv.load_dotenv(dotenv_path="./.env.local")

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("API Key not found")

LOG_FILE = "agent_workflow.log"

def setup_dual_logging(log_file: str, log_level=logging.DEBUG):
    """Configures logging to output to both console and a file."""
    
    logging.getLogger().handlers.clear()
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )

    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    print(f"Logging configured with output to {LOG_FILE} + console")

setup_dual_logging(LOG_FILE)

localIssueAnalyser = SequentialAgent(
    name="Local_Issue_Analyser",
    description="A multi-stage AI pipeline for analyzing public sentiment and reports related to local community issues (e.g., infrastructure, services, safety). It processes raw data, classifies unique issues, and delivers a final, ranked priority report.",
    sub_agents=[harvesterAgent, classifierAgent, prioritizerAgent],
)

app = FastAPI(
    title="Local Issue Analyser API",
    description="API for running the multi-agent system to prioritize local community concerns."
)

class AnalysisRequest(BaseModel):
    prompt: str

@app.post("/analyze", response_model=Dict[str, Any])
async def analyze_local_issues(request: AnalysisRequest):
    """
    Runs the SequentialAgent pipeline to analyze, classify, and prioritize issues 
    based on the provided prompt.
    """
    prompt = request.prompt
    
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        logger = LoggingPlugin(name="agent_logger")
        runner = InMemoryRunner(agent=localIssueAnalyser, plugins=[logger])
        agent_output = await runner.run_debug(prompt)
        
        final_report = agent_output[7]
        text_summary = agent_output[8]
        
        return {
            "status": "success",
            "prompt": prompt,
            "report": final_report,
            "summary": text_summary
        }

    except Exception as e:
        print(f"Error during agent run: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {e}")

@app.get("/")
def health_check():
    return {"message": "Local Issue Analyser API is running."}