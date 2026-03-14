"""
Tavily web search tool for the Researcher agent.

Provides a LangChain @tool that searches the web for information about
UAE logistics, shipping, supply chain, and related topics.
Falls back to a mock if TAVILY_API_KEY is not set.
"""

import os
from langchain_core.tools import tool


def _has_tavily_key() -> bool:
    key = os.environ.get("TAVILY_API_KEY", "")
    return bool(key and key.startswith("tvly-"))


@tool
def tavily_search(query: str) -> str:
    """
    Search the web for information about logistics, shipping, supply chain,
    and trade in the UAE. Use specific queries for best results.

    Args:
        query: A specific search query, e.g. "UAE customs clearance delays 2025"
    """
    if _has_tavily_key():
        from langchain_tavily import TavilySearch

        search = TavilySearch(
            max_results=5,
            topic="general",
            include_answer=True,
        )
        results = search.invoke({"query": query})

        # Format results into readable text
        if isinstance(results, dict):
            answer = results.get("answer", "")
            sources = results.get("results", [])
            output = f"Answer: {answer}\n\nSources:\n"
            for s in sources[:5]:
                output += f"- {s.get('title', 'N/A')}: {s.get('content', '')[:200]}...\n"
                output += f"  URL: {s.get('url', 'N/A')}\n"
            return output
        return str(results)
    else:
        # Fallback: curated mock results for common logistics queries
        return _mock_search(query)


def _mock_search(query: str) -> str:
    """Provide curated data when Tavily API key is not available."""
    q = query.lower()

    if "customs" in q or "clearance" in q:
        return (
            "UAE Customs & Clearance Insights (offline data):\n"
            "- Dubai Customs processes ~1.6M declarations annually through DubaiTrade portal\n"
            "- Average clearance time: 24 hours for sea freight, 4 hours for air freight\n"
            "- Key pain points: document mismatches (HS code errors), re-export compliance,\n"
            "  bonded warehouse tracking, FTA certificate validation\n"
            "- Dubai Customs has adopted smart systems but many freight forwarders still\n"
            "  use manual document preparation\n"
            "- Sources: Dubai Customs annual report, Gulf News logistics section"
        )

    elif "last mile" in q or "last-mile" in q or "delivery" in q:
        return (
            "UAE Last-Mile Delivery Insights (offline data):\n"
            "- UAE e-commerce market ~$8B, growing 15% YoY\n"
            "- Key challenge: addressability — many areas lack standard street addresses,\n"
            "  relying on landmark-based navigation (Makani numbers partially solve this)\n"
            "- Extreme heat (45°C+) impacts delivery windows and product integrity\n"
            "- High failed-delivery rates in residential towers (no-one home, access issues)\n"
            "- Players: Aramex, Fetchr, Quiqup, Careem (last-mile), noon, Amazon.ae\n"
            "- Sources: Euromonitor, TechCrunch Middle East"
        )

    elif "warehouse" in q or "fulfillment" in q or "storage" in q:
        return (
            "UAE Warehouse & Fulfillment Insights (offline data):\n"
            "- Total warehousing space: ~22M sqm across UAE (JAFZA alone: 7M sqm)\n"
            "- Cold chain is critical: 40% of food imports require temp-controlled storage\n"
            "- Key pain points: manual inventory counts, forklift-dependent ops,\n"
            "  fragmented WMS platforms across different free zones\n"
            "- Growing demand for micro-fulfillment centers near urban areas\n"
            "- Temperature excursions in pharma logistics cause ~$35B losses globally\n"
            "- Sources: JLL MENA logistics report, CBRE UAE industrial outlook"
        )

    elif "port" in q or "jebel ali" in q or "shipping" in q or "maritime" in q:
        return (
            "UAE Ports & Maritime Insights (offline data):\n"
            "- Jebel Ali (DP World): largest port in Middle East, 15M+ TEUs annually\n"
            "- Khalifa Port (AD Ports): rapidly expanding, handles bulk & containers\n"
            "- Key pain points: vessel berthing delays, container dwell time averaging 5-7 days,\n"
            "  lack of real-time yard visibility, manual gate processes\n"
            "- DP World investing in autonomous cranes and digital twin technology\n"
            "- Re-export hub: ~50% of containers are transshipped\n"
            "- Sources: DP World annual report, AD Ports investor deck"
        )

    elif "regulation" in q or "compliance" in q or "law" in q:
        return (
            "UAE Logistics Regulation Insights (offline data):\n"
            "- Federal Transport Authority (FTA) oversees land transport\n"
            "- General Civil Aviation Authority (GCAA) for air freight\n"
            "- Federal Customs Authority harmonizes cross-emirate customs\n"
            "- Key complexity: each free zone has its own customs & licensing rules\n"
            "- VAT (5%) considerations for cross-free-zone transfers\n"
            "- Upcoming: mandatory e-invoicing, tighter ESG/sustainability reporting\n"
            "- Sources: UAE Federal Gazette, PwC Middle East regulatory updates"
        )

    else:
        return (
            "UAE Logistics General Overview (offline data):\n"
            "- UAE logistics market valued at ~$30B, CAGR 6-10% through 2030\n"
            "- Strategic location: gateway between Asia, Europe, and Africa\n"
            "- Key infrastructure: Jebel Ali Port, Al Maktoum Airport, Etihad Rail\n"
            "- Major free zones: JAFZA, KIZAD, SAIF Zone, DAFZA\n"
            "- Top players: DP World, Agility, Aramex, GAC, Tristar, RSA Logistics\n"
            "- Government initiatives: UAE Vision 2031, Dubai Silk Road strategy\n"
            "- Key challenges: talent shortage, data fragmentation, last-mile costs,\n"
            "  customs complexity, temperature-sensitive goods management\n"
            "- Sources: Mordor Intelligence, Frost & Sullivan MENA"
        )
