#region generated meta
import typing
class Inputs(typing.TypedDict):
    cerebro: typing.Any
    strategy: typing.Literal["MeanReversion", "DualMA"]
class Outputs(typing.TypedDict):
    cerebro: typing.Any
#endregion

from oocana import Context
import backtrader as bt


def main(params: Inputs, context: Context) -> Outputs:
    cerebro = params['cerebro']
    strategy = params['strategy']
    if strategy == "MeanReversion":
        cerebro.addstrategy(MeanReversionStrategy)
    elif strategy == "DualMA":
        cerebro.addstrategy(DualMAStrategy)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return { "cerebro": cerebro }

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

class DualMAStrategy(bt.Strategy):
    params = (('fast', 10), ('slow', 30),)
    def __init__(self):
        self.ma_fast = bt.ind.SMA(self.data.close, period=self.params.fast)
        self.ma_slow = bt.ind.SMA(self.data.close, period=self.params.slow)
        self.crossover = bt.ind.CrossOver(self.ma_fast, self.ma_slow)
    
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy(size=100)
        else:
            if self.crossover < 0:
                self.sell(size=100)

