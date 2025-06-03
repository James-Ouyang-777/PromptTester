import time
from typing import Dict, Any
import anthropic
from .base import BaseProvider
from ..models.base import Prompt, TestCase

class AnthropicProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key)

    async def generate(self, prompt: Prompt, test_case: TestCase, parameters: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        
        # Prepare the full prompt
        full_prompt = f"{prompt.content}\n\nInput: {test_case.input_text}"
        
        # Make the API call
        response = await self.client.messages.create(
            model=parameters.get("model", "claude-3-opus-20240229"),
            max_tokens=parameters.get("max_tokens", 1000),
            temperature=parameters.get("temperature", 0.7),
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        # Calculate latency
        latency = time.time() - start_time
        
        # Calculate cost
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        return {
            "output": response.content[0].text,
            "cost": cost,
            "latency": latency,
            "metadata": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "model": parameters.get("model", "claude-3-opus-20240229"),
            }
        }

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        # Claude 3 Opus pricing (as of 2024)
        input_cost_per_1k = 0.015
        output_cost_per_1k = 0.075
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return input_cost + output_cost 