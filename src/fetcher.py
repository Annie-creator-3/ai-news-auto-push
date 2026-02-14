import feedparser
import requests
from typing import List, Dict
import config

def fetch_rss_feeds() -> List[Dict]:
    """抓取所有RSS源"""
    all_news = []
    
    for source_name, url in config.RSS_SOURCES.items():
        try:
            print(f"正在抓取: {source_name}")
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:10]:
                news = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "published": entry.get("published", ""),
                    "source": source_name,
                }
                all_news.append(news)
                
        except Exception as e:
            print(f"抓取 {source_name} 失败: {e}")
    
    return all_news

def fetch_hacker_news() -> List[Dict]:
    """抓取Hacker News AI相关热帖"""
    try:
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        top_ids = response.json()[:30]
        
        ai_news = []
        for item_id in top_ids:
            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
                timeout=10
            ).json()
            
            if item and "title" in item:
                title = item["title"].lower()
                if any(kw in title for kw in ["ai", "llm", "gpt", "openai", "machine learning"]):
                    ai_news.append({
                        "title": item["title"],
                        "link": item.get("url", f"https://news.ycombinator.com/item?id={item_id}"),
                        "summary": "",
                        "published": "",
                        "source": "Hacker News",
                    })
        
        return ai_news[:5]
        
    except Exception as e:
        print(f"抓取 Hacker News 失败: {e}")
        return []
