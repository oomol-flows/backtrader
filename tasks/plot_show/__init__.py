#region generated meta
import typing
class Inputs(typing.TypedDict):
    df: typing.Any
    cerebro: typing.Any
Outputs = typing.Dict[str, typing.Any]
#endregion

from oocana import Context
import backtrader as bt



def main(params: Inputs, context: Context) -> Outputs:
    df = params['df']
    cerebro = params['cerebro']
    data = bt.feeds.PandasData(dataname=df)  # 加载数据[1,6](@ref)
    cerebro.adddata(data)                # 添加数据源
    cerebro.run()  # 执行策略模拟[1,4](@ref)
    # portvalue = cerebro.broker.getvalue()  # 获取最终资产总额
    # pnl = portvalue - 100000
    # print(f'总资产: {portvalue:.2f}, 净收益: {pnl:.2f}')  # 示例输出：总资产101015.87，收益1015元[1](@ref)
    cerebro.plot()
