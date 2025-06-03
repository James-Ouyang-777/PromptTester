from setuptools import setup, find_packages

setup(
    name="prompt_tuner",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "anthropic>=0.5.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pytest>=7.4.0",
        "python-multipart>=0.0.6",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for A/B testing prompts with different LLM APIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PromptTuner",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 