from setuptools import setup, find_packages

setup(
    name="semantic-search-generated-app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "chromadb",
        "openai",
        "pydantic",
    ],
) 