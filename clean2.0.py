#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sys
from pathlib import Path

# 文件分类规则
FILE_CATEGORIES = {
    '图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    '视频': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.3gp', '.m4v'],
    '音频': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    '文档': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.epub'],
    '压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'APK': ['.apk'],
    '安装包': ['.exe', '.deb', '.rpm', '.dmg'],
    '脚本': ['.py', '.sh', '.js', '.html', '.css', '.php', '.java'],
}

def get_category(file_extension):
    """根据文件扩展名返回分类"""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return '其他文件'

def organize_files(directory):
    """整理指定目录下的文件"""
    
    directory = Path(directory).expanduser().resolve()
    
    if not directory.exists():
        print(f"❌ 错误: 目录 {directory} 不存在")
        return
    
    if not directory.is_dir():
        print(f"❌ 错误: {directory} 不是一个目录")
        return
    
    print(f"📁 正在整理目录: {directory}")
    print("-" * 50)
    
    # 统计信息
    stats = {}
    moved_files = 0
    
    for item in directory.iterdir():
        # 只处理文件，跳过目录和隐藏文件
        if not item.is_file():
            continue
        
        # 跳过隐藏文件（以.开头）
        if item.name.startswith('.'):
            continue
            
        # 获取文件扩展名
        file_extension = item.suffix
        if not file_extension:
            file_extension = '.no_extension'
        
        # 确定文件分类
        category = get_category(file_extension)
        
        # 创建分类目录
        category_dir = directory / category
        category_dir.mkdir(exist_ok=True)
        
        # 检查目标文件是否已存在
        destination = category_dir / item.name
        if destination.exists():
            # 处理重名文件
            base_name = item.stem
            counter = 1
            while destination.exists():
                new_name = f"{base_name}_{counter}{item.suffix}"
                destination = category_dir / new_name
                counter += 1
        
        try:
            # 移动文件
            shutil.move(str(item), str(destination))
            moved_files += 1
            
            # 统计
            stats[category] = stats.get(category, 0) + 1
            print(f"✅ 移动: {item.name} → {category}/")
            
        except Exception as e:
            print(f"❌ 错误: 无法移动 {item.name} - {str(e)}")
    
    print("-" * 50)
    print(f"✨ 整理完成！共移动 {moved_files} 个文件")
    
    if moved_files > 0:
        print("\n📊 分类统计:")
        for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count} 个文件")
    
    return moved_files

def main():
    print("=" * 50)
    print("📱 Termux 文件整理工具")
    print("=" * 50)
    
    # 获取当前目录
    current_dir = os.getcwd()
    
    print(f"\n当前目录: {current_dir}")
    print("\n选项:")
    print("1. 整理当前目录")
    print("2. 整理指定目录")
    print("3. 整理内部存储")
    print("0. 退出")
    
    choice = input("\n请选择 (0/1/2/3): ").strip()
    
    if choice == '0':
        print("👋 再见！")
        sys.exit(0)
    
    elif choice == '1':
        target_dir = current_dir
        
    elif choice == '2':
        target_dir = input("请输入要整理的目录路径: ").strip()
        if not target_dir:
            print("❌ 未输入路径")
            return
            
    elif choice == '3':
        # Termux内部存储路径
        internal_storage = Path.home() / "storage"
        if not internal_storage.exists():
            print("❌ 未找到内部存储，请运行: termux-setup-storage")
            return
        target_dir = internal_storage / "downloads"  # 默认整理下载目录
        print(f"📂 将整理下载目录: {target_dir}")
        confirm = input("确认继续? (y/n): ").strip().lower()
        if confirm != 'y':
            print("已取消")
            return
    else:
        print("❌ 无效选择")
        return
    
    # 确认操作
    print(f"\n⚠️  警告: 将在 {target_dir} 目录下创建分类文件夹并移动文件")
    confirm = input("确认继续? (y/n): ").strip().lower()
    
    if confirm == 'y':
        organize_files(target_dir)
    else:
        print("❌ 已取消")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1) 

