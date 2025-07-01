import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin, urlparse
import time

class JobScraper:
    def __init__(self):
        self.session = requests.Session()
        # Ignore robots.txt as requested
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = 'https://www.jobontop.be'
        self.main_page = 'https://www.jobontop.be/jobs-dub.html'
        
    def get_job_links(self):
        """Extract all job links from the main page after h3 elements with class 'itemTitle actItemTitle'"""
        print("Fetching main page...")
        try:
            response = self.session.get(self.main_page)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_links = []
            h3_elements = soup.find_all('h3', class_='itemTitle actItemTitle')
            
            print(f"Found {len(h3_elements)} job title elements")
            
            for h3 in h3_elements:
                # Look for the next link after the h3 element
                link_element = h3.find('a')
                if not link_element:
                    # If no link in h3, look for the next sibling or parent containing a link
                    parent = h3.parent
                    if parent:
                        link_element = parent.find('a')
                
                if link_element and link_element.get('href'):
                    href = link_element.get('href')
                    full_url = urljoin(self.base_url, href)
                    job_links.append(full_url)
                    print(f"Found job link: {full_url}")
            
            print(f"Total job links found: {len(job_links)}")
            return job_links
            
        except requests.RequestException as e:
            print(f"Error fetching main page: {e}")
            return []
    
    def extract_text_between_tags(self, soup, start_tag_text, end_tag_text, end_tag_class=None):
        """Extract text between two specific HTML tags"""
        try:
            # Find the start tag
            start_tag = soup.find('h2', class_='subHeader jbdSh jbdTextSh', string=start_tag_text)
            if not start_tag:
                return ""
            
            # Collect all text between start and end tags
            content = []
            current = start_tag.next_sibling
            
            while current:
                if hasattr(current, 'name'):
                    # If it's a tag
                    if current.name == 'h2':
                        # Check for specific end conditions
                        if end_tag_class and end_tag_class in current.get('class', []):
                            break
                        elif current.get_text(strip=True) == end_tag_text:
                            break
                    # Add the text content of the tag
                    content.append(current.get_text(strip=True))
                else:
                    # If it's a text node
                    text = str(current).strip()
                    if text:
                        content.append(text)
                
                current = current.next_sibling
            
            return ' '.join(content).strip()
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def scrape_job_details(self, job_url):
        """Scrape the Bedrijf and Solliciteren sections from a job page"""
        try:
            print(f"Scraping job: {job_url}")
            response = self.session.get(job_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract Bedrijf section
            bedrijf_text = self.extract_text_between_tags(soup, 'Bedrijf', 'Taken')
            
            # Extract Solliciteren section (ends at next h2 with class 'subHeader jbdSh jbdShReg')
            solliciteren_text = self.extract_text_between_tags(soup, 'Solliciteren', '', end_tag_class='jbdShReg')
            
            return {
                'url': job_url,
                'bedrijf': bedrijf_text,
                'solliciteren': solliciteren_text
            }
            
        except requests.RequestException as e:
            print(f"Error scraping job {job_url}: {e}")
            return {
                'url': job_url,
                'bedrijf': f"Error: {e}",
                'solliciteren': f"Error: {e}"
            }
    
    def scrape_all_jobs(self):
        """Main method to scrape all jobs and return data"""
        job_links = self.get_job_links()
        
        if not job_links:
            print("No job links found!")
            return []
        
        job_data = []
        
        for i, job_url in enumerate(job_links, 1):
            print(f"Processing job {i}/{len(job_links)}")
            job_details = self.scrape_job_details(job_url)
            job_data.append(job_details)
            
            # Add a small delay to be respectful to the server
            time.sleep(1)
        
        return job_data
    
    def display_results_table(self, job_data):
        """Display the scraped data in a table format"""
        if not job_data:
            print("No data to display!")
            return
        
        # Create DataFrame
        df = pd.DataFrame(job_data)
        
        # Set display options for better table viewing
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', 100)
        pd.set_option('display.width', None)
        
        print("\n" + "="*150)
        print("JOB SCRAPING RESULTS")
        print("="*150)
        print(f"Total jobs scraped: {len(job_data)}")
        print("="*150)
        
        for i, row in df.iterrows():
            print(f"\nJOB {i+1}:")
            print("-" * 80)
            print(f"URL: {row['url']}")
            print(f"\nBEDRIJF:")
            print(row['bedrijf'][:500] + "..." if len(row['bedrijf']) > 500 else row['bedrijf'])
            print(f"\nSOLLICITEREN:")
            print(row['solliciteren'][:500] + "..." if len(row['solliciteren']) > 500 else row['solliciteren'])
            print("-" * 80)
        
        # Save to CSV for further analysis
        df.to_csv('job_scraping_results.csv', index=False, encoding='utf-8')
        print(f"\nResults saved to 'job_scraping_results.csv'")

def main():
    scraper = JobScraper()
    
    print("Starting job scraping process...")
    print("Ignoring robots.txt as requested...")
    
    # Scrape all jobs
    job_data = scraper.scrape_all_jobs()
    
    # Display results in table format
    scraper.display_results_table(job_data)
    
    print("\nScraping completed!")

if __name__ == "__main__":
    main()
