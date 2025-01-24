from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

# Create individual agents

# Web Agent: Responsible for handling web-based queries using DuckDuckGo. This agent is configured to include sources in its responses.
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama3-70b-8192"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources in your response."],
    show_tool_calls=True,
    markdown=True,
)

# Finance Agent: Responsible for handling financial queries. This agent uses YFinance tools to retrieve stock prices, analyst recommendations, company information, and news.
finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama3-70b-8192"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data concisely."],
    show_tool_calls=True,
    markdown=True,
)

# Create a multi-agent system

# Multi-agent system combines the Web Agent and Finance Agent, leveraging their respective strengths.
# The Web Agent handles web-based queries and ensures inclusion of relevant and up-to-date information.
# The Finance Agent specializes in financial tasks, retrieving detailed stock and market insights.
multi_ai_agent = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama3-70b-8192"),
    instructions=["Always include sources and use tables for clarity where appropriate."],
    show_tool_calls=True,
    markdown=True,
)

# Summarize analyst recommendations for NVIDIA (NVDA)
print("\n▰▰▰▰▰▰▱ Summarizing Analyst Recommendations ▱▱▱▱▱▱▱\n")
# This call is meant to delegate the task of summarizing financial analyst recommendations to the Finance Agent.
multi_ai_agent.print_response(
    "Summarize analyst recommendations for NVIDIA (NVDA) briefly.",
    stream=True
)

# Fetch the latest news for NVIDIA (NVDA)
print("\n▰▰▰▰▰▰▱ Fetching Latest News ▱▱▱▱▱▱▱\n")
# This task leverages the Web Agent to fetch recent news articles about NVIDIA (NVDA).
# The Web Agent ensures the information retrieved is recent and includes relevant sources for credibility.
multi_ai_agent.print_response(
    "Fetch the 3 most recent and relevant news articles about NVIDIA (NVDA). Include article summaries and sources.",
    stream=True
)
