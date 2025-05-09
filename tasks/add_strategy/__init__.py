#region generated meta
import typing
class Inputs(typing.TypedDict):
    cerebro: typing.Any
    strategy: typing.Literal["MeanReversion", "DualMA", "GridTradingStrategy", "BollingerBandsStrategy", "RsiMacdStrategy"]
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
    elif strategy == "GridTradingStrategy": 
        cerebro.addstrategy(GridTradingStrategy)
    elif strategy == "BollingerBandsStrategy":
        cerebro.addstrategy(BollingerBandsStrategy)
    elif strategy == "RsiMacdStrategy":
        cerebro.addstrategy(RsiMacdStrategy)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return { "cerebro": cerebro }

# 均值回归策略
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

# 移动平均线交叉策略
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


# 网格交易策略
class GridTradingStrategy(bt.Strategy):
    params = (
        ('grid_size', 0.05),  # 网格大小（价格变动百分比）
        ('num_grids', 10),    # 网格数量
        ('order_size', 0.1),  # 每次订单占比
    )

    def __init__(self):
        self.initial_price = None
        self.grid_levels = None
        self.initial_cash = self.broker.getvalue()  # 获取初始资金
        self.orders = []  # 用于存储未完成的订单

    def next(self):
        if not self.initial_price:
            self.initial_price = self.data.close[0]
            # 计算网格水平、注意这里修改为正确的列表推导式
            self.grid_levels = [self.initial_price * (1 + i * self.params.grid_size) 
                               for i in range(-self.params.num_grids, self.params.num_grids + 1)]

        current_price = self.data.close[0]

        # 计算订单大小，确保不超过当前资金的一定比例
        order_size = self.broker.getvalue() * self.params.order_size

        # 初始化标志变量
        buy_triggered = False
        sell_triggered = False

        # 遍历网格水平，检查买入和卖出条件
        for i, level in enumerate(self.grid_levels):
            # 买入逻辑：当价格低于某个网格水平，且没有持仓时
            if current_price <= level and not self.position and not self.orders and not buy_triggered:
                # 计算可以购买的数量
                size = int(order_size / current_price)
                # 确保购买数量为正
                if size > 0:
                    order = self.buy(size=size)
                    self.orders.append(order)
                    buy_triggered = True  # 设置买入标志，避免多次买入

            # 卖出逻辑：当价格高于某个网格水平，且有持仓时
            elif current_price >= level and self.position and not self.orders and not sell_triggered:
                # 计算可以卖出的数量
                size = int(order_size / current_price)
                # 确保卖出数量不超过持仓数量
                size = min(size, self.position.size)
                if size > 0:
                    order = self.sell(size=size)
                    self.orders.append(order)
                    sell_triggered = True  # 设置卖出标志，避免多次卖出

        # 检查订单状态，如果订单已完成则从列表中移除
        for order in self.orders[:]:
            if order.status in [order.Completed, order.Canceled, order.Margin]:
                self.orders.remove(order)


# 布林带策略
class BollingerBandsStrategy(bt.Strategy):
    params = (
        ('period', 20),  # 布林带周期
        ('devfactor', 2.0),  # 布林带标准差倍数
    )
    
    def __init__(self):
        self.boll = bt.indicators.BollingerBands(self.data.close, period=self.params.period, devfactor=self.params.devfactor)
    
    def next(self):
        if not self.position:
            if self.data.close[0] < self.boll.bot:
                self.buy(size=100)
        else:
            if self.data.close[0] > self.boll.top:
                self.sell(size=100)

# RSI-MACD组合策略
# 这个策略有点问题，并不会实现买入和卖出
class RsiMacdStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),  # RSI周期
        ('rsi_overbought', 70),  # RSI超买阈值
        ('rsi_oversold', 30),  # RSI超卖阈值
        ('macd1', 12),  # MACD快线周期
        ('macd2', 26),  # MACD慢线周期
        ('macdsignal', 9),  # MACD信号线周期
    )
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.macd = bt.indicators.MACD(self.data.close, period_me1=self.params.macd1, period_me2=self.params.macd2, period_signal=self.params.macdsignal)
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.order = None  # 用于跟踪当前订单
    
    def next(self):
        if self.order:
            return  # 如果有未完成的订单，先处理订单
        
        # 打印调试信息
        print(f"Date: {self.data.datetime.date(0)}, Close: {self.data.close[0]:.2f}, RSI: {self.rsi[0]:.2f}, MACD: {self.macd.macd[0]:.2f}, Signal: {self.macd.signal[0]:.2f}, Crossover: {self.crossover[0]:.2f}")
        
        if not self.position:
            # 买入条件：RSI低于超卖阈值且MACD快线向上穿过信号线
            if self.rsi[0] < self.params.rsi_oversold and self.crossover[0] > 0:
                self.order = self.buy(size=100)
                print(f"买入订单已提交，价格: {self.data.close[0]:.2f}")
        else:
            # 卖出条件：RSI高于超买阈值或MACD快线向下穿过信号线
            if self.rsi[0] > self.params.rsi_overbought or self.crossover[0] < 0:
                self.order = self.sell(size=100)
                print(f"卖出订单已提交，价格: {self.data.close[0]:.2f}")

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # 订单已提交或已接受，无须进一步操作
            return

        # 检查订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                print(f"买入完成，价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}")
            elif order.issell():
                print(f"卖出完成，价格: {order.executed.price:.2f}, 成本: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}")
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f"订单被取消/拒绝，状态:{order.status}")

        self.order = None  # 重置订单

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        print(f"交易毛利润: {trade.pnl:.2f}, 净利润: {trade.pnlcomm:.2f}")