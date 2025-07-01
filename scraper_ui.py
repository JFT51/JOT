import streamlit as st
import pandas as pd
import re
from job_scraper import JobScraper
from data_extractor import JobDataExtractor
import time
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="JobOnTop Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data():
    """Load the scraped job data from CSV"""
    try:
        return pd.read_csv('job_scraping_results.csv')
    except FileNotFoundError:
        st.error("No scraped data found. Please run the scraper first.")
        return None

def run_scraper():
    """Run the web scraper and return the data"""
    with st.spinner('Scraping job listings... This may take a while...'):
        scraper = JobScraper()
        job_data = scraper.scrape_all_jobs()
        
        if job_data:
            # Save to CSV
            df = pd.DataFrame(job_data)
            df.to_csv('job_scraping_results.csv', index=False, encoding='utf-8')
            st.success(f"Successfully scraped {len(job_data)} job listings!")
            return df
        else:
            st.error("No job data was scraped.")
            return None

# Main UI
st.title("🔍 JobOnTop.be Job Scraper")
st.markdown("---")

# Sidebar for controls
st.sidebar.header("Controls")

if st.sidebar.button("🚀 Run New Scraping", type="primary"):
    data = run_scraper()
else:
    data = load_data()

if data is not None and not data.empty:
    # Display summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs", len(data))
    with col2:
        bedrijf_filled = data['bedrijf'].str.len() > 0
        st.metric("Jobs with Company Info", bedrijf_filled.sum())
    with col3:
        solliciteren_filled = data['solliciteren'].str.len() > 0
        st.metric("Jobs with Application Info", solliciteren_filled.sum())
    
    st.markdown("---")
    
    # Sidebar filters
    st.sidebar.subheader("🔍 Filters")
    
    # Search in company info
    bedrijf_search = st.sidebar.text_input("Search in Company Info (Bedrijf)")
    
    # Search in application info
    solliciteren_search = st.sidebar.text_input("Search in Application Info (Solliciteren)")
    
    # URL filter
    url_filter = st.sidebar.text_input("Filter by URL keyword")
    
    # Apply filters
    filtered_data = data.copy()
    
    if bedrijf_search:
        filtered_data = filtered_data[filtered_data['bedrijf'].str.contains(bedrijf_search, case=False, na=False)]
    
    if solliciteren_search:
        filtered_data = filtered_data[filtered_data['solliciteren'].str.contains(solliciteren_search, case=False, na=False)]
    
    if url_filter:
        filtered_data = filtered_data[filtered_data['url'].str.contains(url_filter, case=False, na=False)]
    
    # Display filtered results count
    if len(filtered_data) != len(data):
        st.info(f"Showing {len(filtered_data)} of {len(data)} jobs (filtered)")
    
    # Display options
    st.sidebar.subheader("📊 Display Options")
    show_full_text = st.sidebar.checkbox("Show full text (may be slow for large datasets)")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📋 Table View", "📑 Detailed View", "📊 Export Data"])
    
    with tab1:
        st.subheader("Job Listings Table")
        
        if not show_full_text:
            # Show truncated version for better performance
            display_data = filtered_data.copy()
            display_data['bedrijf'] = display_data['bedrijf'].str[:200] + "..."
            display_data['solliciteren'] = display_data['solliciteren'].str[:200] + "..."
            st.dataframe(display_data, use_container_width=True)
        else:
            st.dataframe(filtered_data, use_container_width=True)
    
    with tab2:
        st.subheader("Detailed Job View")
        
        if len(filtered_data) > 0:
            # Job selector
            job_urls = filtered_data['url'].tolist()
            selected_job_idx = st.selectbox(
                "Select a job to view details:",
                range(len(job_urls)),
                format_func=lambda x: f"Job {x+1}: {job_urls[x].split('/')[-1]}"
            )
            
            if selected_job_idx is not None:
                selected_job = filtered_data.iloc[selected_job_idx]
                
                st.markdown(f"### Job Details")
                st.markdown(f"**URL:** [{selected_job['url']}]({selected_job['url']})")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🏢 Company Info (Bedrijf)")
                    if selected_job['bedrijf']:
                        st.write(selected_job['bedrijf'])
                    else:
                        st.write("*No company information available*")
                
                with col2:
                    st.markdown("#### 📧 Application Info (Solliciteren)")
                    if selected_job['solliciteren']:
                        st.write(selected_job['solliciteren'])
                    else:
                        st.write("*No application information available*")
        else:
            st.write("No jobs match the current filters.")
    
    with tab3:
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download Filtered Data as CSV"):
                csv = filtered_data.to_csv(index=False)
                st.download_button(
                    label="💾 Download CSV File",
                    data=csv,
                    file_name=f"jobontop_filtered_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("**Export Options:**")
            st.write(f"- Total jobs to export: {len(filtered_data)}")
            st.write("- Format: CSV")
            st.write("- Encoding: UTF-8")

else:
    st.warning("No job data available. Click 'Run New Scraping' to start scraping job listings.")
    
    if st.button("🚀 Start Scraping", type="primary"):
        data = run_scraper()

# Footer
st.markdown("---")
st.markdown("*JobOnTop.be Scraper - Built with Streamlit*")
