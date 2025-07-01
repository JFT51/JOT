# 🤖 JobOnTop.be AI-Powered Web Scraper

An advanced web scraping system with AI-powered data extraction for JobOnTop.be job listings. This tool automatically extracts job postings and uses artificial intelligence to parse structured business contact information from unstructured text.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![BeautifulSoup](https://img.shields.io/badge/beautifulsoup-v4.12+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Features

### 🕷️ **Advanced Web Scraping**
- Automatically discovers job listings from JobOnTop.be
- Extracts detailed job information from individual pages
- Respectful scraping with rate limiting
- Robust error handling and retry mechanisms

### 🤖 **AI-Powered Data Extraction**
- **Company Names**: 97% success rate extracting clean company names
- **Locations**: 95% success rate identifying Belgian cities
- **Email Addresses**: 92% success rate finding contact emails
- **Phone Numbers**: 51% success rate extracting Belgian phone numbers
- **Addresses**: 90% success rate parsing business addresses
- **Contact Persons**: 26% success rate identifying contact names

### 🌐 **Multiple User Interfaces**
- **Streamlit Dashboard**: Interactive web interface with analytics
- **HTML Viewer**: Standalone browser-based viewer (no server required)
- **CSV Export**: Structured data export for further analysis
- **Command Line**: Full automation support

### 📊 **Analytics & Visualization**
- Interactive charts showing location distribution
- Contact information availability metrics
- Real-time filtering and search capabilities
- Export functionality with timestamped files

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection for scraping

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JFT51/JOT.git
   cd JOT
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the complete workflow**
   ```bash
   python deploy.py
   ```
   Choose option 1 for full scraping + AI extraction + viewer

### Quick Usage Options

#### Option 1: Full Automated Workflow
```bash
python deploy.py
# Select option 1: Full scraping + AI extraction + launch viewer
```

#### Option 2: Streamlit Dashboard
```bash
python launch_ui.py
# Opens interactive web dashboard at http://localhost:8502
```

#### Option 3: Standalone HTML Viewer
```bash
# Simply open job_results.html in your browser
start job_results.html  # Windows
open job_results.html   # Mac
```

## 📁 Project Structure

```
JOT/
├── 🕷️ Core Scraper
│   ├── job_scraper.py          # Main web scraper
│   ├── data_extractor.py       # AI data extraction engine
│   └── deploy.py               # Full workflow automation
│
├── 🌐 User Interfaces
│   ├── streamlit_app.py        # Advanced web dashboard
│   ├── job_results.html        # Standalone HTML viewer
│   └── launch_ui.py            # Quick Streamlit launcher
│
├── 📊 Sample Data
│   ├── job_scraping_results.csv     # Sample raw scraped data
│   ├── job_data_structured.csv      # Sample AI-extracted data
│   └── job_results.html             # Sample HTML viewer
│
└── 📚 Documentation
    ├── README.md               # This file
    ├── PROJECT_SUMMARY.md      # Technical project overview
    ├── USAGE_GUIDE.md         # Detailed usage instructions
    └── requirements.txt        # Python dependencies
```

## 🛠️ Usage Examples

### 1. Run Complete Scraping Workflow
```bash
python deploy.py
# Choose option 1
# ✅ Scrapes 39 job listings
# ✅ AI extracts structured data
# ✅ Launches HTML viewer
```

### 2. Launch Interactive Dashboard
```bash
python launch_ui.py
# Opens Streamlit dashboard with:
# • Analytics charts
# • Advanced filtering
# • Export capabilities
# • Job details viewer
```

### 3. Process Existing Data
```bash
python deploy.py
# Choose option 2
# ✅ Runs AI extraction on existing data
# ✅ Updates HTML viewer
```

### 4. Command Line Data Extraction
```bash
python data_extractor.py
# Processes existing CSV data
# Outputs extraction summary
```

## 📊 Sample Results

### Extraction Performance
- **39 jobs processed** (100% discovery rate)
- **38 company names** extracted (97% success)
- **37 locations** found (95% success)
- **36 email addresses** extracted (92% success)
- **35 addresses** parsed (90% success)

### Sample Extracted Data
| Company | Location | Email | Phone | Address |
|---------|----------|-------|-------|---------|
| Ciconia | Schoten | info@brasserie-ciconia.be | - | Horstebaan 12, 2900 Schoten |
| La Tannerie | Durbuy | tom@latanneriededurbuy.be | 0476415652 | Rue Du Canal 12, Bomal-Sur-Ourthe |
| Verso Café | Antwerpen | - | - | Lange Gasthuisstraat 9, 2000 Antwerpen |

## 🔧 Configuration

### Customizing Scraping Behavior
Edit `job_scraper.py` to modify:
- Rate limiting delays
- User agent strings
- Target URLs
- HTML parsing patterns

### AI Extraction Patterns
Edit `data_extractor.py` to customize:
- Company name extraction patterns
- Location recognition
- Contact information parsing
- Data validation rules

## 📈 Advanced Features

### Streamlit Dashboard
- **Analytics Tab**: Interactive charts and metrics
- **Structured Data Tab**: AI-extracted information with filters
- **Raw Data Tab**: Original scraped content
- **Job Details Tab**: Individual job viewer
- **Export Tab**: CSV download with filtering

### HTML Viewer
- **No server required**: Opens directly in browser
- **Interactive filtering**: Real-time search and filters
- **Mobile responsive**: Works on all devices
- **Export functionality**: Download filtered data

## 🔍 Technical Details

### AI Extraction Engine
- **Regex Pattern Matching**: Advanced patterns for emails, phones, addresses
- **Natural Language Processing**: Company name and location extraction
- **Belgian Location Database**: Comprehensive city recognition
- **Contact Person Identification**: Context-aware name extraction
- **Multilingual Support**: Dutch, French, and English text processing

### Web Scraping Architecture
- **BeautifulSoup**: HTML parsing and content extraction
- **Requests**: HTTP client with session management
- **Rate Limiting**: Respectful scraping with delays
- **Error Handling**: Robust retry mechanisms
- **User Agent Rotation**: Avoid detection

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚠️ Legal Disclaimer

This tool is designed for educational and research purposes. Users are responsible for:
- Complying with website terms of service
- Respecting robots.txt files (when not explicitly overridden)
- Following applicable data protection laws (GDPR, etc.)
- Using scraped data ethically and legally

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check `USAGE_GUIDE.md` for detailed instructions
- **Issues**: Report bugs on GitHub Issues
- **Technical Details**: See `PROJECT_SUMMARY.md`

## 🎉 Acknowledgments

- JobOnTop.be for providing the job listing data
- BeautifulSoup and Requests libraries for web scraping capabilities
- Streamlit for the interactive dashboard framework
- The open-source community for inspiration and tools

---

**Made with ❤️ for the Belgian job market**

*Last updated: January 2025*
