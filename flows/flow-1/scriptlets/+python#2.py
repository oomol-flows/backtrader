#region generated meta
import typing
class Inputs(typing.TypedDict):
    df: typing.Any
class Outputs(typing.TypedDict):
    output: str
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
    df = params['df']
    # your code
    cerebro = bt.Cerebro()  # 初始化核心引擎[1,4](@ref)
    data = bt.feeds.PandasData(dataname=df)  # 加载数据[1,6](@ref)
    cerebro.adddata(data)                # 添加数据源
    cerebro.addstrategy(MeanReversionStrategy)  # 添加策略
    cerebro.broker.setcash(100000)       # 设置初始资金为10万元[1,6](@ref)
    cerebro.broker.setcommission(commission=0.001)  # 设置交易佣金0.1%[1,4](@ref)
    cerebro.run()  # 执行策略模拟[1,4](@ref)
    portvalue = cerebro.broker.getvalue()  # 获取最终资产总额
    pnl = portvalue - 100000
    print(f'总资产: {portvalue:.2f}, 净收益: {pnl:.2f}')  # 示例输出：总资产101015.87，收益1015元[1](@ref)
    cerebro.plot()
    return { "output": "output_value" }
