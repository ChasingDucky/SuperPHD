"""
Scrapers package for university rankings
"""
from .qs_scraper import QSScraper
from .the_scraper import THEScraper
from .usnews_scraper import USNewsScraper
from .arwu_scraper import ARWUScraper
from .csrankings_scraper import CSRankingsScraper

__all__ = ['QSScraper', 'THEScraper', 'USNewsScraper', 'ARWUScraper', 'CSRankingsScraper']
