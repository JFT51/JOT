# 🚀 JobOnTop.be AI Scraper - Usage Guide

## 🎯 Quick Start

### Option 1: View Results Immediately
```bash
# Open the HTML viewer (no server needed)
start job_results.html
# or double-click job_results.html
```

### Option 2: Full Streamlit Dashboard
```bash
# Launch the advanced web interface
python launch_ui.py
# or
streamlit run streamlit_app.py
```

### Option 3: Run New Scraping
```bash
# Complete scraping workflow
python deploy.py
```

## 📊 What's Available

### 🌐 **Streamlit Web App** (`http://localhost:8502`)
- **📊 Analytics Dashboard**: Charts and metrics
- **🏢 Structured Data**: AI-extracted information with filters
- **📋 Raw Data**: Original scraped content
- **🔍 Job Details**: Individual job viewer
- **📥 Export**: Download CSV files

### 📄 **HTML Viewer** (`job_results.html`)
- **No server required**: Opens directly in browser
- **Interactive filtering**: Search by company, location, email
- **Export functionality**: Download filtered data as CSV
- **Mobile responsive**: Works on all devices

## 🗂️ File Structure

```
scrapeJOT/
├── 🕷️ Core Scraper
│   ├── job_scraper.py          # Main web scraper
│   ├── data_extractor.py       # AI data extraction
│   └── deploy.py               # Full workflow automation
│
├── 🌐 User Interfaces
│   ├── streamlit_app.py        # Advanced web dashboard
│   ├── job_results.html        # Standalone HTML viewer
│   └── launch_ui.py            # Quick Streamlit launcher
│
├── 📊 Data Files
│   ├── job_scraping_results_*.csv     # Raw scraped data
│   ├── job_data_structured_*.csv      # AI-extracted data
│   └── job_results_live_*.html        # Updated HTML viewers
│
└── 📚 Documentation
    ├── PROJECT_SUMMARY.md       # Complete project overview
    ├── USAGE_GUIDE.md          # This file
    └── requirements.txt         # Python dependencies
```

## 🔧 Commands Reference

### 🕷️ Scraping
```bash
# Full workflow: scrape + AI extraction + viewer
python deploy.py
# Choose option 1

# Just AI extraction on existing data
python deploy.py
# Choose option 2
```

### 🌐 User Interfaces
```bash
# Launch Streamlit dashboard
python launch_ui.py

# Launch HTML viewer
start job_results.html

# Manual Streamlit launch
streamlit run streamlit_app.py --server.port 8502
```

### 📊 Data Access
```bash
# View latest files
dir job_*.csv
dir job_*.html

# Open CSV in Excel
start job_data_structured_*.csv
```

## 🎯 Features Overview

### 📊 **Analytics Dashboard**
- **Success Metrics**: Company extraction rates, email findings
- **Location Charts**: Top job locations in Belgium
- **Contact Info**: Availability of emails, phones, addresses
- **Interactive Visualizations**: Plotly charts with zoom/filter

### 🔍 **Advanced Filtering**
- **Company Name**: Search for specific businesses
- **Location**: Filter by Belgian cities
- **Contact Availability**: Show only jobs with emails/phones
- **Real-time Results**: Instant filtering as you type

### 📥 **Export Options**
- **CSV Downloads**: Raw data, structured data, summary reports
- **Timestamped Files**: Automatic file naming with dates
- **Filtered Exports**: Download only the data you've filtered
- **Multiple Formats**: Compatible with Excel, Google Sheets

### 🤖 **AI Extraction Results**
Based on latest scraping session:
- ✅ **39 jobs processed** (100% success)
- ✅ **38 company names** extracted (97% success)
- ✅ **37 locations** found (95% success)
- ✅ **36 email addresses** extracted (92% success)
- ✅ **35 addresses** parsed (90% success)
- ✅ **20 phone numbers** found (51% success)

## 🐛 Troubleshooting

### Common Issues

**❌ "No scraped data found"**
```bash
# Solution: Run the scraper first
python deploy.py
# Choose option 1
```

**❌ Streamlit won't start**
```bash
# Solution: Try different port
streamlit run streamlit_app.py --server.port 8503
```

**❌ Permission denied on CSV files**
```bash
# Solution: Close Excel/CSV viewers and try again
# Or use timestamped files that avoid conflicts
```

**❌ HTML viewer shows old data**
```bash
# Solution: Generate fresh HTML viewer
python deploy.py
# Choose option 1 or 2
```

### Performance Tips

- **Large datasets**: Use the "Show full text" option sparingly
- **Better filtering**: Use specific search terms for faster results
- **Memory usage**: Refresh the Streamlit app if it becomes slow
- **Export speed**: Filter data before exporting for faster downloads

## 🔄 Workflow Examples

### Daily Job Monitoring
```bash
# 1. Run morning scrape
python deploy.py  # Option 1

# 2. Launch dashboard
python launch_ui.py

# 3. Filter for new opportunities
# Use Streamlit filters for location/company type

# 4. Export contact list
# Download structured CSV from Export tab
```

### Data Analysis
```bash
# 1. Use existing data
python deploy.py  # Option 2

# 2. Analyze in Streamlit
# View Analytics dashboard
# Check location distribution
# Review contact availability

# 3. Export summary
# Download summary report from Export tab
```

---

## 🎉 Success! Your Scraper is Ready

The JobOnTop.be AI scraper is now fully operational with multiple interfaces and export options. Choose the method that works best for your workflow!

**Need help?** Check the `PROJECT_SUMMARY.md` for technical details.
