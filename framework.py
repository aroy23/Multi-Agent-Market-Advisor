import getpass
import os
import streamlit as st

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.graph import StateGraph, START
from IPython.display import Image, display
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from typing import Literal

st.sidebar.header("API Keys")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
tavily_api_key = st.sidebar.text_input("Tavily API Key", type="password")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
if tavily_api_key:
    os.environ["TAVILY_API_KEY"] = tavily_api_key

# Check if keys are provided; if not, warn the user.
if not openai_api_key or not tavily_api_key:
    st.warning("Please enter your API keys in the sidebar to continue.")
    st.stop()

tavily_tool = TavilySearchResults(max_results=5)

def make_system_prompt(suffix: str) -> str:
    return (
        "You are a helpful AI assistant, collaborating with other assistants."
        " Use the provided tools to progress towards answering the question."
        " If you are unable to fully answer, that's OK, another assistant with different tools "
        " will help where you left off. Execute what you can to make progress."
        " If you or any of the other assistants have the final answer or deliverable,"
        " prefix your response with FINAL ANSWER so the team knows to stop."
        f"\n{suffix}"
    )

llm = ChatOpenAI(model="gpt-4o-mini")

def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        return END
    return goto

research_agent = create_react_agent(
    llm,
    tools=[tavily_tool],
    prompt=make_system_prompt(
        "You can only perform research on the latest financial market data from the current year. "
        "Work with your colleague to generate investment advice."
        "You should not generate investment advice, leave that to your colleague."
    ),
)

def research_node(state: MessagesState) -> Command[Literal["investment_advisor", END]]:
    result = research_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "investment_advisor")
    # Ensure the last message is wrapped as a HumanMessage for consistency
    result["messages"][-1] = HumanMessage(content=result["messages"][-1].content, name="researcher")
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )

investment_agent = create_react_agent(
    llm,
    tools=[],  # No additional tools required for now
    prompt=make_system_prompt(
        "You can only generate investment predictions and market advice based on the research data provided. "
        "Support your advice with quantitative metrics like stock price percent changes, key ratios, and other relevant data."
        "Collaborate with your researcher colleague to produce the final answer."
        "If the question is regarding investment the final answer should point to one direction: invest or do not invest."
    ),
)

def investment_node(state: MessagesState) -> Command[Literal["researcher", END]]:
    result = investment_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "researcher")
    result["messages"][-1] = HumanMessage(content=result["messages"][-1].content, name="investment_advisor")
    return Command(
        update={"messages": result["messages"]},
        goto=goto,
    )


workflow = StateGraph(MessagesState)
workflow.add_node("researcher", research_node)
workflow.add_node("investment_advisor", investment_node)
workflow.add_edge(START, "researcher")
graph = workflow.compile()

col1, col2 = st.columns([4, 2])

with col2:
    with st.expander("Agent Workflow Graph", expanded=True):
        try:
            graph_img = graph.get_graph().draw_mermaid_png()
            st.image(graph_img, caption="Workflow Graph")
        except Exception as e:
            st.error(f"Error displaying graph: {e}")

flow = []
with col1:
    st.title("Multi Agent Market Advisor")
    st.write("Enter your prompt below and see the resulting financial insights.")

    user_prompt = st.text_input(
        "Enter your investing related prompt:",
        ""
    )

    submit = st.button("Submit", disabled=(not user_prompt))

    if submit:
        status_placeholder = st.empty()
        status_placeholder.info("Processing your request...")

        events = graph.stream(
            {
                "messages": [
                    ("user", user_prompt)
                ],
            },
            {"recursion_limit": 150},
        )

        for event in events:
            if event.get("investment_advisor", {}) or event.get("researcher", {}):
                if event.get("investment_advisor", {}):  
                    data = event.get("investment_advisor", {})
                    flow.append("Advisor")
                elif event.get("researcher", {}):
                    data = event.get("researcher", {})
                    flow.append("Researcher")
        
        if data:
            final_answer = data["messages"][-1].content.strip()

        status_placeholder.empty()

        if data:
            st.subheader("Final Answer")
            st.markdown(final_answer)
        else:
            st.write("No final answer was produced.")
        
        with col2:
            with st.expander("Response Flow", expanded=False):
                depiction = ""
                for i, step in enumerate(flow):
                    if i < len(flow)-1:
                        depiction += step + " -> "
                    else:
                        depiction += step
                st.write(depiction)

