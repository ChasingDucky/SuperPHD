"""
THE (Times Higher Education) World University Rankings Scraper
"""
import requests
from bs4 import BeautifulSoup
import json
import re
from .data_loader import get_the_sample_data

class THEScraper:
    def __init__(self):
        self.base_url = "https://www.timeshighereducation.com/world-university-rankings"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self):
        """
        Scrape THE World University Rankings
        Returns: list of dicts with university data
        """
        rankings = []

        try:
            url = f"{self.base_url}/2024/world-ranking"
            response = requests.get(url, headers=self.headers, timeout=30)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # THE uses various structures, try to find the data
                # Often they have JSON data embedded
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and 'ranking' in script.string.lower():
                        try:
                            # Try to extract JSON data
                            json_match = re.search(r'\{.*"universities".*\}', script.string, re.DOTALL)
                            if json_match:
                                data = json.loads(json_match.group())
                                # Process data based on structure
                        except:
                            continue

            print(f"THE Scraper: Found {len(rankings)} universities")

        except Exception as e:
            print(f"Error scraping THE rankings: {e}")

        # If scraping fails, return sample data
        if not rankings:
            print("Using sample data for THE rankings")
            rankings = get_the_sample_data()

        return rankings
