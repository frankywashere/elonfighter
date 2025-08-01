#!/usr/bin/env python3
"""
Scale down Elon's throw sprite by 20%
"""

from PIL import Image
import os

def scale_sprite(input_path, output_path, scale_factor=0.8):
    """Scale down a sprite by the given factor."""
    img = Image.open(input_path)
    
    # Calculate new dimensions
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)
    
    # Resize with high-quality resampling
    scaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save with same format
    scaled_img.save(output_path, 'PNG')
    
    print(f"Scaled {input_path}")
    print(f"  Original: {img.width}x{img.height}")
    print(f"  New: {new_width}x{new_height}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Scale Elon's throw sprite
    elon_throw = os.path.join(base_dir, 'elon/Elon1_normalized_v3/throw.png')
    
    if os.path.exists(elon_throw):
        # Create backup first
        backup_path = elon_throw.replace('.png', '_backup.png')
        img = Image.open(elon_throw)
        img.save(backup_path)
        print(f"Created backup: {backup_path}")
        
        # Scale down by 20% (scale factor 0.8)
        scale_sprite(elon_throw, elon_throw, 0.8)
    else:
        print(f"Error: {elon_throw} not found!")

if __name__ == "__main__":
    main()