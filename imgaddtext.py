#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片添加文字工具
功能：
1. 给图片添加文字
2. 支持多种免费字体
3. 可自定义颜色
4. 可自定义位置
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import argparse
from pathlib import Path
import glob
import re
import random

class ImageTextAdder:
    def __init__(self):
        self.fonts_dir = Path("fonts")
        self.available_fonts = self._get_available_fonts()
        
    def _get_available_fonts(self):
        """获取可用的字体列表"""
        fonts = {}
        
        # 创建fonts目录如果不存在
        self.fonts_dir.mkdir(exist_ok=True)
        
        # 优先尝试中文字体
        chinese_fonts = [
            ("bbhbold", "波波黑"),
            ("sanjixinkai", "三级行楷"),
            ("kmhaiou", "海鸥体"),
            ("slidexiaxing", "行楷"),
            ("simkai", "楷体"),
            ("simsun", "宋体"),
            ("simhei", "黑体"),
            ("simfang", "仿宋"),
            ("microsoft-yahei", "微软雅黑"),
            ("kaiti", "楷体"),
            ("fangsong", "仿宋"),
            ("heiti", "黑体"),
            ("songti", "宋体")
        ]
        
        # 尝试加载中文字体
        for font_key, font_name in chinese_fonts:
            try:
                font = ImageFont.truetype(font_key, 40)
                fonts[font_key] = font_name
            except:
                continue
        
        # 系统默认字体
        system_fonts = [
            ("arial", "Arial"),
            ("calibri", "Calibri"), 
            ("times", "Times New Roman"),
            ("verdana", "Verdana"),
            ("comic", "Comic Sans MS"),
            ("impact", "Impact"),
            ("trebuchet", "Trebuchet MS")
        ]
        
        # 尝试加载系统字体
        for font_key, font_name in system_fonts:
            try:
                font = ImageFont.truetype(font_key, 40)
                fonts[font_key] = font_name
            except:
                continue
                
        # 检查fonts目录中的字体文件
        font_files = list(self.fonts_dir.glob("*.ttf")) + list(self.fonts_dir.glob("*.otf"))
        for font_file in font_files:
            try:
                font_key = font_file.stem
                fonts[font_key] = font_key
            except:
                continue
                
        return fonts
    
    def parse_color(self, color_input):
        """解析颜色输入，支持多种格式"""
        if isinstance(color_input, str):
            # 处理命名颜色
            color_names = {
                'black': (0, 0, 0),
                'white': (255, 255, 255),
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'yellow': (255, 255, 0),
                'cyan': (0, 255, 255),
                'magenta': (255, 0, 255),
                'gray': (128, 128, 128),
                'orange': (255, 165, 0),
                'purple': (128, 0, 128),
                'pink': (255, 192, 203),
                'brown': (165, 42, 42),
                'lime': (0, 255, 0),
                'navy': (0, 0, 128),
                'teal': (0, 128, 128)
            }
            
            if color_input.lower() in color_names:
                return color_names[color_input.lower()]
            
            # 处理十六进制颜色
            if color_input.startswith('#'):
                hex_color = color_input.lstrip('#')
                if len(hex_color) == 6:
                    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # 处理RGB元组字符串，如 "255,0,0"
            if ',' in color_input:
                try:
                    rgb_values = [int(x.strip()) for x in color_input.split(',')]
                    if len(rgb_values) == 3 and all(0 <= x <= 255 for x in rgb_values):
                        return tuple(rgb_values)
                except ValueError:
                    pass
        
        # 如果输入已经是元组
        elif isinstance(color_input, (tuple, list)) and len(color_input) == 3:
            if all(0 <= x <= 255 for x in color_input):
                return tuple(color_input)
        
        # 默认返回黑色
        return (0, 0, 0)
    
    def get_font(self, font_name, font_size):
        """获取字体对象"""
        try:
            # 尝试从fonts目录加载
            font_path = self.fonts_dir / f"{font_name}.ttf"
            if font_path.exists():
                return ImageFont.truetype(str(font_path), font_size)
            
            font_path = self.fonts_dir / f"{font_name}.otf"
            if font_path.exists():
                return ImageFont.truetype(str(font_path), font_size)
            
            # 尝试系统字体
            return ImageFont.truetype(font_name, font_size)
        except:
            # 使用默认字体
            try:
                return ImageFont.truetype("arial.ttf", font_size)
            except:
                return ImageFont.load_default()
    
    def parse_position_and_size_from_filename(self, image_path):
        """从图片文件名解析位置和字体大小信息"""
        try:
            # 获取文件名（不含扩展名）
            filename = os.path.splitext(os.path.basename(image_path))[0]
            
            # 用 - 分割文件名
            parts = filename.split('-')
            
            # 检查是否有至少两部分
            if len(parts) < 2:
                return None, None
            
            # 第二部分应该包含位置信息
            position_part = parts[1]
            
            # 第三部分可能包含字体大小信息
            font_size = None
            if len(parts) >= 3:
                try:
                    font_size = int(parts[2].strip())
                except ValueError:
                    pass
            
            # 用 x 分割坐标
            if 'x' in position_part:
                coords = position_part.split('x')
                if len(coords) == 2:
                    x_part = coords[0].strip()
                    y_part = coords[1].strip()
                    
                    # 处理x坐标
                    try:
                        if x_part.lower() == 'center':
                            x = 'center'
                        else:
                            x = int(x_part)
                    except ValueError:
                        x = x_part  # 保留原始字符串，如 'vcenter'
                    
                    # 处理y坐标
                    try:
                        if y_part.lower() in ['center', 'vcenter']:
                            y = y_part.lower()
                        else:
                            y = int(y_part)
                    except ValueError:
                        y = y_part  # 保留原始字符串
                    
                    return (x, y), font_size
            
            return None, None
            
        except Exception:
            return None, None
    
    def parse_position(self, position_input, image_size, text_size, image_path=None):
        """解析位置输入，支持多种格式"""
        img_width, img_height = image_size
        text_width, text_height = text_size
        
        if isinstance(position_input, str):
            position = position_input.lower()
            
            # 预定义位置 - 所有位置都是文字区域top的坐标
            positions = {
                'top-left': (10, 10),  # 文字区域top距离顶部10像素
                'top-center': ((img_width - text_width) // 2, 10),  # 水平居中，top距离顶部10像素
                'top-right': (img_width - text_width - 10, 10),  # 右上角，top距离顶部10像素
                'center-left': (10, (img_height - text_height) // 2),  # 垂直居中，左对齐
                'center': ((img_width - text_width) // 2, (img_height - text_height) // 2),  # 完全居中
                'center-right': (img_width - text_width - 10, (img_height - text_height) // 2),  # 垂直居中，右对齐
                'bottom-left': (10, img_height - text_height - 10),  # 左下角
                'bottom-center': ((img_width - text_width) // 2, img_height - text_height - 10),  # 底部居中
                'bottom-right': (img_width - text_width - 10, img_height - text_height - 10),  # 右下角
                'vcenter': ((img_width - text_width) // 2, (img_height - text_height) // 2)  # 垂直居中，水平居中
            }
            
            if position in positions:
                return positions[position]
            
            # 处理坐标字符串，如 "100,200" 或 "100,vcenter"
            if ',' in position:
                try:
                    parts = [x.strip() for x in position.split(',')]
                    if len(parts) == 2:
                        x_pos = parts[0]
                        y_pos = parts[1]
                        
                        # 处理x坐标
                        if x_pos.lower() == 'center':
                            x = (img_width - text_width) // 2
                        else:
                            x = int(x_pos)
                        
                        # 处理y坐标
                        if y_pos.lower() == 'vcenter':
                            # vcenter: 整个文字区域在图片垂直中心
                            # 计算文字区域top位置 = (图片高度 - 文字高度) / 2
                            y = (img_height - text_height) // 2
                        elif y_pos.lower() == 'center':
                            # center: 整个文字区域在图片垂直中心
                            y = (img_height - text_height) // 2
                        else:
                            # 具体数字: 文字区域top距离图片顶部的距离
                            y = int(y_pos)
                        
                        return (x, y)
                except ValueError:
                    pass
        
        # 如果输入已经是元组或列表
        elif isinstance(position_input, (tuple, list)) and len(position_input) == 2:
            return tuple(position_input)
        
        # 默认返回左上角
        return (10, 10)
    
    def add_text_to_image(self, image_path, text, output_path=None, 
                         font_name="arial", font_size=40, 
                         color="black", position=None, 
                         outline_color=None, outline_width=0):
        """
        给图片添加文字
        
        参数:
        - image_path: 输入图片路径
        - text: 要添加的文字
        - output_path: 输出图片路径（可选）
        - font_name: 字体名称
        - font_size: 字体大小
        - color: 文字颜色
        - position: 文字位置
        - outline_color: 描边颜色（可选）
        - outline_width: 描边宽度
        """
        
        try:
            # 尝试从文件名解析位置和字体大小
            parsed_position, parsed_font_size = self.parse_position_and_size_from_filename(image_path)
            
            # 处理位置解析
            if position is None:
                if parsed_position:
                    x_part, y_part = parsed_position
                    position = f"{x_part},{y_part}"
                    print(f"📋 从文件名解析位置: {position}")
                else:
                    position = "top-left"
                    print(f"📋 使用默认位置: {position}")
            
            # 处理字体大小解析
            if parsed_font_size is not None:
                font_size = parsed_font_size
                print(f"📋 从文件名解析字体大小: {font_size}")
            
            # 打开图片
            image = Image.open(image_path)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # 创建透明图层用于文字
            text_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(text_layer)
            
            # 获取字体
            font = self.get_font(font_name, font_size)
            
            # 解析颜色
            text_color = self.parse_color(color)
            outline_color_parsed = None
            if outline_color:
                outline_color_parsed = self.parse_color(outline_color)
            
            # 获取文字尺寸（处理多行文字）
            lines = text.split('\n')
            line_height = font_size + 5  # 使用参数中的字体大小 + 行间距
            
            # 计算最大行宽度
            max_width = 0
            for line in lines:
                if line.strip():  # 只计算非空行
                    bbox = draw.textbbox((0, 0), line, font=font)
                    line_width = bbox[2] - bbox[0]
                    max_width = max(max_width, line_width)
            
            text_width = max_width
            text_height = len([line for line in lines if line.strip()]) * line_height
            
            # 解析位置
            pos = self.parse_position(position, image.size, (text_width, text_height), image_path)
            
            # 按照正确思路计算多行文字位置：
            # 1. 先算行数
            non_empty_lines = [line for line in lines if line.strip()]
            line_count = len(non_empty_lines)
            
            # 2. 根据字体大小算整个文字区域的高度
            total_height = line_count * line_height
            
            # 3. 基于解析出的位置计算起始位置
            # pos[1] 是解析出的Y坐标，这应该是文字区域top距离图片顶部的距离
            start_y = pos[1]
            
            # 绘制描边（如果有）- 支持多行文字
            if outline_color_parsed and outline_width > 0:
                line_index = 0
                for line in lines:
                    if not line.strip():  # 跳过空行
                        continue
                        
                    line_y = start_y + line_index * line_height
                    line_pos = (pos[0], line_y)
                    
                    for dx in range(-outline_width, outline_width + 1):
                        for dy in range(-outline_width, outline_width + 1):
                            if dx != 0 or dy != 0:
                                draw.text((line_pos[0] + dx, line_pos[1] + dy), line, 
                                        font=font, fill=outline_color_parsed)
                    line_index += 1
            
            # 绘制每一行文字
            line_index = 0
            for line in lines:
                if not line.strip():  # 跳过空行
                    continue
                    
                line_y = start_y + line_index * line_height
                line_pos = (pos[0], line_y)
                
                # 绘制加粗效果（通过多次绘制实现加粗效果）
                bold_offset = 1  # 加粗偏移量
                for dx in range(-bold_offset, bold_offset + 1):
                    for dy in range(-bold_offset, bold_offset + 1):
                        if dx == 0 and dy == 0:
                            continue  # 跳过原始位置
                        draw.text((line_pos[0] + dx, line_pos[1] + dy), line, 
                                font=font, fill=text_color + (255,))
                
                # 绘制主文字
                draw.text(line_pos, line, font=font, fill=text_color + (255,))
                line_index += 1
            
            # 合并图层
            result = Image.alpha_composite(image, text_layer)
            
            # 保存图片
            if output_path is None:
                name, ext = os.path.splitext(image_path)
                output_path = f"{name}_with_text{ext}"
            
            # 根据输出格式转换图片模式
            output_ext = os.path.splitext(output_path)[1].lower()
            if output_ext in ['.jpg', '.jpeg']:
                # JPEG格式不支持透明通道，转换为RGB
                result = result.convert('RGB')
            elif output_ext == '.png':
                # PNG格式保持RGBA
                pass
            else:
                # 其他格式转换为RGB
                result = result.convert('RGB')
            
            result.save(output_path)
            
            print(f"✅ 成功添加文字到图片: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return None
    
    def list_available_fonts(self):
        """列出可用字体"""
        print("📝 可用字体:")
        for font_key, font_name in self.available_fonts.items():
            print(f"  - {font_key} ({font_name})")
        
        if not self.available_fonts:
            print("  ⚠️  未找到字体文件")
            print(f"  💡 请将字体文件(.ttf或.otf)放入 {self.fonts_dir} 目录")
    
    def show_color_examples(self):
        """显示颜色示例"""
        print("🎨 支持的颜色格式:")
        print("  命名颜色: black, white, red, green, blue, yellow, cyan, magenta, gray, orange, purple, pink, brown, lime, navy, teal")
        print("  十六进制: #FF0000, #00FF00, #0000FF")
        print("  RGB值: 255,0,0 或 (255,0,0)")
    
    def show_position_examples(self):
        """显示位置示例"""
        print("📍 支持的位置格式:")
        print("  预定义位置: top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right")
        print("  自定义坐标: 100,200 或 (100,200)")
        print("  垂直居中: 100,vcenter (水平坐标100，垂直居中)")
        print("  水平居中: center,200 (水平居中，垂直坐标200)")
        print("  完全居中: center,center 或 vcenter")
    
    def parse_text_paragraphs(self, text_file_path):
        """从文本文件中解析段落，以连续两个换行为界限"""
        try:
            with open(text_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按连续两个换行符分割段落
            paragraphs = re.split(r'\n\s*\n', content)
            
            # 清理段落内容
            cleaned_paragraphs = []
            for para in paragraphs:
                # 去除首尾空白，但保持换行符用于多行显示
                cleaned = para.strip()
                if cleaned:  # 只保留非空段落
                    cleaned_paragraphs.append(cleaned)
            
            print(f"📖 从 {text_file_path} 中解析出 {len(cleaned_paragraphs)} 个段落")
            return cleaned_paragraphs
            
        except Exception as e:
            print(f"❌ 读取文本文件失败: {str(e)}")
            return []
    
    def get_image_files(self, folder_path):
        """获取文件夹中的图片文件，按文件名排序，排除已处理的文件"""
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
        image_files = []
        
        for ext in image_extensions:
            pattern = os.path.join(folder_path, ext)
            image_files.extend(glob.glob(pattern))
            pattern = os.path.join(folder_path, ext.upper())
            image_files.extend(glob.glob(pattern))
        
        # 去重并过滤掉已处理的文件
        unique_files = list(set(image_files))  # 去重
        original_files = []
        for file_path in unique_files:
            filename = os.path.basename(file_path)
            # 排除已处理的文件（包含 _text 或 _with_text 的文件）
            if '_text' not in filename and '_with_text' not in filename:
                original_files.append(file_path)
        
        # 按文件名第一个数值排序
        def get_sort_key(filepath):
            filename = os.path.basename(filepath)
            # 用-分割，取第一部分
            first_part = filename.split('-')[0]
            try:
                # 尝试提取数字
                import re
                numbers = re.findall(r'\d+', first_part)
                if numbers:
                    return int(numbers[0])
                else:
                    return 0
            except:
                return 0
        
        original_files.sort(key=get_sort_key)
        print(f"🖼️  在 {folder_path} 中找到 {len(original_files)} 张原始图片")
        return original_files
    
    def batch_process_images(self, folder_path, text_file_path, output_folder=None,
                           font_name="simkai", font_size=40, color="black", 
                           position="center", outline_color=None, outline_width=0):
        """
        批量处理图片，将文本段落分配给图片
        
        参数:
        - folder_path: 图片文件夹路径
        - text_file_path: 文本文件路径
        - output_folder: 输出文件夹路径（可选）
        - font_name: 字体名称
        - font_size: 字体大小
        - color: 文字颜色
        - position: 文字位置
        - outline_color: 描边颜色
        - outline_width: 描边宽度
        """
        
        # 解析文本段落
        paragraphs = self.parse_text_paragraphs(text_file_path)
        if not paragraphs:
            print("❌ 没有找到有效的文本段落")
            return
        
        # 获取图片文件
        image_files = self.get_image_files(folder_path)
        if not image_files:
            print("❌ 没有找到图片文件")
            return
        
        # 设置输出文件夹
        if output_folder is None:
            output_folder = os.path.join(folder_path, "output")
        
        # 创建输出文件夹
        os.makedirs(output_folder, exist_ok=True)
        
        # 处理图片和文本的配对
        processed_count = 0
        min_count = min(len(paragraphs), len(image_files))
        
        print(f"\n🔄 开始批量处理，将处理 {min_count} 张图片...")
        
        for i in range(min_count):
            image_path = image_files[i]
            text_content = paragraphs[i]
            
            # 生成输出文件名
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_folder, f"{image_name}_text.jpg")
            
            print(f"\n📝 处理第 {i+1} 张图片: {os.path.basename(image_path)}")
            print(f"   文本内容: {text_content[:30]}..." if len(text_content) > 30 else f"   文本内容: {text_content}")
            
            # 添加文字到图片（不传递position和font_size，让方法内部解析）
            result = self.add_text_to_image(
                image_path=image_path,
                text=text_content,
                output_path=output_path,
                font_name=font_name,
                font_size=font_size,
                color=color,
                position=None,  # 让方法内部从文件名解析
                outline_color=outline_color,
                outline_width=outline_width
            )
            
            if result:
                processed_count += 1
                print(f"   ✅ 保存到: {output_path}")
            else:
                print(f"   ❌ 处理失败")
        
        print(f"\n🎉 批量处理完成！成功处理 {processed_count} 张图片")
        print(f"📁 输出文件夹: {output_folder}")
        
        # 显示剩余内容统计
        if len(paragraphs) > len(image_files):
            print(f"⚠️  还有 {len(paragraphs) - len(image_files)} 个文本段落没有处理")
        elif len(image_files) > len(paragraphs):
            print(f"⚠️  还有 {len(image_files) - len(paragraphs)} 张图片没有使用")
        
        return processed_count
    
    def auto_process_images(self, folder_path, img_source_folder="D:\\cursor\\imgaddtext\\xiaoshani\\img", 
                           output_folder=None, font_name="simkai", font_size=40, 
                           color="black", outline_color=None, outline_width=0):
        """
        自动处理图片，从指定文件夹的0.txt读取段落，随机选择10张图片添加文字
        
        参数:
        - folder_path: 包含0.txt文件的文件夹路径
        - img_source_folder: 图片源文件夹路径
        - output_folder: 输出文件夹路径（可选）
        - font_name: 字体名称
        - font_size: 字体大小
        - color: 文字颜色
        - outline_color: 描边颜色
        - outline_width: 描边宽度
        """
        
        # 检查0.txt文件是否存在
        text_file_path = os.path.join(folder_path, "0.txt")
        if not os.path.exists(text_file_path):
            print(f"❌ 0.txt文件不存在: {text_file_path}")
            return 0
        
        # 检查图片源文件夹是否存在
        if not os.path.exists(img_source_folder):
            print(f"❌ 图片源文件夹不存在: {img_source_folder}")
            return 0
        
        # 解析文本段落
        paragraphs = self.parse_text_paragraphs(text_file_path)
        if not paragraphs:
            print("❌ 没有找到有效的文本段落")
            return 0
        
        # 获取图片源文件夹中的所有图片文件
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff']
        all_image_files = []
        
        for ext in image_extensions:
            pattern = os.path.join(img_source_folder, ext)
            all_image_files.extend(glob.glob(pattern))
            pattern = os.path.join(img_source_folder, ext.upper())
            all_image_files.extend(glob.glob(pattern))
        
        # 去重
        all_image_files = list(set(all_image_files))
        
        if len(all_image_files) < 10:
            print(f"❌ 图片源文件夹中只有 {len(all_image_files)} 张图片，需要至少10张")
            return 0
        
        # 随机选择10张图片
        selected_images = random.sample(all_image_files, 10)
        print(f"🎲 从 {len(all_image_files)} 张图片中随机选择了10张")
        
        # 设置输出文件夹
        if output_folder is None:
            output_folder = os.path.join(folder_path, "output")
        
        # 创建输出文件夹
        os.makedirs(output_folder, exist_ok=True)
        
        # 处理图片和文本的配对
        processed_count = 0
        min_count = min(len(paragraphs), len(selected_images))
        
        print(f"\n🔄 开始自动处理，将处理 {min_count} 张图片...")
        
        for i in range(min_count):
            image_path = selected_images[i]
            text_content = paragraphs[i]
            
            # 生成输出文件名
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_folder, f"{image_name}_text.jpg")
            
            print(f"\n📝 处理第 {i+1} 张图片: {os.path.basename(image_path)}")
            print(f"   文本内容: {text_content[:30]}..." if len(text_content) > 30 else f"   文本内容: {text_content}")
            
            # 添加文字到图片（不传递position和font_size，让方法内部解析）
            result = self.add_text_to_image(
                image_path=image_path,
                text=text_content,
                output_path=output_path,
                font_name=font_name,
                font_size=font_size,
                color=color,
                position=None,  # 让方法内部从文件名解析
                outline_color=outline_color,
                outline_width=outline_width
            )
            
            if result:
                processed_count += 1
                print(f"   ✅ 保存到: {output_path}")
            else:
                print(f"   ❌ 处理失败")
        
        print(f"\n🎉 自动处理完成！成功处理 {processed_count} 张图片")
        print(f"📁 输出文件夹: {output_folder}")
        
        # 显示剩余内容统计
        if len(paragraphs) > len(selected_images):
            print(f"⚠️  还有 {len(paragraphs) - len(selected_images)} 个文本段落没有处理")
        elif len(selected_images) > len(paragraphs):
            print(f"⚠️  还有 {len(selected_images) - len(paragraphs)} 张图片没有使用")
        
        return processed_count

def main():
    parser = argparse.ArgumentParser(description="给图片添加文字的工具")
    parser.add_argument("image", nargs='?', help="输入图片路径")
    parser.add_argument("-t", "--text", help="要添加的文字")
    parser.add_argument("-o", "--output", help="输出图片路径")
    parser.add_argument("-f", "--font", default="slidexiaxing", help="字体名称")
    parser.add_argument("-s", "--size", type=int, default=40, help="字体大小")
    parser.add_argument("-c", "--color", default="black", help="文字颜色")
    parser.add_argument("-p", "--position", default=None, help="文字位置")
    parser.add_argument("--outline-color", help="描边颜色")
    parser.add_argument("--outline-width", type=int, default=0, help="描边宽度")
    parser.add_argument("--list-fonts", action="store_true", help="列出可用字体")
    parser.add_argument("--show-colors", action="store_true", help="显示颜色示例")
    parser.add_argument("--show-positions", action="store_true", help="显示位置示例")
    
    # 批量处理参数
    parser.add_argument("--batch", action="store_true", help="批量处理模式")
    parser.add_argument("--folder", help="图片文件夹路径（批量处理时使用）")
    parser.add_argument("--text-file", help="文本文件路径（批量处理时使用）")
    parser.add_argument("--output-folder", help="输出文件夹路径（批量处理时使用）")
    
    # 自动处理参数
    parser.add_argument("--auto", help="自动处理模式，从指定文件夹的0.txt读取段落，随机选择10张图片")
    parser.add_argument("--img-source", default="D:\\cursor\\imgaddtext\\xiaoshani\\img", help="图片源文件夹路径（自动处理时使用）")
    
    args = parser.parse_args()
    
    adder = ImageTextAdder()
    
    if args.list_fonts:
        adder.list_available_fonts()
        return
    
    if args.show_colors:
        adder.show_color_examples()
        return
    
    if args.show_positions:
        adder.show_position_examples()
        return
    
    # 批量处理模式
    if args.batch:
        if not args.folder or not args.text_file:
            print("❌ 批量处理模式需要指定 --folder 和 --text-file 参数")
            print("示例: python imgaddtext.py --batch --folder ./images --text-file ./text.txt")
            return
        
        if not os.path.exists(args.folder):
            print(f"❌ 图片文件夹不存在: {args.folder}")
            return
        
        if not os.path.exists(args.text_file):
            print(f"❌ 文本文件不存在: {args.text_file}")
            return
        
        # 执行批量处理
        result = adder.batch_process_images(
            folder_path=args.folder,
            text_file_path=args.text_file,
            output_folder=args.output_folder,
            font_name=args.font,
            font_size=args.size,
            color=args.color,
            position=args.position,
            outline_color=args.outline_color,
            outline_width=args.outline_width
        )
        
        if result:
            print(f"\n🎉 批量处理成功完成！共处理 {result} 张图片")
        return
    
    # 自动处理模式
    if args.auto:
        if not os.path.exists(args.auto):
            print(f"❌ 文件夹不存在: {args.auto}")
            return
        
        # 执行自动处理
        result = adder.auto_process_images(
            folder_path=args.auto,
            img_source_folder=args.img_source,
            output_folder=args.output_folder,
            font_name=args.font,
            font_size=args.size,
            color=args.color,
            outline_color=args.outline_color,
            outline_width=args.outline_width
        )
        
        if result:
            print(f"\n🎉 自动处理成功完成！共处理 {result} 张图片")
        return
    
    # 检查是否提供了必需参数
    if not args.image or not args.text:
        parser.print_help()
        return
    
    # 检查输入文件是否存在
    if not os.path.exists(args.image):
        print(f"❌ 错误: 图片文件不存在: {args.image}")
        return
    
    # 添加文字
    result = adder.add_text_to_image(
        image_path=args.image,
        text=args.text,
        output_path=args.output,
        font_name=args.font,
        font_size=args.size,
        color=args.color,
        position=args.position,
        outline_color=args.outline_color,
        outline_width=args.outline_width
    )
    
    if result:
        print(f"🎉 处理完成! 输出文件: {result}")

if __name__ == "__main__":
    main()
