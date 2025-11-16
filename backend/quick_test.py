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
print("\nFirst 5 universities:")
print("-" * 60)

for i, uni in enumerate(rankings[:5], 1):
    print(f"\n{i}. {uni.get('name', 'N/A')}")
    print(f"   Rank: {uni.get('arwu_rank', 'N/A')}")
    print(f"   Score: {uni.get('arwu_score', 'N/A')}")
    print(f"   Country: {uni.get('country', 'N/A')}")

# Check for the duplicate name issue
print("\n" + "=" * 60)
print("Checking for duplicate name issues...")
duplicates_found = False
for uni in rankings[:10]:
    name = uni.get('name', '')
    # Check if name appears twice
    words = name.split()
    if len(words) >= 2:
        first_word = words[0]
        if words.count(first_word) > 1:
            print(f"⚠️  Possible duplicate: {name}")
            duplicates_found = True

if not duplicates_found:
    print("✓ No duplicate names found!")

print("\n" + "=" * 60)
print("Sample data comparison:")
print("-" * 60)

from scrapers.data_loader import get_arwu_sample_data
sample = get_arwu_sample_data()
print(f"Sample data has {len(sample)} universities")
print(f"First sample: {sample[0] if sample else 'None'}")
