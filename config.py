"""
记账小程序 - 项目配置文件
"""

# ========== 应用配置 ==========
APP_NAME = "记账小程序"
APP_VERSION = "1.0.0"
APP_AUTHOR = "AI Assistant"

# ========== 窗口配置 ==========
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# ========== 数据配置 ==========
DEFAULT_CATEGORIES = ['餐饮', '购物', '交通', '娱乐', '医疗', '学习', '其他']
CURRENCY_SYMBOL = '¥'
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ========== OCR配置 ==========
OCR_ENABLED = True
OCR_LANGUAGE = 'ch'  # 中文
OCR_USE_GPU = False  # 是否使用GPU加速

# ========== 商户分类映射 ==========
MERCHANT_CATEGORY_MAP = {
    '餐饮': [
        '美团', '饿了么', '餐厅', '咖啡', '奶茶', '烧烤', '日料', '川菜', '面馆',
        '馆', '食', '餐', '外卖', '点餐', '团购', '麦当劳', '肯德基'
    ],
    '购物': [
        '淘宝', '天猫', '京东', '拼多多', '苏宁', '唯品会', '商城', '店', '超市',
        '便利店', '卖场', '商店', '百货', '品牌', 'MALL'
    ],
    '交通': [
        '滴滴', '高德', '携程', '飞猪', '火车', '飞机', '汽车', '地铁', '公交',
        '出租', '网约', '车', '票', '站', '机场', '站点'
    ],
    '娱乐': [
        '电影', '游戏', '音乐', '抖音', '爱奇艺', 'spotify', '网易', '电玩',
        '健身', '游泳', '影院', '演唱会', '演出', 'KTV'
    ],
    '医疗': [
        '医院', '药房', '诊所', '医药', '医疗', '口腔', '眼镜', '挂号',
        '体检', '保健', '按摩', '医生'
    ],
    '学习': [
        '课程', '学习', '教育', '培训', '在线课', '网课', '书', '图书',
        '学校', '大学', '班', '考试', '补习'
    ],
}

# ========== 金额识别模式 ==========
AMOUNT_PATTERNS = [
    r'¥\s*([\d,]+\.?\d*)',
    r'RMB\s*([\d,]+\.?\d*)',
    r'人民币\s*([\d,]+\.?\d*)',
    r'([\d,]+\.?\d*)\s*元',
    r'￥\s*([\d,]+\.?\d*)',
]

# ========== 时间识别模式 ==========
TIME_PATTERNS = [
    r'(\d{4}[-/]\d{2}[-/]\d{2})\s+(\d{2}:\d{2})',
    r'(\d{2}月\d{2}日)\s+(\d{2}:\d{2})',
    r'(\d{4}年\d{2}月\d{2}日)',
]

# ========== 本地存储配置 ==========
STORAGE_DIR = ".expense_tracker_data"
AUTO_BACKUP = True
BACKUP_INTERVAL = 10  # 每10条记录自动备份一次

# ========== UI配置 ==========
THEME = "clam"  # 可选: clam, alt, default, classic
FONT_SIZE = 10
FONT_FAMILY = "TkDefaultFont"

# ========== 日志配置 ==========
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "expense_tracker.log"
