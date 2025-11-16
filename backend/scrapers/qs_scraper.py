"""
QS World University Rankings Scraper
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from .data_loader import get_qs_sample_data

class QSScraper:
    def __init__(self):
        self.base_url = "https://www.topuniversities.com/world-university-rankings"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self):
        """
        Scrape QS World University Rankings
        Returns: list of dicts with university data
        """
        rankings = []

        try:
            # QS rankings are often loaded via JavaScript, so we might need to use their API
            # This is a simplified version - you may need to adjust based on current website structure
            url = f"{self.base_url}?year=2024"
            response = requests.get(url, headers=self.headers, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Try to find JSON data in script tags (common pattern)
                scripts = soup.find_all('script', type='application/json')
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        # Extract university data from JSON
                        # This part depends on the actual JSON structure
                        if 'universities' in str(data) or 'rankings' in str(data):
                            # Parse the data structure
                            pass
                    except:
                        continue

                # Alternative: scrape from HTML table if available
                table = soup.find('table') or soup.find('div', class_=re.compile('ranking|table'))
                if table:
                    rows = table.find_all('tr')[1:101]  # Top 100

                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 2:
                            try:
                                rank_text = cols[0].get_text(strip=True)
                                rank = int(re.search(r'\d+', rank_text).group()) if re.search(r'\d+', rank_text) else None

                                name = cols[1].get_text(strip=True)

                                # Try to extract country if available
                                country = None
                                country_elem = row.find('span', class_=re.compile('country|location'))
                                if country_elem:
                                    country = country_elem.get_text(strip=True)

                                # Try to extract score if available
                                score = None
                                if len(cols) > 2:
                                    score_text = cols[-1].get_text(strip=True)
                                    try:
                                        score = float(score_text)
                                    except:
                                        pass

                                rankings.append({
                                    'name': name,
                                    'qs_rank': rank,
                                    'qs_score': score,
                                    'country': country
                                })
                            except Exception as e:
                                continue

            print(f"QS Scraper: Found {len(rankings)} universities")

        except Exception as e:
            print(f"Error scraping QS rankings: {e}")

        # If scraping fails, return sample data for demonstration
        if not rankings:
            print("Using sample data for QS rankings")
            rankings = get_qs_sample_data()

        return rankings
