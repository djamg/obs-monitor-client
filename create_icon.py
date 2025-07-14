#!/usr/bin/env python3
"""
Create a simple icon for the OBS Monitor Client
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application"""
    # Create a 256x256 image with a dark background
    size = 256
    img = Image.new('RGBA', (size, size), (24, 25, 42, 255))  # Dark background
    draw = ImageDraw.Draw(img)
    
    # Draw a simple monitor icon
    # Monitor frame
    monitor_width = 180
    monitor_height = 120
    x = (size - monitor_width) // 2
    y = (size - monitor_height) // 2 - 20
    
    # Monitor screen
    draw.rectangle([x, y, x + monitor_width, y + monitor_height], 
                  fill=(167, 139, 250, 255), outline=(230, 230, 240, 255), width=3)
    
    # Monitor stand
    stand_width = 40
    stand_height = 30
    stand_x = (size - stand_width) // 2
    stand_y = y + monitor_height
    draw.rectangle([stand_x, stand_y, stand_x + stand_width, stand_y + stand_height], 
                  fill=(230, 230, 240, 255))
    
    # Status indicator dot
    dot_size = 12
    dot_x = x + monitor_width - 20
    dot_y = y + 15
    draw.ellipse([dot_x, dot_y, dot_x + dot_size, dot_y + dot_size], 
                 fill=(76, 175, 80, 255))  # Green dot for "monitoring"
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✓ Icon created: icon.ico")

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw
        create_icon()
    except ImportError:
        print("Pillow not installed. Installing...")
        import subprocess
        import sys
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'Pillow'])
        create_icon() 