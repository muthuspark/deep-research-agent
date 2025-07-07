# Deep Research Agent

A Python implementation of the AI-powered deep research system that performs iterative research on any topic using search engines and large language models, with advanced date filtering and recency prioritization.

## ✨ Features

- **🔍 Iterative Research**: Performs deep research by recursively generating search queries and diving deeper based on findings
- **🕐 Date Filtering & Recency**: Prioritizes recent information with configurable date ranges (last days/weeks/months)
- **🤖 Multiple AI Providers**: Supports OpenAI and Google Gemini APIs with automatic provider detection
- **🎯 Smart Query Generation**: Uses LLMs to generate targeted search queries with date-aware terms
- **📊 Depth & Breadth Control**: Configurable parameters to control research scope and iteration depth
- **💡 Intelligent Follow-up**: Generates contextual follow-up questions for better research direction
- **📝 Comprehensive Reports**: Produces detailed markdown reports with findings, sources, and timestamps
- **⚡ Concurrent Processing**: Handles multiple searches in parallel for maximum efficiency
- **🔧 Flexible Configuration**: Command-line arguments and interactive mode for different use cases

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/muthuspark/deep-research-agent.git
cd deep-research-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Keys

Copy the environment template and add your API keys:

```bash
cp env.example .env
```

Edit `.env` file with your API keys:

```bash
# Choose your AI provider
OPENAI_KEY=your_openai_key_here
GEMINI_KEY=your_gemini_key_here

# Required for web search
FIRECRAWL_KEY=your_firecrawl_key_here

# Optional: Date filtering defaults
DEFAULT_PRIORITIZE_RECENT=true
DEFAULT_DAYS_BACK=730  # 2 years
```

### 3. Test Your Setup

```bash
python test_providers.py
```

### 4. Start Researching!

```bash
# Quick start with recent data (default)
python main.py "latest AI developments"

# Custom date range (last 30 days)
python main.py --days-back 30 "current market trends"

# Interactive mode
python main.py --interactive
```

## 📖 Usage Guide

### 🎯 Command Line Options

```bash
# Basic usage with recent data prioritization (default)
python main.py "your research topic"

# Custom date filtering
python main.py --days-back 30 "latest tech news"          # Last 30 days
python main.py --days-back 7 "weekly market update"       # Last 7 days
python main.py --days-back 365 "annual industry report"   # Last year

# Disable recent prioritization for historical research
python main.py --no-recent "history of artificial intelligence"

# Advanced research parameters
python main.py --breadth 6 --depth 3 --days-back 90 "comprehensive analysis"

# Quick answers instead of full reports
python main.py --type answer --days-back 7 "what happened this week"
```

### 🔧 Available Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--breadth N` | Number of parallel search queries (1-10) | 4 |
| `--depth N` | Number of recursive research iterations (1-5) | 2 |
| `--days-back N` | Only search information from last N days | 730 (2 years) |
| `--recent` | Explicitly enable recent prioritization | ✅ Enabled |
| `--no-recent` | Disable recent prioritization | ❌ Disabled |
| `--type report\|answer` | Output type: detailed report or concise answer | report |
| `--interactive` | Force interactive mode with prompts | ❌ Disabled |

### 📋 Common Use Cases

#### 📰 Breaking News & Current Events
```bash
# Breaking news (last 24 hours)
python main.py --days-back 1 "latest news on [topic]"

# Weekly industry updates
python main.py --days-back 7 "weekly tech industry news"

# Monthly market analysis
python main.py --days-back 30 "monthly market performance"
```

#### 🏢 Business & Finance
```bash
# Current market conditions
python main.py --days-back 30 "current stock market analysis"

# Recent mergers and acquisitions
python main.py --days-back 90 "latest business mergers 2024"

# Quarterly earnings reports
python main.py --days-back 90 "Q4 2024 earnings reports"
```

#### 💻 Technology Research
```bash
# Latest tech developments
python main.py --days-back 60 "latest AI breakthroughs"

# Recent product launches
python main.py --days-back 30 "new tech product releases"

# Current programming trends
python main.py --days-back 90 "programming language trends 2024"
```

#### 📚 Academic & Research
```bash
# Recent academic papers
python main.py --days-back 180 "recent research papers on [topic]"

# Current scientific developments
python main.py --days-back 60 "latest scientific discoveries"

# Historical analysis (all available data)
python main.py --no-recent "comprehensive literature review"
```

