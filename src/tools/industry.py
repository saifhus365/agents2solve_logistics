"""
UAE logistics industry data lookup tool.

Provides curated, structured knowledge about the UAE logistics ecosystem:
key ports, free zones, companies, pain points, and market data.
This gives the Researcher agent domain-specific data without needing web access.
"""

from langchain_core.tools import tool


# Curated knowledge base
UAE_LOGISTICS_DATA = {
    "ports": {
        "title": "Major UAE Ports",
        "data": [
            {
                "name": "Jebel Ali Port (DP World)",
                "location": "Dubai",
                "capacity": "22.4M TEUs (2025 target)",
                "specialties": "Container, Ro-Ro, general cargo",
                "digitization": "Smart gate systems, automated cranes, blockchain-based trade finance",
                "pain_points": [
                    "Container dwell time averages 5-7 days vs global best of 3 days",
                    "Manual documentation for ~30% of shipments",
                    "Yard congestion during peak seasons (Q4)",
                    "Limited real-time visibility for freight forwarders",
                ],
            },
            {
                "name": "Khalifa Port (AD Ports Group)",
                "location": "Abu Dhabi",
                "capacity": "5M TEUs, expanding to 15M",
                "specialties": "Container, bulk, cruise",
                "digitization": "Semi-automated terminal (CSP Abu Dhabi), RFID tracking",
                "pain_points": [
                    "Integration between port systems and free zone ERP systems",
                    "Truck appointment systems not consistently used",
                    "Customs pre-clearance delays for non-standard cargo",
                ],
            },
            {
                "name": "Port Rashid",
                "location": "Dubai",
                "capacity": "Being converted to cruise & tourism",
                "specialties": "Cruise, marina",
                "digitization": "Minimal for cargo (legacy systems)",
                "pain_points": ["Legacy system decommissioning challenges"],
            },
        ],
    },
    "free_zones": {
        "title": "Key Free Zones for Logistics",
        "data": [
            {
                "name": "JAFZA (Jebel Ali Free Zone)",
                "companies": "8,700+",
                "focus": "Trade, logistics, manufacturing",
                "challenges": "Complex inter-zone transfer docs, fragmented vendor management",
            },
            {
                "name": "KIZAD (Khalifa Industrial Zone Abu Dhabi)",
                "companies": "800+",
                "focus": "Industrial, logistics, food",
                "challenges": "Distance from main Dubai logistics corridor, developing infrastructure",
            },
            {
                "name": "DAFZA (Dubai Airport Free Zone)",
                "companies": "1,800+",
                "focus": "Air cargo, technology, pharma",
                "challenges": "Capacity constraints, cold-chain handoff between airline and warehouse",
            },
            {
                "name": "SAIF Zone (Sharjah)",
                "companies": "8,000+",
                "focus": "General trade, SME hub",
                "challenges": "Older IT infrastructure, manual customs processes",
            },
        ],
    },
    "pain_points": {
        "title": "Top Industry Pain Points (AI Opportunity Areas)",
        "data": [
            {
                "area": "Customs & Compliance",
                "severity": "High",
                "details": (
                    "Document preparation is 60% manual. HS code classification errors "
                    "cause 15-20% of customs delays. Each free zone has different requirements. "
                    "Cross-emirate transfers need separate documentation."
                ),
                "ai_opportunity": "Automated document classification, HS code prediction, compliance checking",
            },
            {
                "area": "Last-Mile Delivery",
                "severity": "High",
                "details": (
                    "Failed delivery rate ~18% in residential areas. Lack of standardized "
                    "addresses (Makani numbers not universally adopted). Extreme heat limits "
                    "delivery windows. High driver turnover (>40% annually)."
                ),
                "ai_opportunity": "Smart routing with address disambiguation, delivery time prediction, driver matching",
            },
            {
                "area": "Cold Chain Management",
                "severity": "Critical",
                "details": (
                    "40% of food imports need temperature control. Temperature excursions "
                    "in transit are often undetected until destination. Pharma logistics "
                    "require GDP compliance with continuous monitoring."
                ),
                "ai_opportunity": "IoT + AI anomaly detection, predictive maintenance for reefer units, automated compliance alerts",
            },
            {
                "area": "Warehouse Operations",
                "severity": "Medium-High",
                "details": (
                    "Many facilities still use paper-based inventory systems. Forklift "
                    "utilization below 60%. Space utilization averaging 65% vs best-in-class 85%. "
                    "Labor-intensive pick/pack processes."
                ),
                "ai_opportunity": "Automated inventory management, robotic picking optimization, space utilization AI",
            },
            {
                "area": "Cross-Border Data Integration",
                "severity": "High",
                "details": (
                    "Fragmented systems: TMS, WMS, port community systems, customs portals "
                    "don't talk to each other. Each stakeholder uses different data formats. "
                    "Average shipment generates 30+ documents across 15+ parties."
                ),
                "ai_opportunity": "Intelligent data harmonization, automated document extraction (OCR+NLP), API orchestration",
            },
            {
                "area": "Demand Forecasting",
                "severity": "Medium",
                "details": (
                    "Seasonal demand spikes (Ramadan, Dubai Shopping Festival) are predictable "
                    "but poorly planned for. SME importers lack forecasting tools entirely. "
                    "Inventory carrying costs are 25-30% of product value."
                ),
                "ai_opportunity": "ML-based demand prediction, automated reorder points, seasonal pattern recognition",
            },
        ],
    },
    "market_stats": {
        "title": "UAE Logistics Market Statistics",
        "data": {
            "market_size_2025": "$30-32 billion",
            "cagr": "6.3-10% through 2030",
            "ecommerce_market": "$8 billion (15% YoY growth)",
            "air_cargo_volume": "3.1M tonnes annually (DXB + DWC)",
            "sea_cargo_volume": "15M+ TEUs (Jebel Ali alone)",
            "logistics_employment": "~200,000 workers in logistics sector",
            "digital_adoption": "45% of large companies, <15% of SMEs",
            "key_trade_partners": "China, India, USA, Saudi Arabia, Germany",
        },
    },
}


