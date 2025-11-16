"""
Test ARWU scraper specifically to debug parsing issues
"""
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.shanghairanking.com/rankings/arwu/2023"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("Fetching ARWU page...")
response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')

# Find the table
table = soup.find('table')
if not table:
    print("No table found, looking for divs...")
    table = soup.find('div', class_=re.compile('ranking'))

if table:
    print(f"\nFound table: {table.name}")
    rows = table.find_all('tr')[:5]  # First 5 rows

    for i, row in enumerate(rows):
        print(f"\n--- Row {i} ---")
        cols = row.find_all(['td', 'th'])
        print(f"Number of columns: {len(cols)}")

        for j, col in enumerate(cols):
            # Get text
            text = col.get_text(strip=True)
            # Get HTML for inspection
            html = str(col)[:200]
            print(f"  Col {j}: '{text[:50]}...' ")

            # Check for links (university names often in links)
            link = col.find('a')
            if link:
                print(f"    Link text: '{link.get_text(strip=True)}'")

            # Check for specific classes
            if col.get('class'):
                print(f"    Classes: {col.get('class')}")
else:
    print("No table found!")

    # Look for other structures
    print("\nLooking for alternative structures...")
    rankings = soup.find_all('div', class_=re.compile('rank'))
    print(f"Found {len(rankings)} divs with 'rank' in class")
