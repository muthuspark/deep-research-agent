# Deep Research Agent - Usage Guide

## Getting Recent and Up-to-Date Information

The Deep Research Agent now includes powerful date filtering and recency prioritization features to ensure you get the most current information available.

## 🕐 Date Filtering Features

### 1. **Automatic Recent Data Prioritization (Default)**
By default, the agent prioritizes recent information:
- Adds date terms to search queries (2024, 2025, "latest", "recent", "current")
- Filters search results to last 2 years
- Sorts results by freshness/recency

### 2. **Custom Date Range Filtering**
Limit searches to specific time periods:
```bash
# Get information from last 30 days only
python main.py --days-back 30 "latest AI developments"

# Get information from last 7 days
python main.py --days-back 7 "stock market news"

# Get information from last year
python main.py --days-back 365 "climate change reports"
```

### 3. **Disable Recent Prioritization**
For historical research or when you want all available information:
```bash
python main.py --no-recent "history of artificial intelligence"
```

## 🎯 Command Line Usage

### Basic Usage with Recent Data (Default)
```bash
python main.py "latest trends in renewable energy"
```

### Advanced Usage with Date Filtering
```bash
# Recent data with custom parameters
python main.py --breadth 6 --depth 3 --days-back 90 "cryptocurrency market analysis"

# Disable recent prioritization for comprehensive historical research
python main.py --no-recent --breadth 8 --depth 2 "evolution of machine learning"

# Quick answer with recent data
python main.py --type answer --days-back 7 "current inflation rate"
```

### Interactive Mode with Date Options
```bash
python main.py --interactive
```

## 📊 Configuration Options

### Environment Variables
Add to your `.env` file:
```bash
# Date Filtering Configuration
DEFAULT_PRIORITIZE_RECENT=true
DEFAULT_DAYS_BACK=730  # 2 years in days
```

### Command Line Arguments
```bash
--recent             # Explicitly enable recent prioritization (default)
--no-recent          # Disable recent prioritization
--days-back N        # Only search last N days
--breadth N          # Research breadth (1-10)
--depth N            # Research depth (1-5)
--type report|answer # Output type
--interactive        # Force interactive mode
```

## 🔍 How Date Filtering Works

### 1. **Query Enhancement**
- Original query: "artificial intelligence developments"
- Enhanced query: "artificial intelligence developments 2024 latest recent"

### 2. **Search Filtering**
- Adds date range filters: `after:2023-01-01`
- Prioritizes results with recent publication dates
- Includes date-related metadata in scraping

### 3. **Result Scoring**
- Results with recent dates in URL get higher scores
- Content with "2024", "latest", "recent" keywords prioritized
- Sorts by freshness before processing

## 📋 Best Practices

### For Current Events & News
```bash
# Breaking news - last 24 hours
python main.py --days-back 1 "latest news on [topic]"

# Weekly updates
python main.py --days-back 7 "weekly [industry] report"
```

### For Market Analysis
```bash
# Current market conditions
python main.py --days-back 30 "current stock market analysis"

# Quarterly reports
python main.py --days-back 90 "Q4 2024 earnings reports"
```

### For Technology Research
```bash
# Latest tech developments
python main.py --days-back 60 "latest AI breakthroughs 2024"

# Recent product launches
python main.py --days-back 30 "new product releases [company]"
```

### For Academic Research
```bash
# Recent publications
python main.py --days-back 180 "recent research papers on [topic]"

# Disable date filtering for comprehensive literature review
python main.py --no-recent "comprehensive review of [academic topic]"
```

## ⚠️ Important Notes

1. **Data Freshness**: The recency of results depends on:
   - How recently the information was published online
   - How quickly search engines index new content
   - The availability of recent sources on your topic

2. **Balance**: For comprehensive research, consider running both:
   - Recent data search: `--days-back 90`
   - Historical context: `--no-recent`

3. **Performance**: More recent data filtering may return fewer results but higher quality/relevance.

## 🛠️ Troubleshooting

### Getting Too Few Results?
- Increase `--days-back` value
- Use `--no-recent` for broader search
- Increase `--breadth` parameter

### Getting Outdated Information?
- Decrease `--days-back` value
- Add specific year to your query
- Use terms like "latest", "current", "2024" in your query

### Mixed Results Quality?
- Use moderate `--days-back` values (30-90 days)
- Combine with higher `--depth` for better analysis
- Try different query phrasings

## 📝 Examples

### Recent Business News
```bash
python main.py --days-back 14 --breadth 5 "latest business mergers and acquisitions"
```

### Current Technology Trends
```bash
python main.py --days-back 30 --depth 3 "emerging technology trends 2024"
```

### Historical Analysis
```bash
python main.py --no-recent --breadth 8 --depth 2 "history of renewable energy development"
```

### Quick Recent Update
```bash
python main.py --type answer --days-back 7 "what happened in AI this week"
```

## 🔧 Advanced Configuration

For developers and power users, you can modify the date filtering behavior in:
- `src/firecrawl_client.py`: Adjust search parameters
- `src/deep_research.py`: Modify query generation logic
- `main.py`: Add custom date filtering options

This flexible system ensures you can get exactly the type of information you need, whether it's breaking news or comprehensive historical analysis. 