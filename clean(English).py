#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sys
from pathlib import Path

# File categorization rules
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.3gp', '.m4v'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.epub'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'APK': ['.apk'],
    'Installers': ['.exe', '.deb', '.rpm', '.dmg'],
    'Scripts': ['.py', '.sh', '.js', '.html', '.css', '.php', '.java'],
}

def get_category(file_extension):
    """Return category based on file extension"""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return 'Other'

def organize_files(directory):
    """Organize files in the specified directory"""
    
    directory = Path(directory).expanduser().resolve()
    
    if not directory.exists():
        print(f"❌ Error: Directory {directory} does not exist")
        return
    
    if not directory.is_dir():
        print(f"❌ Error: {directory} is not a directory")
        return
    
    print(f"📁 Organizing directory: {directory}")
    print("-" * 50)
    
    # Statistics
    stats = {}
    moved_files = 0
    
    for item in directory.iterdir():
        # Process only files, skip directories and hidden files
        if not item.is_file():
            continue
        
        # Skip hidden files (starting with .)
        if item.name.startswith('.'):
            continue
            
        # Get file extension
        file_extension = item.suffix
        if not file_extension:
            file_extension = '.no_extension'
        
        # Determine file category
        category = get_category(file_extension)
        
        # Create category directory
        category_dir = directory / category
        category_dir.mkdir(exist_ok=True)
        
        # Check if destination file already exists
        destination = category_dir / item.name
        if destination.exists():
            # Handle duplicate filenames
            base_name = item.stem
            counter = 1
            while destination.exists():
                new_name = f"{base_name}_{counter}{item.suffix}"
                destination = category_dir / new_name
                counter += 1
        
        try:
            # Move file
            shutil.move(str(item), str(destination))
            moved_files += 1
            
            # Update statistics
            stats[category] = stats.get(category, 0) + 1
            print(f"✅ Moved: {item.name} → {category}/")
            
        except Exception as e:
            print(f"❌ Error: Could not move {item.name} - {str(e)}")
    
    print("-" * 50)
    print(f"✨ Organization complete! Moved {moved_files} files")
    
    if moved_files > 0:
        print("\n📊 Statistics by category:")
        for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count} files")
    
    return moved_files

def main():
    print("=" * 50)
    print("📱 Termux File Organizer")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.getcwd()
    
    print(f"\nCurrent directory: {current_dir}")
    print("\nOptions:")
    print("1. Organize current directory")
    print("2. Organize specified directory")
    print("3. Organize internal storage")
    print("0. Exit")
    
    choice = input("\nPlease choose (0/1/2/3): ").strip()
    
    if choice == '0':
        print("👋 Goodbye!")
        sys.exit(0)
    
    elif choice == '1':
        target_dir = current_dir
        
    elif choice == '2':
        target_dir = input("Enter directory path to organize: ").strip()
        if not target_dir:
            print("❌ No path entered")
            return
            
    elif choice == '3':
        # Termux internal storage path
        internal_storage = Path.home() / "storage"
        if not internal_storage.exists():
            print("❌ Internal storage not found. Please run: termux-setup-storage")
            return
        target_dir = internal_storage / "downloads"  # Default to downloads folder
        print(f"📂 Will organize downloads folder: {target_dir}")
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled")
            return
    else:
        print("❌ Invalid choice")
        return
    
    # Confirm operation
    print(f"\n⚠️  Warning: Will create category folders and move files in {target_dir}")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm == 'y':
        organize_files(target_dir)
    else:
        print("❌ Cancelled")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)