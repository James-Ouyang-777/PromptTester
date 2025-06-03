import asyncio
from typing import Dict, List, Any
from ..models.base import Experiment, Result, ProviderType
from ..providers.openai_provider import OpenAIProvider
from ..providers.anthropic_provider import AnthropicProvider

class ExperimentRunner:
    def __init__(self, openai_api_key: str, anthropic_api_key: str):
        self.providers = {
            ProviderType.OPENAI: OpenAIProvider(openai_api_key),
            ProviderType.ANTHROPIC: AnthropicProvider(anthropic_api_key)
        }

    async def run_experiment(self, experiment: Experiment) -> List[Result]:
        results = []
        
        # Run each prompt against each test case
        for prompt in experiment.prompts:
            for test_case in experiment.test_cases:
                # Get the appropriate provider
                provider = self.providers[experiment.provider]
                
                # Generate response
                response = await provider.generate(
                    prompt=prompt,
                    test_case=test_case,
                    parameters=experiment.parameters
                )
                
                # Create result
                result = Result(
                    experiment_id=experiment.name,
                    prompt_name=prompt.name,
                    test_case_id=str(test_case.input_text[:50]),  # Using first 50 chars as ID
                    input_text=test_case.input_text,
                    output=response["output"],
                    cost=response["cost"],
                    latency=response["latency"],
                    metadata=response["metadata"]
                )
                
                results.append(result)
        
        return results

    async def run_experiments(self, experiments: List[Experiment]) -> Dict[str, List[Result]]:
        """Run multiple experiments in parallel."""
        tasks = [self.run_experiment(exp) for exp in experiments]
        results = await asyncio.gather(*tasks)
        
        return {
            experiment.name: result_list
            for experiment, result_list in zip(experiments, results)
        } 