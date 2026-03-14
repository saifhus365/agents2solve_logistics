"""
Orchestrator Agent — LangGraph supervisor that routes to sub-agents.

Uses the langgraph-supervisor package to create a supervisor agent that:
1. Receives the user's request
2. Routes to the Researcher first (gather data)
3. Routes to Strategy Agent (identify opportunities) 
4. Routes to Solutions Architect (propose solutions)
5. Can loop back to Researcher if more data is needed
6. Synthesizes the final report
"""

from langgraph_supervisor import create_supervisor
from src.llm import get_llm
from src.agents.researcher import create_researcher_agent
from src.agents.strategy import create_strategy_agent
from src.agents.solutions import create_solutions_agent


ORCHESTRATOR_SYSTEM_PROMPT = """You are the Lead Orchestrator for a multi-agent team analyzing 
the UAE logistics industry to identify where AI agents can fill critical niches.

YOUR TEAM:
1. **researcher** — Gathers data using web search, industry databases, and news tools
2. **strategy** — Analyzes findings to identify AI niche opportunities
3. **solutions_architect** — Designs concrete AI agent solutions

WORKFLOW:
1. First, send the task to the **researcher** to gather comprehensive data about UAE logistics
2. Once research is complete, send findings to the **strategy** agent for analysis
3. Then send the strategy analysis to the **solutions_architect** for concrete proposals  
4. If the solutions_architect flags data gaps, route back to the **researcher**
5. Finally, synthesize everything into a cohesive final report

FINAL REPORT should include:
- Executive Summary
- Key Research Findings
- Top AI Niche Opportunities (ranked)
- Proposed AI Agent Solutions
- Recommended Next Steps

Be decisive in routing. Don't ask which agent to use — follow the logical workflow above."""


def build_orchestrated_graph():
    """
    Build the full multi-agent graph with supervisor orchestration.
    
    Returns a compiled LangGraph that can be invoked with .invoke() or streamed.
    """
    llm = get_llm(temperature=0.3)

    # Create the sub-agents
    researcher = create_researcher_agent()
    strategy = create_strategy_agent()
    solutions = create_solutions_agent()

    # Build supervisor graph
    graph = create_supervisor(
        agents=[researcher, strategy, solutions],
        model=llm,
        prompt=ORCHESTRATOR_SYSTEM_PROMPT,
    )

    return graph.compile()
