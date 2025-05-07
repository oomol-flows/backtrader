#region generated meta
import typing
class Inputs(typing.TypedDict):
    cerebro: typing.Any
class Outputs(typing.TypedDict):
    cerebro: typing.Any
#endregion

from oocana import Context
import backtrader as bt

class MeanReversionStrategy(bt.Strategy):
    params = (
        ('ma_period', 20),    # 移动平均周期
        ('dev_threshold', 2), # 标准差阈值
    )
    
    def __init__(self):
        # 计算布林带指标
        self.bollinger = bt.indicators.BollingerBands(
            self.data.close, period=self.p.ma_period, devfactor=self.p.dev_threshold
        )
    
    def next(self):
        if not self.position:  # 无持仓时
            # 价格触及下轨：买入信号
            if self.data.close[0] < self.bollinger.bot:
                self.buy(size=10)
        else:  # 持仓时
            # 价格触及上轨：卖出信号
            if self.data.close[0] > self.bollinger.top:
                self.sell(size=10)


def main(params: Inputs, context: Context) -> Outputs:
    cerebro = params['cerebro']
    cerebro.addstrategy(MeanReversionStrategy)  # 添加策略

    return { "cerebro": cerebro }
