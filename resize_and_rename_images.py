#!/usr/bin/env python3
"""
Resize images to smaller resolution for token-efficient review.
Creates a 'thumbnails' folder with reduced-size versions (800px max width).
"""

import os
from PIL import Image
from pathlib import Path

images_dir = Path("/home/yessenia/Documents/Universe.Expansion/images")
thumbnails_dir = images_dir / "thumbnails"

# Create thumbnails directory if it doesn't exist
thumbnails_dir.mkdir(exist_ok=True)

# Get all PNG files
png_files = sorted(images_dir.glob("*.png"))

print(f"Found {len(png_files)} images to process.\n")

for img_path in png_files:
    if img_path.parent == thumbnails_dir:
        continue

    try:
        img = Image.open(img_path)
        original_size = img.size

        # Resize to max 800px width, maintaining aspect ratio
        max_width = 800
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        else:
            img_resized = img

        # Save to thumbnails folder
        thumb_path = thumbnails_dir / img_path.name
        img_resized.save(thumb_path, quality=85, optimize=True)

        original_mb = img_path.stat().st_size / (1024 * 1024)
        thumb_mb = thumb_path.stat().st_size / (1024 * 1024)
        reduction = (1 - thumb_mb / original_mb) * 100

        print(f"{img_path.name}")
        print(f"  Original: {original_size} ({original_mb:.2f} MB)")
        print(f"  Resized:  {img_resized.size} ({thumb_mb:.2f} MB, {reduction:.1f}% smaller)\n")

    except Exception as e:
        print(f"Error processing {img_path.name}: {e}\n")

print(f"Thumbnails saved to: {thumbnails_dir}")
print("\nNext step: Review thumbnails and provide purpose/description for each.")
print("Then run: python scripts/apply_image_renames.py")
