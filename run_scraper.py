#!/usr/bin/env python3
"""
Simple runner for the Universal Scraper
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from universal_scraper import UniversalScraper

def main():
    print("🌐 Universal Web Scraper")
    print("=" * 40)
    
    # Get target website from user
    website = input("Enter website URL (e.g., https://doartenergy.com): ").strip()
    if not website:
        website = "https://doartenergy.com"
    
    print(f"\nTarget: {website}")
    print("\nScraping Options:")
    print("1. Single Page (Quick)")
    print("2. Multiple Pages (Crawl site)")
    print("3. Custom URL List")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    scraper = UniversalScraper(base_delay=2, max_retries=3)
    
    if choice == "1":
        print(f"\n📄 Scraping single page: {website}")
        data = scraper.scrape_url(website)
        
        if data:
            scraper.export_data({website: data}, 'single_page_report', ['json', 'csv', 'excel'])
            print(f"✅ Success! Check 'single_page_report_*.json/csv/xlsx' files")
        else:
            print("❌ Failed to scrape the page")
    
    elif choice == "2":
        max_pages = input("Max pages to scrape (default 20): ").strip()
        max_pages = int(max_pages) if max_pages.isdigit() else 20
        
        print(f"\n🕷️ Crawling {website} (max {max_pages} pages)...")
        all_data = scraper.scrape_site(website, max_pages=max_pages, same_domain=True)
        
        print(f"✅ Scraped {len(all_data)} pages successfully!")
        scraper.export_data(all_data, 'full_site_report', ['json', 'csv', 'excel'])
        print("📊 Reports saved as 'full_site_report_*.json/csv/xlsx'")
    
    elif choice == "3":
        print("\nEnter URLs (one per line). Press Enter twice when done:")
        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            if url.startswith(('http://', 'https://')):
                urls.append(url)
            else:
                print("⚠️  Please enter full URL with http:// or https://")
        
        if not urls:
            urls = [website]
        
        print(f"\n📄 Scraping {len(urls)} custom URLs...")
        all_data = {}
        for url in urls:
            data = scraper.scrape_url(url)
            if data:
                all_data[url] = data
                print(f"✅ {url}")
            else:
                print(f"❌ {url}")
        
        scraper.export_data(all_data, 'custom_urls_report', ['json', 'csv', 'excel'])
        print(f"📊 Reports saved for {len(all_data)} pages")
    
    else:
        print("❌ Invalid choice. Running single page scrape...")
        data = scraper.scrape_url(website)
        if data:
            scraper.export_data({website: data}, 'quick_report', ['json', 'csv'])
            print("✅ Quick report generated!")

if __name__ == "__main__":
    main()
