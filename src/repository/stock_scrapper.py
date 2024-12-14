import yfinance as yf
import requests

from bs4 import BeautifulSoup


class StockScrapper:
    def __init__(self):
        pass

    def get_ticker_info(self, ticker: str) -> yf.Ticker | None:
        try:
            ticker_data = yf.Ticker(ticker)
            if ticker_data:
                return ticker_data
            return None
        except Exception as e:
            return None

    def get_sp500_tickers(self):
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'constituents'})

        if not table:
            raise Exception("Could not find the S&P 500 table on the page.")

        tickers = []
        rows = table.find_all('tr')[1:]  # Skip the header row

        for row in rows:
            columns = row.find_all('td')
            if columns:
                ticker = columns[0].text.strip()  # The first column usually contains the ticker symbol
                tickers.append(ticker)

        return tickers
