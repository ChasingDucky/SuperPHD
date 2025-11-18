"""
Flask API for University Rankings
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Database
from scrapers import QSScraper, THEScraper, USNewsScraper, ARWUScraper, CSRankingsScraper
import threading
import config

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

@app.route('/api/compare', methods=['POST'])
def compare_universities():
    """
    Compare multiple universities
    Request body: {
        "universities": ["Harvard University", "MIT", "Stanford University"],
        "sources": ["qs", "the", "usnews", "arwu", "cs"]  # optional
    }
    """
    data = request.json
    university_names = data.get('universities', [])
    sources = data.get('sources', ['qs', 'the', 'usnews', 'arwu', 'cs'])

    if not university_names or len(university_names) < 2:
        return jsonify({'error': 'Please provide at least 2 universities to compare'}), 400

    results = []
    for name in university_names:
        universities = db.search_universities(name)
        if universities:
            # Get the first match
            uni = universities[0]
            uni_dict = uni.to_dict()

            # Calculate average rank for selected sources
            ranks = []
            for source in sources:
                rank = uni_dict['rankings'][source]['rank']
                if rank is not None:
                    ranks.append(rank)

            avg_rank = sum(ranks) / len(ranks) if ranks else None

            results.append({
                'name': uni_dict['name'],
                'data': uni_dict,
                'average_rank': round(avg_rank, 2) if avg_rank else None,
                'sources_count': len(ranks)
            })
        else:
            results.append({
                'name': name,
                'data': None,
                'error': 'University not found'
            })

    return jsonify(results)

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """
    Get list of all countries in the database
    """
    universities = db.get_all_universities()
    countries = set()

    for uni in universities:
        if uni.country:
            countries.add(uni.country)

    return jsonify(sorted(list(countries)))

@app.route('/api/filter', methods=['GET'])
def filter_universities():
    """
    Filter universities by country
    Query parameters: country, min_rank, max_rank
    """
    country = request.args.get('country')
    min_rank = request.args.get('min_rank', type=int)
    max_rank = request.args.get('max_rank', type=int)

    universities = db.get_all_universities()
    results = []

    for uni in universities:
        uni_dict = uni.to_dict()

        # Filter by country
        if country and uni.country != country:
            continue

        # Filter by rank range (using average rank)
        if min_rank or max_rank:
            ranks = []
            for source in ['qs', 'the', 'usnews', 'arwu', 'cs']:
                rank = uni_dict['rankings'][source]['rank']
                if rank is not None:
                    ranks.append(rank)

            if ranks:
                avg_rank = sum(ranks) / len(ranks)
                if min_rank and avg_rank < min_rank:
                    continue
                if max_rank and avg_rank > max_rank:
                    continue

        results.append(uni_dict)

    return jsonify(results)

@app.route('/api/export', methods=['GET'])
def export_data():
    """
    Export data as CSV
    Query parameter: format (csv)
    """
    import csv
    from io import StringIO

    universities = db.get_all_universities()

    # Create CSV
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'University', 'Country',
        'QS Rank', 'QS Score',
        'THE Rank', 'THE Score',
        'US News Rank', 'US News Score',
        'ARWU Rank', 'ARWU Score',
        'CS Rank', 'CS Score'
    ])

    # Data rows
    for uni in universities:
        writer.writerow([
            uni.name,
            uni.country or '',
            uni.qs_rank or '',
            uni.qs_score or '',
            uni.the_rank or '',
            uni.the_score or '',
            uni.usnews_rank or '',
            uni.usnews_score or '',
            uni.arwu_rank or '',
            uni.arwu_score or '',
            uni.cs_rank or '',
            uni.cs_score or ''
        ])

    # Return CSV as response
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=university_rankings.csv'
    }

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get database statistics
    """
    universities = db.get_all_universities()
    total_universities = len(universities)

    # Count by country
    countries = {}
    for uni in universities:
        if uni.country:
            countries[uni.country] = countries.get(uni.country, 0) + 1

    # Count by ranking source
    source_counts = {
        'qs': 0, 'the': 0, 'usnews': 0, 'arwu': 0, 'cs': 0
    }

    for uni in universities:
        if uni.qs_rank is not None:
            source_counts['qs'] += 1
        if uni.the_rank is not None:
            source_counts['the'] += 1
        if uni.usnews_rank is not None:
            source_counts['usnews'] += 1
        if uni.arwu_rank is not None:
            source_counts['arwu'] += 1
        if uni.cs_rank is not None:
            source_counts['cs'] += 1

    return jsonify({
        'total_universities': total_universities,
        'by_country': dict(sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]),
        'by_source': source_counts,
        'last_updated': 'Check individual university records'
    })

if __name__ == '__main__':
    # Initialize database with sample data on first run
    print("Checking database...")
    if len(db.get_all_universities()) == 0:
        print("Database is empty, populating with sample data...")
        update_database()

    print("\nStarting Flask server...")
    print(f"API will be available at http://localhost:{config.FLASK_PORT}")
    print("\nAvailable endpoints:")
    print("  GET  /api/rankings - Get all rankings")
    print("  GET  /api/search?q=<query> - Search universities")
    print("  POST /api/average-ranking - Calculate average rankings")
    print("  POST /api/compare - Compare multiple universities")
    print("  GET  /api/countries - Get list of countries")
    print("  GET  /api/filter?country=<country> - Filter by country")
    print("  GET  /api/export - Export data as CSV")
    print("  POST /api/update - Update rankings from sources")
    print("  GET  /api/stats - Get database statistics")
    print("\n")

    app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT)
