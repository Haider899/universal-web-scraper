🌐 Universal Web Scraper Pro




Universal Web Scraper Pro is a powerful, flexible web scraping tool designed to work on any website.
It offers an interactive menu, multiple scraping modes, and exports data in professional formats — no coding required.

⚠️ Use responsibly. Respect website terms of service and robots.txt.

✨ Key Features

🌍 Universal Compatibility — Works on almost any website

🎛️ Interactive Menu System — Beginner-friendly, no coding needed

🕷️ Multiple Scraping Modes — Single page, full site crawl, batch URLs

🧠 Smart Data Extraction — Text, images, links, emails & more

📤 Multiple Export Formats — JSON, CSV, Excel

🛡️ Respectful Scraping — Rate limiting & robots.txt compliance

🔄 Advanced Error Handling — Automatic retries & recovery

🚀 Quick Start
# Clone the repository
git clone https://github.com/Haider899/universal-web-scraper.git
cd universal-web-scraper

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python advanced_scraper.py

📦 Requirements

Python 3.8+

pip (Python package manager)

Required libraries (installed automatically):

requests — HTTP requests

beautifulsoup4 — HTML parsing

pandas — Data processing & export

openpyxl — Excel support

lxml — Fast HTML parsing

🎯 Usage
🔹 Interactive Mode (Recommended)
python advanced_scraper.py


You’ll see an interactive menu:

🌐==================================================🌐
           UNIVERSAL WEB SCRAPER PRO
🌐==================================================🌐

📋 MAIN MENU:
1. 🎯 Scrape Single URL
2. 🕷️  Crawl Entire Website
3. 📝 Scrape Multiple URLs
4. ⚙️  Settings & Configuration
5. 🧪 Test Popular Websites
6. 📊 View Previous Results
7. ❌ Exit

🔹 Single URL Scraping

Choose Option 1

Enter target URL (e.g. https://example.com)

Monitor real-time progress

Select export format (JSON / CSV / Excel)

Results saved automatically

🧩 Python API Usage
from universal_scraper import UniversalScraper

scraper = UniversalScraper(base_delay=2)

data = scraper.scrape_url("https://example.com")

scraper.export_data(
    {'result': data},
    filename='my_report',
    formats=['json', 'csv']
)

🪟 Windows Installation
🚀 Easy Method (Recommended)

Download ZIP (Code → Download ZIP)

Extract to Desktop

Double-click install_and_run.bat

Follow on-screen instructions

🔧 Manual Method
cd Desktop\universal-web-scraper
pip install -r requirements.txt
python advanced_scraper.py

🐧 Linux / macOS Installation
# Ubuntu / Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS
brew install python

pip3 install -r requirements.txt
python3 advanced_scraper.py

💡 Examples
Batch Scraping Example
from universal_scraper import UniversalScraper

urls = ["https://site1.com", "https://site2.com"]
scraper = UniversalScraper()

results = {url: scraper.scrape_url(url) for url in urls}

scraper.export_data(results, 'batch_results', ['excel'])

❓ Troubleshooting
Python Not Found

Windows: Reinstall Python and check Add Python to PATH

Linux: sudo apt install python3

macOS: brew install python

Module Not Found
pip install requests beautifulsoup4 pandas openpyxl lxml

🤝 Contributing

Contributions are welcome!

git checkout -b feature/AmazingFeature
git commit -m "Add AmazingFeature"
git push origin feature/AmazingFeature


Open a Pull Request 🚀

📄 License

This project is licensed under the MIT License.
See the LICENSE
 file for details.

🙏 Acknowledgments

BeautifulSoup4 — HTML parsing

Requests — HTTP operations

Pandas — Data processing & export

⭐ Support the Project

If you find this tool useful, please star the repository ⭐
It helps the project grow and motivates further development.
