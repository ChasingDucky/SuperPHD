"""
ARWU (Shanghai Ranking/软科) Scraper
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from .data_loader import get_arwu_sample_data

class ARWUScraper:
    def __init__(self):
        self.base_url = "https://www.shanghairanking.com/rankings/arwu/2023"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self):
        """
        Scrape ARWU (Shanghai Ranking) data
        Returns: list of dicts with university data
        """
        rankings = []

        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for the rankings table
                table = soup.find('table') or soup.find('div', class_=re.compile('ranking'))

                if table:
                    rows = table.find_all('tr')[1:101]  # Top 100

                    for row in rows:
                        try:
                            cols = row.find_all(['td', 'th'])
                            if len(cols) >= 2:
                                rank_text = cols[0].get_text(strip=True)
                                rank = int(re.search(r'\d+', rank_text).group()) if re.search(r'\d+', rank_text) else None

                                name = cols[1].get_text(strip=True)

                                # Extract country if available
                                country = None
                                if len(cols) > 2:
                                    country = cols[2].get_text(strip=True)

                                # Extract score if available
                                score = None
                                if len(cols) > 3:
                                    try:
                                        score = float(cols[-1].get_text(strip=True))
                                    except:
                                        pass

                                rankings.append({
                                    'name': name,
                                    'arwu_rank': rank,
                                    'arwu_score': score,
                                    'country': country
                                })
                        except:
                            continue

            print(f"ARWU Scraper: Found {len(rankings)} universities")

        except Exception as e:
            print(f"Error scraping ARWU rankings: {e}")

        # If scraping fails, return sample data
        if not rankings:
            print("Using sample data for ARWU rankings")
            rankings = get_arwu_sample_data()

        return rankings
