"""
Main entry point for the UAE Logistics AI Agent System.

Runs the multi-agent orchestration to:
1. Research the UAE logistics industry
2. Identify niches where AI agents can add value
3. Propose concrete AI agent solutions

Usage:
    python main.py
    python main.py --query "Focus on cold chain logistics challenges"
    python main.py --output results.json
"""

import argparse
import json
import sys
from datetime import datetime
from src.graph import build_graph


DEFAULT_QUERY = (
    "Analyze the UAE logistics and shipping industry comprehensively. "
    "Research the major pain points, inefficiencies, and gaps in the current ecosystem. "
    "Identify specific niches where AI agents can solve real problems that logistics "
    "companies, freight forwarders, customs brokers, and warehouse operators face daily. "
    "Propose concrete AI agent solutions with architecture, data requirements, and "
    "implementation roadmaps. Focus on what makes the UAE market unique: its role as a "
    "re-export hub, free zone complexity, extreme climate, and rapid e-commerce growth."
)


def run(query: str | None = None, output_file: str | None = None):
    """Run the multi-agent system with the given query."""
    query = query or DEFAULT_QUERY
    output_file = output_file or "output/results.json"

    print("=" * 80)
    print("🚀 UAE Logistics AI Agent System")
    print("=" * 80)
    print(f"\n📋 Query: {query[:100]}{'...' if len(query) > 100 else ''}")
    print("\n⏳ Building multi-agent graph...")

    # Build the graph
    graph = build_graph()

    print("✅ Graph compiled successfully!")
    print("\n🔄 Running agents (this may take a few minutes)...\n")
    print("-" * 80)

    # Collect structured output for JSON
    agent_outputs = []
    final_messages = []
    current_agent = None

    for chunk in graph.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="updates",
    ):
        # Each chunk is a dict with node_name -> state_update
        for node_name, state_update in chunk.items():
            if node_name != current_agent:
                current_agent = node_name
                agent_emoji = {
                    "supervisor": "🎯",
                    "researcher": "🔍",
                    "strategy": "📊",
                    "solutions_architect": "🏗️",
                }.get(node_name, "🤖")
                print(f"\n{agent_emoji} [{node_name.upper()}] is working...")

            # Collect messages
            if "messages" in state_update:
                for msg in state_update["messages"]:
                    final_messages.append(msg)

                    content = getattr(msg, "content", "") or ""
                    msg_type = type(msg).__name__

                    # Collect for JSON output
                    if content:
                        agent_outputs.append({
                            "agent": node_name,
                            "type": msg_type,
                            "content": content,
                        })

                    # Print to terminal
                    if content:
                        if len(content) > 500:
                            print(f"   {content[:500]}...")
                        else:
                            print(f"   {content}")

    print("\n" + "=" * 80)
    print("📄 FINAL REPORT")
    print("=" * 80)

    # Print the last substantive message (the final synthesis)
    final_report = ""
    if final_messages:
        last_msg = final_messages[-1]
        if hasattr(last_msg, "content") and last_msg.content:
            final_report = last_msg.content
            print(f"\n{final_report}")
        else:
            print("\n(No final report generated. Check agent outputs above.)")

    # ---- Save JSON output ----
    result_json = {
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "final_report": final_report,
        "agent_outputs": agent_outputs,
    }

    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_json, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"✅ Analysis complete! Results saved to: {output_file}")
    print("=" * 80)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="UAE Logistics AI Agent System — Identify AI opportunities in UAE logistics",
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=None,
        help="Custom query to analyze (default: comprehensive UAE logistics analysis)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output/results.json",
        help="Path to save JSON output (default: output/results.json)",
    )
    args = parser.parse_args()

    try:
        run(query=args.query, output_file=args.output)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Is your NVIDIA_API_KEY set in .env? (starts with 'nvapi-')")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. Check your internet connection")
        raise


if __name__ == "__main__":
    main()
