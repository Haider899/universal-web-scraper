# 🌐 Universal Web Scraper Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A powerful universal web scraper that works on ANY website. Features interactive menus, multiple export formats, and intelligent content extraction.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Haider899/universal-web-scraper.git
cd universal-web-scraper

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python advanced_scraper.py
```

✨ Features
✅ Universal Compatibility - Works on any website

✅ Interactive Menu System - No coding required

✅ Multiple Scraping Modes - Single page, site crawling, batch URLs

✅ Smart Data Extraction - Text, images, links, emails, and more

✅ Multiple Export Formats - JSON, CSV, Excel

✅ Respectful Scraping - Rate limiting, robots.txt compliance

✅ Advanced Error Handling - Automatic retries and recovery
=========
🔧 Installation
Prerequisites
Python 3.8 or higher

pip (Python package manager)

=========

Step-by-Step Installation
```bash
# 1. Clone the repository
git clone https://github.com/Haider899/universal-web-scraper.git
cd universal-web-scraper

# 2. Install required packages
pip install -r requirements.txt

# 3. Verify installation
python advanced_scraper.py --help
```
Requirements
The following packages will be automatically installed:

requests>=2.31.0 - HTTP requests

beautifulsoup4>=4.12.2 - HTML parsing

pandas>=1.3.0 - Data manipulation and export

openpyxl>=3.0.0 - Excel file support

lxml>=4.6.0 - Fast HTML parsing
================================
# 🎯 Usage
Interactive Mode (Recommended for Beginners)
The easiest way to use the scraper is through the interactive menu:

```bash
python advanced_scraper.py
```
You'll see this menu:

text
🌐==================================================🌐
           UNIVERSAL WEB SCRAPER PRO
🌐==================================================🌐

📋 MAIN MENU - Choose an option:
1. 🎯 Scrape Single Custom URL
2. 🕷️  Crawl Entire Website
3. 📝 Scrape Multiple Custom URLs
4. ⚙️  Settings & Configuration
5. 🧪 Test on Popular Websites
6. 📊 View Previous Results
7. ❌ Exit

Enter your choice (1-7):
=========
Single URL Scraping
Perfect for quick data extraction from one page:

Choose option 1 from the main menu

Enter the target URL (e.g., https://example.com)

View real-time scraping progress

Choose export format (JSON, CSV, or Excel)

Results are saved automatically
======
Python API
python
from universal_scraper import UniversalScraper

# Initialize scraper
scraper = UniversalScraper(base_delay=2)

# Scrape single URL
data = scraper.scrape_url("https://example.com")

# Export results
scraper.export_data({'result': data}, 'my_report', ['json', 'csv'])


# 🪟 Windows Installation
🚀 Easy Method (Recommended for Beginners)
Download this repository as ZIP (Code → Download ZIP)

Extract to your Desktop

Double-click install_and_run.bat

Follow the prompts - it will automatically install everything!

### 🔧 Manual Method
```cmd
# 1. Open Command Prompt in the project folder
cd Desktop\universal-web-scraper

# 2. Install dependencies
pip install requests beautifulsoup4 pandas openpyxl lxml

# 3. Run the scraper
python advanced_scraper.py
```
# 🐧 Linux/macOS Installation
```bash
# Install Python and pip (if not already installed)
sudo apt update  # Ubuntu/Debian
sudo apt install python3 python3-pip

# Or on macOS
brew install python

# Install dependencies
pip3 install -r requirements.txt

# Run the scraper
python3 advanced_scraper.py
```
======
💡 Examples
Example 1: Quick Data Extraction
```bash
from universal_scraper import UniversalScraper

urls = ["https://site1.com", "https://site2.com"]
scraper = UniversalScraper()
results = {}

for url in urls:
    results[url] = scraper.scrape_url(url)

scraper.export_data(results, 'batch_results', ['excel'])
```
❓ Troubleshooting
Python Not Found
Windows: Reinstall Python and check "Add Python to PATH"
Linux: sudo apt install python3
macOS: brew install python or download from python.org
======
Module Not Found Errors
```bash
pip install requests beautifulsoup4 pandas openpyxl lxml
```
# 🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

# 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

# 🙏 Acknowledgments
Built with BeautifulSoup4 for HTML parsing

Uses Requests for HTTP operations

Pandas for data export and manipulation

# ⭐ Star this repo if you find it useful!


