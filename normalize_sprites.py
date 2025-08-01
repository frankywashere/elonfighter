#!/usr/bin/env python3
"""
Sprite Normalizer - Preprocesses PNG sprites by removing transparent padding
and saving normalized versions with metadata.
"""

import os
import json
from PIL import Image
import numpy as np

def find_content_bounds(image):
    """Find the bounding box of non-transparent pixels."""
    # Convert to RGBA if not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get pixel data as numpy array
    data = np.array(image)
    
    # Get alpha channel
    alpha = data[:, :, 3]
    
    # Find non-transparent pixels (alpha > 10 to ignore very faint pixels)
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        # Image is fully transparent
        return None
    
    # Find the bounding box
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return (cmin, rmin, cmax + 1, rmax + 1)

def normalize_sprite(input_path, output_path):
    """Normalize a single sprite by cropping transparent padding."""
    try:
        # Open the image
        img = Image.open(input_path)
        original_width, original_height = img.size
        
        # Find content bounds
        bounds = find_content_bounds(img)
        
        if bounds is None:
            print(f"  Warning: {input_path} appears to be fully transparent")
            # Just copy the original
            img.save(output_path)
            return {
                'original_width': int(original_width),
                'original_height': int(original_height),
                'crop_x': 0,
                'crop_y': 0,
                'crop_width': int(original_width),
                'crop_height': int(original_height),
                'center_offset_x': 0.0,
                'center_offset_y': 0.0
            }
        
        # Crop the image
        cropped = img.crop(bounds)
        crop_x, crop_y, crop_right, crop_bottom = bounds
        crop_width = crop_right - crop_x
        crop_height = crop_bottom - crop_y
        
        # Calculate center offsets for proper alignment
        original_center_x = original_width / 2
        original_center_y = original_height
        new_center_x = crop_width / 2
        new_center_y = crop_height
        center_offset_x = (crop_x + new_center_x) - original_center_x
        center_offset_y = (crop_y + new_center_y) - original_center_y
        
        # Save the cropped image
        cropped.save(output_path)
        
        metadata = {
            'original_width': int(original_width),
            'original_height': int(original_height),
            'crop_x': int(crop_x),
            'crop_y': int(crop_y),
            'crop_width': int(crop_width),
            'crop_height': int(crop_height),
            'center_offset_x': float(center_offset_x),
            'center_offset_y': float(center_offset_y)
        }
        
        print(f"  Normalized: {original_width}x{original_height} -> {crop_width}x{crop_height}")
        print(f"  Offset: ({center_offset_x:.1f}, {center_offset_y:.1f})")
        
        return metadata
        
    except Exception as e:
        print(f"  Error processing {input_path}: {e}")
        return None

def process_character_sprites(character_name, input_dir, output_dir):
    """Process all sprites for a character."""
    print(f"\nProcessing {character_name} sprites...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    metadata = {}
    
    # Process all PNG files in the directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"\n  {filename}:")
            sprite_metadata = normalize_sprite(input_path, output_path)
            
            if sprite_metadata:
                # Store metadata without .png extension
                sprite_name = filename[:-4]
                metadata[sprite_name] = sprite_metadata
    
    # Save metadata
    metadata_path = os.path.join(output_dir, 'sprite_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n  Saved metadata to {metadata_path}")

def main():
    """Main function to process all character sprites."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Characters to process
    characters = [
        ('elon', 'elon/Elon1', 'elon/Elon1_normalized'),
        ('trump', 'trump1', 'trump1_normalized')
    ]
    
    print("Sprite Normalization Tool")
    print("=" * 50)
    
    for char_name, input_dir, output_dir in characters:
        input_path = os.path.join(base_dir, input_dir)
        output_path = os.path.join(base_dir, output_dir)
        
        if os.path.exists(input_path):
            process_character_sprites(char_name, input_path, output_path)
        else:
            print(f"\nSkipping {char_name}: Directory {input_path} not found")
    
    print("\n" + "=" * 50)
    print("Normalization complete!")
    print("\nTo use normalized sprites, update your game to use:")
    print("  - elon/Elon1_normalized/ instead of elon/Elon1/")
    print("  - trump1_normalized/ instead of trump1/")

if __name__ == "__main__":
    main()