# LangGraph Chatbot

A collection of chatbot implementations built with **LangGraph** and **LangChain**.

The files in this repository are different versions and variations of the same chatbot project. Each version experiments with or improves features such as conversation flow, memory, tool usage, state management, and LangSmith tracing.

## Project Overview

This repository was created to learn and demonstrate how chatbots can be built using LangGraph.

The chatbot uses a graph-based workflow where each step is represented as a node. LangGraph controls how the chatbot processes user messages, calls the language model, uses tools, stores conversation state, and returns responses.

## Features

- LLM-powered chatbot
- LangGraph-based conversation workflow
- Conversation state management
- Chat history and memory
- Tool integration
- Conditional routing
- LangSmith tracing and debugging
- Multiple chatbot versions for learning and experimentation

## How It Works

A typical chatbot workflow in this repository follows these steps:

1. The user sends a message.
2. The message is added to the chatbot state.
3. LangGraph sends the conversation to the language model.
4. The model generates a response or requests a tool.
5. Tool results are returned to the graph when required.
6. The updated conversation state is saved.
7. The final response is shown to the user.

## Tech Stack

- Python
- LangGraph
- LangChain
- LangSmith
- Large Language Models
- Python dotenv

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/langgraph-chatbot.git
cd langgraph-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project folder.

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=langgraph-chatbot

# Add the API key required by the model used in your code
OPENAI_API_KEY=your_api_key
```

Replace or add environment variables according to the model provider used in the chatbot.

Do not upload the `.env` file or expose API keys publicly.

### 5. Run a chatbot version

```bash
python chatbot_v1.py
```

Replace `chatbot_v1.py` with the actual filename you want to run.

## LangSmith Integration

LangSmith can be used to trace and debug the chatbot workflow.

It helps inspect:

- User inputs
- Model responses
- Graph execution
- Node transitions
- Tool calls
- Errors
- Latency
- Token usage

## Purpose

The purpose of this repository is to understand LangGraph by building multiple versions of a chatbot and gradually adding more advanced features.

## Author

**Shubham Upadhyay**

## License

This project is available under the license included in the repository.
