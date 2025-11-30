import os
import dotenv
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.agents import SequentialAgent, Agent
from google.adk.runners import InMemoryRunner

from agents.prioritizer import prioritizerAgent
from agents.harvester import harvesterAgent
from agents.classifier import classifierAgent

dotenv.load_dotenv(dotenv_path="./.env.local")

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    # Raise an error if the key is missing before starting the app
    raise ValueError("API Key not found. Please set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file.")


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
        runner = InMemoryRunner(agent=localIssueAnalyser)
        final_report = await runner.run_debug(prompt)
        
        return {
            "status": "success",
            "prompt": prompt,
            "report": final_report
        }

    except Exception as e:
        print(f"Error during agent run: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {e}")

@app.get("/")
def health_check():
    return {"message": "Local Issue Analyser API is running."}