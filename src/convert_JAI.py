import os
import sys
import subprocess
from PIL import Image

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.width, img.height

def run_encoder(image_path, output_path, bpp_m100):
    """Runs the JPEG AI encoder with the given target_bpp multiplied by 100."""
    cmd = [
        "python", "-m", "src.reco.coders.encoder",
        image_path,
        output_path,
        "--set_target_bpp", str(int(round(bpp_m100))),
        "--cfg", "cfg/tools_on.json", "cfg/profiles/base.json"
    ]
    
    print(f"-> Running encoder with --set_target_bpp {int(round(bpp_m100))}...")
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(f"Error running encoder:\n{result.stderr}")
        sys.exit(1)

def smart_compress(image_path, output_path, target_size_kb):
    target_size_bytes = target_size_kb * 1000
    width, height = get_image_dimensions(image_path)
    total_pixels = width * height
    
    target_bpp = (target_size_bytes * 8) / total_pixels
    bpp_m100 = target_bpp * 100
    
    print(f"Image dimensions: {width}x{height} ({total_pixels} pixels)")
    print(f"Target size: {target_size_kb} KB ({target_size_bytes} bytes)")
    print(f"Calculated baseline BPP*100: {bpp_m100:.2f}")
    print("-" * 50)

    run_encoder(image_path, output_path, bpp_m100)
    current_size = os.path.getsize(output_path)
    print(f"Initial compression result: {current_size / 1000:.2f} KB")

    attempts = 0
    max_attempts = 20
    
    # CASE 1: Size is too large -> Downwards search until we are under budget
    if current_size > target_size_bytes:
        while current_size > target_size_bytes and attempts < max_attempts:
            attempts += 1
            bpp_m100 -= 1
            print(f"\n[Attempt {attempts}] Size ({current_size/1000:.2f} KB) exceeds budget. Decreasing bit rate to {int(round(bpp_m100))}...")
            run_encoder(image_path, output_path, bpp_m100)
            current_size = os.path.getsize(output_path)
            print(f"New compression result: {current_size / 1000:.2f} KB")

    # CASE 2: Size is under budget -> Upwards search to get as close as possible
    else:
        while current_size <= target_size_bytes and attempts < max_attempts:
            # Save the current valid state before pushing higher
            last_valid_bpp = bpp_m100
            last_valid_size = current_size
            
            attempts += 1
            bpp_m100 += 1
            print(f"\n[Attempt {attempts}] Size ({current_size/1000:.2f} KB) under budget. Increasing bit rate to {int(round(bpp_m100))}...")
            run_encoder(image_path, output_path, bpp_m100)
            current_size = os.path.getsize(output_path)
            print(f"New compression result: {current_size / 1000:.2f} KB")
            
            # If the increase pushed us over budget, roll back to the last valid step and stop
            if current_size > target_size_bytes:
                print(f"\nExceeded budget ({current_size/1000:.2f} KB). Rolling back to bpp_m100: {int(round(last_valid_bpp))}")
                run_encoder(image_path, output_path, last_valid_bpp)
                current_size = last_valid_size
                break
        
    print("-" * 50)
    if current_size <= target_size_bytes:
        print(f"SUCCESS! Final file size: {current_size / 1000:.2f} KB (Under budget by {(target_size_bytes - current_size)/1000:.2f} KB)")
    else:
        print(f"FAILED to meet strict target. Closest achieved size: {current_size / 1000:.2f} KB")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python smart_compress.py <INPUT_PNG> <OUTPUT_BITSTREAM> <TARGET_SIZE_IN_KB>")
        sys.exit(1)
        
    input_png = sys.argv[1]
    output_bitstream = sys.argv[2]
    target_kb = float(sys.argv[3])
    
    smart_compress(input_png, output_bitstream, target_kb)