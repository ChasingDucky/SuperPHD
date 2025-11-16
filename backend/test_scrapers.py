"""
Test script to check scrapers and debug issues
"""
import sys
import requests
from scrapers import QSScraper, THEScraper, USNewsScraper, ARWUScraper, CSRankingsScraper

def test_website_access():
    """Test if we can access the ranking websites"""
    print("Testing website accessibility...")
    print("=" * 60)

    websites = {
        'QS': 'https://www.topuniversities.com/world-university-rankings',
        'THE': 'https://www.timeshighereducation.com/world-university-rankings',
        'US News': 'https://www.usnews.com/education/best-global-universities/rankings',
        'ARWU': 'https://www.shanghairanking.com/rankings/arwu/2023',
        'CS Rankings': 'https://csrankings.org'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for name, url in websites.items():
        try:
            print(f"\n{name}: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Content length: {len(response.content)} bytes")

            # Check if it's HTML or JSON
            content_type = response.headers.get('Content-Type', '')
            print(f"  Content-Type: {content_type}")

            # Check for common indicators of JavaScript-loaded content
            if 'text/html' in content_type:
                if b'__NEXT_DATA__' in response.content or b'window.__data' in response.content:
                    print("  ⚠️  Uses client-side JavaScript rendering")
                else:
                    print("  ✓ Server-side rendered HTML")

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)

def test_scrapers():
    """Test each scraper"""
    print("\n\nTesting scrapers...")
    print("=" * 60)

    scrapers = [
        ("QS", QSScraper()),
        ("THE", THEScraper()),
        ("US News", USNewsScraper()),
        ("ARWU", ARWUScraper()),
        ("CS Rankings", CSRankingsScraper())
    ]

    for name, scraper in scrapers:
        print(f"\n{name} Scraper:")
        try:
            data = scraper.scrape()
            print(f"  Found {len(data)} universities")

            if data and len(data) > 0:
                print(f"  Sample data: {data[0]}")
            else:
                print("  No data returned - using sample data")

        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)

if __name__ == '__main__':
    print("University Ranking Scraper - Diagnostic Tool")
    print("=" * 60)

    test_website_access()
    test_scrapers()

    print("\n\nRECOMMENDATIONS:")
    print("-" * 60)
    print("Most university ranking websites use JavaScript to load data.")
    print("To scrape them effectively, you need:")
    print("  1. Use Selenium with headless browser")
    print("  2. Find and use their public APIs (if available)")
    print("  3. Use the sample data provided for demonstration")
    print("\nCurrent implementation uses sample data as fallback.")
