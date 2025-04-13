import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Add parent directory to path to import the crawler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from naver_news_downloader import get_naver_news, save_to_excel

st.set_page_config(page_title="Naver News Downloader", layout="wide")

st.title("Naver News Downloader")

def make_clickable(link):
    # Returns a clickable link that opens in a new tab
    return f'<a href="{link}" target="_blank">{link}</a>'

with st.form("search_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keyword = st.text_input("Search Keyword", placeholder="Enter keyword...")
    
    with col2:
        pages = st.number_input("Number of Pages", min_value=1, max_value=20, value=5)
    
    submitted = st.form_submit_button("Search")
    
    if submitted and keyword:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create a custom function to handle progress updates
        def get_news_with_progress():
            articles = []
            status_text.text(f"Searching for '{keyword}' news...")
            
            for page in range(1, pages + 1):
                progress = (page - 1) / pages
                progress_bar.progress(progress)
                status_text.text(f"Fetching page {page}/{pages}...")
                
                # Call the original function but with our specific page
                page_articles = get_naver_news(keyword, max_pages=1, start_page=page)
                articles.extend(page_articles)
            
            progress_bar.progress(1.0)
            return articles
        
        # Get articles
        try:
            articles = get_news_with_progress()
            
            if articles:
                # Convert to DataFrame for display
                df = pd.DataFrame(articles)
                
                # Apply the clickable link function to the 링크 column
                df_display = df.copy()
                df_display['링크'] = df_display['링크'].apply(make_clickable)
                
                # Show results
                status_text.text(f"Found {len(articles)} articles")
                st.dataframe(df_display.to_html(escape=False), unsafe_allow_html=True)
                
                # Create Excel file
                today = datetime.now().strftime('%Y%m%d')
                filename = f"downloads/{keyword}_news_{today}.xlsx"
                os.makedirs("downloads", exist_ok=True)
                
                save_to_excel(articles, filename)
                
                # Provide download button - fix the error by reading the file first
                try:
                    with open(filename, "rb") as file:
                        file_data = file.read()
                        
                    st.download_button(
                        label="Download Excel File",
                        data=file_data,
                        file_name=f"{keyword}_news_{today}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"Download button error: {str(e)}")
                    st.write("You can manually download the file from the 'downloads' folder")
            else:
                status_text.text("No articles found.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
