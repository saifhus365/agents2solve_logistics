# 🚀 UAE Logistics AI Agent System

A multi-agent orchestration system that analyzes the UAE logistics & shipping industry to identify where **AI agents can fill critical niches**. Built with **LangGraph**, **LangChain**, and **NVIDIA NIM API** (Qwen3.5-122B-A10B).

## Architecture

```
                    ┌─────────────────────┐
                    │   Orchestrator      │
                    │  (LangGraph         │
                    │   Supervisor)       │
                    └────┬───┬───┬────────┘
                         │   │   │
            ┌────────────┘   │   └────────────┐
            │                │                │
   ┌────────▼──────┐ ┌──────▼───────┐ ┌──────▼──────────┐
   │  Researcher   │ │   Strategy   │ │   Solutions     │
   │  Agent        │ │   Agent      │ │   Architect     │
   │  🔍 + Tools   │ │   📊         │ │   🏗️            │
   └───────┬───────┘ └──────────────┘ └─────────────────┘
           │
    ┌──────┴──────┐
    │   Tools     │
    ├─────────────┤
    │ Web Search  │  (Tavily API)
    │ Industry DB │  (Curated UAE data)
    │ News Search │  (Latest headlines)
    └─────────────┘
```

### Agent Roles

| Agent | Role | Tools |
|---|---|---|
| **Orchestrator** | Routes tasks to the right agent | Built-in handoff |
| **Researcher** | Gathers UAE logistics data via tool calling | Web search, industry DB, news |
| **Strategy** | Identifies AI niche opportunities | Reasoning only |
| **Solutions Architect** | Designs concrete AI agent solutions | Reasoning only |

## Quick Start

### 1. Prerequisites

- Python 3.11+
- [NVIDIA NIM API key](https://build.nvidia.com) (free) — starts with `nvapi-`
- [Tavily API key](https://tavily.com) (free, optional) — enables live web search

### 2. Setup

```bash
# Clone and enter the project
cd agents2solve_logistics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and paste your NVIDIA_API_KEY (required)
# Optionally add TAVILY_API_KEY for live web search
```

### 3. Run

```bash
# Run with default comprehensive analysis
python main.py

# Run with a custom query
python main.py --query "Focus on cold chain logistics and pharma supply chain in UAE"
```

## Where to Put Your API Key

Open the `.env` file and replace the placeholder:

```env
NVIDIA_API_KEY=nvapi-YOUR_ACTUAL_KEY_HERE
TAVILY_API_KEY=tvly-YOUR_KEY_HERE  # Optional
```

Get your free NVIDIA API key at [build.nvidia.com](https://build.nvidia.com):
1. Create account → log in
2. Click profile → **API Keys**
3. Click **Generate API Key**
4. Copy the key (starts with `nvapi-`)

## How It Works

1. **User sends a query** about UAE logistics challenges
2. **Orchestrator** (LangGraph supervisor) routes to the **Researcher** first
3. **Researcher** uses tool calling to:
   - Search the web for logistics data (Tavily)
   - Look up curated UAE industry data (ports, free zones, pain points)
   - Find recent logistics news
4. **Strategy Agent** analyzes findings and identifies AI niche opportunities
5. **Solutions Architect** designs concrete AI agent solutions with architecture and roadmaps
6. **Orchestrator** synthesizes everything into a final report

### Frameworks Used

| Framework | Purpose |
|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Multi-agent state graph orchestration |
| [LangChain](https://python.langchain.com/) | LLM abstractions, tool definitions |
| [langchain-nvidia-ai-endpoints](https://pypi.org/project/langchain-nvidia-ai-endpoints/) | `ChatNVIDIA` — connects to Qwen3.5-122B-A10B via NVIDIA NIM |
| [langgraph-supervisor](https://pypi.org/project/langgraph-supervisor/) | Pre-built supervisor pattern for agent routing |
| [langchain-tavily](https://pypi.org/project/langchain-tavily/) | Web & news search tools |

## Project Structure

```
agents2solve_logistics/
├── .env.example            # API key template
├── requirements.txt        # Python dependencies
├── main.py                 # CLI entry point
├── src/
│   ├── config.py           # Environment & model configuration
│   ├── llm.py              # ChatNVIDIA LLM factory
│   ├── state.py            # Shared LangGraph state schema
│   ├── graph.py            # Graph assembly
│   ├── tools/
│   │   ├── search.py       # Tavily web search tool
│   │   ├── industry.py     # Curated UAE logistics data
│   │   └── news.py         # News search tool
│   └── agents/
│       ├── orchestrator.py # LangGraph supervisor
│       ├── researcher.py   # Research agent (tool calling)
│       ├── strategy.py     # Strategy analysis agent
│       └── solutions.py    # Solutions architect agent
└── README.md
```

## License

MIT