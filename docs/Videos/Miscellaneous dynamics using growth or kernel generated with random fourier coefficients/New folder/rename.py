import os
import glob
import argparse
import random

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Rename video files sequentially.')
    parser.add_argument('prefix', type=str, help='Prefix for renamed files')
    args = parser.parse_args()
    
    # Define video file extensions
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm']
    
    # Get all video files in the current directory
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(f'*{ext}'))
    
    if not video_files:
        print("No video files found in the current directory.")
        return
    
    # Sort files to ensure consistent ordering
    video_files.sort()
    
    # Check for potential conflicts
    new_names = []
    for i, file in enumerate(video_files, 1):
        _, ext = os.path.splitext(file)
        new_name = f"{args.prefix}_{i}{ext}"
        new_names.append(new_name)
    
    # Rename files using a two-phase approach to avoid conflicts
    # Phase 1: Rename to temporary names
    temp_names = []
    for i, file in enumerate(video_files):
        temp_name = f"__temp_{i}_{random.randint(1000, 9999)}"
        os.rename(file, temp_name)
        temp_names.append(temp_name)
    
    # Phase 2: Rename from temporary names to final names
    for i, temp_name in enumerate(temp_names):
        new_name = new_names[i]
        os.rename(temp_name, new_name)
        original_name = video_files[i]
        print(f"Renamed '{original_name}' to '{new_name}'")
    
    print(f"Renamed {len(video_files)} video files.")

if __name__ == "__main__":
    main()