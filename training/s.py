import os
from PIL import Image, ImageDraw

def create_a4_page():
    print("Initializing A4 Page canvas generation...")
    
    # Standard dimensions for A4 at 300 DPI
    DPI = 300
    width_px = 2480
    height_px = 3508
    
    # 1. Create canvas structure securely
    try:
        a4_image = Image.new("RGB", (width_px, height_px), color="white")
        draw = ImageDraw.Draw(a4_image)
        
        # 2. Draw mock template items to guarantee data density
        # Outer boundary margin
        draw.rectangle([100, 100, width_px - 100, height_px - 100], outline="black", width=10)
        
        # Synthesize horizontal lines across the canvas
        for y in range(300, height_px - 300, 150):
            draw.line([(200, y), (width_px - 200, y)], fill="blue", width=4)
            
        # 3. Define definitive file output destinations
        local_filename = "synthetic_a4_page.png"
        shared_dest = "/sdcard/Download/synthetic_a4_page.png"
        
        # Save locally inside the project folder first
        a4_image.save(local_filename, format="PNG", dpi=(DPI, DPI))
        print(f"Success! Local file saved: {os.path.abspath(local_filename)}")
        print(f"Local file payload size: {os.path.getsize(local_filename)} bytes")
        
        # Attempt direct save to Android Downloads if permissions allow
        if os.path.exists("/sdcard/"):
            a4_image.save(shared_dest, format="PNG", dpi=(DPI, DPI))
            print(f"Success! Shared file pushed directly to: {shared_dest}")
            
    except Exception as e:
        print(f"🚨 CRITICAL RUNTIME ERROR: {str(e)}")

if __name__ == "__main__":
    create_a4_page()

