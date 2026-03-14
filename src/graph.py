"""
Full LangGraph assembly — builds and compiles the multi-agent orchestration graph.

This is the main entry point for constructing the graph. It delegates to the
orchestrator module which handles all the wiring via langgraph-supervisor.
"""

from src.agents.orchestrator import build_orchestrated_graph


def build_graph():
    """
    Build and compile the full multi-agent graph.
    
    Architecture:
        Orchestrator (Supervisor)
            ├── Researcher Agent (tools: web search, industry data, news)
            ├── Strategy Agent (reasoning-only)
            └── Solutions Architect Agent (reasoning-only)
    
    Returns:
        A compiled LangGraph ready for .invoke() or .stream()
    """
    return build_orchestrated_graph()
