#!/usr/bin/env python3
"""
Advanced Sprite Normalizer - Ensures consistent character sizing across all sprites
by using a reference sprite and maintaining proper height ratios.
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
    
    # Find non-transparent pixels (alpha > 10 to ignore very faint pixels)
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        return None
    
    # Find the bounding box
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return (cmin, rmin, cmax + 1, rmax + 1)

def get_character_height(image_path):
    """Get the actual character height from an image."""
    img = Image.open(image_path)
    bounds = find_content_bounds(img)
    if bounds:
        return bounds[3] - bounds[1]  # height
    return img.height

def normalize_character_sprites(character_name, input_dir, output_dir, target_height=None):
    """Process all sprites for a character with consistent sizing."""
    print(f"\nProcessing {character_name} sprites...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # First pass: Find reference height from standing sprite
    reference_sprite = 'standing.png'
    reference_path = os.path.join(input_dir, reference_sprite)
    
    if not os.path.exists(reference_path):
        print(f"  Warning: No standing.png found, using first available sprite as reference")
        # Find first available sprite
        for filename in os.listdir(input_dir):
            if filename.lower().endswith('.png'):
                reference_path = os.path.join(input_dir, filename)
                reference_sprite = filename
                break
    
    if target_height is None:
        # Get the character height from reference sprite
        ref_img = Image.open(reference_path)
        ref_bounds = find_content_bounds(ref_img)
        if ref_bounds:
            target_height = ref_bounds[3] - ref_bounds[1]
            print(f"  Reference sprite: {reference_sprite}")
            print(f"  Target height: {target_height}px")
        else:
            target_height = ref_img.height
            print(f"  Warning: Could not detect bounds in reference, using full height: {target_height}px")
    
    metadata = {}
    
    # Second pass: Process all sprites with consistent scaling
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"\n  {filename}:")
            
            try:
                # Open the image
                img = Image.open(input_path)
                original_width, original_height = img.size
                
                # Find content bounds
                bounds = find_content_bounds(img)
                
                if bounds is None:
                    print(f"    Warning: No visible content found")
                    img.save(output_path)
                    continue
                
                # Crop to content
                crop_x, crop_y, crop_right, crop_bottom = bounds
                crop_width = crop_right - crop_x
                crop_height = crop_bottom - crop_y
                cropped = img.crop(bounds)
                
                # Calculate scale factor to match target height
                scale_factor = target_height / crop_height
                
                # Special handling for certain sprites
                if 'crouch' in filename.lower() or 'thrown' in filename.lower():
                    # These sprites should be shorter
                    scale_factor *= 0.7
                elif 'jump' in filename.lower():
                    # Jump sprites might need different scaling
                    scale_factor *= 0.9
                
                # Calculate new dimensions
                new_width = int(crop_width * scale_factor)
                new_height = int(crop_height * scale_factor)
                
                # Resize the cropped image
                resized = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create output image with standard dimensions
                # Make canvas large enough for any sprite
                canvas_width = int(target_height * 1.5)  # Wide enough for kicks
                canvas_height = int(target_height * 1.2)  # Tall enough for jumps
                
                output_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
                
                # Center the sprite on the canvas
                paste_x = (canvas_width - new_width) // 2
                paste_y = canvas_height - new_height  # Align to bottom
                
                output_img.paste(resized, (paste_x, paste_y))
                
                # Save the normalized image
                output_img.save(output_path)
                
                # Store metadata
                sprite_name = filename[:-4]
                metadata[sprite_name] = {
                    'original_width': int(original_width),
                    'original_height': int(original_height),
                    'crop_x': int(crop_x),
                    'crop_y': int(crop_y),
                    'crop_width': int(crop_width),
                    'crop_height': int(crop_height),
                    'scale_factor': float(scale_factor),
                    'canvas_width': canvas_width,
                    'canvas_height': canvas_height,
                    'paste_x': paste_x,
                    'paste_y': paste_y
                }
                
                print(f"    Original: {original_width}x{original_height}")
                print(f"    Cropped: {crop_width}x{crop_height}")
                print(f"    Scaled: {new_width}x{new_height} (factor: {scale_factor:.2f})")
                print(f"    Canvas: {canvas_width}x{canvas_height}")
                
            except Exception as e:
                print(f"    Error processing: {e}")
    
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
        ('elon', 'elon/Elon1', 'elon/Elon1_normalized_v2'),
        ('trump', 'trump1', 'trump1_normalized_v2')
    ]
    
    print("Advanced Sprite Normalization Tool")
    print("=" * 50)
    
    for char_name, input_dir, output_dir in characters:
        input_path = os.path.join(base_dir, input_dir)
        output_path = os.path.join(base_dir, output_dir)
        
        if os.path.exists(input_path):
            normalize_character_sprites(char_name, input_path, output_path)
        else:
            print(f"\nSkipping {char_name}: Directory {input_path} not found")
    
    print("\n" + "=" * 50)
    print("Normalization complete!")
    print("\nAll sprites now have consistent sizing:")
    print("  - Same character height across all poses")
    print("  - Centered on standardized canvas")
    print("  - Ready for use without further scaling")

if __name__ == "__main__":
    main()