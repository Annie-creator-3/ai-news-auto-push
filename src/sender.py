import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import config

def create_html_content(news_by_category: Dict[str, List[Dict]]) -> str:
    """生成HTML邮件内容"""
    from datetime import datetime
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #e74c3c; margin-top: 20px; }}
            .news-item {{ margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
            .news-title {{ font-size: 16px; font-weight: bold; margin-bottom: 5px; }}
            .news-title a {{ color: #2980b9; text-decoration: none; }}
            .news-meta {{ font-size: 12px; color: #7f8c8d; }}
            .score {{ color: #e74c3c; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>🤖 每日 AI 资讯推送</h1>
        <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    """
    
    for category, news_list in news_by_category.items():
        if not news_list:
            continue
            
        html += f"<h2>{category} ({len(news_list)}条)</h2>"
        
        for news in news_list:
            score = news.get("priority_score", 0)
            summary = news.get("summary", "")[:200]
            html += f"""
            <div class="news-item">
                <div class="news-title">
                    <a href="{news['link']}">{news['title']}</a>
                    <span class="score">[{score}分]</span>
                </div>
                <div class="news-meta">来源: {news.get('source', '未知')}</div>
                <div class="news-summary">{summary}...</div>
            </div>
            """
    
    html += """
        <hr>
        <p style="font-size: 12px; color: #95a5a6;">
            由 GitHub Actions 自动推送
        </p>
    </body>
    </html>
    """
    return html

def send_email(news_by_category: Dict[str, List[Dict]]) -> bool:
    """发送邮件（支持多收件人）"""
    try:
        password = os.environ.get("EMAIL_PASSWORD")
        
        if not password:
            print("错误: 未设置 EMAIL_PASSWORD")
            return False
        
        # 支持多收件人
        to_emails = config.TO_EMAILS
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🤖 AI资讯日报 - {__import__('datetime').datetime.now().strftime('%m月%d日')}"
        msg["From"] = config.FROM_EMAIL
        msg["To"] = ", ".join(to_emails)  # 多个收件人用逗号分隔
        
        html_content = create_html_content(news_by_category)
        msg.attach(MIMEText(html_content, "html", "utf-8"))
        
        server = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT)
        server.login(config.FROM_EMAIL, password)
        server.sendmail(config.FROM_EMAIL, to_emails, msg.as_string())  # to_emails是列表
        server.quit()
        
        print(f"邮件发送成功至: {', '.join(to_emails)}")
        return True
        
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False
