# ShopLens AI 🛍️

Shop smarter, not harder, with **ShopWise AI**! 🚀✨ This AI-powered platform revolutionizes the shopping experience by detecting products in videos, analyzing them, and providing real-time price comparisons across popular platforms like Amazon 🛒, Flipkart 🛍️, and Walmart 🏬.

## Features ✨

- **Product Detection** 👀: Automatically identifies products in videos.
- **Smart Recommendations** 🌍: Personalized shopping suggestions based on your preferences and context.
- **Price Comparisons** 💸: Displays the best deals across multiple e-commerce platforms.
- **Shopping Links** 🔗: Direct access to product pages for easy purchasing.
- **Sentiment Analysis** 📊: Analyze product reviews to make informed decisions.

## Demo 🎥
[Watch the Demo Video](https://github.com/Harish24-10-2005/ShopLens-/blob/8d70d3ae56bb31b1b19513429c43f25f47e4e8c4/Demo.mp4)

Upload a video or search for a specific product to see **ShopWise AI** in action. Here's a quick overview:
1. Upload a video file (e.g., `.mp4`, `.mov`, `.avi`).
2. Choose to detect all products or search for a specific item.
3. Get real-time results with shopping links and price comparisons!

## Tech Stack 🛠️

- **Frontend**: Streamlit for a user-friendly interface.
- **AI Agent**: Google Gemini for multimodal AI capabilities.
- **Backend**: Python for processing and integration.
- **APIs**: Google Generative AI for product insights and web scraping for shopping links.
- **Other Tools**:
  - BeautifulSoup for web scraping.
  - Tempfile and Pathlib for handling uploaded video files.
  - Dotenv for secure API key management.

## Installation 🚀

Follow these steps to set up **ShopWise AI** locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/shopwise-ai.git
   cd shopwise-ai
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Google API key**:
   - Create a `.env` file in the root directory.
   - Add the following line:
     ```env
     GOOGLE_API_KEY=your_google_api_key
     ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage 💻

1. **Upload a video**: Choose a video file containing products you want to analyze.
2. **Select analysis type**: Detect all products or search for a specific item.
3. **View results**: Access shopping links and compare prices in real-time.

## Folder Structure 📂

```
VideoSumarizer/
├── Agents/app.py              # Main application file
├── css/styles.css          # Custom CSS for styling
├── requirements.txt    # Dependencies
├── .env                # API key configuration
├── README.md           # Project documentation
└── ...                 # Other project files
```


## Contact 📧

For questions or feedback, reach out via:
- Email: harishravikumar24@gmail.com
- LinkedIn: [Harish R]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/harish-r-12372b28b/))

---

Thank you for checking out **ShopLens AI**! Happy shopping! 🛒✨
