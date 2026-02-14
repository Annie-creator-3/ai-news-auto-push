from typing import List, Dict
import config

def calculate_priority(news: Dict) -> int:
    """计算新闻重要性分数"""
    title = news.get("title", "").lower()
    summary = news.get("summary", "").lower()
    text = title + " " + summary
    
    score = 0
    
    for kw in config.HIGH_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            score += 10
    
    for kw in config.MEDIUM_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            score += 5
    
    if news.get("source") in ["Hacker News", "OpenAI Blog"]:
        score += 3
    
    return score

def filter_and_sort(news_list: List[Dict], max_items: int = 20) -> List[Dict]:
    """筛选并排序新闻"""
    seen_links = set()
    unique_news = []
    for news in news_list:
        link = news.get("link", "")
        if link and link not in seen_links:
            seen_links.add(link)
            unique_news.append(news)
    
    for news in unique_news:
        news["priority_score"] = calculate_priority(news)
    
    sorted_news = sorted(
        unique_news, 
        key=lambda x: (x["priority_score"], x.get("source", "")), 
        reverse=True
    )
    
    return sorted_news[:max_items]

def categorize_news(news_list: List[Dict]) -> Dict[str, List[Dict]]:
    """按重要性分类"""
    high = [n for n in news_list if n["priority_score"] >= 10]
    medium = [n for n in news_list if 5 <= n["priority_score"] < 10]
    normal = [n for n in news_list if n["priority_score"] < 5]
    
    return {
        "🔥 重要": high,
        "📌 关注": medium,
        "📖 一般": normal
    }
