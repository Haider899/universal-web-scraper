# Configuration for Universal Scraper
SCRAPER_CONFIG = {
    'default_delay': 2,
    'max_retries': 3,
    'timeout': 30,
    'max_pages': 100,
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0'
    ],
    'skip_extensions': ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.xls', '.xlsx'],
    'skip_protocols': ['mailto:', 'tel:', 'javascript:', 'ftp:']
}
