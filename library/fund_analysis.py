import pandas as pd
import yfinance
import pandas
import sqlalchemy
from datetime import datetime

TODAY = datetime.today().strftime('%Y-%m-%d')

# Defining 10 funds
FUNDS = dict()
FUNDS["VFIAX"] = "Vanguard 500 Index Fund"
FUNDS["MDLOX"] = "BlackRock Global Allocation Fund"
FUNDS["OPGIX"] = "Invesco Global Opportunities Fund"
FUNDS["MAPIX"] = "Matthews Asia Dividend Fund"
FUNDS["VGHCX"] = "Vanguard Health Care Fund"
FUNDS["AGTHX"] = "American Funds The Growth Fund of America"
FUNDS["FCNTX"] = "Fidelity Contrafund"
FUNDS["INIVX"] = "VanEck International Investors Gold Fund"
FUNDS["JMIEX"] = "JPMorgan Emerging Markets Equity Fund"
FUNDS["FLPSX"] = "Fidelity Low-Priced Stock Fund"

USER = "admin"
PASS = "mysqlfund"
ENGINE = sqlalchemy.create_engine(
    f"mysql://{USER}:{PASS}@fund.cojr28wufwf9.us-west-1.rds.amazonaws.com:3306/fund_db")

# Download function
def load_return_data(funds=None, start_date=None, end_date=None):
    """
    This function aims to calculate 1,3,5,7,10 year compounded annual growth rate (CAGR) for each fund and stores it in
    "mutual_fund_returns" table in mysql database.
    :return:
    """

    # If not given take above defined funds
    if not funds:
        funds = FUNDS

    # Initailise empty fund data list
    fund_data_list = list()

    # Loop over each ticker, get data from sql, calculate fund returns and append data into above list
    for ticker in funds:
        fund_name = funds[ticker]
        query = """
                    SELECT 
                        * 
                    FROM 
                        fund_db.daily_fund_data
                    WHERE
                        ticker = '{}'
                """.format(ticker)
        data = pd.read_sql(sql=query, con=ENGINE)

        # CAGR
        one_yr_CAGR = (data.iloc[-1]["price"] / data.iloc[-252]["price"] - 1) * 100
        three_yr_CAGR = ((data.iloc[-1]["price"] / data.iloc[-3 * 252]["price"]) ** (1 / 3) - 1) * 100
        five_yr_CAGR = ((data.iloc[-1]["price"] / data.iloc[-5 * 252]["price"]) ** (1 / 5) - 1) * 100
        seven_yr_CAGR = ((data.iloc[-1]["price"] / data.iloc[-7 * 252]["price"]) ** (1 / 7) - 1) * 100
        ten_yr_CAGR = ((data.iloc[-1]["price"] / data.iloc[-10 * 252]["price"]) ** (1 / 10) - 1) * 100
        fund_data = [TODAY, ticker, fund_name, one_yr_CAGR, three_yr_CAGR, five_yr_CAGR, seven_yr_CAGR, ten_yr_CAGR]
        fund_data_list.append(fund_data)

    # Create a dataframe that look like our table and push the data into table.
    df = pandas.DataFrame(data=fund_data_list,
                          columns=["date", "ticker", "fund_name", "CAGR_1Y", "CAGR_3Y", "CAGR_5Y",
                                   "CAGR_7Y", "CAGR_10Y"])
    df.to_sql(name="mutual_fund_returns", con=ENGINE, schema="fund_db", if_exists="append", index=False)
    return


def download_daily_data(funds=None):
    """
    This function aims to download daily fund data from yahoo finance api for input funds for all available dates
    and stores it in mysql table "daily_fund_data".
    :param funds:
    :return:
    """
    # If funds are not specified take 10 default funds
    if not funds:
        funds = FUNDS

    # Loop over each ticker, download data, calculate fund returns and append data into above list
    for ticker in funds:
        data = yfinance.download(tickers=ticker, period="max").reset_index()
        data["ticker"] = ticker
        data["Date"] = data["Date"].apply(lambda x: x.strftime("%y-%m-%d"))
        data = data.rename(columns={"Date": "date", "Adj Close": "price"})
        data = data[["date", "ticker", "price"]]
        data.to_sql(name="daily_fund_data", con=ENGINE, schema="fund_db", if_exists="append", index=False)

    return

load_return_data()