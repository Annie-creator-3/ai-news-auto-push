#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from src.fetcher import fetch_rss_feeds, fetch_hacker_news
from src.filter import filter_and_sort, categorize_news
from src.sender import send_email

def main():
    print("=" * 50)
    print("🤖 AI资讯自动推送系统启动")
    print("=" * 50)
    
    print("\n📡 正在抓取资讯...")
    rss_news = fetch_rss_feeds()
    hn_news = fetch_hacker_news()
    all_news = rss_news + hn_news
    
    print(f"共抓取到 {len(all_news)} 条原始资讯")
    
    print("\n🔍 正在筛选排序...")
    filtered_news = filter_and_sort(all_news, max_items=20)
    print(f"筛选后剩余 {len(filtered_news)} 条")
    
    news_by_category = categorize_news(filtered_news)
    for cat, items in news_by_category.items():
        print(f"  {cat}: {len(items)}条")
    
    print("\n📧 正在发送邮件...")
    success = send_email(news_by_category)
    
    if success:
        print("\n✅ 任务完成！")
    else:
        print("\n❌ 任务失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
