#region generated meta
import typing
class Inputs(typing.TypedDict):
    cerebro: typing.Any
    cash: float
Outputs = typing.Dict[str, typing.Any]
#endregion

from backtrader import cerebro
from oocana import Context, data

def main(params: Inputs, context: Context) -> Outputs:
    cerebro = params['cerebro']
    cash = params['cash']
    portvalue = cerebro.broker.getvalue()  # 获取最终资产总额
    pnl = portvalue - cash
    formatted_text = f"""| 指标名称   | 数值         |
|:-----------|-------------:|
| 初始资产   | {cash}       |
| 总资产     | {portvalue:.2f} |
| 净收益     | {pnl:.2f}    |"""
    context.preview({
        "type": 'markdown',
        "data": formatted_text
    })
