"""
记账小程序 - 主程序入口
功能包括：手动记账、OCR识别、数据保存/加载、统计可视化
作者：AI Assistant
日期：2026-06-07
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime
import os
import csv
from pathlib import Path

# 导入自定义模块
from utils.ocr_handler import OCRHandler
from utils.data_manager import DataManager
from utils.visualization import VisualizationManager

class ExpenseTrackerApp:
    """记账应用主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("记账小程序")
        self.root.geometry("900x600")
        
        # 初始化数据管理器
        self.data_manager = DataManager()
        self.records = self.data_manager.load_records()
        
        # 初始化OCR处理器
        self.ocr_handler = OCRHandler()
        
        # 初始化可视化管理器
        self.viz_manager = VisualizationManager()
        
        # 样式设置
        style = ttk.Style()
        style.theme_use("clam")
        
        # 构建UI
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        
        # ========== 顶部输入区域 ==========
        input_frame = ttk.LabelFrame(self.root, text="添加消费记录", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 时间输入
        ttk.Label(input_frame, text="时间 (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # 时间快速选择
        ttk.Button(input_frame, text="今天", command=lambda: self.date_entry.delete(0, tk.END) or 
                   self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))).grid(row=0, column=2, padx=5, pady=5)
        
        # 金额输入
        ttk.Label(input_frame, text="金额 (¥):").grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        
        # 分类选择
        ttk.Label(input_frame, text="分类:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ['餐饮', '购物', '交通', '娱乐', '医疗', '学习', '其他']
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, 
                                            values=categories, width=15, state='readonly')
        self.category_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.category_combo.set('其他')
        
        # 备注输入
        ttk.Label(input_frame, text="备注:").grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.note_entry = ttk.Entry(input_frame, width=30)
        self.note_entry.grid(row=1, column=4, sticky=tk.W, padx=5, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=5, pady=10)
        
        ttk.Button(button_frame, text="✓ 添加记录", command=self.add_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📷 上传截图", command=self.upload_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 统计图表", command=self.show_statistics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 保存数据", command=self.save_records).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 加载数据", command=self.load_records).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📥 导出CSV", command=self.export_csv).pack(side=tk.LEFT, padx=5)
        
        # ========== 表格显示区域 ==========
        table_frame = ttk.LabelFrame(self.root, text="消费记录", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建Treeview表格
        columns = ('时间', '金额', '分类', '备注')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # 定义列
        self.tree.column('时间', width=120, anchor=tk.CENTER)
        self.tree.column('金额', width=100, anchor=tk.CENTER)
        self.tree.column('分类', width=100, anchor=tk.CENTER)
        self.tree.column('备注', width=300, anchor=tk.W)
        
        self.tree.heading('时间', text='时间')
        self.tree.heading('金额', text='金额 (¥)')
        self.tree.heading('分类', text='分类')
        self.tree.heading('备注', text='备注')
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右键菜单 - 删除记录
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # 初始加载记录到表格
        self.refresh_table()
        
        # ========== 底部状态栏 ==========
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text=f"已加载 {len(self.records)} 条记录")
        self.status_label.pack(side=tk.LEFT)
        
    def add_record(self):
        """添加新的消费记录"""
        date = self.date_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_var.get()
        note = self.note_entry.get().strip()
        
        # 校验输入
        if not date or not amount or not category:
            messagebox.showerror("错误", "请填写日期、金额和分类！")
            return
        
        # 验证日期格式
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("错误", "日期格式错误！请使用 YYYY-MM-DD 格式")
            return
        
        # 验证金额格式
        try:
            float(amount)
        except ValueError:
            messagebox.showerror("错误", "金额必须为数字！")
            return
        
        # 添加记录
        new_record = {
            '时间': date,
            '金额': float(amount),
            '分类': category,
            '备注': note
        }
        
        self.records = pd.concat([self.records, pd.DataFrame([new_record])], ignore_index=True)
        self.refresh_table()
        
        # 清空输入框
        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        
        messagebox.showinfo("成功", "记录已添加！")
        
    def upload_screenshot(self):
        """上传截图并识别"""
        file_path = filedialog.askopenfilename(
            title="选择支付截图",
            filetypes=[("图像文件", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if not file_path:
            return
        
        try:
            messagebox.showinfo("提示", "正在识别，请稍候...")
            result = self.ocr_handler.process_screenshot(file_path)
            
            if result:
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, result['时间'])
                
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, str(result['金额']))
                
                self.category_var.set(result['分类'])
                
                self.note_entry.delete(0, tk.END)
                self.note_entry.insert(0, result['备注'])
                
                messagebox.showinfo("识别成功", 
                    f"金额: ¥{result['金额']}\n分类: {result['分类']}\n描述: {result['备注']}")
            else:
                messagebox.showerror("识别失败", "无法识别图片中的支付信息")
                
        except Exception as e:
            messagebox.showerror("错误", f"处理图片时出错: {str(e)}")
    
    def show_statistics(self):
        """显示统计图表"""
        if len(self.records) == 0:
            messagebox.showwarning("提示", "没有可统计的数据")
            return
        
        try:
            self.viz_manager.show_statistics(self.records)
        except Exception as e:
            messagebox.showerror("错误", f"生成图表失败: {str(e)}")
    
    def save_records(self):
        """保存记录到本地文件"""
        self.data_manager.save_records(self.records)
        messagebox.showinfo("成功", "数据已自动保存到本地！")
    
    def load_records(self):
        """从文件加载记录"""
        file_path = filedialog.askopenfilename(
            title="选择CSV文件",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                self.records = pd.read_csv(file_path)
                self.refresh_table()
                messagebox.showinfo("成功", f"已加载 {len(self.records)} 条记录！")
            except Exception as e:
                messagebox.showerror("错误", f"加载失败: {str(e)}")
    
    def export_csv(self):
        """导出数据为CSV文件"""
        if len(self.records) == 0:
            messagebox.showwarning("提示", "没有数据可导出")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                self.records.to_csv(file_path, index=False, encoding='utf-8-sig')
                messagebox.showinfo("成功", f"已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def refresh_table(self):
        """刷新表格显示"""
        # 清除现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新数据
        for idx, row in self.records.iterrows():
            self.tree.insert('', 'end', values=(
                row['时间'],
                f"¥{row['金额']:.2f}",
                row['分类'],
                row['备注']
            ))
        
        # 更新状态栏
        total = self.records['金额'].sum() if len(self.records) > 0 else 0
        self.status_label.config(
            text=f"已加载 {len(self.records)} 条记录 | 总支出: ¥{total:.2f}"
        )
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.tree.selection()
        if not item:
            return
        
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="删除此记录", 
                        command=lambda: self.delete_record(item[0]))
        menu.post(event.x_global, event.y_global)
    
    def delete_record(self, item):
        """删除选中的记录"""
        idx = self.tree.index(item)
        self.records = self.records.drop(idx).reset_index(drop=True)
        self.refresh_table()
        messagebox.showinfo("成功", "记录已删除！")


def main():
    """主程序入口"""
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
