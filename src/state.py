"""
Shared state schema for the LangGraph multi-agent system.

All agents read from and write to this shared state, enabling
the Strategy and Solutions agents to see each other's outputs.
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Shared state that flows through all agents in the graph.

    Attributes:
        messages: The conversation history (LangGraph manages appending via add_messages).
                  All agent outputs and tool results are stored here.
    """
    messages: Annotated[list, add_messages]
