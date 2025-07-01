import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import glob
import time
import os
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 JobOnTop AI Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .filter-section {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def find_latest_files():
    """Find the most recent scraped and structured data files"""
    raw_files = glob.glob("job_scraping_results_*.csv")
    structured_files = glob.glob("job_data_structured_*.csv")
    
    latest_raw = max(raw_files, key=os.path.getctime) if raw_files else None
    latest_structured = max(structured_files, key=os.path.getctime) if structured_files else None
    
    return latest_raw, latest_structured

@st.cache_data
def load_data_safe(file_path):
    """Safely load CSV data with error handling"""
    try:
        if file_path and os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return None

def create_download_link(df, filename, label):
    """Create a download button for dataframe"""
    csv = df.to_csv(index=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = f"{filename}_{timestamp}.csv"
    
    st.download_button(
        label=label,
        data=csv,
        file_name=filename_with_timestamp,
        mime="text/csv"
    )

def display_metrics(df_structured):
    """Display key metrics from structured data"""
    if df_structured is None or df_structured.empty:
        st.warning("No structured data available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_jobs = len(df_structured)
        st.metric("Total Jobs", total_jobs)
    
    with col2:
        companies_found = df_structured['company_name'].notna().sum()
        success_rate = f"{(companies_found/total_jobs*100):.1f}%" if total_jobs > 0 else "0%"
        st.metric("Companies Found", f"{companies_found}", delta=success_rate)
    
    with col3:
        emails_found = (df_structured['email_addresses'].str.len() > 0).sum()
        email_rate = f"{(emails_found/total_jobs*100):.1f}%" if total_jobs > 0 else "0%"
        st.metric("Emails Found", f"{emails_found}", delta=email_rate)
    
    with col4:
        phones_found = (df_structured['phone_numbers'].str.len() > 0).sum()
        phone_rate = f"{(phones_found/total_jobs*100):.1f}%" if total_jobs > 0 else "0%"
        st.metric("Phones Found", f"{phones_found}", delta=phone_rate)

def create_location_chart(df_structured):
    """Create location distribution chart"""
    if df_structured is None or df_structured.empty:
        return None
    
    location_counts = df_structured['location'].value_counts().head(10)
    if location_counts.empty:
        return None
    
    fig = px.bar(
        x=location_counts.values,
        y=location_counts.index,
        orientation='h',
        title="🌍 Top 10 Job Locations",
        labels={'x': 'Number of Jobs', 'y': 'Location'},
        color=location_counts.values,
        color_continuous_scale="viridis"
    )
    fig.update_layout(height=400, showlegend=False)
    return fig

def create_contact_info_chart(df_structured):
    """Create contact information availability chart"""
    if df_structured is None or df_structured.empty:
        return None
    
    contact_data = {
        'Email': (df_structured['email_addresses'].str.len() > 0).sum(),
        'Phone': (df_structured['phone_numbers'].str.len() > 0).sum(),
        'Address': df_structured['address'].notna().sum(),
        'Contact Person': df_structured['contact_person'].notna().sum()
    }
    
    fig = px.bar(
        x=list(contact_data.keys()),
        y=list(contact_data.values()),
        title="📞 Contact Information Availability",
        labels={'x': 'Contact Type', 'y': 'Number of Jobs'},
        color=list(contact_data.values()),
        color_continuous_scale="blues"
    )
    fig.update_layout(height=400, showlegend=False)
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 JobOnTop.be AI-Powered Job Scraper</h1>
        <p>Advanced job scraping with AI-powered data extraction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load latest data files
    latest_raw, latest_structured = find_latest_files()
    
    if not latest_raw and not latest_structured:
        st.error("❌ No scraped data found! Please run the scraper first using `python deploy.py`")
        st.info("💡 Run the deployment script to scrape fresh data and then refresh this page.")
        return
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controls")
    
    # File selection
    if latest_raw:
        st.sidebar.success(f"✅ Raw data: {latest_raw}")
    if latest_structured:
        st.sidebar.success(f"✅ Structured data: {latest_structured}")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Load data
    df_raw = load_data_safe(latest_raw)
    df_structured = load_data_safe(latest_structured)
    
    # Main tabs
    if df_structured is not None:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Analytics", 
            "🏢 Structured Data", 
            "📋 Raw Data", 
            "🔍 Job Details", 
            "📥 Export"
        ])
    else:
        tab1, tab2, tab3 = st.tabs([
            "📋 Raw Data", 
            "🔍 Job Details", 
            "📥 Export"
        ])
    
    # Analytics Tab
    if df_structured is not None:
        with tab1:
            st.header("📊 Job Market Analytics")
            
            # Metrics
            display_metrics(df_structured)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                location_fig = create_location_chart(df_structured)
                if location_fig:
                    st.plotly_chart(location_fig, use_container_width=True)
                else:
                    st.info("No location data available for visualization")
            
            with col2:
                contact_fig = create_contact_info_chart(df_structured)
                if contact_fig:
                    st.plotly_chart(contact_fig, use_container_width=True)
                else:
                    st.info("No contact data available for visualization")
        
        # Structured Data Tab
        with tab2:
            st.header("🏢 AI-Extracted Structured Data")
            
            if df_structured is not None and not df_structured.empty:
                # Filters
                st.subheader("🔍 Filters")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    company_filter = st.text_input("🏢 Company Name")
                    
                with col2:
                    location_options = ["All"] + sorted(df_structured['location'].dropna().unique().tolist())
                    location_filter = st.selectbox("📍 Location", location_options)
                
                with col3:
                    st.write("**Data Availability:**")
                    has_email = st.checkbox("Has Email")
                    has_phone = st.checkbox("Has Phone")
                    has_contact = st.checkbox("Has Contact Person")
                
                # Apply filters
                filtered_df = df_structured.copy()
                
                if company_filter:
                    filtered_df = filtered_df[
                        filtered_df['company_name'].str.contains(company_filter, case=False, na=False)
                    ]
                
                if location_filter != "All":
                    filtered_df = filtered_df[filtered_df['location'] == location_filter]
                
                if has_email:
                    filtered_df = filtered_df[filtered_df['email_addresses'].str.len() > 0]
                
                if has_phone:
                    filtered_df = filtered_df[filtered_df['phone_numbers'].str.len() > 0]
                
                if has_contact:
                    filtered_df = filtered_df[filtered_df['contact_person'].notna()]
                
                # Display results
                st.info(f"📋 Showing {len(filtered_df)} of {len(df_structured)} jobs")
                
                # Select columns to display
                display_columns = ['company_name', 'location', 'contact_person', 'email_addresses', 'phone_numbers', 'address']
                
                if not filtered_df.empty:
                    st.dataframe(
                        filtered_df[display_columns],
                        use_container_width=True,
                        column_config={
                            "company_name": st.column_config.TextColumn("Company", width="medium"),
                            "location": st.column_config.TextColumn("Location", width="small"),
                            "contact_person": st.column_config.TextColumn("Contact", width="medium"),
                            "email_addresses": st.column_config.TextColumn("Email", width="medium"),
                            "phone_numbers": st.column_config.TextColumn("Phone", width="small"),
                            "address": st.column_config.TextColumn("Address", width="large"),
                        }
                    )
                else:
                    st.warning("No jobs match the selected filters")
            else:
                st.warning("No structured data available")
    
    # Raw Data Tab
    raw_tab = tab3 if df_structured is not None else tab1
    with raw_tab:
        st.header("📋 Raw Scraped Data")
        
        if df_raw is not None and not df_raw.empty:
            # Basic filters for raw data
            st.subheader("🔍 Search")
            col1, col2 = st.columns(2)
            
            with col1:
                bedrijf_search = st.text_input("Search in Company Info (Bedrijf)")
            with col2:
                solliciteren_search = st.text_input("Search in Application Info (Solliciteren)")
            
            # Apply filters
            filtered_raw = df_raw.copy()
            
            if bedrijf_search:
                filtered_raw = filtered_raw[
                    filtered_raw['bedrijf'].str.contains(bedrijf_search, case=False, na=False)
                ]
            
            if solliciteren_search:
                filtered_raw = filtered_raw[
                    filtered_raw['solliciteren'].str.contains(solliciteren_search, case=False, na=False)
                ]
            
            # Display options
            show_full_text = st.checkbox("Show full text content")
            
            # Display data
            if len(filtered_raw) != len(df_raw):
                st.info(f"📋 Showing {len(filtered_raw)} of {len(df_raw)} jobs (filtered)")
            
            if not show_full_text:
                # Truncated view
                display_df = filtered_raw.copy()
                display_df['bedrijf'] = display_df['bedrijf'].str[:200] + "..."
                display_df['solliciteren'] = display_df['solliciteren'].str[:200] + "..."
                st.dataframe(display_df, use_container_width=True)
            else:
                # Full view
                st.dataframe(filtered_raw, use_container_width=True)
        else:
            st.warning("No raw data available")
    
    # Job Details Tab
    details_tab = tab4 if df_structured is not None else tab2
    with details_tab:
        st.header("🔍 Detailed Job View")
        
        if df_raw is not None and not df_raw.empty:
            # Job selector
            job_urls = df_raw['url'].tolist()
            selected_idx = st.selectbox(
                "Select a job to view details:",
                range(len(job_urls)),
                format_func=lambda x: f"Job {x+1}: {job_urls[x].split('/')[-1]}"
            )
            
            if selected_idx is not None:
                selected_job = df_raw.iloc[selected_idx]
                
                # Job header
                st.markdown(f"### Job Details")
                st.markdown(f"**🔗 URL:** [{selected_job['url']}]({selected_job['url']})")
                
                # Show AI-extracted info if available
                if df_structured is not None:
                    structured_job = df_structured[df_structured['url'] == selected_job['url']]
                    if not structured_job.empty:
                        job_info = structured_job.iloc[0]
                        
                        st.markdown("#### 🤖 AI-Extracted Information")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**🏢 Company:** {job_info.get('company_name', 'N/A')}")
                            st.write(f"**📍 Location:** {job_info.get('location', 'N/A')}")
                            st.write(f"**👤 Contact:** {job_info.get('contact_person', 'N/A')}")
                        
                        with col2:
                            st.write(f"**📧 Email:** {job_info.get('email_addresses', 'N/A')}")
                            st.write(f"**📞 Phone:** {job_info.get('phone_numbers', 'N/A')}")
                            st.write(f"**🏠 Address:** {job_info.get('address', 'N/A')}")
                        
                        st.markdown("---")
                
                # Original scraped content
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🏢 Company Info (Bedrijf)")
                    if selected_job['bedrijf']:
                        st.text_area("", selected_job['bedrijf'], height=300, key="bedrijf")
                    else:
                        st.write("*No company information available*")
                
                with col2:
                    st.markdown("#### 📧 Application Info (Solliciteren)")
                    if selected_job['solliciteren']:
                        st.text_area("", selected_job['solliciteren'], height=300, key="solliciteren")
                    else:
                        st.write("*No application information available*")
        else:
            st.warning("No job data available")
    
    # Export Tab
    export_tab = tab5 if df_structured is not None else tab3
    with export_tab:
        st.header("📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Raw Data Export")
            if df_raw is not None and not df_raw.empty:
                create_download_link(df_raw, "jobontop_raw_data", "📥 Download Raw Data CSV")
                st.write(f"📊 Total jobs: {len(df_raw)}")
            else:
                st.warning("No raw data available for export")
        
        with col2:
            if df_structured is not None:
                st.subheader("Structured Data Export")
                if not df_structured.empty:
                    create_download_link(df_structured, "jobontop_structured_data", "📥 Download Structured Data CSV")
                    st.write(f"📊 Total jobs: {len(df_structured)}")
                else:
                    st.warning("No structured data available for export")
            else:
                st.info("Run AI extraction to enable structured data export")
        
        # Additional export options
        st.markdown("---")
        st.subheader("📊 Export Summary")
        
        if df_structured is not None and not df_structured.empty:
            summary_data = {
                "Metric": ["Total Jobs", "Companies Found", "Locations Found", "Emails Found", "Phones Found", "Addresses Found"],
                "Count": [
                    len(df_structured),
                    df_structured['company_name'].notna().sum(),
                    df_structured['location'].notna().sum(),
                    (df_structured['email_addresses'].str.len() > 0).sum(),
                    (df_structured['phone_numbers'].str.len() > 0).sum(),
                    df_structured['address'].notna().sum()
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            create_download_link(summary_df, "jobontop_summary", "📊 Download Summary Report")

if __name__ == "__main__":
    main()
