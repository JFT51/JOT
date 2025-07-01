#!/usr/bin/env python3
"""
Deployment script for JobOnTop.be scraper
Handles the complete workflow: scraping -> AI extraction -> UI launch
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['requests', 'beautifulsoup4', 'pandas', 'streamlit', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        for package in missing_packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])
    else:
        print("✅ All dependencies are installed")

def run_scraper():
    """Run the job scraper"""
    print("🕷️  Starting job scraper...")
    try:
        from job_scraper import JobScraper
        scraper = JobScraper()
        job_data = scraper.scrape_all_jobs()
        
        if job_data:
            # Save to a timestamped file to avoid permission issues
            import pandas as pd
            df = pd.DataFrame(job_data)
            timestamp = int(time.time())
            filename = f'job_scraping_results_{timestamp}.csv'
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"✅ Scraped {len(job_data)} jobs and saved to {filename}")
            return filename
        else:
            print("❌ No job data was scraped")
            return None
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return None

def run_ai_extraction(input_file):
    """Run AI extraction on scraped data"""
    print("🤖 Starting AI data extraction...")
    try:
        import pandas as pd
        from data_extractor import JobDataExtractor
        
        # Load data
        df = pd.read_csv(input_file)
        
        # Extract structured data
        extractor = JobDataExtractor()
        structured_df = extractor.extract_structured_data(df)
        
        # Save structured data
        timestamp = int(time.time())
        output_file = f'job_data_structured_{timestamp}.csv'
        structured_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"✅ AI extraction completed and saved to {output_file}")
        
        # Display summary
        print("\n=== EXTRACTION SUMMARY ===")
        print(f"Company names extracted: {structured_df['company_name'].notna().sum()}")
        print(f"Locations extracted: {structured_df['location'].notna().sum()}")
        print(f"Contact persons extracted: {structured_df['contact_person'].notna().sum()}")
        print(f"Email addresses extracted: {(structured_df['email_addresses'] != '').sum()}")
        print(f"Phone numbers extracted: {(structured_df['phone_numbers'] != '').sum()}")
        print(f"Addresses extracted: {structured_df['address'].notna().sum()}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error during AI extraction: {e}")
        return None

def create_simple_viewer(structured_file):
    """Create a simple HTML viewer with the actual data"""
    print("📄 Creating HTML viewer...")
    try:
        import pandas as pd
        
        # Load structured data
        df = pd.read_csv(structured_file)
        
        # Convert to JavaScript data
        jobs_data = []
        for _, row in df.iterrows():
            job = {
                'company_name': str(row.get('company_name', '')),
                'location': str(row.get('location', '')),
                'contact_person': str(row.get('contact_person', '')),
                'email_addresses': str(row.get('email_addresses', '')),
                'phone_numbers': str(row.get('phone_numbers', '')),
                'address': str(row.get('address', '')),
                'url': str(row.get('url', ''))
            }
            jobs_data.append(job)
        
        # Generate JavaScript array
        js_data = "const jobsData = [\n"
        for job in jobs_data:
            js_data += "    {\n"
            for key, value in job.items():
                # Escape quotes in values
                escaped_value = value.replace('"', '\\"').replace('\n', '\\n')
                js_data += f'        {key}: "{escaped_value}",\n'
            js_data += "    },\n"
        js_data += "];\n"
        
        # Read the HTML template and replace the data
        html_file = 'job_results.html'
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Replace the sample data with actual data
            start_marker = "const jobsData = ["
            end_marker = "];"
            
            start_idx = html_content.find(start_marker)
            if start_idx != -1:
                end_idx = html_content.find(end_marker, start_idx) + len(end_marker)
                new_html = html_content[:start_idx] + js_data + html_content[end_idx:]
                
                # Save updated HTML
                timestamp = int(time.time())
                new_html_file = f'job_results_live_{timestamp}.html'
                with open(new_html_file, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                
                print(f"✅ Live HTML viewer created: {new_html_file}")
                return new_html_file
        
        print("❌ Could not update HTML viewer")
        return None
        
    except Exception as e:
        print(f"❌ Error creating HTML viewer: {e}")
        return None

def launch_viewer(html_file):
    """Launch the HTML viewer"""
    print(f"🚀 Launching viewer: {html_file}")
    try:
        if os.name == 'nt':  # Windows
            os.startfile(html_file)
        else:  # Mac/Linux
            subprocess.run(['open', html_file])
        print("✅ Viewer launched in browser")
    except Exception as e:
        print(f"❌ Could not launch viewer: {e}")
        print(f"Please manually open: {html_file}")

def main():
    """Main deployment workflow"""
    print("🤖 JobOnTop.be Scraper Deployment")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Ask user what to do
    print("\nChoose an option:")
    print("1. Run full scraping + AI extraction + launch viewer")
    print("2. Run AI extraction on existing data + launch viewer")
    print("3. Just launch HTML viewer")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Full workflow
        print("\n🚀 Starting full workflow...")
        
        # Step 1: Scrape
        scraped_file = run_scraper()
        if not scraped_file:
            print("❌ Scraping failed, aborting")
            return
        
        # Step 2: AI Extract
        structured_file = run_ai_extraction(scraped_file)
        if not structured_file:
            print("❌ AI extraction failed, aborting")
            return
        
        # Step 3: Create viewer
        html_file = create_simple_viewer(structured_file)
        if html_file:
            launch_viewer(html_file)
        
    elif choice == "2":
        # AI extraction on existing data
        print("\n🤖 Running AI extraction on existing data...")
        
        # Look for existing scraped data
        scraped_files = [f for f in os.listdir('.') if f.startswith('job_scraping_results') and f.endswith('.csv')]
        if not scraped_files:
            print("❌ No scraped data found. Run option 1 first.")
            return
        
        # Use the most recent file
        scraped_file = max(scraped_files, key=os.path.getctime)
        print(f"Using: {scraped_file}")
        
        structured_file = run_ai_extraction(scraped_file)
        if structured_file:
            html_file = create_simple_viewer(structured_file)
            if html_file:
                launch_viewer(html_file)
    
    elif choice == "3":
        # Just launch existing viewer
        print("\n📄 Launching existing HTML viewer...")
        
        # Look for HTML files
        html_files = [f for f in os.listdir('.') if f.startswith('job_results') and f.endswith('.html')]
        if html_files:
            # Use the most recent
            html_file = max(html_files, key=os.path.getctime)
            launch_viewer(html_file)
        else:
            print("❌ No HTML viewer found. Run option 1 or 2 first.")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
