# News Aggregator & Scraper

![Python](https://img.shields.io/badge/-Python-blue) ![Feedparser](https://img.shields.io/badge/-Feedparser-blue) ![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-blue) ![SQLite](https://img.shields.io/badge/-SQLite-blue)

Aggregates tech news from multiple sources (RSS feeds + web scraping). Deduplicates and ranks by relevance.

## Features

- Parses RSS feeds from 10+ tech sites
- Scrapes article content for full text
- Deduplicates articles by title similarity
- SQLite database for storage
- Basic relevance ranking

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/news-aggregator.git
cd news-aggregator

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py --url "https://example.com" --output output/results.csv
```

## Output Format

Results are saved as CSV with the following columns:

| Column | Description |
|--------|-------------|
| name   | Item name   |
| value  | Item value  |
| url    | Source URL  |

## Testing

```bash
pytest tests/
```

## License

MIT License

## Contact

For questions or custom scraping projects, contact me at [your-email]

---

**Note:** This is a portfolio project demonstrating web scraping capabilities. Use responsibly and respect websites' Terms of Service.
