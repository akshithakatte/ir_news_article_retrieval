import streamlit as st
from news_ir import NewsIRSystem
import pandas as pd
from datetime import datetime
import os

# Configure the Streamlit page
st.set_page_config(
    page_title="News Search Engine",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the IR system
@st.cache_resource
def initialize_ir_system():
    ir_system = NewsIRSystem()
    # Get the absolute path to the JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'Data', 'news.json')
    ir_system.load_articles_from_json(json_path)
    return ir_system

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Search container */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Article card styling */
    .article-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Category badge styling */
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
        background: #e9ecef;
        color: #495057;
        margin-right: 0.5rem;
    }
    
    /* Date styling */
    .date-text {
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* Score styling */
    .score-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 10px;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize the IR system
ir_system = initialize_ir_system()

# Title and description
st.title("📰 News Search Engine")
st.markdown("""
    <div class="search-container">
        <p>Search through our collection of news articles using natural language queries. 
        The system will find the most relevant articles based on your search terms.</p>
    </div>
""", unsafe_allow_html=True)

# Search interface
query = st.text_input("Enter your search query:", placeholder="Type your search query here...")

# Number of results selector
num_results = st.slider("Number of results to show:", min_value=1, max_value=10, value=5)

if query:
    # Perform search
    results = ir_system.search(query, top_k=num_results)
    
    if results:
        st.markdown("### Search Results")
        
        for idx, score in results:
            # Create article card
            st.markdown(f"""
                <div class="article-card">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <h3 style="margin: 0;">{ir_system.headlines[idx]}</h3>
                        <span class="score-badge">Score: {score:.3f}</span>
                    </div>
                    <div style="margin-bottom: 0.5rem;">
                        <span class="category-badge">{ir_system.categories[idx]}</span>
                        <span class="date-text">{ir_system.dates[idx]}</span>
                    </div>
                    <p>{ir_system.descriptions[idx]}</p>
                    <a href="{ir_system.links[idx]}" target="_blank">Read full article →</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No articles found matching your query.")

# Sidebar with dataset statistics
st.sidebar.markdown("""
    <div style="color: white;">
        <h2 style="color: blue;">📊 Dataset Statistics</h2>
    </div>
""", unsafe_allow_html=True)

# Display dataset statistics
total_articles = len(ir_system.documents)
categories = pd.Series(ir_system.categories).value_counts()

st.sidebar.metric("Total Articles", total_articles)

st.sidebar.markdown("### Categories Distribution")
for cat, count in categories.items():
    st.sidebar.text(f"{cat}: {count} articles")
