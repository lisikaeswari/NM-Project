import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Indian Express News Search",
    page_icon="📰",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1E3A8A;
    }
    .news-item {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

def load_datasets():
    """Load all available news datasets"""
    data_files = {
        'Business': 'business_data.csv',
        'Education': 'education_data.csv',
        'Entertainment': 'entertainment_data.csv',
        'Sports': 'sports_data.csv',
        'Technology': 'technology_data.csv'
    }
    
    datasets = {}
    for category, filename in data_files.items():
        try:
            file_path = Path(filename)
            if file_path.exists():
                df = pd.read_csv(file_path)
                datasets[category] = df
        except Exception as e:
            st.error(f"Error loading {filename}: {str(e)}")
    
    return datasets

def main():
    # Header
    st.title("📰 Indian Express News Article Search")
    st.markdown("---")
    
    # Load datasets
    datasets = load_datasets()
    
    if not datasets:
        st.error("No datasets found. Please ensure the news CSV files are in the correct location.")
        return
    
    # Sidebar for category selection
    st.sidebar.title("Search Options")
    selected_category = st.sidebar.selectbox(
        "Select News Category",
        options=list(datasets.keys())
    )
    
    # Search functionality
    search_query = st.text_input("🔍 Search articles (leave empty to show all):", "")
    
    if selected_category in datasets:
        df = datasets[selected_category]
        
        # Filter based on search query if provided
        if search_query:
            mask = df['title'].str.contains(search_query, case=False, na=False) | \
                  df['content'].str.contains(search_query, case=False, na=False)
            filtered_df = df[mask]
        else:
            filtered_df = df
        
        # Show results count
        st.subheader(f"Found {len(filtered_df)} articles in {selected_category}")
        st.markdown("---")
        
        # Display articles
        for idx, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="news-item">
                    <h3>{row['title']}</h3>
                    <p>{row['content'][:300]}...</p>
                    <small>Date: {row.get('date', 'N/A')}</small>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
