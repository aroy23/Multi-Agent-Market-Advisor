# Multi-Agent Market Advisor

A multi-agent system that gathers market data and research insights to generate investment predictions or market advice. <br>

- **LangChain** – For chaining language model operations.
- **LangGraph** – library to create a robust, multi-agent workflow.
- **[OpenAI API](https://openai.com/api/)** – Powers the agents with an LLM
- **[Tavily Search API](https://tavily.com/)** – For fetching financial market data.

Deployed at: https://multi-agent-market-advisor.streamlit.app/

## Running
First, clone the repository and create a virtual environment
```shell
pip install -r requirements.txt
```
Run the Streamlit web app
```shell
streamlit run framework.py
```

(Optional) Changing LLM: [Available Models](https://platform.openai.com/docs/models)
```python
# Change model here
llm = ChatOpenAI(model="gpt-4o-mini")
```

## Overview

The program divides complex financial analysis into specialized tasks handled by two distinct agents:
- **Research Agent**: Gathers market data and research insights using search tools.
    - Collects up-to-date market data and financial insights.
    - Uses specialized search tools to find relevant information.
- **Advisor Agent**: Processes the research data to generate actionable market advice and investment predictions.
    - Analyzes the research data.
    - Generates actionable investment judgements and market advice based on the gathered information.
<img width="1779" alt="page" src="https://github.com/user-attachments/assets/0b78a6e6-8953-49ad-9e9b-b9ae9b90e1b1" />
