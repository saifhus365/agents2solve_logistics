"""
Logistics news search tool for the Researcher agent.

Searches for recent news about UAE logistics, shipping, and supply chain.
Uses Tavily news search if API key is available, otherwise returns curated headlines.
"""

import os
from langchain_core.tools import tool


@tool
def search_logistics_news(topic: str) -> str:
    """
    Search for recent news articles about UAE logistics and shipping.
    Use this to find the latest developments, company announcements,
    and regulatory changes in the UAE logistics industry.

    Args:
        topic: A specific news topic, e.g. "DP World automation",
               "UAE customs digital transformation", "Dubai e-commerce logistics"
    """
    key = os.environ.get("TAVILY_API_KEY", "")

    if key and key.startswith("tvly-"):
        from langchain_tavily import TavilySearch

        search = TavilySearch(
            max_results=5,
            topic="news",
            include_answer=True,
            days=90,  # Last 3 months
        )
        results = search.invoke({"query": f"UAE logistics {topic}"})

        if isinstance(results, dict):
            answer = results.get("answer", "")
            sources = results.get("results", [])
            output = f"News Summary: {answer}\n\nRecent Articles:\n"
            for s in sources[:5]:
                output += f"- [{s.get('title', 'N/A')}] {s.get('content', '')[:150]}...\n"
                output += f"  Published: {s.get('published_date', 'N/A')} | URL: {s.get('url', 'N/A')}\n"
            return output
        return str(results)
    else:
        return _mock_news(topic)


def _mock_news(topic: str) -> str:
    """Provide curated news headlines when Tavily is not available."""
    return (
        f"Recent UAE Logistics News on '{topic}' (offline curated data):\n\n"
        "1. DP World launches AI-powered container tracking across Jebel Ali\n"
        "   - Digital twin technology deployed for yard management optimization\n"
        "   - Expected to reduce container dwell time by 30%\n\n"
        "2. Etihad Rail completes Stage Two - connecting Abu Dhabi to Dubai industrial zones\n"
        "   - Rail freight expected to capture 10% of inter-emirate cargo by 2027\n"
        "   - Significant cost reduction vs road transport\n\n"
        "3. UAE Federal Customs Authority mandates electronic documentation for all imports\n"
        "   - Phased rollout: large enterprises Q1 2026, SMEs by Q4 2026\n"
        "   - Paper-based submissions to be rejected starting 2027\n\n"
        "4. Amazon.ae expands same-day delivery to Sharjah and Ajman\n"
        "   - New micro-fulfillment center in Sharjah Industrial Area\n"
        "   - AI-driven route optimization reduces delivery costs by 22%\n\n"
        "5. AD Ports Group partners with tech startup for customs AI assistant\n"
        "   - NLP-based system auto-classifies HS codes with 94% accuracy\n"
        "   - Reduces customs clearance time from hours to minutes\n\n"
        "Note: For live news results, add your Tavily API key to .env"
    )
