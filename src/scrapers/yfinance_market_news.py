import re

from bs4 import Tag
from src.utils.utility import yahoo_web_request
from src.scrapers.yfinance_market_screener import get_yfinance_screener_data


def get_stock_news(ticker: str):
    """
    Gets list of news of current day related to tickers retrieved from screener
    :param ticker: str
    :return:
    """
    stock_news_url = f"https://finance.yahoo.com/quote/{ticker}/news/"
    publishing_time_pattern = re.compile("(\d+\shours?\sago)|(\d+\sminutes?\sago)")

    html_snippet = yahoo_web_request(stock_news_url)
    raw_news_list = html_snippet.find("ul", class_="stream-items")
    news_list = {}

    for news in raw_news_list:
        if isinstance(news, Tag) and news.has_attr("class") and 'story-item' in news['class']:
            publishing_time = news.find("div", class_="publishing").text

            if re.search(publishing_time_pattern, publishing_time):
                news_link = news.find("a", class_="subtle-link")["href"]
                news_title = news.find("h3", class_="clamp").text
                news_list[news_title] = f"{news_link}"
            else:
                break

    df_stocks = get_yfinance_screener_data()
    idx = df_stocks[df_stocks['stock_symbol'] == ticker].index.item()
    df_stocks.loc[idx, 'news'] = [news_list]
