# Multi Agent Financial Advisor

A multi-agent system that gathers market data and research insights to generate investment predictions or market advice. <br>

This system leverages the LangGraph library to create a robust, multi-agent workflow.

## Overview

The program divides complex financial analysis into specialized tasks handled by two distinct agents:
- **Research Agent**: Gathers market data and research insights using search tools.
    - Collects up-to-date market data and financial insights.
    - Uses specialized search tools to find relevant information.
- **Investment Advisor Agent**: Processes the research data to generate actionable investment predictions and market advice.
    - Analyzes the research data.
    - Generates actionable investment strategies and market advice based on the gathered information.

## Implementation

The multi-agent system is implemented using:
- **LangGraph**: To design and manage the multi-agent workflow.
- **LangChain**: To connect language model tasks and prompts.
- **An LLM** (In my case, OpenAI's GPT-4o): Powers the specialized agents for natural language understanding and generation.
