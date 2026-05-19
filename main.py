import os
import requests
from datetime import datetime

# News RSS sources with valid feeds
NEWS_SOURCES = {
    "BBC": "https://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://www.reuters.com/rssFeed/worldNews",
    "CNBC": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
    "Bloomberg": "https://www.bloomberg.com/feed/podcast/etf-report.xml"
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def fetch_rss(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def extract_titles(xml_text, source):
    titles = []
    if not xml_text:
        return titles
    # simple extraction
    parts = xml_text.split("<title>")[2:6]
    for p in parts:
        title = p.split("</title>")[0]
        titles.append(f"[{source}] {title}")
    return titles


def summarize(items):
    unique = []
    seen = set()
    for i in items:
        key = i.split("] ")[-1][:25]
        if key not in seen:
            seen.add(key)
            unique.append(i)
    return "\n".join(unique[:6])


def send_telegram(msg: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("未设置 Telegram 环境变量")
        return
    api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(api, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg})


def main():
    items = []
    for name, url in NEWS_SOURCES.items():
        xml = fetch_rss(url)
        titles = extract_titles(xml, name)
        items.extend(titles)

    summary = summarize(items)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"📰 自动新闻摘要 ({timestamp})\n\n" + summary

    send_telegram(message)


if __name__ == "__main__":
    main()