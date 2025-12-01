import streamlit as st
from langchain_config2Copy1 import llm_chain, get_news_articles

# --------------------------------------------------------------
# Streamlit Page Setup
# --------------------------------------------------------------
st.set_page_config(page_title="Equity Research News Tool", layout="wide")

st.markdown('<h1 style="text-align:center;">📈 Equity Research News Tool</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#3366FF; font-size:18px; font-weight:500; margin-top:-10px;">'
    'Enter a topic to fetch news and generate AI summaries.'
    '</p>',
    unsafe_allow_html=True
)

# ==============================================================
# Create a placeholder WHERE ALL RESULTS WILL BE DISPLAYED
# ==============================================================

results_area = st.container()   # <— results will ALWAYS appear at bottom


# --------------------------------------------------------------
# Fetch & Display Function (Uses results_area)
# --------------------------------------------------------------
def fetch_and_display_news():
    query = st.session_state.query_input.strip()

    if not query:
        results_area.error("❌ Please enter a valid topic.")
        return

    with results_area:
        results_area.write("")  # clear previous content
        results_area.info(f"🔎 Searching news for **{query}** ...")

        try:
            articles = get_news_articles(query)

            if not articles:
                results_area.warning("⚠️ No articles found.")
                return

            results_area.success(f"✅ Found {len(articles)} articles")

            for idx, art in enumerate(articles):
                title = art.get("title", "No Title")
                source = art.get("source", "Unknown")
                url = art.get("url", "")

                with st.expander(f"📰 {idx+1}. {title} ({source})"):
                    # AI Summary
                    response = llm_chain.invoke({
                        "title": title,
                        "description": art.get("description", ""),
                        "content": art.get("content", "")
                    })

                    if isinstance(response, dict):
                        text = response.get("text") or response.get("output") or str(response)
                    else:
                        text = str(response)

                    st.markdown(f"**AI Summary:**\n{text}")

                    if url:
                        st.markdown(f"[🔗 Read Full Article]({url})")

        except Exception as e:
            results_area.error(f"❌ Error: {e}")


# --------------------------------------------------------------
# Example queries
# --------------------------------------------------------------
example_queries = [
    "Indian economy",
    "Tesla earnings",
    "Artificial Intelligence news",
    "Global markets",
    "Cryptocurrency trends"
]

selected_query = st.selectbox(
    "Choose topic from dropdown OR use search box",
    [""] + example_queries,
    index=0,
)

if selected_query:
    st.session_state["query_input"] = selected_query


# --------------------------------------------------------------
# Search Box (Enter triggers search)
# --------------------------------------------------------------
st.text_input(
    "🔍 Search Topic",
    key="query_input",
    placeholder="e.g., Indian economy, Tesla earnings, AI news, Global markets, Crypto trends",
    on_change=fetch_and_display_news
)


# --------------------------------------------------------------
# Styled Button
# --------------------------------------------------------------
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(90deg, #7b2ff7, #f107a3);
    color: white;
    padding: 12px 26px;
    border-radius: 12px;
    border: none;
    font-size: 17px;
    font-weight: 600;
}
.stButton>button:hover {
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

st.button("🔎 Get News", on_click=fetch_and_display_news)
