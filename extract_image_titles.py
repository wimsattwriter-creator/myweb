#!/usr/bin/env python3
"""
Extract titles/descriptions from images and create a mapping file.
Uses pytesseract for OCR or manual entry fallback.
"""

import json
import os
from pathlib import Path
from PIL import Image
import re

images_dir = Path("/home/yessenia/Documents/Universe.Expansion/images")
thumbnails_dir = images_dir / "thumbnails"
mapping_file = images_dir / "image_mapping.json"

# Try to use OCR if available
try:
    import pytesseract
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("pytesseract not available. Will provide manual entry option.\n")

png_files = sorted(thumbnails_dir.glob("*.png"))
mapping = {}

print(f"Processing {len(png_files)} images...\n")

for i, img_path in enumerate(png_files, 1):
    print(f"\n[{i}/{len(png_files)}] {img_path.name}")

    # Try OCR extraction if available
    title = None
    if HAS_OCR:
        try:
            img = Image.open(img_path)
            text = pytesseract.image_to_string(img)
            # Try to find title-like text (usually in caps or first line)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if lines:
                # Prefer lines that are all caps or look like titles
                for line in lines:
                    if len(line) < 100 and (line.isupper() or '&' in line or line.startswith('THE')):
                        title = line
                        break
                if not title and lines:
                    title = lines[0][:80]  # Use first line, truncated
        except Exception as e:
            print(f"  OCR error: {e}")

    # Fallback: ask user
    if not title:
        print(f"  Could not extract title via OCR. View the image and describe its purpose:")
        print(f"  (Or paste the title text you see in the image)")
        title = input("  > ").strip()

    if title:
        # Sanitize for filename
        safe_name = re.sub(r'[^a-z0-9_\-]', '_', title.lower())
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')
        mapping[img_path.name] = {
            "original_filename": img_path.name,
            "title": title,
            "suggested_name": f"{safe_name}.png"
        }
        print(f"  ✓ Title: {title}")
        print(f"  ✓ Suggested: {safe_name}.png")
    else:
        print(f"  ✗ Skipped")

# Save mapping
with open(mapping_file, 'w') as f:
    json.dump(mapping, f, indent=2)

print(f"\n\nMapping saved to: {mapping_file}")
print(f"\nNext step: Review the mapping and then run:")
print(f"  python scripts/apply_image_renames.py")
