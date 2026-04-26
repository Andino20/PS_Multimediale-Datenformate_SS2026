import typer
from tqdm import tqdm
from pathlib import Path
from collections.abc import Callable
import subprocess

out_dir = Path('imgs')

def get_out_file_path(img: Path, extension: str) -> Path:
    return out_dir / img.with_suffix(extension).name

def jpeg_tool(img: Path, quality: int) -> int:
    out_file = get_out_file_path(img=img, extension='.jpeg')
    with open(out_file, "wb") as f:
        subprocess.run(['cjpeg', '-quality', str(quality), str(img)], 
                    stdout=f,
                    stderr=subprocess.DEVNULL)
    return out_file.stat().st_size

def j2k_tool(img: Path, quality: int) -> int:
    out_file = get_out_file_path(img=img, extension='.j2k')
    subprocess.run(['opj_compress', '-r', str(101 - quality), '-i', str(img), '-o', str(out_file)], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
    return out_file.stat().st_size

def jxl_tool(img: Path, quality: int) -> int:
    out_file = get_out_file_path(img=img, extension='.jxl')
    subprocess.run(['cjxl', str(img), str(out_file), '-q', str(quality)], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
    return out_file.stat().st_size

def jxr_tool(img: Path, quality: int) -> int:
    out_file = get_out_file_path(img=img, extension='.jxr')
    subprocess.run(['JxrEncApp', '-q', str(quality / 100.0), '-i', str(img), '-o', str(out_file)], 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
    return out_file.stat().st_size

def run_tool(img: Path, target_size: int, tool: Callable[[Path, int], int]):
    left = 1
    right = 101
    
    size = 0
    mid = 0
    while left + 1 < right:
        mid = (left + right) // 2
        size = tool(img, mid)

        if size == target_size:
            break
        elif size < target_size:
            left = mid
        elif size > target_size:
            right = mid

    size = tool(img, left)
    if size > target_size:
        print(f'Failed to compress {img} to {target_size}B. left = {left} & right = {right}')

def main(tool: str, target_size: int, file_paths: list[Path]):
    available_tools = ['jpeg', 'j2k', 'jxl', 'jxr']
    assert tool in available_tools, 'Tool has to be one of jpeg, j2k, jxl or jxr'
    
    global out_dir
    out_dir = Path(*['imgs', 'out', tool, str(target_size)])
    out_dir.mkdir(parents=True, exist_ok=True)

    for img in tqdm(file_paths, f'{tool} conversion to {target_size}B'):
        if not img.is_file() and img.suffix == '.ppm':
            pass
        
        if tool == 'jpeg':
            run_tool(img, target_size, jpeg_tool)
        elif tool == 'j2k':
            run_tool(img, target_size, j2k_tool)
        elif tool == 'jxl':
            run_tool(img, target_size, jxl_tool)
        elif tool == 'jxr':
            run_tool(img, target_size, jxr_tool)

if __name__ == "__main__":
    typer.run(main)