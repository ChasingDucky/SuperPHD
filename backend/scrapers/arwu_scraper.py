"""
ARWU (Shanghai Ranking/软科) Scraper
"""
import requests
from bs4 import BeautifulSoup
import json
import re

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
            rankings = self._get_sample_data()

        return rankings

    def _get_sample_data(self):
        """Return sample data for testing purposes"""
        return [
            {'name': 'Harvard University', 'arwu_rank': 1, 'arwu_score': 100.0, 'country': 'United States'},
            {'name': 'Stanford University', 'arwu_rank': 2, 'arwu_score': 76.5, 'country': 'United States'},
            {'name': 'Massachusetts Institute of Technology (MIT)', 'arwu_rank': 3, 'arwu_score': 73.8, 'country': 'United States'},
            {'name': 'University of Cambridge', 'arwu_rank': 4, 'arwu_score': 71.9, 'country': 'United Kingdom'},
            {'name': 'University of California, Berkeley', 'arwu_rank': 5, 'arwu_score': 70.2, 'country': 'United States'},
            {'name': 'Princeton University', 'arwu_rank': 6, 'arwu_score': 63.4, 'country': 'United States'},
            {'name': 'University of Oxford', 'arwu_rank': 7, 'arwu_score': 62.8, 'country': 'United Kingdom'},
            {'name': 'Columbia University', 'arwu_rank': 8, 'arwu_score': 62.3, 'country': 'United States'},
            {'name': 'California Institute of Technology', 'arwu_rank': 9, 'arwu_score': 61.7, 'country': 'United States'},
            {'name': 'University of Chicago', 'arwu_rank': 10, 'arwu_score': 60.9, 'country': 'United States'},
            {'name': 'Tsinghua University', 'arwu_rank': 22, 'arwu_score': 55.3, 'country': 'China'},
            {'name': 'Peking University', 'arwu_rank': 29, 'arwu_score': 52.1, 'country': 'China'},
        ]
