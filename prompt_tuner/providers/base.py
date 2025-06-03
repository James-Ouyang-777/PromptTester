from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models.base import Prompt, TestCase

class BaseProvider(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    async def generate(self, prompt: Prompt, test_case: TestCase, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response from the LLM provider.
        
        Args:
            prompt: The prompt to use
            test_case: The test case to evaluate
            parameters: Additional parameters for the generation
            
        Returns:
            Dict containing:
                - output: str
                - cost: float
                - latency: float
                - metadata: Dict[str, Any]
        """
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate the cost of the API call."""
        pass 