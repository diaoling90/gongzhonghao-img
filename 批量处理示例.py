#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理示例 - 从文件读取文案并按段落分配给图片
"""

from imgaddtext import ImageTextAdder
import os

def demo_batch_processing():
    """演示批量处理功能"""
    
    print("🖼️  批量处理图片添加文字工具演示")
    print("="*50)
    
    # 创建工具实例
    adder = ImageTextAdder()
    
    # 示例1: 基本批量处理
    print("\n📝 示例1: 基本批量处理")
    print("命令: python imgaddtext.py --batch --folder ./images --text-file ./text.txt")
    
    # 示例2: 自定义参数的批量处理
    print("\n📝 示例2: 自定义参数的批量处理")
    print("命令: python imgaddtext.py --batch --folder ./images --text-file ./text.txt --font simkai --size 50 --color red --position center")
    
    # 示例3: 带描边效果的批量处理
    print("\n📝 示例3: 带描边效果的批量处理")
    print("命令: python imgaddtext.py --batch --folder ./images --text-file ./text.txt --font simhei --size 60 --color white --outline-color black --outline-width 2")
    
    # 示例4: 指定输出文件夹
    print("\n📝 示例4: 指定输出文件夹")
    print("命令: python imgaddtext.py --batch --folder ./images --text-file ./text.txt --output-folder ./results")
    
    print("\n" + "="*50)
    print("📋 批量处理功能说明:")
    print("1. 文本文件按连续两个换行符分割段落")
    print("2. 图片文件按文件名顺序处理")
    print("3. 每个段落对应一张图片")
    print("4. 如果图片不够，剩余的文本段落会被忽略")
    print("5. 如果文本不够，剩余的图片不会被处理")
    print("6. 输出文件会保存在指定文件夹中")
    
    print("\n🎨 支持的图片格式: JPG, JPEG, PNG, BMP, GIF, TIFF")
    print("📝 支持的文本格式: TXT (UTF-8编码)")
    
    print("\n💡 使用建议:")
    print("- 确保文本文件使用UTF-8编码")
    print("- 段落之间用两个换行符分隔")
    print("- 图片文件名建议使用数字或字母排序")
    print("- 输出文件夹会自动创建")

def create_sample_files():
    """创建示例文件"""
    
    print("\n🛠️  创建示例文件...")
    
    # 创建示例文本文件
    sample_text = """这是第一个段落的内容
可以包含多行文字

这是第二个段落
内容也可以很长

这是第三个段落
最后一段内容"""
    
    with open("示例文本.txt", "w", encoding="utf-8") as f:
        f.write(sample_text)
    
    print("✅ 已创建示例文本文件: 示例文本.txt")
    print("📝 包含3个段落，用连续两个换行符分隔")
    
    print("\n💡 使用方法:")
    print("1. 将你的图片放入一个文件夹")
    print("2. 准备你的文本文件，段落间用两个换行符分隔")
    print("3. 运行批量处理命令:")
    print("   python imgaddtext.py --batch --folder 你的图片文件夹 --text-file 你的文本文件.txt")

if __name__ == "__main__":
    demo_batch_processing()
    create_sample_files()
