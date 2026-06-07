"""数据管理模块 - 处理数据的保存和加载，支持CSV格式的本地存储"""

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
        """从本地文件加载记录"""
        if os.path.exists(self.DEFAULT_DATA_FILE):
            try:
                df = pd.read_csv(self.DEFAULT_DATA_FILE)
                df['时间'] = pd.to_datetime(df['时间']).dt.strftime("%Y-%m-%d")
                df['金额'] = df['金额'].astype(float)
                return df
            except Exception as e:
                print(f"加载数据失败: {e}")
                return self._create_empty_dataframe()
        else:
            return self._create_empty_dataframe()
    
    def save_records(self, df: pd.DataFrame, file_path: Optional[str] = None) -> bool:
        """保存记录到本地文件"""
        target_path = file_path or self.DEFAULT_DATA_FILE
        try:
            Path(target_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(target_path, index=False, encoding='utf-8-sig')
            print(f"数据已保存到: {target_path}")
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def get_statistics(self, df: pd.DataFrame) -> dict:
        """获取统计信息"""
        if len(df) == 0:
            return {'总支出': 0.0, '平均消费': 0.0, '最大消费': 0.0, '最小消费': 0.0, '消费次数': 0, '分类统计': {}}
        
        return {
            '总支出': df['金额'].sum(),
            '平均消费': df['金额'].mean(),
            '最大消费': df['金额'].max(),
            '最小消费': df['金额'].min(),
            '消费次数': len(df),
            '分类统计': df.groupby('分类')['金额'].agg(['sum', 'count']).to_dict()
        }
    
    def filter_by_category(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """按分类过滤记录"""
        return df[df['分类'] == category].reset_index(drop=True)
    
    def get_categories(self, df: pd.DataFrame) -> list:
        """获取所有分类"""
        return df['分类'].unique().tolist() if len(df) > 0 else []
    
    @staticmethod
    def _create_empty_dataframe() -> pd.DataFrame:
        """创建空的DataFrame"""
        return pd.DataFrame(columns=['时间', '金额', '分类', '备注'])
