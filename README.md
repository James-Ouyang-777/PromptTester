# PromptTuner

A powerful tool for A/B testing prompts across different LLM providers while tracking costs and accuracy metrics.

## Features

- Support for multiple LLM providers (OpenAI, Anthropic)
- A/B testing framework for prompts
- Cost tracking per API call
- Custom evaluation metrics
- Easy-to-use API interface
- Results visualization and analysis

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/PromptTuner.git
cd PromptTuner
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Usage

1. Start the API server:

```bash
uvicorn prompt_tuner.api.main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

## Project Structure

```
prompt_tuner/
├── api/            # FastAPI application
├── core/           # Core functionality
├── models/         # Data models
├── providers/      # LLM provider implementations
├── evaluators/     # Custom evaluation metrics
└── utils/          # Utility functions
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.
