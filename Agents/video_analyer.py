import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from google.generativeai import upload_file, get_file
import google.generativeai as genai
import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
import json


load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def search_shopping_links(product_name, num_results=3):
    """Search for shopping links across different platforms."""
    try:
        amazon_url = f"https://www.amazon.in/s?k={quote_plus(product_name)}"
        flipkart_url = f"https://www.flipkart.com/search?q={quote_plus(product_name)}"
        walmart_url = f"https://www.walmart.com/search?q={quote_plus(product_name)}"
        
        shopping_links = [
            {
                "title": "Amazon",
                "link": amazon_url,
                "icon": "🛒"
            },
            {
                "title": "Flipkart",
                "link": flipkart_url,
                "icon": "🛍️"
            },
            {
                "title": "Walmart",
                "link": walmart_url,
                "icon": "🏬"
            }
        ]
        
        return shopping_links[:num_results]
    except Exception as e:
        st.warning(f"Error fetching shopping links: {str(e)}")
        return []

def load_css():
    """Load the custom CSS styles."""
    with open('D:\AI_Agents\VideoSummarizer\css\style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_shopping_links(product_name, shopping_results):
    """Display shopping links in a styled card format."""
    st.markdown(f"""
        <div class="product-card">
            <h3>{product_name}</h3>
            <div class="shopping-links">
    """, unsafe_allow_html=True)

    for result in shopping_results:
        price_class = "best-price" if result.get('is_best_price') else "average-price"
        st.markdown(f"""
            <a href="{result['link']}" target="_blank" class="shop-link">
                <span class="shop-icon">{result['icon']}</span>
                <div class="shop-details">
                    <div class="shop-name">{result['title']}</div>
                    <div class="shop-price">Click to check current price</div>
                </div>
                <span class="price-badge {price_class}">
                    {result.get('price_indicator', 'Compare')}
                </span>
            </a>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

def display_shopping_results(products):
    """Display shopping results in a grid layout."""
    st.markdown('<div class="product-grid">', unsafe_allow_html=True)
    
    for product in products:
        product_name = product["name"]
        shopping_results = search_shopping_links(product_name)
        display_shopping_links(product_name, shopping_results)
    
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the Gemini agent."""
    return Agent(
        name="Product Detection Assistant",
        model=Gemini(id="gemini-2.0-flash-exp"),
        markdown=True,
    )

def process_video(video_path, user_query, analysis_type, multimodal_Agent):
    """Process the uploaded video and analyze products."""
    with st.spinner("🎥 Processing video..."):
        progress_bar = st.progress(0)
        processed_video = upload_file(video_path)
        
        while processed_video.state.name == "PROCESSING":
            time.sleep(1)
            processed_video = get_file(processed_video.name)

        analysis_prompt = """
        Analyze the video and:
        1. Identify all visible products/items
        2. For each product, provide:
           - Detailed description
           - Brand name (if visible)
           - Specific features
           - Category
           - Estimated price range (if possible)
        3. Format the response as a structured list
        """ if analysis_type == "Detect All Products" else f"""
        Analyze the video and focus on finding:
        {user_query}
        Provide:
        1. Exact description of the product
        2. Brand name (if visible)
        3. Specific features
        4. Category
        5. Estimated price range (if possible)
        6. Best search terms for finding this product online
        """

        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])
        
        st.markdown("""
            <div class='results-section' style='margin-top: 2rem;'>
                <h2 style='color:rgb(255, 255, 255);'>📝 Analysis Results</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='product-card'>
                {response.content}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='shopping-section' style='margin-top: 2rem;'>
                <h2 style='color:rgb(255, 255, 255);'>🛒 Shopping Options</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("🔎 Finding best shopping options..."):
            shopping_prompt = f"""
            From the previous analysis:
            {response.content}
            
            Extract the main product names and their categories as a list of JSON objects.
            Format: {{"name": "product name", "category": "category"}}
            Include only the most specific and searchable terms.
            """
            products_response = multimodal_Agent.run(shopping_prompt)
            products_json = products_response.content
            cleaned_json = products_json.replace("```json", "").replace("```", "").strip()
            
            try:
                products = json.loads(cleaned_json)
                display_shopping_results(products)

                st.markdown("""
                    <div class="info-box">
                        💡 Pro Tip: Compare prices across different retailers and check for seasonal deals!
                    </div>
                """, unsafe_allow_html=True)

            except json.JSONDecodeError as e:
                st.error(f"Error processing product data: {e}")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Smart Shopping Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load CSS
    load_css()
    
    # Initialize agent
    multimodal_Agent = initialize_agent()
    
    # Header
    st.markdown("""
        <div class="header">
            <h1>Smart Shopping Assistant 🛒</h1>
            <p>Your go-to tool for detecting and analyzing products in videos! 🎥🔍</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div class="sidebar">
                <h3>✨ About</h3>
                <ul>
                    <li><span>🛍️</span> Detect products in videos</li>
                    <li><span>📊</span> Provide detailed analysis</li>
                    <li><span>🔗</span> Find shopping links</li>
                    <li><span>💸</span> Compare prices</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Analysis Options
    st.markdown("""
        <div class="analysis-options">
            <div class="option active">Detect All Products</div>
            <div class="option">Search Specific Product</div>
        </div>
    """, unsafe_allow_html=True)

    # Main content layout
    col1, col2 = st.columns([2, 1])

    with col1:
        video_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'mov', 'avi'],
            help="Upload a video to detect products and get shopping links"
        )

    with col2:
        analysis_type = st.radio(
            "Select Analysis Type",
            ["Detect All Products", "Search Specific Product"],
            help="Choose your analysis method"
        )

    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name

        st.video(video_path, format="video/mp4", start_time=0)

        if analysis_type == "Search Specific Product":
            user_query = st.text_area(
                "What product are you looking for?",
                placeholder="Example: 'Find the blue jacket the person is wearing'",
                help="Be specific about the product you want to find"
            )
        else:
            user_query = ""

        if st.button("🔍 Analyze Video", key="detect_products_button"):
            try:
                process_video(video_path, user_query, analysis_type, multimodal_Agent)
            except Exception as error:
                st.error(f"❌ Analysis Error: {error}")
            finally:
                Path(video_path).unlink(missing_ok=True)
    else:
        st.info("👆 Upload a video to begin your smart shopping experience!")

if __name__ == "__main__":
    main()