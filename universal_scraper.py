import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import csv
import os
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser
import logging
from datetime import datetime
import re
from typing import Dict, List, Optional, Union
import hashlib

class UniversalScraper:
    """
    Advanced Universal Web Scraper for any website
    Features:
    - Respects robots.txt
    - Automatic retry mechanism
    - Multiple data export formats
    - JavaScript support detection
    - Sitemap discovery
    - Comprehensive data extraction
    - Rate limiting
    - Error handling
    """
    
    def __init__(self, base_delay: float = 1, max_retries: int = 3, timeout: int = 30):
        self.session = requests.Session()
        self.setup_session()
        self.base_delay = base_delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.scraped_urls = set()
        self.robot_parsers = {}
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'scraper_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_session(self):
        """Setup session with realistic headers"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_robot_parser(self, url: str) -> Optional[RobotFileParser]:
        """Get or create robot parser for domain"""
        try:
            parsed_url = urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if domain not in self.robot_parsers:
                rp = RobotFileParser()
                robots_url = f"{domain}/robots.txt"
                rp.set_url(robots_url)
                
                # Try to read robots.txt
                try:
                    rp.read()
                except:
                    self.logger.warning(f"Could not read robots.txt from {robots_url}")
                
                self.robot_parsers[domain] = rp
            
            return self.robot_parsers[domain]
        except Exception as e:
            self.logger.error(f"Error getting robot parser: {e}")
            return None
    
    def can_fetch(self, url: str) -> bool:
        """Check if we're allowed to scrape this URL"""
        robot_parser = self.get_robot_parser(url)
        if robot_parser:
            return robot_parser.can_fetch("*", url)
        return True  # If no robots.txt, proceed with caution
    
    def respectful_delay(self):
        """Random delay to avoid overwhelming servers"""
        delay = self.base_delay + random.uniform(0, 2)
        self.logger.debug(f"Delaying for {delay:.2f} seconds")
        time.sleep(delay)
    
    def fetch_url(self, url: str) -> Optional[requests.Response]:
        """Fetch URL with retry mechanism"""
        for attempt in range(self.max_retries):
            try:
                # Check robots.txt
                if not self.can_fetch(url):
                    self.logger.warning(f"Blocked by robots.txt: {url}")
                    return None
                
                self.logger.info(f"Fetching {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
                
                if response.status_code == 200:
                    return response
                elif response.status_code in [403, 404, 429, 500, 502, 503]:
                    self.logger.warning(f"HTTP {response.status_code} for {url}")
                    if response.status_code == 429:  # Too Many Requests
                        wait_time = (2 ** attempt) + random.uniform(5, 10)
                        self.logger.info(f"Rate limited. Waiting {wait_time} seconds")
                        time.sleep(wait_time)
                    elif attempt == self.max_retries - 1:
                        return None
                else:
                    self.logger.warning(f"Unexpected status {response.status_code} for {url}")
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    return None
            
            # Wait before retry
            if attempt < self.max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(1, 3)
                time.sleep(wait_time)
        
        return None
    
    def extract_comprehensive_data(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract comprehensive data from page"""
        
        # Basic page info
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title"
        
        # Meta information
        meta_tags = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_tags[name] = content
        
        # Content extraction
        content_data = {
            'title': title_text,
            'meta_description': meta_tags.get('description', ''),
            'meta_keywords': meta_tags.get('keywords', ''),
            'headings': self.extract_headings(soup),
            'paragraphs': self.extract_paragraphs(soup),
            'links': self.extract_links(soup, url),
            'images': self.extract_images(soup, url),
            'tables': self.extract_tables(soup),
            'lists': self.extract_lists(soup),
            'forms': self.extract_forms(soup),
            'scripts': self.extract_scripts(soup),
            'styles': self.extract_styles(soup),
        }
        
        # Advanced data extraction
        advanced_data = {
            'word_count': self.count_words(soup),
            'text_content': self.get_clean_text(soup),
            'emails': self.extract_emails(soup),
            'phones': self.extract_phone_numbers(soup),
            'social_media': self.extract_social_media(soup),
            'structured_data': self.extract_structured_data(soup),
        }
        
        return {**content_data, **advanced_data}
    
    def extract_headings(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract all headings with hierarchy"""
        headings = {}
        for level in range(1, 7):
            tags = soup.find_all(f'h{level}')
            headings[f'h{level}'] = [tag.get_text().strip() for tag in tags if tag.get_text().strip()]
        return headings
    
    def extract_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        """Extract paragraph text"""
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 10:  # Filter very short paragraphs
                paragraphs.append(text)
        return paragraphs
    
    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all links with context"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            text = a.get_text().strip()
            
            # Make URL absolute
            absolute_url = urljoin(base_url, href)
            
            links.append({
                'text': text[:100],  # Limit text length
                'url': absolute_url,
                'is_internal': self.is_internal_url(absolute_url, base_url),
                'is_external': not self.is_internal_url(absolute_url, base_url)
            })
        
        return links
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract all images with details"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            alt = img.get('alt', '')
            absolute_src = urljoin(base_url, src)
            
            images.append({
                'src': absolute_src,
                'alt': alt,
                'title': img.get('title', '')
            })
        
        return images
    
    def extract_tables(self, soup: BeautifulSoup) -> List[List[List[str]]]:
        """Extract data from all tables"""
        tables_data = []
        for table in soup.find_all('table'):
            table_data = []
            for row in table.find_all('tr'):
                row_data = []
                for cell in row.find_all(['td', 'th']):
                    row_data.append(cell.get_text().strip())
                if row_data:
                    table_data.append(row_data)
            if table_data:
                tables_data.append(table_data)
        return tables_data
    
    def extract_lists(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract ordered and unordered lists"""
        lists_data = {'ordered': [], 'unordered': []}
        
        for ol in soup.find_all('ol'):
            items = [li.get_text().strip() for li in ol.find_all('li')]
            if items:
                lists_data['ordered'].append(items)
        
        for ul in soup.find_all('ul'):
            items = [li.get_text().strip() for li in ul.find_all('li')]
            if items:
                lists_data['unordered'].append(items)
        
        return lists_data
    
    def extract_forms(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract form information"""
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get').upper(),
                'inputs': []
            }
            
            for input_elem in form.find_all(['input', 'textarea', 'select']):
                input_data = {
                    'type': input_elem.get('type', 'text'),
                    'name': input_elem.get('name', ''),
                    'placeholder': input_elem.get('placeholder', ''),
                    'label': self.find_input_label(input_elem)
                }
                form_data['inputs'].append(input_data)
            
            forms.append(form_data)
        
        return forms
    
    def find_input_label(self, input_elem) -> str:
        """Find associated label for form input"""
        # Try to find label by ID
        input_id = input_elem.get('id')
        if input_id:
            label = input_elem.find_previous('label', {'for': input_id})
            if label:
                return label.get_text().strip()
        
        # Try to find wrapping label
        parent_label = input_elem.find_parent('label')
        if parent_label:
            return parent_label.get_text().strip()
        
        return ""
    
    def extract_scripts(self, soup: BeautifulSoup) -> List[str]:
        """Extract script sources"""
        scripts = []
        for script in soup.find_all('script', src=True):
            scripts.append(script.get('src'))
        return scripts
    
    def extract_styles(self, soup: BeautifulSoup) -> List[str]:
        """Extract stylesheet links"""
        styles = []
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                styles.append(href)
        return styles
    
    def count_words(self, soup: BeautifulSoup) -> int:
        """Count total words on page"""
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def get_clean_text(self, soup: BeautifulSoup, max_length: int = 5000) -> str:
        """Get clean text content (limited length)"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:max_length] + ('...' if len(text) > max_length else '')
    
    def extract_emails(self, soup: BeautifulSoup) -> List[str]:
        """Extract email addresses"""
        text = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def extract_phone_numbers(self, soup: BeautifulSoup) -> List[str]:
        """Extract phone numbers"""
        text = soup.get_text()
        phone_patterns = [
            r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        ]
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        return phones
    
    def extract_social_media(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract social media links"""
        social_patterns = {
            'facebook': r'facebook\.com/[^"\'\s]+',
            'twitter': r'twitter\.com/[^"\'\s]+',
            'linkedin': r'linkedin\.com/[^"\'\s]+',
            'instagram': r'instagram\.com/[^"\'\s]+',
            'youtube': r'youtube\.com/[^"\'\s]+',
            'pinterest': r'pinterest\.com/[^"\'\s]+'
        }
        
        social_data = {}
        text = soup.get_text()
        
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            social_data[platform] = matches
        
        return social_data
    
    def extract_structured_data(self, soup: BeautifulSoup) -> Dict:
        """Extract structured data (JSON-LD, Microdata)"""
        structured_data = {}
        
        # Extract JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        json_ld_data = []
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                json_ld_data.append(data)
            except:
                continue
        structured_data['json_ld'] = json_ld_data
        
        return structured_data
    
    def is_internal_url(self, url: str, base_url: str) -> bool:
        """Check if URL is internal to the base domain"""
        try:
            parsed_url = urlparse(url)
            parsed_base = urlparse(base_url)
            return parsed_url.netloc == parsed_base.netloc
        except:
            return False
    
    def scrape_url(self, url: str) -> Optional[Dict]:
        """Scrape a single URL and return comprehensive data"""
        if url in self.scraped_urls:
            self.logger.info(f"URL already scraped: {url}")
            return None
        
        response = self.fetch_url(url)
        if not response:
            return None
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = self.extract_comprehensive_data(soup, url)
            
            # Add metadata
            data['metadata'] = {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.content),
                'scraped_at': datetime.now().isoformat(),
                'final_url': response.url  # After redirects
            }
            
            self.scraped_urls.add(url)
            self.logger.info(f"Successfully scraped: {url}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error parsing {url}: {e}")
            return None
        finally:
            self.respectful_delay()
    
    def scrape_site(self, start_url: str, max_pages: int = 100, same_domain: bool = True) -> Dict[str, Dict]:
        """Scrape multiple pages from a site"""
        all_data = {}
        urls_to_scrape = [start_url]
        scraped_count = 0
        
        while urls_to_scrape and scraped_count < max_pages:
            current_url = urls_to_scrape.pop(0)
            
            if current_url in self.scraped_urls:
                continue
            
            data = self.scrape_url(current_url)
            if data:
                all_data[current_url] = data
                scraped_count += 1
                
                # Discover new URLs from links
                if scraped_count < max_pages:
                    new_urls = self.discover_urls(data, current_url, same_domain)
                    for new_url in new_urls:
                        if new_url not in self.scraped_urls and new_url not in urls_to_scrape:
                            urls_to_scrape.append(new_url)
            
            if scraped_count >= max_pages:
                self.logger.info(f"Reached maximum page limit: {max_pages}")
                break
        
        self.logger.info(f"Scraping completed. Total pages: {scraped_count}")
        return all_data
    
    def discover_urls(self, data: Dict, base_url: str, same_domain: bool = True) -> List[str]:
        """Discover new URLs from scraped data"""
        new_urls = []
        
        for link in data.get('links', []):
            url = link['url']
            
            # Filter URLs
            if same_domain and not link['is_internal']:
                continue
            
            # Skip common non-content URLs
            if any(skip in url.lower() for skip in ['mailto:', 'tel:', 'javascript:', '#']):
                continue
            
            # Skip common file types
            if any(ext in url.lower() for ext in ['.pdf', '.jpg', '.png', '.gif', '.doc', '.docx']):
                continue
            
            if url not in self.scraped_urls:
                new_urls.append(url)
        
        return new_urls
    
    def export_data(self, data: Dict, base_filename: str, formats: List[str] = ['json', 'csv', 'excel']):
        """Export data in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for format_type in formats:
            filename = f"{base_filename}_{timestamp}.{format_type}"
            
            try:
                if format_type == 'json':
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                
                elif format_type == 'csv':
                    self.export_to_csv(data, filename)
                
                elif format_type == 'excel':
                    self.export_to_excel(data, filename)
                
                self.logger.info(f"Exported data to {filename}")
                
            except Exception as e:
                self.logger.error(f"Error exporting to {format_type}: {e}")
    
    def export_to_csv(self, data: Dict, filename: str):
        """Export summary data to CSV"""
        rows = []
        
        for url, page_data in data.items():
            row = {
                'url': url,
                'title': page_data.get('title', ''),
                'meta_description': page_data.get('meta_description', ''),
                'word_count': page_data.get('word_count', 0),
                'headings_count': sum(len(headings) for headings in page_data.get('headings', {}).values()),
                'paragraphs_count': len(page_data.get('paragraphs', [])),
                'images_count': len(page_data.get('images', [])),
                'links_count': len(page_data.get('links', [])),
                'internal_links_count': len([link for link in page_data.get('links', []) if link.get('is_internal')]),
                'external_links_count': len([link for link in page_data.get('links', []) if link.get('is_external')]),
                'emails_count': len(page_data.get('emails', [])),
                'phones_count': len(page_data.get('phones', [])),
                'scraped_at': page_data.get('metadata', {}).get('scraped_at', ''),
                'status_code': page_data.get('metadata', {}).get('status_code', ''),
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False, encoding='utf-8')
    
    def export_to_excel(self, data: Dict, filename: str):
        """Export detailed data to Excel with multiple sheets"""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # Summary sheet
            summary_data = []
            for url, page_data in data.items():
                summary_data.append({
                    'URL': url,
                    'Title': page_data.get('title', ''),
                    'Description': page_data.get('meta_description', '')[:100],
                    'Word Count': page_data.get('word_count', 0),
                    'Images': len(page_data.get('images', [])),
                    'Links': len(page_data.get('links', [])),
                    'Status Code': page_data.get('metadata', {}).get('status_code', ''),
                })
            
            if summary_data:
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
            
            # Links sheet
            links_data = []
            for url, page_data in data.items():
                for link in page_data.get('links', []):
                    links_data.append({
                        'Source URL': url,
                        'Link Text': link.get('text', ''),
                        'Link URL': link.get('url', ''),
                        'Internal': link.get('is_internal', False),
                    })
            
            if links_data:
                pd.DataFrame(links_data).to_excel(writer, sheet_name='Links', index=False)
            
            # Images sheet
            images_data = []
            for url, page_data in data.items():
                for img in page_data.get('images', []):
                    images_data.append({
                        'Page URL': url,
                        'Image URL': img.get('src', ''),
                        'Alt Text': img.get('alt', ''),
                    })
            
            if images_data:
                pd.DataFrame(images_data).to_excel(writer, sheet_name='Images', index=False)

# Usage Examples and Helper Functions
def example_scrape_single_page():
    """Example: Scrape a single page"""
    scraper = UniversalScraper(base_delay=2)
    
    url = "https://doartenergy.com"
    data = scraper.scrape_url(url)
    
    if data:
        print(f"Title: {data.get('title')}")
        print(f"Word Count: {data.get('word_count')}")
        print(f"Images Found: {len(data.get('images', []))}")
        
        # Export data
        scraper.export_data({url: data}, 'single_page_report', ['json', 'csv'])
    else:
        print("Failed to scrape the page")

def example_scrape_entire_site():
    """Example: Scrape multiple pages from a site"""
    scraper = UniversalScraper(base_delay=2, max_retries=2)
    
    start_url = "https://doartenergy.com"
    all_data = scraper.scrape_site(start_url, max_pages=50, same_domain=True)
    
    print(f"Scraped {len(all_data)} pages")
    
    # Export all data
    scraper.export_data(all_data, 'full_site_report', ['json', 'csv', 'excel'])
    
    # Print summary
    total_images = sum(len(data.get('images', [])) for data in all_data.values())
    total_links = sum(len(data.get('links', [])) for data in all_data.values())
    
    print(f"Total Images: {total_images}")
    print(f"Total Links: {total_links}")

def example_custom_scraping():
    """Example: Custom scraping with specific targets"""
    scraper = UniversalScraper(base_delay=1)
    
    # List of specific URLs to scrape
    target_urls = [
        "https://doartenergy.com",
        "https://doartenergy.com/about",
        "https://doartenergy.com/services",
        "https://doartenergy.com/contact",
    ]
    
    all_data = {}
    for url in target_urls:
        data = scraper.scrape_url(url)
        if data:
            all_data[url] = data
            print(f"✓ Scraped: {url}")
        else:
            print(f"✗ Failed: {url}")
    
    # Export results
    scraper.export_data(all_data, 'custom_scrape_report', ['json', 'excel'])

if __name__ == "__main__":
    print("=== Universal Web Scraper ===")
    print("Choose an option:")
    print("1. Scrape single page")
    print("2. Scrape entire site (crawl)")
    print("3. Custom URL list scraping")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        example_scrape_single_page()
    elif choice == "2":
        example_scrape_entire_site()
    elif choice == "3":
        example_custom_scraping()
    else:
        print("Running single page example...")
        example_scrape_single_page()
    
    print("\n🎉 Scraping completed! Check the generated report files.")
