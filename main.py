import os
import requests

NEWS_SOURCES = [
    "https://www.bbc.com/news",
    "https://www.reuters.com/world",
    "https://www.cnbc.com/world/",
    "https://www.bloomberg.com"
]

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def fetch_news():
    items = []
    for url in NEWS_SOURCES:
        try:
            resp = requests.get(url, timeout=10)
            items.append(f"来自 {url} 的新闻标题")
        except Exception:
            pass
    return items


def send_telegram(msg: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("未设置 Telegram 环境变量")
        return

    api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(api, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})


def main():
    news = fetch_news()
    summary = "\n".join(news)
    send_telegram(summary)


if __name__ == "__main__":
    main()
