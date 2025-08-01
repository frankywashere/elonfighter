#!/usr/bin/env python3
"""
Cross-Character Sprite Normalizer
Normalizes all sprites using Elon as the reference, ensuring Trump is properly scaled relative to Elon.
"""

import os
import json
from PIL import Image
import numpy as np

def find_content_bounds(image):
    """Find the bounding box of non-transparent pixels."""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    data = np.array(image)
    alpha = data[:, :, 3]
    
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        return None
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return (cmin, rmin, cmax + 1, rmax + 1)

def normalize_sprites(character_name, input_dir, output_dir, reference_height, trump_scale_factor=1.0):
    """
    Process all sprites for a character with consistent sizing.
    Both characters will be normalized to the same height.
    """
    print(f"\nProcessing {character_name} sprites...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Both characters use the same target height
    target_height = reference_height
    
    print(f"  Target height: {target_height}px")
    
    metadata = {}
    
    # Process all sprites
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"\n  {filename}:")
            
            try:
                img = Image.open(input_path)
                original_width, original_height = img.size
                
                bounds = find_content_bounds(img)
                
                if bounds is None:
                    print(f"    Warning: No visible content found")
                    img.save(output_path)
                    continue
                
                crop_x, crop_y, crop_right, crop_bottom = bounds
                crop_width = crop_right - crop_x
                crop_height = crop_bottom - crop_y
                cropped = img.crop(bounds)
                
                # Calculate scale factor
                scale_factor = target_height / crop_height
                
                # Special handling for certain poses
                if 'crouch' in filename.lower() or 'thrown' in filename.lower():
                    scale_factor *= 0.7
                elif 'jump' in filename.lower():
                    scale_factor *= 0.9
                
                # Calculate new dimensions
                new_width = int(crop_width * scale_factor)
                new_height = int(crop_height * scale_factor)
                
                # Resize the cropped image
                resized = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create standardized canvas
                # Use Elon's reference height for canvas size calculation
                canvas_width = int(reference_height * 1.5)
                canvas_height = int(reference_height * 1.2)
                
                output_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
                
                # Center the sprite on the canvas
                paste_x = (canvas_width - new_width) // 2
                paste_y = canvas_height - new_height  # Align to bottom
                
                output_img.paste(resized, (paste_x, paste_y))
                output_img.save(output_path)
                
                # Store metadata
                sprite_name = filename[:-4]
                metadata[sprite_name] = {
                    'original_size': f"{original_width}x{original_height}",
                    'crop_size': f"{crop_width}x{crop_height}",
                    'final_size': f"{new_width}x{new_height}",
                    'scale_factor': round(scale_factor, 2),
                    'canvas_size': f"{canvas_width}x{canvas_height}"
                }
                
                print(f"    Processed: {crop_width}x{crop_height} -> {new_width}x{new_height} (scale: {scale_factor:.2f})")
                
            except Exception as e:
                print(f"    Error: {e}")
    
    # Save metadata
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

def main():
    """Main function to process all sprites with Elon as reference."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("Cross-Character Sprite Normalization")
    print("=" * 50)
    
    # First, get Elon's reference height
    elon_standing = os.path.join(base_dir, 'elon/Elon1/standing.png')
    if not os.path.exists(elon_standing):
        print("Error: Elon's standing.png not found!")
        return
    
    # Get Elon's character height
    img = Image.open(elon_standing)
    bounds = find_content_bounds(img)
    if bounds:
        elon_height = bounds[3] - bounds[1]
    else:
        elon_height = img.height
    
    print(f"Reference: Elon's standing height = {elon_height}px")
    
    # Process both characters
    characters = [
        ('elon', 'elon/Elon1', 'elon/Elon1_normalized_v3'),
        ('trump', 'trump1', 'trump1_normalized_v3')
    ]
    
    for char_name, input_dir, output_dir in characters:
        input_path = os.path.join(base_dir, input_dir)
        output_path = os.path.join(base_dir, output_dir)
        
        if os.path.exists(input_path):
            normalize_sprites(char_name, input_path, output_path, elon_height)
        else:
            print(f"\nSkipping {char_name}: Directory not found")
    
    print("\n" + "=" * 50)
    print("Normalization complete!")
    print("\nBoth characters now have the same height:")
    print("  - All sprites normalized to consistent sizing")
    print("  - Same canvas dimensions for smooth animations")
    print("  - Proper alignment maintained across all poses")

if __name__ == "__main__":
    main()