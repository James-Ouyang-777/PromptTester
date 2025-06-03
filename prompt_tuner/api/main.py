import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from ..models.base import Experiment, Result
from ..core.experiment_runner import ExperimentRunner

# Load environment variables
load_dotenv()

app = FastAPI(
    title="PromptTuner",
    description="A tool for A/B testing prompts with different LLM APIs",
    version="1.0.0"
)

# Initialize experiment runner
experiment_runner = ExperimentRunner(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)

@app.post("/experiments/run", response_model=Dict[str, List[Result]])
async def run_experiment(experiment: Experiment):
    """Run a single experiment."""
    try:
        results = await experiment_runner.run_experiment(experiment)
        return {experiment.name: results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/experiments/run-batch", response_model=Dict[str, List[Result]])
async def run_experiments(experiments: List[Experiment]):
    """Run multiple experiments in parallel."""
    try:
        results = await experiment_runner.run_experiments(experiments)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 