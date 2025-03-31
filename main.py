import concurrent.futures
from datetime import datetime

from src.scrapers.yfinance_market_news import get_stock_news
from src.scrapers.yfinance_market_screener import get_yfinance_screener_data
from src.utils.utility import save_parquet_data

current_time = datetime.now().strftime("%H:%M:%S")
market_time_open = "15:30:00"
market_time_closed = "22:00:00"


def get_market_info():
    """
    When time matches, the pipeline is triggered
    :return:
    """
    # stocks_list = ""
    if market_time_closed >= current_time >= market_time_open:
        print("Market is open.. started getting data")
        df_stocks = get_yfinance_screener_data()
        stocks_list = list(df_stocks["stock_symbol"])
        with concurrent.futures.ThreadPoolExecutor(3) as executor:
            news_list = executor.map(get_stock_news, stocks_list)

        for news in news_list:
            idx = df_stocks.stock_symbol[df_stocks['stock_symbol'] == news["ticker"]].index.item()
            df_stocks.loc[idx, 'news'] = [news["news_list"]]

        return df_stocks
    # elif stocks_list and current_time == market_time_closed:
    #     save_parquet_data(stocks_list)
        # TODO: save data in parquet partition by datetime (opening and closing date of df stock)


if __name__ == '__main__':
    df_new = get_market_info()
    print(df_new)
