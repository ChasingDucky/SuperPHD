"""
CS Rankings Scraper (csrankings.org)
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from .data_loader import get_cs_sample_data

class CSRankingsScraper:
    def __init__(self):
        self.base_url = "https://csrankings.org"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self):
        """
        Scrape CS Rankings data
        Returns: list of dicts with university data
        """
        rankings = []

        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # CS Rankings data is usually in a table or loaded via JavaScript
                # Look for the data in the HTML or scripts
                table = soup.find('table', class_=re.compile('ranking'))

                if table:
                    rows = table.find_all('tr')[1:101]  # Top 100

                    for idx, row in enumerate(rows, 1):
                        try:
                            cols = row.find_all(['td', 'th'])
                            if len(cols) >= 2:
                                name = cols[1].get_text(strip=True)

                                score = None
                                if len(cols) > 2:
                                    try:
                                        score = float(cols[2].get_text(strip=True))
                                    except:
                                        pass

                                rankings.append({
                                    'name': name,
                                    'cs_rank': idx,
                                    'cs_score': score
                                })
                        except:
                            continue

            print(f"CS Rankings Scraper: Found {len(rankings)} universities")

        except Exception as e:
            print(f"Error scraping CS Rankings: {e}")

        # If scraping fails, return sample data
        if not rankings:
            print("Using sample data for CS Rankings")
            rankings = get_cs_sample_data()

        return rankings
