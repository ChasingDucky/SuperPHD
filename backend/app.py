"""
Flask API for University Rankings
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Database
from scrapers import QSScraper, THEScraper, USNewsScraper, ARWUScraper, CSRankingsScraper
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize database
db = Database('rankings.db')

def merge_university_data(universities_list):
    """
    Merge data from multiple ranking sources for the same university
    """
    merged = {}

    for uni_data in universities_list:
        name = uni_data.get('name', '').strip()
        if not name:
            continue

        # Normalize university names for better matching
        normalized_name = normalize_university_name(name)

        if normalized_name not in merged:
            merged[normalized_name] = {
                'name': name,  # Keep original name
                'country': uni_data.get('country')
            }

        # Merge rankings
        for key in ['qs_rank', 'qs_score', 'the_rank', 'the_score',
                    'usnews_rank', 'usnews_score', 'arwu_rank', 'arwu_score',
                    'cs_rank', 'cs_score']:
            if key in uni_data and uni_data[key] is not None:
                merged[normalized_name][key] = uni_data[key]

        # Update country if not set
        if not merged[normalized_name].get('country') and uni_data.get('country'):
            merged[normalized_name]['country'] = uni_data['country']

    return list(merged.values())

def normalize_university_name(name):
    """
    Normalize university names for better matching across different rankings
    """
    # Convert to lowercase and remove common variations
    normalized = name.lower()
    normalized = normalized.replace('the ', '')
    normalized = normalized.replace(' (', ' ')
    normalized = normalized.replace(')', '')
    normalized = normalized.replace(',', '')
    normalized = normalized.strip()
    return normalized

def update_database():
    """
    Scrape all rankings and update database
    """
    print("Starting to scrape rankings...")

    all_universities = []

    # Scrape QS
    print("Scraping QS rankings...")
    qs_scraper = QSScraper()
    all_universities.extend(qs_scraper.scrape())

    # Scrape THE
    print("Scraping THE rankings...")
    the_scraper = THEScraper()
    all_universities.extend(the_scraper.scrape())

    # Scrape US News
    print("Scraping US News rankings...")
    usnews_scraper = USNewsScraper()
    all_universities.extend(usnews_scraper.scrape())

    # Scrape ARWU
    print("Scraping ARWU rankings...")
    arwu_scraper = ARWUScraper()
    all_universities.extend(arwu_scraper.scrape())

    # Scrape CS Rankings
    print("Scraping CS Rankings...")
    cs_scraper = CSRankingsScraper()
    all_universities.extend(cs_scraper.scrape())

    # Merge data from different sources
    print("Merging data from different sources...")
    merged_universities = merge_university_data(all_universities)

    # Update database
    print(f"Updating database with {len(merged_universities)} universities...")
    for uni in merged_universities:
        name = uni.pop('name')
        db.add_or_update_university(name, **uni)

    print("Database update complete!")

@app.route('/api/rankings', methods=['GET'])
def get_rankings():
    """
    Get all university rankings
    """
    universities = db.get_all_universities()
    return jsonify([uni.to_dict() for uni in universities])

@app.route('/api/search', methods=['GET'])
def search_universities():
    """
    Search universities by name
    Query parameter: q (search query)
    """
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    universities = db.search_universities(query)
    return jsonify([uni.to_dict() for uni in universities])

@app.route('/api/university/<int:university_id>', methods=['GET'])
def get_university(university_id):
    """
    Get a specific university by ID
    """
    university = db.session.query(db.session.query(University).get(university_id))
    if not university:
        return jsonify({'error': 'University not found'}), 404
    return jsonify(university.to_dict())

@app.route('/api/average-ranking', methods=['POST'])
def calculate_average_ranking():
    """
    Calculate average ranking for universities based on selected sources
    Request body: {
        "sources": ["qs", "the", "usnews", "arwu", "cs"],
        "universities": [list of university IDs or search query]
    }
    """
    data = request.json
    sources = data.get('sources', [])
    query = data.get('query', '')

    if not sources:
        return jsonify({'error': 'No ranking sources specified'}), 400

    # Get universities
    if query:
        universities = db.search_universities(query)
    else:
        universities = db.get_all_universities()

    results = []
    for uni in universities:
        ranks = []
        uni_dict = uni.to_dict()

        # Collect ranks from selected sources
        for source in sources:
            rank = uni_dict['rankings'][source]['rank']
            if rank is not None:
                ranks.append(rank)

        # Calculate average if there are any ranks
        if ranks:
            avg_rank = sum(ranks) / len(ranks)
            results.append({
                'university': uni_dict,
                'average_rank': round(avg_rank, 2),
                'sources_count': len(ranks),
                'total_sources': len(sources)
            })

    # Sort by average rank
    results.sort(key=lambda x: x['average_rank'])

    return jsonify(results)

@app.route('/api/update', methods=['POST'])
def trigger_update():
    """
    Trigger database update (scrape all rankings)
    """
    # Run update in background thread to avoid timeout
    thread = threading.Thread(target=update_database)
    thread.daemon = True
    thread.start()

    return jsonify({'message': 'Update started in background'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get database statistics
    """
    total_universities = len(db.get_all_universities())

    return jsonify({
        'total_universities': total_universities,
        'last_updated': 'Check individual university records'
    })

if __name__ == '__main__':
    # Initialize database with sample data on first run
    print("Checking database...")
    if len(db.get_all_universities()) == 0:
        print("Database is empty, populating with sample data...")
        update_database()

    print("\nStarting Flask server...")
    print("API will be available at http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /api/rankings - Get all rankings")
    print("  GET  /api/search?q=<query> - Search universities")
    print("  POST /api/average-ranking - Calculate average rankings")
    print("  POST /api/update - Update rankings from sources")
    print("  GET  /api/stats - Get database statistics")
    print("\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
