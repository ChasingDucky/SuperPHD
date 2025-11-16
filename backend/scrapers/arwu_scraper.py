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
                                # Extract rank
                                rank_text = cols[0].get_text(strip=True)
                                rank = int(re.search(r'\d+', rank_text).group()) if re.search(r'\d+', rank_text) else None

                                # Extract university name - prefer link text to avoid duplication
                                name_col = cols[1]
                                name_link = name_col.find('a')
                                if name_link:
                                    name = name_link.get_text(strip=True)
                                else:
                                    name = name_col.get_text(strip=True)

                                # Skip if name is empty or invalid
                                if not name or len(name) < 2:
                                    continue

                                # Extract country - look for specific patterns
                                country = None
                                # Try to find country in a specific column or div
                                for col in cols[1:]:
                                    # Look for common country indicators
                                    country_elem = col.find('img', alt=True)  # Country flag
                                    if country_elem:
                                        country = country_elem.get('alt')
                                        break
                                    # Or look for text that looks like a country
                                    col_text = col.get_text(strip=True)
                                    if col_text and len(col_text) < 50 and col_text != name:
                                        # This might be a country
                                        if any(c in col_text for c in ['USA', 'UK', 'China', 'Japan', 'Germany']):
                                            country = col_text
                                            break

                                # Extract score - usually in the last column
                                score = None
                                if len(cols) > 2:
                                    # Try last few columns for score
                                    for col in reversed(cols[-3:]):
                                        score_text = col.get_text(strip=True)
                                        try:
                                            # ARWU scores are typically 0-100
                                            potential_score = float(score_text)
                                            if 0 <= potential_score <= 100:
                                                score = potential_score
                                                break
                                        except:
                                            continue

                                rankings.append({
                                    'name': name,
                                    'arwu_rank': rank,
                                    'arwu_score': score,
                                    'country': country
                                })
                        except Exception as e:
                            # Skip problematic rows but continue
                            continue

            print(f"ARWU Scraper: Found {len(rankings)} universities")

        except Exception as e:
            print(f"Error scraping ARWU rankings: {e}")

        # If scraping fails, return sample data
        if not rankings:
            print("Using sample data for ARWU rankings")
            rankings = get_arwu_sample_data()

        return rankings
