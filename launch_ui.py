#!/usr/bin/env python3
"""
Quick launcher for the JobOnTop.be Scraper Streamlit UI
"""

import subprocess
import sys
import os
import webbrowser
import time

def launch_streamlit():
    """Launch the Streamlit app"""
    print("🚀 Launching JobOnTop.be AI Scraper UI...")
    print("📱 Opening Streamlit interface...")
    
    try:
        # Start Streamlit in a subprocess
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8502",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8502")
        
        print("✅ Streamlit app launched!")
        print("🌐 Access your scraper at: http://localhost:8502")
        print("📊 Features available:")
        print("   • Analytics Dashboard with charts")
        print("   • Structured Data View with filters")
        print("   • Raw Data Explorer")
        print("   • Detailed Job Viewer")
        print("   • CSV Export functionality")
        print("\n💡 Press Ctrl+C to stop the server")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping Streamlit server...")
        process.terminate()
        print("✅ Server stopped successfully!")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")
        print("💡 Try running manually: streamlit run streamlit_app.py")

def main():
    """Main function"""
    print("🤖 JobOnTop.be AI Scraper - Streamlit Launcher")
    print("=" * 50)
    
    # Check if data files exist
    import glob
    raw_files = glob.glob("job_scraping_results_*.csv")
    structured_files = glob.glob("job_data_structured_*.csv")
    
    if not raw_files and not structured_files:
        print("❌ No scraped data found!")
        print("💡 Run 'python deploy.py' first to scrape data")
        return
    
    if raw_files:
        latest_raw = max(raw_files, key=os.path.getctime)
        print(f"✅ Found raw data: {latest_raw}")
    
    if structured_files:
        latest_structured = max(structured_files, key=os.path.getctime)
        print(f"✅ Found structured data: {latest_structured}")
    
    print("\n🚀 Starting Streamlit UI...")
    launch_streamlit()

if __name__ == "__main__":
    main()
