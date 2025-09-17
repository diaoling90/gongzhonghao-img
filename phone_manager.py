#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机相册管理脚本
功能：
1. 将指定文件夹的图片传输到手机相册
2. 删除手机相册中指定文件夹的图片
3. 文件夹名称只支持数字
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path
import re

class PhoneManager:
    def __init__(self):
        self.supported_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
        
    def validate_folder_name(self, folder_name):
        """验证文件夹名称是否只包含数字"""
        return re.match(r'^\d+$', folder_name) is not None or folder_name == "output" or folder_name == "xiaoshani"
    
    def get_image_files(self, folder_path):
        """获取文件夹中的所有图片文件"""
        if not os.path.exists(folder_path):
            print(f"❌ 文件夹不存在: {folder_path}")
            return []
        
        image_files = []
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in self.supported_image_extensions):
                image_files.append(os.path.join(folder_path, file))
        
        return image_files
    
    def check_adb_connection(self):
        """检查ADB连接状态"""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                devices = [line for line in lines if line.strip() and 'device' in line]
                if devices:
                    print(f"✅ 检测到 {len(devices)} 个设备已连接")
                    return True
                else:
                    print("❌ 没有检测到已连接的设备")
                    return False
            else:
                print("❌ ADB命令执行失败")
                return False
        except FileNotFoundError:
            print("❌ 未找到ADB命令，请确保已安装Android SDK并配置环境变量")
            return False
        except subprocess.TimeoutExpired:
            print("❌ ADB命令超时")
            return False
        except Exception as e:
            print(f"❌ 检查ADB连接时出错: {e}")
            return False
    
    def create_phone_folder(self, folder_name):
        """在手机相册中创建文件夹"""
        if not self.validate_folder_name(folder_name):
            print(f"❌ 文件夹名称 '{folder_name}' 不符合要求，只支持数字")
            return False
        
        try:
            # 在手机DCIM目录下创建文件夹
            phone_folder_path = f"/sdcard/DCIM/{folder_name}"
            result = subprocess.run(['adb', 'shell', f'mkdir -p "{phone_folder_path}"'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"✅ 在手机相册中创建文件夹: {folder_name}")
                return True
            else:
                print(f"❌ 创建手机文件夹失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 创建手机文件夹时出错: {e}")
            return False
    
    def transfer_images_to_phone(self, folder_path):
        """将指定文件夹的图片传输到手机相册"""
        folder_name = os.path.basename(folder_path)
        
        # 验证文件夹名称
        if not self.validate_folder_name(folder_name):
            print(f"❌ 文件夹名称 '{folder_name}' 不符合要求，只支持数字")
            return False
        
        # 检查ADB连接
        if not self.check_adb_connection():
            return False
        
        # 获取图片文件
        image_files = self.get_image_files(folder_path)
        if not image_files:
            print(f"❌ 文件夹中没有找到图片文件: {folder_path}")
            return False
        
        print(f"📁 找到 {len(image_files)} 张图片")
        
        # 创建手机文件夹
        if not self.create_phone_folder(folder_name):
            return False
        
        # 传输图片
        success_count = 0
        phone_folder_path = f"/sdcard/DCIM/{folder_name}"
        
        for i, image_file in enumerate(image_files, 1):
            try:
                filename = os.path.basename(image_file)
                phone_file_path = f"{phone_folder_path}/{filename}"
                
                print(f"📤 传输第 {i}/{len(image_files)} 张: {filename}")
                
                # 使用adb push传输文件
                result = subprocess.run(['adb', 'push', image_file, phone_file_path], 
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    success_count += 1
                    print(f"   ✅ 传输成功")
                else:
                    print(f"   ❌ 传输失败: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"   ❌ 传输超时: {filename}")
            except Exception as e:
                print(f"   ❌ 传输出错: {filename} - {e}")
        
        print(f"\n🎉 传输完成！成功传输 {success_count}/{len(image_files)} 张图片")
        
        # 刷新手机相册
        try:
            subprocess.run(['adb', 'shell', 'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM'], 
                          capture_output=True, text=True, timeout=10)
            print("📱 已刷新手机相册")
        except:
            print("⚠️  刷新手机相册失败，请手动刷新")
        
        return success_count > 0
    
    def delete_phone_folder_images(self, folder_name):
        """删除手机相册中指定文件夹的图片"""
        if not self.validate_folder_name(folder_name):
            print(f"❌ 文件夹名称 '{folder_name}' 不符合要求，只支持数字")
            return False
        
        # 检查ADB连接
        if not self.check_adb_connection():
            return False
        
        phone_folder_path = f"/sdcard/DCIM/{folder_name}"
        
        try:
            # 检查文件夹是否存在
            result = subprocess.run(['adb', 'shell', f'ls "{phone_folder_path}"'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"❌ 手机相册中不存在文件夹: {folder_name}")
                return False
            
            # 获取文件夹中的文件列表
            files = result.stdout.strip().split('\n')
            image_files = [f for f in files if any(f.lower().endswith(ext) for ext in self.supported_image_extensions)]
            
            if not image_files:
                print(f"❌ 文件夹中没有图片文件: {folder_name}")
                return False
            
            print(f"📁 找到 {len(image_files)} 张图片需要删除")
            
            # 确认删除
            confirm = input(f"⚠️  确定要删除手机相册中文件夹 '{folder_name}' 的所有图片吗？(y/N): ")
            if confirm.lower() != 'y':
                print("❌ 取消删除操作")
                return False
            
            # 删除图片
            success_count = 0
            for i, filename in enumerate(image_files, 1):
                try:
                    phone_file_path = f"{phone_folder_path}/{filename}"
                    print(f"🗑️  删除第 {i}/{len(image_files)} 张: {filename}")
                    
                    result = subprocess.run(['adb', 'shell', f'rm "{phone_file_path}"'], 
                                          capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        success_count += 1
                        print(f"   ✅ 删除成功")
                    else:
                        print(f"   ❌ 删除失败: {result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    print(f"   ❌ 删除超时: {filename}")
                except Exception as e:
                    print(f"   ❌ 删除出错: {filename} - {e}")
            
            # 删除空文件夹
            try:
                subprocess.run(['adb', 'shell', f'rmdir "{phone_folder_path}"'], 
                              capture_output=True, text=True, timeout=10)
                print(f"📁 已删除空文件夹: {folder_name}")
            except:
                pass
            
            print(f"\n🎉 删除完成！成功删除 {success_count}/{len(image_files)} 张图片")
            
            # 刷新手机相册
            try:
                subprocess.run(['adb', 'shell', 'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM'], 
                              capture_output=True, text=True, timeout=10)
                print("📱 已刷新手机相册")
            except:
                print("⚠️  刷新手机相册失败，请手动刷新")
            
            return success_count > 0
            
        except Exception as e:
            print(f"❌ 删除手机图片时出错: {e}")
            return False
    
    def list_phone_folders(self):
        """列出手机相册中的数字文件夹"""
        if not self.check_adb_connection():
            return
        
        try:
            result = subprocess.run(['adb', 'shell', 'ls /sdcard/DCIM/'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                folders = result.stdout.strip().split('\n')
                number_folders = [f for f in folders if self.validate_folder_name(f.strip())]
                
                if number_folders:
                    print(f"📁 手机相册中的数字文件夹:")
                    for folder in sorted(number_folders):
                        print(f"   - {folder}")
                else:
                    print("📁 手机相册中没有数字文件夹")
            else:
                print("❌ 无法列出手机相册文件夹")
                
        except Exception as e:
            print(f"❌ 列出手机文件夹时出错: {e}")

def main():
    parser = argparse.ArgumentParser(description='手机相册管理工具')
    parser.add_argument('action', choices=['transfer', 'delete', 'list'], 
                       help='操作类型: transfer(传输), delete(删除), list(列出文件夹)')
    parser.add_argument('folder', nargs='?', help='文件夹路径或文件夹名称')
    
    args = parser.parse_args()
    
    manager = PhoneManager()
    
    if args.action == 'transfer':
        if not args.folder:
            print("❌ 请指定要传输的文件夹路径")
            sys.exit(1)
        
        folder_path = os.path.abspath(args.folder)
        manager.transfer_images_to_phone(folder_path)
        
    elif args.action == 'delete':
        if not args.folder:
            print("❌ 请指定要删除的文件夹名称")
            sys.exit(1)
        
        manager.delete_phone_folder_images(args.folder)
        
    elif args.action == 'list':
        manager.list_phone_folders()

if __name__ == "__main__":
    main()
