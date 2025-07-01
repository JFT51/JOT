import streamlit as st
import pandas as pd
import re
from job_scraper import JobScraper
from data_extractor import JobDataExtractor
import time
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="JobOnTop AI Scraper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_raw_data():
    """Load the scraped job data from CSV"""
    try:
        return pd.read_csv('job_scraping_results.csv')
    except FileNotFoundError:
        return None

@st.cache_data
def load_structured_data():
    """Load the AI-extracted structured data from CSV"""
    try:
        return pd.read_csv('job_data_structured.csv')
    except FileNotFoundError:
        return None

def run_scraper():
    """Run the web scraper and return the data"""
    with st.spinner('🕷️ Scraping job listings... This may take a while...'):
        scraper = JobScraper()
        job_data = scraper.scrape_all_jobs()
        
        if job_data:
            # Save raw data
            df = pd.DataFrame(job_data)
            df.to_csv('job_scraping_results.csv', index=False, encoding='utf-8')
            
            # Extract structured data using AI
            with st.spinner('🤖 Extracting structured data with AI...'):
                extractor = JobDataExtractor()
                structured_df = extractor.extract_structured_data(df)
                structured_df.to_csv('job_data_structured.csv', index=False, encoding='utf-8')
            
            st.success(f"Successfully scraped and processed {len(job_data)} job listings!")
            st.cache_data.clear()  # Clear cache to reload new data
            return df, structured_df
        else:
            st.error("No job data was scraped.")
            return None, None

def run_ai_extraction():
    """Run AI extraction on existing raw data"""
    raw_data = load_raw_data()
    if raw_data is not None:
        with st.spinner('🤖 Extracting structured data with AI...'):
            extractor = JobDataExtractor()
            structured_df = extractor.extract_structured_data(raw_data)
            structured_df.to_csv('job_data_structured.csv', index=False, encoding='utf-8')
            st.success("AI extraction completed!")
            st.cache_data.clear()  # Clear cache to reload new data
            return structured_df
    return None

# Main UI
st.title("🤖 JobOnTop.be AI-Powered Job Scraper")
st.markdown("*Advanced job scraping with AI-powered data extraction*")
st.markdown("---")

# Sidebar for controls
st.sidebar.header("🎛️ Controls")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🚀 Full Scrape", type="primary"):
        raw_data, structured_data = run_scraper()
with col2:
    if st.button("🤖 AI Extract"):
        structured_data = run_ai_extraction()
        raw_data = load_raw_data()

# Load data
if 'raw_data' not in locals():
    raw_data = load_raw_data()
if 'structured_data' not in locals():
    structured_data = load_structured_data()

