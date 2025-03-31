from src.utils.utility import yahoo_web_request
import pandas as pd


def get_yfinance_screener_data() -> pd.DataFrame:
    """
    Gets data from table snippet retrieved from bs4 to populate a Pandas df
    :return:
    """
    print("Started data ingestion from HTML snippet...")

    market_screener_url = "https://finance.yahoo.com/markets/stocks/trending/"
    html_snippet = yahoo_web_request(market_screener_url)
    raw_table = html_snippet.find("table", class_="markets-table")
    real_time_data = {
        "stock_symbol": [],
        "stock_full_name": [],
        "stock_price": [],
        "stock_pct_change": [],
        "stock_volume": [],
        "stock_market_cap": []
    }

    table_rows = raw_table.find_all('tbody')[0].find_all("tr")

    for row in table_rows:
        real_time_data["stock_symbol"].append(
            row.find("span", class_="symbol").text.strip()
        )
        real_time_data["stock_full_name"].append(
            row.td.span.div.a["title"]
        )
        real_time_data["stock_price"].append(
            float(row.find("fin-streamer", attrs={'data-field': 'regularMarketPrice'}).text)
        )
        real_time_data["stock_pct_change"].append(
            row.find("fin-streamer", attrs={'data-field': 'regularMarketChangePercent'}).text
                  .translate(str.maketrans({"(": "", "%": "", ")": ""}))
        )
        real_time_data["stock_volume"].append(
            row.find("fin-streamer", attrs={'data-field': 'regularMarketVolume'}).text
        )
        real_time_data["stock_market_cap"].append(
            row.find("fin-streamer", attrs={'data-field': 'marketCap'}).text
        )

    df_stocks = pd.DataFrame(real_time_data).sort_values(by=["stock_pct_change"], ascending=False)

    return df_stocks
