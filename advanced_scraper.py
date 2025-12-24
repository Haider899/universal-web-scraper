#!/usr/bin/env python3
"""
ADVANCED Universal Web Scraper with Interactive Menu
Features:
- Custom URL input
- Multiple scraping modes
- Export options
- Settings configuration
- Batch processing
"""
import sys
import os
from universal_scraper import UniversalScraper
import json
import time
from datetime import datetime

class AdvancedScraperMenu:
    def __init__(self):
        self.scraper = None
        self.settings = {
            'base_delay': 2,
            'max_retries': 3,
            'timeout': 30,
            'max_pages': 50
        }
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display beautiful header"""
        self.clear_screen()
        print("🌐" + "="*50 + "🌐")
        print("           UNIVERSAL WEB SCRAPER PRO")
        print("🌐" + "="*50 + "🌐")
        print()
    
    def get_custom_url(self):
        """Get custom URL from user"""
        self.display_header()
        print("🎯 ENTER WEBSITE URL")
        print("-" * 40)
        
        while True:
            url = input("Enter website URL (e.g., https://example.com): ").strip()
            
            if not url:
                print("❌ URL cannot be empty. Please try again.")
                continue
            
            # Add https:// if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                print(f"⚠️  Added https:// -> {url}")
            
            # Basic URL validation
            if '.' not in url:
                print("❌ Invalid URL. Please include domain (e.g., example.com)")
                continue
            
            return url
    
    def main_menu(self):
        """Main interactive menu"""
        while True:
            self.display_header()
            print("📋 MAIN MENU - Choose an option:")
            print("1. 🎯 Scrape Single Custom URL")
            print("2. 🕷️  Crawl Entire Website") 
            print("3. 📝 Scrape Multiple Custom URLs")
            print("4. ⚙️  Settings & Configuration")
            print("5. 🧪 Test on Popular Websites")
            print("6. 📊 View Previous Results")
            print("7. ❌ Exit")
            print()
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.single_url_scraping()
            elif choice == '2':
                self.website_crawling()
            elif choice == '3':
                self.multiple_urls_scraping()
            elif choice == '4':
                self.settings_menu()
            elif choice == '5':
                self.test_popular_sites()
            elif choice == '6':
                self.view_results()
            elif choice == '7':
                print("👋 Thank you for using Universal Web Scraper!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                input("Press Enter to continue...")
    
    def single_url_scraping(self):
        """Scrape a single custom URL"""
        self.display_header()
        print("🎯 SINGLE URL SCRAPING")
        print("-" * 40)
        
        url = self.get_custom_url()
        
        print(f"\n🔧 Configuring scraper for: {url}")
        print("   Default settings: 2s delay, 3 retries")
        
        custom_delay = input("   Enter custom delay in seconds (press Enter for default 2): ").strip()
        if custom_delay and custom_delay.replace('.', '').isdigit():
            self.settings['base_delay'] = float(custom_delay)
        
        print(f"\n🚀 Starting scrape...")
        
        # Initialize scraper with current settings
        self.scraper = UniversalScraper(
            base_delay=self.settings['base_delay'],
            max_retries=self.settings['max_retries'],
            timeout=self.settings['timeout']
        )
        
        start_time = time.time()
        data = self.scraper.scrape_url(url)
        end_time = time.time()
        
        if data:
            print(f"✅ SUCCESS! Scraped in {end_time - start_time:.1f} seconds")
            self.display_scraping_results(data, url)
            self.export_menu_single(url, data)
        else:
            print(f"❌ FAILED to scrape {url}")
            print("Possible reasons:")
            print("  - Website is blocking scrapers")
            print("  - Invalid URL")
            print("  - Network issues")
            print("  - Server not responding")
        
        input("\nPress Enter to continue...")
    
    def website_crawling(self):
        """Crawl entire website"""
        self.display_header()
        print("🕷️  WEBSITE CRAWLING")
        print("-" * 40)
        
        url = self.get_custom_url()
        
        print(f"\n🔧 Crawling configuration for: {url}")
        
        max_pages = input("   Enter maximum pages to crawl (default 50): ").strip()
        if max_pages and max_pages.isdigit():
            self.settings['max_pages'] = int(max_pages)
        
        custom_delay = input("   Enter delay between requests in seconds (default 2): ").strip()
        if custom_delay and custom_delay.replace('.', '').isdigit():
            self.settings['base_delay'] = float(custom_delay)
        
        print(f"\n🚀 Starting website crawl...")
        print(f"   Target: {url}")
        print(f"   Max pages: {self.settings['max_pages']}")
        print(f"   Delay: {self.settings['base_delay']}s")
        print("\n⏳ This may take a while. Please wait...")
        
        self.scraper = UniversalScraper(
            base_delay=self.settings['base_delay'],
            max_retries=self.settings['max_retries'],
            timeout=self.settings['timeout']
        )
        
        start_time = time.time()
        all_data = self.scraper.scrape_site(
            url, 
            max_pages=self.settings['max_pages'], 
            same_domain=True
        )
        end_time = time.time()
        
        if all_data:
            print(f"\n✅ CRAWLING COMPLETED!")
            print(f"📊 Results: {len(all_data)} pages scraped in {end_time - start_time:.1f} seconds")
            
            # Calculate statistics
            total_images = sum(len(data.get('images', [])) for data in all_data.values())
            total_links = sum(len(data.get('links', [])) for data in all_data.values())
            total_words = sum(data.get('word_count', 0) for data in all_data.values())
            
            print(f"📈 Statistics:")
            print(f"   - Total pages: {len(all_data)}")
            print(f"   - Total images: {total_images}")
            print(f"   - Total links: {total_links}")
            print(f"   - Total words: {total_words}")
            
            self.export_menu_multiple(all_data, f"full_crawl_{url.split('//')[1].replace('/', '_')}")
        else:
            print("❌ Failed to crawl website. No data collected.")
        
        input("\nPress Enter to continue...")
    
    def multiple_urls_scraping(self):
        """Scrape multiple custom URLs"""
        self.display_header()
        print("📝 MULTIPLE URLS SCRAPING")
        print("-" * 40)
        
        print("Enter URLs (one per line). Press Enter twice when done:")
        print("Example: https://example.com/page1")
        print()
        
        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            
            # Validate and format URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if url not in urls:
                urls.append(url)
                print(f"✓ Added: {url}")
            else:
                print("⚠️  URL already added")
        
        if not urls:
            print("❌ No URLs provided. Returning to main menu.")
            input("Press Enter to continue...")
            return
        
        print(f"\n🎯 Ready to scrape {len(urls)} URLs")
        
        self.scraper = UniversalScraper(
            base_delay=self.settings['base_delay'],
            max_retries=self.settings['max_retries'],
            timeout=self.settings['timeout']
        )
        
        print("🚀 Starting batch scraping...")
        all_data = {}
        success_count = 0
        
        for i, url in enumerate(urls, 1):
            print(f"   [{i}/{len(urls)}] Scraping: {url}")
            data = self.scraper.scrape_url(url)
            if data:
                all_data[url] = data
                success_count += 1
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed")
        
        print(f"\n📊 Batch scraping completed: {success_count}/{len(urls)} successful")
        
        if success_count > 0:
            self.export_menu_multiple(all_data, f"batch_scrape_{datetime.now().strftime('%H%M%S')}")
        else:
            print("❌ No data to export.")
        
        input("\nPress Enter to continue...")
    
    def display_scraping_results(self, data, url):
        """Display scraping results in a nice format"""
        print(f"\n📊 SCRAPING RESULTS for: {url}")
        print("-" * 50)
        print(f"📄 Title: {data.get('title', 'No title')}")
        print(f"📝 Description: {data.get('meta_description', 'No description')[:100]}...")
        print(f"📈 Statistics:")
        print(f"   - Word count: {data.get('word_count', 0)}")
        print(f"   - Images: {len(data.get('images', []))}")
        print(f"   - Links: {len(data.get('links', []))}")
        print(f"   - Headings: {sum(len(headings) for headings in data.get('headings', {}).values())}")
        print(f"   - Paragraphs: {len(data.get('paragraphs', []))}")
        
        # Show sample content
        if data.get('headings'):
            print(f"\n📑 Sample Headings:")
            for level in ['h1', 'h2', 'h3']:
                headings = data['headings'].get(level, [])
                if headings:
                    print(f"   {level.upper()}: {headings[0][:60]}...")
        
        if data.get('emails'):
            print(f"📧 Emails found: {', '.join(data['emails'][:3])}{'...' if len(data['emails']) > 3 else ''}")
    
    def export_menu_single(self, url, data):
        """Export menu for single URL"""
        print(f"\n💾 EXPORT OPTIONS for single page")
        print("1. JSON (Full data)")
        print("2. CSV (Summary)")
        print("3. Excel (Detailed)")
        print("4. All formats")
        print("5. Don't export")
        
        choice = input("Choose export option (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            filename = f"single_page_{url.split('//')[1].replace('/', '_')}"
            
            if choice == '1':
                formats = ['json']
            elif choice == '2':
                formats = ['csv']
            elif choice == '3':
                formats = ['excel']
            else:  # choice == '4'
                formats = ['json', 'csv', 'excel']
            
            self.scraper.export_data({url: data}, filename, formats)
            print(f"✅ Exported to {filename}.*")
    
    def export_menu_multiple(self, all_data, base_filename):
        """Export menu for multiple URLs"""
        print(f"\n💾 EXPORT OPTIONS for {len(all_data)} pages")
        print("1. JSON (Full data)")
        print("2. CSV (Summary)")
        print("3. Excel (Detailed sheets)")
        print("4. All formats")
        print("5. Don't export")
        
        choice = input("Choose export option (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            if choice == '1':
                formats = ['json']
            elif choice == '2':
                formats = ['csv']
            elif choice == '3':
                formats = ['excel']
            else:  # choice == '4'
                formats = ['json', 'csv', 'excel']
            
            self.scraper.export_data(all_data, base_filename, formats)
            print(f"✅ Exported to {base_filename}.*")
    
    def settings_menu(self):
        """Configure scraper settings"""
        while True:
            self.display_header()
            print("⚙️  SCRAPER SETTINGS")
            print("-" * 40)
            print(f"1. Base Delay: {self.settings['base_delay']} seconds")
            print(f"2. Max Retries: {self.settings['max_retries']}")
            print(f"3. Timeout: {self.settings['timeout']} seconds") 
            print(f"4. Max Pages (for crawling): {self.settings['max_pages']}")
            print("5. Reset to Defaults")
            print("6. Back to Main Menu")
            print()
            
            choice = input("Choose setting to change (1-6): ").strip()
            
            if choice == '1':
                new_delay = input(f"Enter new base delay (current: {self.settings['base_delay']}): ").strip()
                if new_delay and new_delay.replace('.', '').isdigit():
                    self.settings['base_delay'] = float(new_delay)
                    print("✅ Delay updated")
            
            elif choice == '2':
                new_retries = input(f"Enter new max retries (current: {self.settings['max_retries']}): ").strip()
                if new_retries and new_retries.isdigit():
                    self.settings['max_retries'] = int(new_retries)
                    print("✅ Max retries updated")
            
            elif choice == '3':
                new_timeout = input(f"Enter new timeout (current: {self.settings['timeout']}): ").strip()
                if new_timeout and new_timeout.isdigit():
                    self.settings['timeout'] = int(new_timeout)
                    print("✅ Timeout updated")
            
            elif choice == '4':
                new_max_pages = input(f"Enter new max pages (current: {self.settings['max_pages']}): ").strip()
                if new_max_pages and new_max_pages.isdigit():
                    self.settings['max_pages'] = int(new_max_pages)
                    print("✅ Max pages updated")
            
            elif choice == '5':
                self.settings = {
                    'base_delay': 2,
                    'max_retries': 3,
                    'timeout': 30,
                    'max_pages': 50
                }
                print("✅ Settings reset to defaults")
            
            elif choice == '6':
                break
            
            else:
                print("❌ Invalid choice")
            
            input("Press Enter to continue...")
    
    def test_popular_sites(self):
        """Test scraper on popular websites"""
        self.display_header()
        print("🧪 TEST ON POPULAR WEBSITES")
        print("-" * 40)
        
        test_sites = [
            ("https://httpbin.org/html", "HTTPBin HTML Test"),
            ("https://httpbin.org/json", "HTTPBin JSON Test"),
            ("https://books.toscrape.com", "Books to Scrape (Demo E-commerce)"),
            ("https://quotes.toscrape.com", "Quotes to Scrape (Demo Site)"),
            ("https://example.com", "Example.com"),
        ]
        
        print("Available test sites:")
        for i, (url, desc) in enumerate(test_sites, 1):
            print(f"  {i}. {desc} - {url}")
        
        print(f"  6. Test ALL sites")
        print()
        
        choice = input("Choose site to test (1-6): ").strip()
        
        if choice == '6':
            # Test all sites
            for url, desc in test_sites:
                self._test_single_site(url, desc)
                time.sleep(2)
        elif choice.isdigit() and 1 <= int(choice) <= len(test_sites):
            url, desc = test_sites[int(choice) - 1]
            self._test_single_site(url, desc)
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")
    
    def _test_single_site(self, url, description):
        """Test a single site"""
        print(f"\n🔍 Testing: {description}")
        print(f"   URL: {url}")
        
        self.scraper = UniversalScraper(base_delay=1, max_retries=2)
        data = self.scraper.scrape_url(url)
        
        if data:
            print(f"   ✅ SUCCESS")
            print(f"   📄 Title: {data.get('title', 'No title')[:50]}...")
            print(f"   📊 Found: {len(data.get('images', []))} images, {len(data.get('links', []))} links")
        else:
            print(f"   ❌ FAILED")
    
    def view_results(self):
        """View previous scraping results"""
        self.display_header()
        print("📊 PREVIOUS RESULTS")
        print("-" * 40)
        
        # Look for result files
        result_files = []
        for file in os.listdir('.'):
            if any(file.endswith(ext) for ext in ['.json', '.csv', '.xlsx']):
                if any(prefix in file for prefix in ['single_page', 'full_crawl', 'batch_scrape']):
                    result_files.append(file)
        
        if not result_files:
            print("No previous results found.")
            print("Scrape some websites first to see results here.")
        else:
            print("Found result files:")
            for i, file in enumerate(sorted(result_files), 1):
                size = os.path.getsize(file)
                print(f"  {i}. {file} ({size:,} bytes)")
            
            print(f"\nOpen these files with:")
            print("  - JSON: Any text editor or browser")
            print("  - CSV: Excel, Google Sheets, or text editor") 
            print("  - Excel: Microsoft Excel or LibreOffice")
        
        input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    try:
        menu = AdvancedScraperMenu()
        menu.main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please make sure all required packages are installed.")
        print("Run: pip install requests beautifulsoup4 pandas openpyxl lxml")

if __name__ == "__main__":
    main()