### 📖 For detailed usage examples and best practices, see: [USAGE_GUIDE.md](USAGE_GUIDE.md)

## 🏗️ How It Works

1. **🔍 Smart Query Generation**: Creates date-aware search queries with recency terms
2. **🌐 Web Search**: Uses Firecrawl API to extract and filter recent content
3. **📊 Content Analysis**: AI-powered processing to extract key insights and learnings
4. **🔄 Iterative Research**: Recursively explores deeper based on findings
5. **📝 Report Generation**: Compiles findings into comprehensive markdown reports

## 📁 Project Structure

```
deep-research-agent/
├── src/
│   ├── __init__.py
│   ├── ai_providers.py      # OpenAI and Gemini integration
│   ├── deep_research.py     # Core research logic with date filtering
│   ├── feedback.py          # Follow-up question generation
│   ├── firecrawl_client.py  # Enhanced web search client
│   └── prompts.py           # AI prompts and templates
├── reports/                 # Generated research reports (auto-created)
├── main.py                  # Enhanced CLI interface
├── test_providers.py        # AI provider test script
├── requirements.txt         # Python dependencies
├── env.example             # Environment template with date config
├── USAGE_GUIDE.md          # Comprehensive usage documentation
├── CHANGELOG.md            # Version history and updates
├── CONTRIBUTING.md         # Contribution guidelines
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables

```bash
# AI Provider Configuration
OPENAI_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o-mini              # Optional: custom model
GEMINI_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-1.5-flash         # Optional: custom model

# Web Search Configuration
FIRECRAWL_KEY=your_firecrawl_key_here
FIRECRAWL_BASE_URL=https://api.firecrawl.dev

# Performance Settings
CONCURRENCY_LIMIT=2                   # Concurrent search requests

# Date Filtering Configuration
DEFAULT_PRIORITIZE_RECENT=true        # Enable recent data by default
DEFAULT_DAYS_BACK=730                 # Default time window (2 years)
```

### AI Provider Selection

The system automatically detects available AI providers:

1. **Explicit Selection**: Set `AI_PROVIDER=openai` or `AI_PROVIDER=gemini`
2. **Auto-detection**: Prefers Gemini if both keys are available
3. **Fallback**: Uses whichever provider key is available

### Supported Models

- **OpenAI**: `gpt-4o-mini` (default), `gpt-4o`, `gpt-3.5-turbo`
- **Gemini**: `gemini-1.5-flash` (default), `gemini-1.5-pro`

## 📊 Output

The system generates timestamped files in the `reports/` directory:

- **Reports**: `report_YYYYMMDD_HHMMSS.md` - Detailed research reports
- **Answers**: `answer_YYYYMMDD_HHMMSS.md` - Concise answers
- **Sources**: All reports include comprehensive source lists

## 🔧 Advanced Features

### Date Filtering Intelligence
- **Automatic Query Enhancement**: Adds "2024", "latest", "recent" terms
- **Smart Result Scoring**: Prioritizes content with recent dates
- **Flexible Time Windows**: From hours to years of historical data
- **Content Freshness**: Sorts results by publication recency

### Research Optimization
- **Parallel Processing**: Concurrent searches for faster results
- **Adaptive Depth**: Intelligent recursion based on content quality
- **Source Validation**: Credibility assessment and deduplication
- **Error Resilience**: Robust handling of API failures and timeouts

## 🛠️ Troubleshooting

### Getting Outdated Information?
- Use `--days-back 30` for recent data
- Add "2024" or "latest" to your query
- Increase search breadth: `--breadth 6`

### Too Few Results?
- Increase time window: `--days-back 365`
- Use `--no-recent` for historical research
- Increase research depth: `--depth 3`

### API Issues?
- Run `python test_providers.py` to verify setup
- Check your API key quotas and limits
- Verify internet connectivity

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - feel free to use and modify as needed.

## 🆕 What's New

- **✨ Date Filtering**: Prioritize recent information with configurable time windows
- **🎯 Smart Queries**: Automatic addition of recency terms to search queries
- **⚡ Enhanced Performance**: Improved result sorting and content freshness scoring
- **🔧 Flexible CLI**: Comprehensive command-line options for different use cases
- **📖 Usage Guide**: Detailed documentation with examples and best practices

---

**Ready to start researching?** 🚀

```bash
python main.py "latest developments in your field of interest"
```