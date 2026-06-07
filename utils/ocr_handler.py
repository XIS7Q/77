"""
OCR 处理模块 - 用于识别支付截图
支持支付宝、微信支付等截图识别
"""

from paddleocr import PaddleOCR
import cv2
import re
from datetime import datetime
from typing import Dict, Optional

class OCRHandler:
    """OCR处理器"""
    
    def __init__(self):
        """初始化OCR引擎"""
        try:
            self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=False)
        except Exception as e:
            print(f"OCR初始化失败: {e}")
            self.ocr = None
    
    def process_screenshot(self, image_path: str) -> Optional[Dict]:
        """
        处理截图并提取支付信息
        
        Args:
            image_path: 图片路径
        
        Returns:
            包含时间、金额、分类、备注的字典，或None
        """
        if self.ocr is None:
            return None
        
        try:
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # 执行OCR识别
            result = self.ocr.ocr(image, cls=True)
            
            if not result or not result[0]:
                return None
            
            # 提取文本
            extracted_texts = [line[1][0] for line in result[0] if line[1]]
            extracted_text = '\n'.join(extracted_texts)
            
            # 解析信息
            return self._parse_payment_info(extracted_text)
            
        except Exception as e:
            print(f"OCR处理失败: {e}")
            return None
    
    def _parse_payment_info(self, text: str) -> Dict:
        """
        解析支付信息
        
        Args:
            text: OCR识别的文本
        
        Returns:
            包含时间、金额、分类、备注的字典
        """
        result = {
            '时间': datetime.now().strftime("%Y-%m-%d"),
            '金额': 0.0,
            '分类': '其他',
            '备注': ''
        }
        
        # 提取金额 (支持 ¥ 和 RMB 格式)
        amount_patterns = [
            r'¥\s*([\d,]+\.?\d*)',
            r'RMB\s*([\d,]+\.?\d*)',
            r'人民币\s*([\d,]+\.?\d*)',
            r'([\d,]+\.?\d*)\s*元',
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, text)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    result['金额'] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        # 提取时间
        time_patterns = [
            r'(\d{4}[-/]\d{2}[-/]\d{2})\s+(\d{2}:\d{2})',  # YYYY-MM-DD HH:MM
            r'(\d{2}月\d{2}日)\s+(\d{2}:\d{2})',  # MM月DD日 HH:MM
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                time_str = match.group(0)
                # 尝试解析时间
                try:
                    if '月' in time_str:
                        # 相对日期，需要补充年份
                        year = datetime.now().year
                        time_str = f"{year}-{time_str.replace('月', '-').replace('日', ' ')}"
                    dt = datetime.strptime(time_str.split()[0], "%Y-%m-%d")
                    result['时间'] = dt.strftime("%Y-%m-%d")
                except:
                    pass
                break
        
        # 分类识别 (基于商户名称)
        category_keywords = {
            '餐饮': ['美团', '饿了么', '餐厅', '咖啡', '奶茶', '烧烤', '日料', '川菜', '面馆', '馆', '食'],
            '购物': ['淘宝', '天猫', '京东', '拼多多', '苏宁', '唯品会', '商城', '店', '超市'],
            '交通': ['滴滴', '高德', '携程', '飞猪', '火车', '飞机', '汽车', '地铁', '公交'],
            '娱乐': ['电影', '游戏', '音乐', '抖音', '爱奇艺', 'spotify', '网易', '电玩'],
            '医疗': ['医院', '药房', '诊所', '医药', '医疗'],
            '学习': ['课程', '学习', '教育', '培训', '在线课', '网课'],
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    result['分类'] = category
                    result['备注'] = keyword
                    return result
        
        # 提取商户名称作为备注
        merchant_patterns = [
            r'([^\s\n¥￥RMB人民币]{2,20})\s*(?:¥|RMB|人民币)',
            r'(?:服务商|商户|收款方)[:：]\s*([^\s\n]+)',
        ]
        
        for pattern in merchant_patterns:
            match = re.search(pattern, text)
            if match:
                result['备注'] = match.group(1).strip()
                break
        
        return result


# 测试代码
if __name__ == "__main__":
    handler = OCRHandler()
    # 这里可以添加测试代码
    print("OCR模块已加载")
