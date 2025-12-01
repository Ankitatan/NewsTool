from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from newsapi import NewsApiClient

# -----------------------------
# API KEYS
# -----------------------------
OPENAI_API_KEY = "sk-Your Key"
NEWSAPI_KEY = "Your Key"

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini"
)

# -----------------------------
# Prompt Template for LCEL
# -----------------------------
template = """
You are an AI assistant helping an equity research analyst.
Given the following news article, summarize the key points clearly in bullet form.

Title: {title}
Description: {description}
Content: {content}

Summary:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["title", "description", "content"]
)

# Output parser
parser = StrOutputParser()
llm_chain = prompt | llm | parser

# -----------------------------
# NewsAPI Function
# -----------------------------
def get_news_articles(query, max_articles=5):
    """
    Fetch top news articles for a given query.
    Returns a list of dictionaries with keys:
    title, description, content, url, source
    """
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    try:
        result = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            page_size=max_articles
        )
        articles = result.get("articles", [])
        cleaned = []
        for art in articles:
            if isinstance(art, dict):
                cleaned.append({
                    "title": art.get("title", "No Title"),
                    "description": art.get("description", ""),
                    "content": art.get("content", ""),
                    "url": art.get("url", ""),
                    "source": art.get("source", {}).get("name", "Unknown")
                })
        return cleaned
    except Exception as e:
        return [{
            "title": "NewsAPI Error",
            "description": f"Unable to fetch news. Error: {str(e)}",
            "content": "",
            "url": "",
            "source": "Error"
        }]
