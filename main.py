import concurrent.futures

from src.scrapers.yfinance_market_news import get_stock_news
from src.scrapers.yfinance_market_screener import get_yfinance_screener_data


def get_market_info():
    df_stocks = get_yfinance_screener_data()
    stocks_list = list(df_stocks["stock_symbol"])
    with concurrent.futures.ThreadPoolExecutor(3) as executor:
        executor.map(get_stock_news, stocks_list)

    print(df_stocks)


if __name__ == '__main__':
    get_market_info()
