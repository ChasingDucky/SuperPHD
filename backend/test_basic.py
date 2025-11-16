"""
Basic tests for the university ranking system
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Database, University
from scrapers import QSScraper, THEScraper, USNewsScraper, ARWUScraper, CSRankingsScraper

def test_database():
    """Test database operations"""
    print("Testing database operations...")

    # Create test database
    db = Database('test_rankings.db')

    # Add a test university
    db.add_or_update_university(
        name="Test University",
        country="Test Country",
        qs_rank=1,
        qs_score=100.0
    )

    # Search for it
    results = db.search_universities("Test")
    assert len(results) > 0, "Search failed"
    assert results[0].name == "Test University", "Search returned wrong result"

    print("✓ Database tests passed")

    # Cleanup
    db.close()
    os.remove('test_rankings.db')

def test_scrapers():
    """Test all scrapers"""
    print("\nTesting scrapers...")

    scrapers = [
        ("QS", QSScraper()),
        ("THE", THEScraper()),
        ("US News", USNewsScraper()),
        ("ARWU", ARWUScraper()),
        ("CS Rankings", CSRankingsScraper())
    ]

    for name, scraper in scrapers:
        print(f"  Testing {name} scraper...")
        data = scraper.scrape()
        assert len(data) > 0, f"{name} scraper returned no data"
        assert 'name' in data[0], f"{name} scraper data missing 'name' field"
        print(f"  ✓ {name} scraper: {len(data)} universities")

    print("✓ All scrapers passed")

def test_data_merge():
    """Test data merging from multiple sources"""
    print("\nTesting data merge...")

    from app import merge_university_data

    test_data = [
        {'name': 'Harvard University', 'qs_rank': 1, 'country': 'United States'},
        {'name': 'Harvard University', 'the_rank': 2},  # Same university, different source
        {'name': 'Stanford University', 'qs_rank': 5, 'country': 'United States'}
    ]

    merged = merge_university_data(test_data)

    # Should merge Harvard data
    harvard = [u for u in merged if 'Harvard' in u['name']][0]
    assert harvard['qs_rank'] == 1, "QS rank not merged correctly"
    assert harvard['the_rank'] == 2, "THE rank not merged correctly"
    assert harvard['country'] == 'United States', "Country not merged correctly"

    print("✓ Data merge tests passed")

if __name__ == '__main__':
    print("=" * 50)
    print("Running basic tests for University Ranking System")
    print("=" * 50)

    try:
        test_database()
        test_scrapers()
        test_data_merge()

        print("\n" + "=" * 50)
        print("✓ All tests passed successfully!")
        print("=" * 50)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
