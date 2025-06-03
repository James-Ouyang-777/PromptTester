import time
from typing import Dict, Any
from openai import AsyncOpenAI
from .base import BaseProvider
from ..models.base import Prompt, TestCase

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate(self, prompt: Prompt, test_case: TestCase, parameters: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        
        # Prepare the full prompt
        full_prompt = f"{prompt.content}\n\nInput: {test_case.input_text}"
        
        # Make the API call
        response = await self.client.chat.completions.create(
            model=parameters.get("model", "gpt-4o"),  # Use gpt-4 as default if not specified
            messages=[{"role": "user", "content": full_prompt}],
            temperature=parameters.get("temperature", 0.7),
            max_tokens=parameters.get("max_tokens", 1000),
        )
        
        # Calculate latency
        latency = time.time() - start_time
        
        # Calculate cost
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = self.calculate_cost(input_tokens, output_tokens, parameters.get("model", "gpt-4o"))
        
        return {
            "output": response.choices[0].message.content,
            "cost": cost,
            "latency": latency,
            "metadata": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "model": parameters.get("model", "gpt-4o"),
            }
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        # OpenAI pricing (as of 2024)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
        }
        
        # Default to gpt-3.5-turbo pricing if model not found
        model_pricing = pricing.get(model, pricing["gpt-3.5-turbo"])
        
        input_cost = (input_tokens / 1000) * model_pricing["input"]
        output_cost = (output_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost 