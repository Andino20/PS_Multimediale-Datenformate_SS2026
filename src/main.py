import typer
from tqdm import tqdm
from pathlib import Path
import subprocess

out_dir = Path('/images/out')
tmp_dir = Path('/images/out/tmp')

def run_jxl_tool(quality: int, path: Path):
    out_file = out_dir / (path.stem + '.jxl')
    subprocess.run(['cjxl', str(path), str(out_file), '-q', str(quality)], 
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

def main(file_paths: list[str]):
    out_dir.mkdir(parents=True, exist_ok=True)

    for path in tqdm([Path(x) for x in file_paths]):
        if path.exists():
            run_jxl_tool(20, path)

if __name__ == "__main__":
    typer.run(main)