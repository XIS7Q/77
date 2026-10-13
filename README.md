# 记账小程序

这是一个功能完整的个人记账应用程序，支持Web版和桌面版两种使用方式。

快速开始

Web版 

直接访问: [https://xis7q.github.io/77/](https://xis7q.github.io/77/)



 桌面版 

```bash
# 1. 克隆仓库
git clone https://github.com/XIS7Q/77.git
cd 77

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行程序
python main.py
```

 主要功能

 基础功能
-  手动记账 - 输入消费金额、时间、类别、备注
-  查看记录 - 表格展示所有记账记录
-  数据保存 - 自动保存数据到本地/浏览器
-  数据加载 - 启动时自动加载历史记录

高级功能
-  统计分析 - 生成消费报表和图表
-  导出功能 - 导出为CSV文件
-  数据管理 - 删除、编辑记录
-  响应式设计 - 完美适配手机、平板、电脑

 功能详解

 Web版特点
-  无需安装，打开即用
-  数据存储在浏览器本地
-  完全手机适配
-  完全离线可用

### 桌面版特点
- 🖥️ 功能最全面
- 📷 OCR识别支付截图
- 📈 高级数据可视化
- 💾 本地文件存储

 使用指南

 Web版使用步骤

1. 打开网站
   ```
   https://xis7q.github.io/77/
   ```

2. 添加记录
   - 选择日期
   - 输入金额
   - 选择分类（餐饮、购物、交通等）
   - 添加备注（可选）
   - 点击"添加记录"

3. 查看统计
   - 点击" 统计分析"
   - 查看分类消费占比
   - 查看详细统计数据

4. 导出数据
   - 点击" 导出数据"
   - 自动下载CSV文件

 桌面版使用步骤

1. 安装Python (3.8+)

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序
   ```bash
   python main.py
   ```

4. *使用OCR识别*
   - 点击" 上传截图"
   - 选择支付宝或微信支付截图
   - 自动识别金额和分类

##  项目结构

```
.
├── index.html                 # Web版主页面
├── main.py                    # 桌面版入口
├── config.py                  # 配置文件
├── requirements.txt           # Python依赖
├── README.md                  # 项目文档
└── utils/
    ├── __init__.py
    ├── ocr_handler.py        # OCR识别模块
    ├── data_manager.py       # 数据管理模块
    └── visualization.py      # 可视化模块
```

##  配置说明

编辑 `config.py` 可自定义：

```python
# 消费分类
DEFAULT_CATEGORIES = ['餐饮', '购物', '交通', '娱乐', '医疗', '学习', '其他']

# 商户自动分类规则
MERCHANT_CATEGORY_MAP = {
    '餐饮': ['美团', '饿了么', '餐厅', ...],
    '购物': ['淘宝', '天猫', '京东', ...],
    ...
}
```

##  数据存储

 Web版
- 存储位置：浏览器 localStorage
- 自动保存：每次添加记录时自动保存
- 导出方式：点击导出按钮下载CSV

 桌面版
- 存储位置：`~/.expense_tracker/records.csv`
- 自动备份：`~/.expense_tracker/backups/`
- 导出方式：通过菜单导出CSV

## 🐛 常见问题

### Q: Web版数据会不会丢失？
A: Web版数据存储在浏览器localStorage中，清除浏览器缓存会删除数据。建议定期导出备份。

 Q: 如何在多设备间同步数据？
A: 
- 从一个设备导出CSV
- 在另一个设备打开��站
- 通过表格导入功能导入CSV

 Q: 桌面版如何安装PaddleOCR？
A: 
```bash
pip install paddleocr opencv-python
# 首次运行时会自动下载OCR模型（约200MB）
```

### Q: 识别截图不准确怎么办？
A: 
- 确保截图清晰完整
- 在 `config.py` 中调整识别规则
- 手动修改识别结果后保存

## 🎨 界面预览

### Web版界面
- 清爽的绿色主题
- 响应式卡片布局
- 实时数据统计
- 交互式图表

### 桌面版界面
- 现代化Tkinter界面
- 完整的数据表格
- 详细的统计图表
- 丰富的菜单功能

## 📈 数据统计

程序自动计算：
- 总消费金额
- 平均消费
- 最大/最小消费
- 按分类统计
- 按日期统计
- 月度汇总

##  数据安全

- 所有数据本地存储
- 不上传到云服务器
- 支持本地备份
- 支持CSV导出

##  后续功能规划

- [ ] 云同步功能
- [ ] 预算提醒
- [ ] 智能分析报告
- [ ] 移动端App
- [ ] 多用户支持
- [ ] 标签系统

## 📝 开发过程

### 第一阶段：基础功能
- [x] Tkinter GUI界面
- [x] 手动记账
- [x] 数据保存/加载
- [x] 表格显示

### 第二阶段：高级功能
- [x] OCR识别
- [x] 数据统计
- [x] 图表可视化
- [x] CSV导出

### 第三阶段：Web版
- [x] HTML/CSS/JS实现
- [x] 响应式设计
- [x] 本地存储
- [x] GitHub Pages部署

##  贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

##  许可证

MIT License - 详见 LICENSE 文件

##  联系方式

- 项目主页：[GitHub](https://github.com/XIS7Q/77)
- 提交问题：[Issues](https://github.com/XIS7Q/77/issues)
- Web版地址：[https://xis7q.github.io/77/](https://xis7q.github.io/77/)
