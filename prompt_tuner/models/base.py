from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class ProviderType(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class Prompt(BaseModel):
    content: str
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)

class TestCase(BaseModel):
    input_text: str
    expected_output: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Experiment(BaseModel):
    name: str
    description: Optional[str] = None
    prompts: List[Prompt]
    test_cases: List[TestCase]
    provider: ProviderType
    model: str = "gpt-4o"
    parameters: Dict[str, Any] = Field(default_factory=dict)

class Result(BaseModel):
    experiment_id: str
    prompt_name: str
    test_case_id: str
    input_text: str
    output: str
    cost: float
    latency: float
    accuracy_score: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict) 