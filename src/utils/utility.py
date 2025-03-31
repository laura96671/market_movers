from bs4 import BeautifulSoup, Tag

import configparser
import json
import pandas as pd
import requests


config = configparser.ConfigParser()
config.read('src/utils/config.ini')


def save_parquet_data(stocks_list: list) -> pd.DataFrame:
    a_vantage_key = config.get("ALPHA_VANTAGE", "API_KEY")

    interval = "5min"
    df = pd.DataFrame()

    for stock in stocks_list:
        url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
               f"&symbol={stock}"
               f"&interval={interval}"
               f"&apikey={a_vantage_key}")
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            inner_data = data[f"Time Series ({interval})"]

            time = list(inner_data.keys())
            df_raw = pd.DataFrame(inner_data).items()
            df = (
                pd.json_normalize(df_raw[1])
                .rename(columns={"1. open": "open",
                                 "2. high": "high",
                                 "3. low": "low",
                                 "4. close": "close",
                                 "5. volume": "volume"})
            )
            df["ticker"] = stock
            df["time"] = time

    return df


def yahoo_web_request(url) -> Tag:
    """
    Gets the HTML snippet for yFinance stock major movers
    :return:
    """
    print(f"Started webpage HTML snippets retrieval of {url}...")

    header_config = config.get("BROWSER_REQUEST", "USER_AGENT")
    headers = {'User-Agent': header_config}

    try:
        request = requests.get(url, headers=headers)
        html_snippet = BeautifulSoup(request.content, 'html5lib')
        print("Snippet retrieved")
        return html_snippet
    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)