# Check if we have data
if raw_data is not None and not raw_data.empty:
    # Main tabs
    if structured_data is not None and not structured_data.empty:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Analytics Dashboard", 
            "🏢 Structured Data", 
            "📋 Raw Data", 
            "🔍 Job Details", 
            "📥 Export"
        ])
    else:
        st.warning("🤖 AI extraction not completed yet. Click 'AI Extract' to process the data.")
        tab1, tab2, tab3 = st.tabs(["📋 Raw Data", "🔍 Job Details", "📥 Export"])
    
    # Sidebar filters for raw data
    st.sidebar.subheader("🔍 Filters")
    bedrijf_search = st.sidebar.text_input("Search in Company Info")
    solliciteren_search = st.sidebar.text_input("Search in Application Info")
    url_filter = st.sidebar.text_input("Filter by URL keyword")
    
    # Apply filters to raw data
    filtered_raw_data = raw_data.copy()
    if bedrijf_search:
        filtered_raw_data = filtered_raw_data[filtered_raw_data['bedrijf'].str.contains(bedrijf_search, case=False, na=False)]
    if solliciteren_search:
        filtered_raw_data = filtered_raw_data[filtered_raw_data['solliciteren'].str.contains(solliciteren_search, case=False, na=False)]
    if url_filter:
        filtered_raw_data = filtered_raw_data[filtered_raw_data['url'].str.contains(url_filter, case=False, na=False)]
    
    # Analytics Dashboard Tab
    if structured_data is not None and not structured_data.empty:
        with tab1:
            st.header("📊 Job Market Analytics")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Jobs", len(structured_data))
            with col2:
                companies_found = structured_data['company_name'].notna().sum()
                st.metric("Companies Identified", companies_found)
            with col3:
                locations_found = structured_data['location'].notna().sum()
                st.metric("Locations Found", locations_found)
            with col4:
                contacts_found = structured_data['contact_person'].notna().sum()
                st.metric("Contact Persons", contacts_found)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📍 Jobs by Location")
                location_counts = structured_data['location'].value_counts().head(10)
                if not location_counts.empty:
                    fig = px.bar(
                        x=location_counts.values,
                        y=location_counts.index,
                        orientation='h',
                        title="Top 10 Job Locations"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No location data available for visualization")
            
            with col2:
                st.subheader("📧 Contact Information Availability")
                contact_data = {
                    'Email': (structured_data['email_addresses'] != '').sum(),
                    'Phone': (structured_data['phone_numbers'] != '').sum(),
                    'Address': structured_data['address'].notna().sum(),
                    'Contact Person': structured_data['contact_person'].notna().sum()
                }
                
                fig = px.bar(
                    x=list(contact_data.keys()),
                    y=list(contact_data.values()),
                    title="Available Contact Information"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Structured Data Tab
        with tab2:
            st.header("🏢 AI-Extracted Structured Data")
            
            # Structured data filters
            st.subheader("🔍 Advanced Filters")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                company_filter = st.text_input("Company Name")
                location_filter = st.selectbox(
                    "Location", 
                    ["All"] + sorted(structured_data['location'].dropna().unique())
                )
            
            with col2:
                has_email = st.checkbox("Has Email")
                has_phone = st.checkbox("Has Phone")
            
            with col3:
                has_contact = st.checkbox("Has Contact Person")
                has_address = st.checkbox("Has Address")
            
            # Apply structured data filters
            filtered_structured = structured_data.copy()
            
            if company_filter:
                filtered_structured = filtered_structured[
                    filtered_structured['company_name'].str.contains(company_filter, case=False, na=False)
                ]
            
            if location_filter != "All":
                filtered_structured = filtered_structured[
                    filtered_structured['location'] == location_filter
                ]
            
            if has_email:
                filtered_structured = filtered_structured[
                    filtered_structured['email_addresses'] != ''
                ]
            
            if has_phone:
                filtered_structured = filtered_structured[
                    filtered_structured['phone_numbers'] != ''
                ]
            
            if has_contact:
                filtered_structured = filtered_structured[
                    filtered_structured['contact_person'].notna()
                ]
            
            if has_address:
                filtered_structured = filtered_structured[
                    filtered_structured['address'].notna()
                ]
            
            st.info(f"Showing {len(filtered_structured)} of {len(structured_data)} jobs")
            
            # Display structured data
            display_columns = [
                'company_name', 'location', 'contact_person', 
                'email_addresses', 'phone_numbers', 'address'
            ]
            
            st.dataframe(
                filtered_structured[display_columns],
                use_container_width=True,
                column_config={
                    "company_name": "Company",
                    "location": "Location",
                    "contact_person": "Contact Person",
                    "email_addresses": "Email(s)",
                    "phone_numbers": "Phone(s)",
                    "address": "Address"
                }
            )
    
    # Raw Data Tab
    if structured_data is not None and not structured_data.empty:
        current_tab = tab3
    else:
        current_tab = tab1
    
    with current_tab:
        st.header("📋 Raw Scraped Data")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Jobs", len(raw_data))
        with col2:
            bedrijf_filled = raw_data['bedrijf'].str.len() > 0
            st.metric("Jobs with Company Info", bedrijf_filled.sum())
        with col3:
            solliciteren_filled = raw_data['solliciteren'].str.len() > 0
            st.metric("Jobs with Application Info", solliciteren_filled.sum())
        
        if len(filtered_raw_data) != len(raw_data):
            st.info(f"Showing {len(filtered_raw_data)} of {len(raw_data)} jobs (filtered)")
        
        # Display options
        show_full_text = st.checkbox("Show full text (may be slow for large datasets)")
        
        if not show_full_text:
            display_data = filtered_raw_data.copy()
            display_data['bedrijf'] = display_data['bedrijf'].str[:200] + "..."
            display_data['solliciteren'] = display_data['solliciteren'].str[:200] + "..."
            st.dataframe(display_data, use_container_width=True)
        else:
            st.dataframe(filtered_raw_data, use_container_width=True)
    
    # Job Details Tab
    if structured_data is not None and not structured_data.empty:
        details_tab = tab4
    else:
        details_tab = tab2
    
    with details_tab:
        st.header("🔍 Detailed Job View")
        
        if len(filtered_raw_data) > 0:
            # Job selector
            job_urls = filtered_raw_data['url'].tolist()
            selected_job_idx = st.selectbox(
                "Select a job to view details:",
                range(len(job_urls)),
                format_func=lambda x: f"Job {x+1}: {job_urls[x].split('/')[-1]}"
            )
            
            if selected_job_idx is not None:
                selected_job = filtered_raw_data.iloc[selected_job_idx]
                
                st.markdown(f"### Job Details")
                st.markdown(f"**URL:** [{selected_job['url']}]({selected_job['url']})")
                
                # Show structured data if available
                if structured_data is not None:
                    structured_job = structured_data[structured_data['url'] == selected_job['url']]
                    if not structured_job.empty:
                        structured_job = structured_job.iloc[0]
                        
                        st.markdown("#### 🤖 AI-Extracted Information")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Company:** {structured_job.get('company_name', 'N/A')}")
                            st.write(f"**Location:** {structured_job.get('location', 'N/A')}")
                            st.write(f"**Contact Person:** {structured_job.get('contact_person', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Email:** {structured_job.get('email_addresses', 'N/A')}")
                            st.write(f"**Phone:** {structured_job.get('phone_numbers', 'N/A')}")
                            st.write(f"**Address:** {structured_job.get('address', 'N/A')}")
                        
                        st.markdown("---")
                
                # Show original text
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
    
    # Export Tab
    if structured_data is not None and not structured_data.empty:
        export_tab = tab5
    else:
        export_tab = tab3
    
    with export_tab:
        st.header("📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Raw Data Export")
            if st.button("📥 Download Raw Data as CSV"):
                csv = filtered_raw_data.to_csv(index=False)
                st.download_button(
                    label="💾 Download Raw CSV",
                    data=csv,
                    file_name=f"jobontop_raw_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            st.write(f"- Total jobs: {len(filtered_raw_data)}")
        
        with col2:
            if structured_data is not None:
                st.subheader("Structured Data Export")
                if st.button("📥 Download Structured Data as CSV"):
                    csv = structured_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Structured CSV",
                        data=csv,
                        file_name=f"jobontop_structured_data_{time.strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                st.write(f"- Total jobs: {len(structured_data)}")
            else:
                st.info("Run AI extraction first to enable structured data export")

else:
    st.warning("No job data available. Click 'Full Scrape' to start scraping job listings.")
    
    if st.button("🚀 Start Scraping", type="primary"):
        raw_data, structured_data = run_scraper()

# Footer
st.markdown("---")
st.markdown("*JobOnTop.be AI Scraper - Built with Streamlit & Advanced AI Extraction*")
