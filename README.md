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
# Default: Scrapes Hacker News
python main.py

# Custom news source or RSS feed
python main.py --url "https://example.com/rss"
```

**Live Demo:** Try it now with Hacker News!

```bash
python main.py
# Aggregates 30 top stories from Hacker News
```

## Output Format

Results are saved as CSV with the following columns:

| Column | Description |
|--------|-------------|
| title   | Article title   |
| link  | Article URL  |
| description | Article description or score |
| published | Publication date |

## Testing

```bash
pytest tests/
```

## License

MIT License

## Contact

For questions or custom scraping projects, contact me at [your-email]

---

**Note:** This project scrapes Hacker News by default, which allows scraping. It's fully functional and collects real data from RSS feeds and HTML. Always respect robots.txt and Terms of Service when scraping websites.
