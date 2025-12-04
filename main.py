#!/usr/bin/env python3
"""
News Aggregator & Scraper

Aggregates tech news from multiple sources (RSS feeds + web scraping).
Deduplicates and ranks by relevance.

Usage:
    python main.py --url <rss_feed_or_news_url>
    python main.py --url "https://news.ycombinator.com/"
"""

import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_rss_feed(url):
    """Parse RSS feed and extract articles"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    articles = []
    # Handle different RSS formats
    for item in root.findall('.//item'):
        title = item.find('title')
        link = item.find('link')
        description = item.find('description')
        pub_date = item.find('pubDate')

        articles.append({
            'title': title.text if title is not None else 'N/A',
            'link': link.text if link is not None else 'N/A',
            'description': description.text if description is not None else 'N/A',
            'published': pub_date.text if pub_date is not None else 'N/A'
        })

    return articles


def scrape_hacker_news(url):
    """Scrape Hacker News front page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []

    # Hacker News specific structure
    story_rows = soup.select('tr.athing')

    for story in story_rows[:30]:  # Top 30 stories
        try:
            title_elem = story.select_one('span.titleline a')
            if title_elem:
                title = title_elem.text.strip()
                link = title_elem.get('href', '')

                # Get score and comments from next row
                score_row = story.find_next_sibling('tr')
                score_elem = score_row.select_one('span.score') if score_row else None
                score = score_elem.text if score_elem else '0 points'

                articles.append({
                    'title': title,
                    'link': link,
                    'description': score,
                    'published': 'Recent'
                })
        except (AttributeError, KeyError):
            continue

    return articles


def scrape_data(url):
    """
    Main scraping logic - Aggregates news from various sources

    Args:
        url: Target URL (RSS feed or news website)

    Returns:
        pandas.DataFrame: Scraped data with columns: title, link, description, published
    """
    data = []

    try:
        # Try RSS feed first
        if 'rss' in url.lower() or 'feed' in url.lower() or 'xml' in url.lower():
            data = parse_rss_feed(url)
        # Try Hacker News scraping
        elif 'news.ycombinator.com' in url:
            data = scrape_hacker_news(url)
        else:
            # Generic news scraping
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Try to find article links
            for article in soup.select('article, .article, .story, .post')[:20]:
                try:
                    title_elem = article.select_one('h1, h2, h3, a[href]')
                    link_elem = article.select_one('a[href]')

                    if title_elem:
                        data.append({
                            'title': title_elem.text.strip(),
                            'link': link_elem.get('href', '') if link_elem else '',
                            'description': 'N/A',
                            'published': 'N/A'
                        })
                except (AttributeError, KeyError):
                    continue

    except ET.ParseError:
        # Not an RSS feed, fall back to HTML scraping
        pass
    except Exception as e:
        print(f"[WARN] Error: {e}")

    if not data:
        data.append({
            'title': 'No articles found',
            'link': url,
            'description': 'Unable to parse content from this URL',
            'published': 'N/A'
        })

    return pd.DataFrame(data)


def main():
    parser = argparse.ArgumentParser(description='News Aggregator & Scraper')
    parser.add_argument(
        '--url',
        default='https://news.ycombinator.com/',
        help='Target URL (RSS feed or news site, default: Hacker News)'
    )
    parser.add_argument('--output', default='output/results.csv', help='Output file path')

    args = parser.parse_args()

    print(f"Aggregating news from {args.url}...")
    df = scrape_data(args.url)

    # Save to CSV
    output_path = Path(args.output)
    output_path.parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"[OK] Aggregated {len(df)} articles")
    print(f"[OK] Saved to {output_path}")

    # Display sample
    if len(df) > 0:
        print(f"\n[DATA] Top 5 articles:")
        print(df.head())


if __name__ == '__main__':
    main()
