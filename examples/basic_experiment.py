import asyncio
import os
from dotenv import load_dotenv
from prompt_tuner.models.base import Experiment, Prompt, TestCase, ProviderType

# Load environment variables from project root
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
print(f"Looking for .env file at: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")
load_dotenv(dotenv_path=env_path)

# Debug prints
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print(f"ANTHROPIC_API_KEY: {os.getenv('ANTHROPIC_API_KEY')}")

async def main():
    # Create test prompts
    prompt_a = Prompt(
        name="Simple Prompt",
        content="You are a helpful assistant. Please answer the following question:",
        description="Basic prompt with minimal context"
    )
    
    prompt_b = Prompt(
        name="Detailed Prompt",
        content="""You are an expert assistant with deep knowledge in various fields.
Please provide a detailed and well-structured answer to the following question.
Include relevant examples and explanations:""",
        description="Detailed prompt with more context and instructions"
    )
    
    # Create test cases
    test_cases = [
        TestCase(
            input_text="What is the capital of France?",
            expected_output="Paris"
        ),
        TestCase(
            input_text="Explain the concept of quantum computing in simple terms.",
            expected_output=None  # No expected output for open-ended questions
        )
    ]
    
    # Create experiment
    experiment = Experiment(
        name="Prompt Comparison Test",
        description="Comparing simple vs detailed prompts",
        prompts=[prompt_a, prompt_b],
        test_cases=test_cases,
        provider=ProviderType.OPENAI
        # model and parameters are optional now
    )

    
    # Run experiment
    from prompt_tuner.core.experiment_runner import ExperimentRunner
    
    runner = ExperimentRunner(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    results = await runner.run_experiment(experiment)
    
    # Print results
    for result in results:
        print(f"\nPrompt: {result.prompt_name}")
        print(f"Input: {result.input_text}")
        print(f"Output: {result.output}")
        print(f"Cost: ${result.cost:.4f}")
        print(f"Latency: {result.latency:.2f}s")
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main()) 