# chainlit_openai

# Chat Code Interpreter

This project is a simple Python application that integrates the OpenAI GPT-3.5 API with Chainlit UI. The app allows users to upload CSV files, provide messages to analyze the data, and get Python code execution results.

## Features

- Upload CSV files and receive data analysis.
- General chit-chat support.
- Code generation and execution using GPT-3.5-turbo.
- Dockerized application for easy deployment.

## Setup

### Prerequisites:

1. Python 3.10
2. Docker (optional for containerization)

### Install Dependencies:

```bash
pip install -r requirements.txt
```

```bash
docker build -t amit .
```

```bash
docker run -p 8003:8003 amit
```

```bash
Locally runing command

chainlit run chainlit_ui.py -w
```