@tool
def lookup_uae_logistics_data(category: str) -> str:
    """
    Look up curated data about the UAE logistics industry.

    Available categories:
    - "ports" — Major UAE ports (Jebel Ali, Khalifa Port, Port Rashid) with
      capacity, digitization status, and pain points
    - "free_zones" — Key free zones (JAFZA, KIZAD, DAFZA, SAIF) with
      company counts and operational challenges
    - "pain_points" — Top industry pain points with severity ratings and
      AI opportunity areas (customs, last-mile, cold chain, etc.)
    - "market_stats" — Market size, growth rates, trade volumes, digital adoption
    - "all" — Returns everything

    Args:
        category: One of "ports", "free_zones", "pain_points", "market_stats", or "all"
    """
    category = category.lower().strip()

    if category == "all":
        sections = []
        for key, section in UAE_LOGISTICS_DATA.items():
            sections.append(_format_section(section))
        return "\n\n---\n\n".join(sections)

    if category in UAE_LOGISTICS_DATA:
        return _format_section(UAE_LOGISTICS_DATA[category])

    available = ", ".join(f'"{k}"' for k in UAE_LOGISTICS_DATA.keys())
    return f'Category "{category}" not found. Available categories: {available}, "all"'


def _format_section(section: dict) -> str:
    """Format a data section into readable text."""
    title = section.get("title", "Data")
    data = section.get("data", {})

    output = f"## {title}\n\n"

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, list):
                        output += f"  {key}:\n"
                        for v in value:
                            output += f"    - {v}\n"
                    else:
                        output += f"  {key}: {value}\n"
                output += "\n"
    elif isinstance(data, dict):
        for key, value in data.items():
            output += f"  {key}: {value}\n"

    return output
