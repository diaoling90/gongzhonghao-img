#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片添加文字工具 - 使用示例
"""

from imgaddtext import ImageTextAdder
import os

def example_usage():
    """演示如何使用图片添加文字工具"""
    
    # 创建工具实例
    adder = ImageTextAdder()
    
    # 假设有一张名为 "example.jpg" 的图片
    image_path = "example.jpg"
    
    # 如果图片不存在，创建一个示例图片
    if not os.path.exists(image_path):
        print("📝 创建示例图片...")
        from PIL import Image, ImageDraw
        
        # 创建一个简单的示例图片
        img = Image.new('RGB', (800, 600), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # 画一些装饰
        draw.rectangle([50, 50, 750, 550], outline='darkblue', width=3)
        draw.ellipse([300, 200, 500, 400], fill='yellow', outline='orange', width=2)
        
        img.save(image_path)
        print(f"✅ 已创建示例图片: {image_path}")
    
    print("\n🎨 开始演示各种功能...\n")
    
    # 示例1: 基本用法 - 添加简单文字
    print("示例1: 基本用法")
    result1 = adder.add_text_to_image(
        image_path=image_path,
        text="Hello World!",
        output_path="example1_basic.jpg",
        font_name="arial",
        font_size=50,
        color="black",
        position="top-center"
    )
    
    # 示例2: 使用不同颜色和位置
    print("\n示例2: 不同颜色和位置")
    result2 = adder.add_text_to_image(
        image_path=image_path,
        text="彩色文字",
        output_path="example2_color.jpg",
        font_name="arial",
        font_size=60,
        color="#FF0000",  # 红色
        position="center"
    )
    
    # 示例3: 使用RGB颜色和自定义位置
    print("\n示例3: RGB颜色和自定义位置")
    result3 = adder.add_text_to_image(
        image_path=image_path,
        text="自定义位置",
        output_path="example3_custom.jpg",
        font_name="arial",
        font_size=45,
        color=(0, 128, 255),  # 蓝色
        position=(100, 300)
    )
    
    # 示例4: 添加描边效果
    print("\n示例4: 描边效果")
    result4 = adder.add_text_to_image(
        image_path=image_path,
        text="描边文字",
        output_path="example4_outline.jpg",
        font_name="arial",
        font_size=55,
        color="white",
        position="bottom-center",
        outline_color="black",
        outline_width=3
    )
    
    # 示例5: 使用命名颜色和底部位置
    print("\n示例5: 命名颜色")
    result5 = adder.add_text_to_image(
        image_path=image_path,
        text="命名颜色",
        output_path="example5_named_color.jpg",
        font_name="arial",
        font_size=48,
        color="purple",
        position="bottom-right"
    )
    
    # 显示可用字体
    print("\n📝 可用字体列表:")
    adder.list_available_fonts()
    
    # 显示颜色示例
    print("\n🎨 颜色格式示例:")
    adder.show_color_examples()
    
    # 显示位置示例
    print("\n📍 位置格式示例:")
    adder.show_position_examples()
    
    print("\n🎉 所有示例演示完成!")
    print("📁 生成的图片文件:")
    for i in range(1, 6):
        filename = f"example{i}_*.jpg"
        print(f"  - {filename}")

def command_line_examples():
    """命令行使用示例"""
    print("\n" + "="*60)
    print("💻 命令行使用示例:")
    print("="*60)
    
    examples = [
        {
            "desc": "基本用法",
            "cmd": "python imgaddtext.py example.jpg -t \"Hello World!\""
        },
        {
            "desc": "指定输出文件",
            "cmd": "python imgaddtext.py example.jpg -t \"标题\" -o output.jpg"
        },
        {
            "desc": "自定义字体大小和颜色",
            "cmd": "python imgaddtext.py example.jpg -t \"大标题\" -s 80 -c red"
        },
        {
            "desc": "使用十六进制颜色",
            "cmd": "python imgaddtext.py example.jpg -t \"彩色文字\" -c \"#FF6600\""
        },
        {
            "desc": "指定位置",
            "cmd": "python imgaddtext.py example.jpg -t \"居中文字\" -p center"
        },
        {
            "desc": "自定义坐标位置",
            "cmd": "python imgaddtext.py example.jpg -t \"自定义位置\" -p \"200,150\""
        },
        {
            "desc": "垂直居中，水平坐标100",
            "cmd": "python imgaddtext.py example.jpg -t \"垂直居中\" -p \"100,vcenter\""
        },
        {
            "desc": "水平居中，垂直坐标200",
            "cmd": "python imgaddtext.py example.jpg -t \"水平居中\" -p \"center,200\""
        },
        {
            "desc": "完全居中",
            "cmd": "python imgaddtext.py example.jpg -t \"完全居中\" -p \"center,center\""
        },
        {
            "desc": "添加描边效果",
            "cmd": "python imgaddtext.py example.jpg -t \"描边文字\" -c white --outline-color black --outline-width 2"
        },
        {
            "desc": "查看可用字体",
            "cmd": "python imgaddtext.py --list-fonts"
        },
        {
            "desc": "查看颜色示例",
            "cmd": "python imgaddtext.py --show-colors"
        },
        {
            "desc": "查看位置示例",
            "cmd": "python imgaddtext.py --show-positions"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['desc']}:")
        print(f"   {example['cmd']}")

if __name__ == "__main__":
    print("🖼️  图片添加文字工具 - 使用示例")
    print("="*50)
    
    # 运行示例
    example_usage()
    
    # 显示命令行示例
    command_line_examples()
    
    print("\n" + "="*60)
    print("📖 更多帮助信息:")
    print("python imgaddtext.py --help")
    print("="*60)



#  python imgaddtext.py --batch --folder ./20250913 --text-file ./20250913/1.txt -f bbhbold -s 120 -c black -p center