"""可视化模块 - 生成统计图表"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.dates as mdates
from datetime import datetime

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

class VisualizationManager:
    """可视化管理器"""
    
    def __init__(self):
        """初始化可视化管理器"""
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def show_statistics(self, df: pd.DataFrame):
        """显示统计图表"""
        if len(df) == 0:
            print("没有数据可显示")
            return
        
        # 创建图表
        fig = plt.figure(figsize=(15, 10))
        fig.suptitle('记账小程序 - 消费统计', fontsize=16, fontweight='bold')
        
        # 分类统计饼图
        ax1 = plt.subplot(2, 2, 1)
        category_sum = df.groupby('分类')['金额'].sum()
        colors = plt.cm.Set3(range(len(category_sum)))
        ax1.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('按分类统计消费占比')
        
        # 分类柱状图
        ax2 = plt.subplot(2, 2, 2)
        category_sum.plot(kind='bar', ax=ax2, color=colors)
        ax2.set_title('各分类消费金额')
        ax2.set_ylabel('消费金额 (¥)')
        ax2.set_xlabel('消费分类')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 时间序列趋势
        ax3 = plt.subplot(2, 2, 3)
        df_sorted = df.sort_values('时间')
        df_sorted['时间'] = pd.to_datetime(df_sorted['时间'])
        daily_sum = df_sorted.groupby('时间')['金额'].sum()
        ax3.plot(daily_sum.index, daily_sum.values, marker='o', linestyle='-', linewidth=2, markersize=6)
        ax3.set_title('每日消费趋势')
        ax3.set_ylabel('消费金额 (¥)')
        ax3.set_xlabel('日期')
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # 统计信息表格
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        
        total = df['金额'].sum()
        avg = df['金额'].mean()
        max_amount = df['金额'].max()
        min_amount = df['金额'].min()
        count = len(df)
        
        stats_text = f"""
        统计信息:
        ━━━━━━━━━━━━━━━━
        总消费: ¥{total:.2f}
        平均消费: ¥{avg:.2f}
        最大消费: ¥{max_amount:.2f}
        最小消费: ¥{min_amount:.2f}
        记录数: {count}
        """
        
        ax4.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()
    
    def show_category_detail(self, df: pd.DataFrame):
        """显示分类详细信息"""
        if len(df) == 0:
            print("没有数据可显示")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        category_stats = df.groupby('分类').agg({'金额': ['sum', 'count', 'mean']})
        category_stats.columns = ['总额', '次数', '平均']
        category_stats = category_stats.sort_values('总额', ascending=False)
        
        x = range(len(category_stats))
        ax.bar(x, category_stats['总额'], label='总额')
        ax.set_xticks(x)
        ax.set_xticklabels(category_stats.index, rotation=45, ha='right')
        ax.set_ylabel('金额 (¥)')
        ax.set_title('分类消费详细统计')
        ax.legend()
        
        plt.tight_layout()
        plt.show()
    
    def show_monthly_trend(self, df: pd.DataFrame):
        """显示月度消费趋势"""
        if len(df) == 0:
            print("没有数据可显示")
            return
        
        df_copy = df.copy()
        df_copy['时间'] = pd.to_datetime(df_copy['时间'])
        df_copy['年月'] = df_copy['时间'].dt.to_period('M')
        
        monthly_sum = df_copy.groupby('年月')['金额'].sum()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_sum.plot(kind='line', ax=ax, marker='o', linewidth=2, markersize=8)
        ax.set_title('月度消费趋势')
        ax.set_ylabel('月度总消费 (¥)')
        ax.set_xlabel('年月')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
