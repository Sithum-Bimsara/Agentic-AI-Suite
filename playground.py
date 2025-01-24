
import phi
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv
from phi.playground import Playground, serve_playground_app
# Load environment variables
load_dotenv()

phi.api = os.getenv("PHI_API_KEY")

# Create individual agents

# Web Agent: Responsible for handling web-based queries using DuckDuckGo. This agent is configured to include sources in its responses.
web_search_agent = Agent(
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


app=Playground(agents=[finance_agent, web_search_agent]).get_app()

if __name__=="__main__":
    serve_playground_app("playground:app", reload=True)