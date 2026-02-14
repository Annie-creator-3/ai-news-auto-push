# 邮件配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
FROM_EMAIL = "siwuxie666@qq.com"  # 发送人
TO_EMAILS = ["siwuxie666@qq.com", "3432881734@qq.com"]  # 收件人列表

# RSS源配置
RSS_SOURCES = {
    "机器之心": "https://www.jiqizhixin.com/rss",
    "量子位": "https://www.qbitai.com/rss",
    "PaperWeekly": "https://www.paperweekly.me/rss",
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
}

# 重要性关键词
HIGH_PRIORITY_KEYWORDS = [
    "GPT", "Claude", "LLM", "大模型", "OpenAI", 
    "融资", "开源", "突破", "Agent", "AGI"
]

MEDIUM_PRIORITY_KEYWORDS = [
    "AI", "人工智能", "深度学习", "NLP", "CV"
]
