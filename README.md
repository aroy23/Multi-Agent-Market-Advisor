# Multi Agent Market Advisor

A multi-agent system that gathers market data and research insights to generate investment predictions or market advice. <br>

- **LangChain** – For chaining language model operations.
- **LangGraph** – library to create a robust, multi-agent workflow.
- **OpenAI API** – Powers the agents with an LLM
- **Tavily Search API** – For fetching financial market data.

## Overview

The program divides complex financial analysis into specialized tasks handled by two distinct agents:
- **Research Agent**: Gathers market data and research insights using search tools.
    - Collects up-to-date market data and financial insights.
    - Uses specialized search tools to find relevant information.
- **Investment Advisor Agent**: Processes the research data to generate actionable investment predictions and market advice.
    - Analyzes the research data.
    - Generates actionable investment strategies and market advice based on the gathered information.
