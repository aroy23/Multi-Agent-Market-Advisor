# Multi Agent Market Advisor

A multi-agent system that gathers market data and research insights to generate investment predictions or market advice. <br>

- **LangChain** – For chaining language model operations.
- **LangGraph** – library to create a robust, multi-agent workflow.
- **OpenAI API** – Powers the agents with an LLM
- **Tavily Search API** – For fetching financial market data.

## Running
First, clone the repository and create a virtual environment
```shell
pip install -r requirements.txt
```
Run the Streamlit web app
```shell
streamlit run framework.py
```

## Overview

The program divides complex financial analysis into specialized tasks handled by two distinct agents:
- **Research Agent**: Gathers market data and research insights using search tools.
    - Collects up-to-date market data and financial insights.
    - Uses specialized search tools to find relevant information.
- **Advisor Agent**: Processes the research data to generate actionable market advice and investment predictions.
    - Analyzes the research data.
    - Generates actionable investment strategies and market advice based on the gathered information.
