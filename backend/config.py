"""
Configuration file for the University Rankings Scraper
"""

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Database Configuration
DATABASE_PATH = 'rankings.db'

# Scraper Configuration
REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Update Interval (in hours) - for future scheduled updates
UPDATE_INTERVAL = 24

# Ranking Sources URLs
RANKING_URLS = {
    'qs': 'https://www.topuniversities.com/world-university-rankings',
    'the': 'https://www.timeshighereducation.com/world-university-rankings',
    'usnews': 'https://www.usnews.com/education/best-global-universities/rankings',
    'arwu': 'https://www.shanghairanking.com/rankings/arwu/2023',
    'cs': 'https://csrankings.org'
}

# Feature Flags
ENABLE_SAMPLE_DATA = True  # Use sample data if scraping fails
ENABLE_CACHING = False     # Enable caching (future feature)
ENABLE_AUTO_UPDATE = False  # Enable automatic updates (future feature)

# Frontend Configuration
FRONTEND_URL = 'http://localhost:8000'  # For CORS configuration
