#region generated meta
import typing
class Inputs(typing.TypedDict):
    ticker: str
    start_time: str
    end_time: str
class Outputs(typing.TypedDict):
    df: typing.Any
#endregion

from oocana import Context
import yfinance as yf
from datetime import datetime

def main(params: Inputs, context: Context) -> Outputs:
    ticker = params['ticker']
    start_time = params['start_time']
    end_time = params['end_time']
    dat = yf.Ticker(ticker=ticker)
    df = dat.history(start=get_time(start_time), end=get_time(end_time))
    context.preview(df)

    return { "df": df }

def get_time (datetime_str):
    datetime_obj = datetime.fromisoformat(datetime_str)
    date_str = datetime_obj.strftime("%Y-%m-%d")
    return date_str



