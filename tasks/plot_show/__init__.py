#region generated meta
import typing
class Inputs(typing.TypedDict):
    df: typing.Any
    cerebro: typing.Any
class Outputs(typing.TypedDict):
    cerebro: typing.Any
#endregion

from oocana import Context
import backtrader as bt



def main(params: Inputs, context: Context) -> Outputs:
    df = params['df']
    cerebro = params['cerebro']
    data = bt.feeds.PandasData(dataname=df)  # 加载数据[1,6](@ref)
    cerebro.adddata(data)                # 添加数据源
    cerebro.run()  # 执行策略模拟[1,4](@ref)
    cerebro.plot()
    return {'cerebro': cerebro}
