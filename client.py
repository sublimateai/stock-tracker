from src.client.news.base import News
from src.client.news.dataflows.yfinance_news import (
    get_news_yfinance,
    get_global_news_yfinance,
)


def start_parsing():
    news_agg = News()

    # print(news_agg.get_news("Google", "2025-01-20", "2026-05-30"))

    print(get_news_yfinance("Tesla", "2025-01-20", "2026-05-30"))


if __name__ == "__main__":
    start_parsing()
