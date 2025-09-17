#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机相册管理工具使用示例
"""

import os
import subprocess
from phone_manager import PhoneManager

def test_phone_manager():
    """测试手机相册管理功能"""
    manager = PhoneManager()
    
    print("🔧 手机相册管理工具测试")
    print("=" * 50)
    
    # 1. 检查ADB连接
    print("\n1. 检查ADB连接状态...")
    if manager.check_adb_connection():
        print("✅ ADB连接正常")
    else:
        print("❌ ADB连接失败，请检查手机连接和USB调试设置")
        return
    
    # 2. 列出手机相册中的数字文件夹
    print("\n2. 列出手机相册中的数字文件夹...")
    manager.list_phone_folders()
    
    # 3. 测试文件夹名称验证
    print("\n3. 测试文件夹名称验证...")
    test_folders = ["123", "20250915", "test", "abc", "1a", "999"]
    for folder in test_folders:
        is_valid = manager.validate_folder_name(folder)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {folder}: {'有效' if is_valid else '无效'}")
    
    # 4. 检查当前目录的图片文件夹
    print("\n4. 检查当前目录的图片文件夹...")
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path) and manager.validate_folder_name(item):
            image_files = manager.get_image_files(item_path)
            print(f"   📁 {item}: {len(image_files)} 张图片")
    
    print("\n" + "=" * 50)
    print("📋 使用说明:")
    print("1. 传输图片: python phone_manager.py transfer <文件夹路径>")
    print("2. 删除图片: python phone_manager.py delete <文件夹名称>")
    print("3. 列出文件夹: python phone_manager.py list")
    print("\n💡 提示: 确保手机已连接并开启USB调试")

def create_test_folders():
    """创建测试文件夹和图片"""
    print("🔧 创建测试文件夹和图片...")
    
    # 创建测试文件夹
    test_folders = ["1", "2", "20250915"]
    
    for folder_name in test_folders:
        folder_path = os.path.join("test_images", folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # 创建简单的测试图片（使用PIL）
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 创建白色背景图片
            img = Image.new('RGB', (400, 300), color='white')
            draw = ImageDraw.Draw(img)
            
            # 添加文字
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            text = f"测试图片 {folder_name}"
            draw.text((50, 100), text, fill='black', font=font)
            
            # 保存图片
            img_path = os.path.join(folder_path, f"test_{folder_name}.jpg")
            img.save(img_path)
            print(f"   ✅ 创建测试图片: {img_path}")
            
        except ImportError:
            print("   ⚠️  需要安装Pillow库来创建测试图片")
        except Exception as e:
            print(f"   ❌ 创建测试图片失败: {e}")
    
    print("✅ 测试文件夹创建完成")

if __name__ == "__main__":
    print("选择操作:")
    print("1. 测试手机相册管理功能")
    print("2. 创建测试文件夹和图片")
    print("3. 退出")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        test_phone_manager()
    elif choice == "2":
        create_test_folders()
    elif choice == "3":
        print("👋 再见！")
    else:
        print("❌ 无效选择")
