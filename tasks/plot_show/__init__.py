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
    """设置柔和的主题配色，适合暗色和亮色背景"""
    # 使用柔和的颜色配置
    plt.rcParams.update({
        # 图表背景
        'figure.facecolor': '#ffffff',  # 纯白色背景
        'axes.facecolor': '#ffffff',    # 纯白色图表区域
        
        # 高清显示设置
        'figure.dpi': 200,              # 进一步提高显示DPI
        'savefig.dpi': 400,             # 超高清保存DPI
        'figure.figsize': (16, 10),     # 进一步增大图表尺寸
        
        # 网格线配置
        'axes.grid': True,
        'grid.color': '#e1e4e8',        # 更浅的灰色网格
        'grid.alpha': 0.8,
        'grid.linewidth': 0.8,          # 稍微加粗网格线
        
        # 坐标轴 - 使用深色确保可见
        'axes.edgecolor': '#1f2328',    # 深灰色边框
        'axes.linewidth': 1.5,          # 加粗坐标轴线
        'axes.labelcolor': '#1f2328',   # 深色标签，确保可见
        'axes.titlecolor': '#1f2328',   # 深色标题
        
        # 刻度 - 使用深色确保可见
        'xtick.color': '#1f2328',       # 深色刻度
        'ytick.color': '#1f2328',
        'xtick.labelsize': 14,          # 增大刻度字体
        'ytick.labelsize': 14,
        'xtick.major.width': 1.2,       # 加粗刻度线
        'ytick.major.width': 1.2,
        'xtick.major.size': 6,          # 增大刻度长度
        'ytick.major.size': 6,
        
        # 线条样式 - 使用对比度高的颜色
        'lines.linewidth': 2.0,         # 加粗线条
        'axes.prop_cycle': plt.cycler('color', [
            '#0969da',  # 蓝色 (主线)
            '#d1242f',  # 红色 (卖出)
            '#1a7f37',  # 绿色 (买入)
            '#8250df',  # 紫色
            '#bc4c00',  # 橙色
            '#656d76',  # 灰色
        ]),
        
        # 字体 - 增大字体并使用深色
        'font.size': 14,                # 增大基础字体
        'font.weight': 'normal',        # 正常字重
        'axes.titlesize': 18,           # 增大标题字体
        'axes.labelsize': 16,           # 增大轴标签字体
        'legend.fontsize': 14,          # 增大图例字体
        'text.color': '#1f2328',        # 深色文字
        
        # 图例 - 确保可见
        'legend.frameon': True,
        'legend.facecolor': '#ffffff',
        'legend.edgecolor': '#d0d7de',
        'legend.framealpha': 1.0,       # 完全不透明
        'legend.shadow': True,          # 添加阴影增强可见度
        
        # 整体样式
        'figure.autolayout': True,
        'savefig.bbox': 'tight',
        'savefig.facecolor': '#ffffff',
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
    
    # 使用高清参数绘制图表
    figs = cerebro.plot(style='candlestick', 
                       barup='#1a7f37', bardown='#cf222e',
                       volup='#1a7f37', voldown='#cf222e',
                       figsize=(16, 10),      # 大尺寸图表
                       iplot=False,           # 确保使用matplotlib后端
                       volume=True,           # 显示成交量
                       zdown=False)           # 优化显示效果
    
    # 进一步优化图表显示
    if figs:
        for fig in figs:
            # 设置高DPI
            fig.set_dpi(200)
            # 调整子图间距
            fig.subplots_adjust(hspace=0.3, wspace=0.1)
            # 优化显示
            fig.tight_layout()
    
    return {'cerebro': cerebro}
