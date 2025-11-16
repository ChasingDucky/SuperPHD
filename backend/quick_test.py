"""
Quick test to verify ARWU scraper improvements
"""
import sys
sys.path.insert(0, '.')

from scrapers import ARWUScraper

print("Testing improved ARWU scraper...")
print("=" * 60)

scraper = ARWUScraper()
rankings = scraper.scrape()

print(f"\nTotal universities found: {len(rankings)}")
print("\nFirst 10 universities:")
print("-" * 60)

for i, uni in enumerate(rankings[:10], 1):
    name = uni.get('name', 'N/A')
    rank = uni.get('arwu_rank', 'N/A')
    score = uni.get('arwu_score', 'N/A')
    country = uni.get('country', 'N/A')

    # Format output
    print(f"\n{i}. {name[:50]}")
    print(f"   Rank: {rank} | Score: {score} | Country: {country}")

# Statistics
print("\n" + "=" * 60)
print("Statistics:")
print("-" * 60)

total = len(rankings)
with_country = sum(1 for uni in rankings if uni.get('country'))
with_score = sum(1 for uni in rankings if uni.get('arwu_score'))

print(f"Total universities: {total}")
print(f"With country info: {with_country} ({with_country/total*100:.1f}%)")
print(f"With score: {with_score} ({with_score/total*100:.1f}%)")

# Check for issues
print("\n" + "=" * 60)
print("Data Quality Checks:")
print("-" * 60)

issues_found = False

# Check for duplicate names
for uni in rankings[:15]:
    name = uni.get('name', '')
    words = name.split()
    if len(words) >= 2 and words.count(words[0]) > 1:
        print(f"⚠️  Duplicate name: {name}")
        issues_found = True

# Check if country equals name (the bug we're fixing)
for uni in rankings[:15]:
    name = uni.get('name', '')
    country = uni.get('country', '')
    if country and country == name:
        print(f"⚠️  Country equals name: {name}")
        issues_found = True

if not issues_found:
    print("✓ No data quality issues found!")

print("\n" + "=" * 60)
print("Note: Country info may be None - this is expected.")
print("The system will merge with sample data to fill in countries.")
print("=" * 60)
