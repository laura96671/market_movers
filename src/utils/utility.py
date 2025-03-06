from bs4 import BeautifulSoup, Tag
import configparser
import requests
import os


def yahoo_web_request(url) -> Tag:
    """
    Gets the HTML snippet for yFinance stock major movers
    :return:
    """
    print(f"Started webpage HTML snippets retrieval of {url}...")

    config = configparser.ConfigParser()
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    try:
        request = requests.get(url, headers=headers)
        html_snippet = BeautifulSoup(request.content, 'html5lib')
        print("Snippet retrieved")
        return html_snippet
    except requests.exceptions.ConnectionError as err:
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)