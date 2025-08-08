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
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle


def setup_gentle_theme():
    """设置 Solarized Light 主题配色"""
    # Solarized Light 颜色方案
    plt.rcParams.update({
        # 图表背景 - Solarized Light
        'figure.facecolor': '#fdf6e3',  # Solarized base3 (背景)
        'axes.facecolor': '#fdf6e3',    # Solarized base3 (图表区域)
        
        # 高清显示设置
        'figure.dpi': 200,              # 进一步提高显示DPI
        'savefig.dpi': 400,             # 超高清保存DPI
        'figure.figsize': (12, 8),      # 调整为稍小的图表尺寸
        
        # 网格线配置 - Solarized
        'axes.grid': True,
        'grid.color': '#eee8d5',        # Solarized base2 (浅色网格)
        'grid.alpha': 0.8,
        'grid.linewidth': 0.8,
        
        # 坐标轴 - Solarized
        'axes.edgecolor': '#93a1a1',    # Solarized base1 (边框)
        'axes.linewidth': 1.5,
        'axes.labelcolor': '#586e75',   # Solarized base01 (标签)
        'axes.titlecolor': '#073642',   # Solarized base02 (标题)
        
        # 刻度 - Solarized
        'xtick.color': '#586e75',       # Solarized base01 (刻度)
        'ytick.color': '#586e75',
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
        'xtick.major.width': 1.2,
        'ytick.major.width': 1.2,
        'xtick.major.size': 6,
        'ytick.major.size': 6,
        
        # 线条样式 - Solarized 强调色 + 通用红绿色
        'lines.linewidth': 2.0,
        'axes.prop_cycle': plt.cycler('color', [
            '#268bd2',  # Solarized blue (主线)
            '#ef4444',  # 柔和通用红色 (下跌/卖出)
            '#22c55e',  # 柔和通用绿色 (上涨/买入)
            '#d33682',  # Solarized magenta
            '#cb4b16',  # Solarized orange
            '#b58900',  # Solarized yellow
            '#2aa198',  # Solarized cyan
            '#6c71c4',  # Solarized violet
        ]),
        
        # 字体 - Solarized
        'font.size': 14,
        'font.weight': 'normal',
        'axes.titlesize': 18,
        'axes.labelsize': 16,
        'legend.fontsize': 14,
        'text.color': '#073642',        # Solarized base02 (深色文字)
        
        # 图例 - Solarized
        'legend.frameon': True,
        'legend.facecolor': '#fdf6e3',  # Solarized base3 (背景)
        'legend.edgecolor': '#93a1a1',  # Solarized base1 (边框)
        'legend.framealpha': 1.0,
        'legend.shadow': True,
        
        # 整体样式
        'figure.autolayout': True,
        'savefig.bbox': 'tight',
        'savefig.facecolor': '#fdf6e3',  # Solarized base3
        'savefig.format': 'png',
        'savefig.transparent': False,
    })


def main(params: Inputs, context: Context) -> Outputs:
    df = params['df']
    cerebro = params['cerebro']
    
    # 设置柔和主题
    setup_gentle_theme()
    
    data = bt.feeds.PandasData(dataname=df)  # 加载数据[1,6](@ref)
    cerebro.adddata(data)                # 添加数据源
    cerebro.run()  # 执行策略模拟[1,4](@ref)
    
    # 使用 Solarized Light 风格绘制图表
    figs = cerebro.plot(style='candlestick', 
                       barup='#22c55e', bardown='#ef4444',      # 柔和的通用绿色/红色
                       volup='#22c55e', voldown='#ef4444',      # 成交量对应颜色
                       figsize=(12, 8),                         # 适中尺寸图表
                       iplot=False,                             # 确保使用matplotlib后端
                       volume=True,                             # 显示成交量
                       zdown=False)                             # 优化显示效果
    
    # 进一步优化图表显示
    if figs:
        for fig_list in figs:
            if isinstance(fig_list, list):
                for fig in fig_list:
                    # 设置高DPI
                    fig.set_dpi(200)
                    # 调整子图间距
                    fig.subplots_adjust(hspace=0.3, wspace=0.1)
                    # 优化显示
                    fig.tight_layout()
            else:
                # 如果直接是图表对象
                fig_list.set_dpi(200)
                fig_list.subplots_adjust(hspace=0.3, wspace=0.1)
                fig_list.tight_layout()
    
    return {'cerebro': cerebro}
