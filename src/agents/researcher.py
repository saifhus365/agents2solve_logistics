"""
Researcher Agent — gathers data on UAE logistics using tool calling.

This agent has access to:
- tavily_search: Web search for logistics information
- lookup_uae_logistics_data: Curated UAE logistics industry data
- search_logistics_news: Recent news about UAE logistics

It uses the ReAct pattern: reason about what data is needed,
call the appropriate tool, observe results, and repeat until
enough information has been gathered.
"""

from langgraph.prebuilt import create_react_agent
from src.llm import get_llm
from src.tools.search import tavily_search
from src.tools.industry import lookup_uae_logistics_data
from src.tools.news import search_logistics_news


RESEARCHER_SYSTEM_PROMPT = """You are a Senior Logistics Research Analyst specializing in the UAE market.

Your job is to gather comprehensive, factual data about the UAE logistics and shipping industry.
You have access to three research tools — use ALL of them to build a complete picture:

1. **lookup_uae_logistics_data** — Start here. Query these categories: "ports", "free_zones", 
   "pain_points", "market_stats" to get structured industry data.

2. **tavily_search** — Use this to search for specific topics like:
   - "UAE customs clearance challenges 2025"
   - "Dubai last mile delivery problems"  
   - "Jebel Ali port digital transformation"
   - "UAE cold chain logistics technology"

3. **search_logistics_news** — Use this for recent developments and trends.

RESEARCH PRIORITIES:
- Current pain points and inefficiencies in UAE logistics
- Where manual processes still dominate
- Areas where technology adoption is low
- Regulatory changes creating new requirements
- Specific gaps where AI agents could make a difference

OUTPUT: Provide a structured research report with:
1. Market Overview (size, growth, key players)
2. Infrastructure Assessment (ports, free zones, transport networks)
3. Top Pain Points (ranked by severity and AI opportunity)
4. Recent Developments & Trends
5. Data Gaps (what you couldn't find and what needs deeper investigation)

Be thorough — the Strategy and Solutions agents depend on the quality of your research."""


def create_researcher_agent():
    """Create the Researcher agent with tool-calling capabilities."""
    llm = get_llm(temperature=0.3)  # Lower temp for factual research

    tools = [tavily_search, lookup_uae_logistics_data, search_logistics_news]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        name="researcher",
        prompt=RESEARCHER_SYSTEM_PROMPT,
    )

    return agent
