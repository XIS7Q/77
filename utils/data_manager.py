"""
数据管理模块 - 处理数据的保存和加载
支持CSV格式的本地存储
"""

import pandas as pd
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

class DataManager:
    """数据管理器"""
    
    # 默认数据文件位置
    DEFAULT_DATA_DIR = os.path.expanduser("~/.expense_tracker")
    DEFAULT_DATA_FILE = os.path.join(DEFAULT_DATA_DIR, "records.csv")
    
    def __init__(self):
        """初始化数据管理器"""
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        Path(self.DEFAULT_DATA_DIR).mkdir(parents=True, exist_ok=True)
    
    def load_records(self) -> pd.DataFrame:
        """
        从本地文件加载记录
        
        Returns:
            包含所有记录的DataFrame
        """
        if os.path.exists(self.DEFAULT_DATA_FILE):
            try:
                df = pd.read_csv(self.DEFAULT_DATA_FILE)
                # 确保数据类型正确
                df['时间'] = pd.to_datetime(df['时间']).dt.strftime("%Y-%m-%d")
                df['金额'] = df['金额'].astype(float)
                return df
            except Exception as e:
                print(f"加载数据失败: {e}")
                return self._create_empty_dataframe()
        else:
            return self._create_empty_dataframe()
    
    def save_records(self, df: pd.DataFrame, file_path: Optional[str] = None) -> bool:
        """
        保存记录到本地文件
        
        Args:
            df: 要保存的DataFrame
            file_path: 自定义保存路径，为None时使用默认路径
        
        Returns:
            是否保存成功
        """
        target_path = file_path or self.DEFAULT_DATA_FILE
        
        try:
            # 确保父目录存在
            Path(target_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存到CSV
            df.to_csv(target_path, index=False, encoding='utf-8-sig')
            print(f"数据已保存到: {target_path}")
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def export_records(self, df: pd.DataFrame, file_path: str) -> bool:
        """
        导出记录到指定路径
        
        Args:
            df: 要导出的DataFrame
            file_path: 导出路径
        
        Returns:
            是否导出成功
        """
        return self.save_records(df, file_path)
    
    def get_statistics(self, df: pd.DataFrame) -> dict:
        """
        获取统计信息
        
        Args:
            df: 数据DataFrame
        
        Returns:
            包含统计信息的字典
        """
        if len(df) == 0:
            return {
                '总支出': 0.0,
                '平均消费': 0.0,
                '最大消费': 0.0,
                '最小消费': 0.0,
                '消费次数': 0,
                '分类统计': {}
            }
        
        stats = {
            '总支出': df['金额'].sum(),
            '平均消费': df['金额'].mean(),
            '最大消费': df['金额'].max(),
            '最小消费': df['金额'].min(),
            '消费次数': len(df),
            '分类统计': df.groupby('分类')['金额'].agg(['sum', 'count']).to_dict()
        }
        
        return stats
    
    def filter_by_date_range(self, df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """
        按日期范围过滤记录
        
        Args:
            df: 原始DataFrame
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
        
        Returns:
            过滤后的DataFrame
        """
        try:
            df_copy = df.copy()
            df_copy['时间'] = pd.to_datetime(df_copy['时间'])
            mask = (df_copy['时间'] >= start_date) & (df_copy['时间'] <= end_date)
            result = df_copy[mask].copy()
            result['时间'] = result['时间'].dt.strftime("%Y-%m-%d")
            return result
        except Exception as e:
            print(f"日期过滤失败: {e}")
            return df
    
    def filter_by_category(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """
        按分类过滤记录
        
        Args:
            df: 原始DataFrame
            category: 分类名称
        
        Returns:
            过滤后的DataFrame
        """
        return df[df['分类'] == category].reset_index(drop=True)
    
    def get_categories(self, df: pd.DataFrame) -> list:
        """
        获取所有分类
        
        Args:
            df: 数据DataFrame
        
        Returns:
            分类列表
        """
        return df['分类'].unique().tolist() if len(df) > 0 else []
    
    def get_monthly_summary(self, df: pd.DataFrame, year: int, month: int) -> dict:
        """
        获取某月的消费汇总
        
        Args:
            df: 数据DataFrame
            year: 年份
            month: 月份 (1-12)
        
        Returns:
            包含月度汇总信息的字典
        """
        df_copy = df.copy()
        df_copy['时间'] = pd.to_datetime(df_copy['时间'])
        
        mask = (df_copy['时间'].dt.year == year) & (df_copy['时间'].dt.month == month)
        monthly_data = df_copy[mask]
        
        if len(monthly_data) == 0:
            return {
                '年月': f"{year}-{month:02d}",
                '总支出': 0.0,
                '记录数': 0,
                '分类汇总': {}
            }
        
        return {
            '年月': f"{year}-{month:02d}",
            '总支出': monthly_data['金额'].sum(),
            '记录数': len(monthly_data),
            '分类汇总': monthly_data.groupby('分类')['金额'].sum().to_dict(),
            '日均支出': monthly_data['金额'].mean()
        }
    
    @staticmethod
    def _create_empty_dataframe() -> pd.DataFrame:
        """
        创建空的DataFrame
        
        Returns:
            空DataFrame
        """
        return pd.DataFrame(columns=['时间', '金额', '分类', '备注'])
    
    def backup_records(self, df: pd.DataFrame) -> bool:
        """
        备份记录到带时间戳的文件
        
        Args:
            df: 要备份的DataFrame
        
        Returns:
            是否备份成功
        """
        backup_dir = os.path.join(self.DEFAULT_DATA_DIR, "backups")
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"records_backup_{timestamp}.csv")
        
        return self.save_records(df, backup_file)


# 测试代码
if __name__ == "__main__":
    manager = DataManager()
    records = manager.load_records()
    print(f"已加载 {len(records)} 条记录")
    print("数据管理模块已加载")
