#region generated meta
import typing
class Inputs(typing.TypedDict):
    cash: float
    commission: float
class Outputs(typing.TypedDict):
    cerebro: typing.Any
#endregion

from oocana import Context
import backtrader as bt

def main(params: Inputs, context: Context) -> Outputs:
    cerebro = bt.Cerebro()  # 初始化核心引擎
    cerebro.broker.set_cash(params['cash'])      # 设置初始资金为10万元[1,6](@ref)
    cerebro.broker.setcommission(params['commission'])  # 设置交易手续费为0.2%[1,6](@ref)
    return { "cerebro": cerebro }
