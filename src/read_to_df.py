import re
from pathlib import Path
from tqdm import tqdm
import pyiqa
import pandas as pd

IQMS = {
    'brisque': pyiqa.create_metric('brisque'),
    'niqe': pyiqa.create_metric('niqe'),
    'nima': pyiqa.create_metric('nima'),
    'clip': pyiqa.create_metric('clipiqa')
}

def extract_file_info(decoded_path, encoded_path) -> pd.DataFrame:
    dir_path = Path(decoded_path)

    if not dir_path.is_dir():
        print(f"Error: The directory '{decoded_path}' does not exist.")
        return

    # (\w+)        -> JPEG variant
    # ([0-9]+)     -> target size in KB
    # (.+)         -> actual filename (everything else before .png)
    # \.png$       -> extension
    pattern = re.compile(r"^(\w+)_([0-9]+)_(.+)\.png$")

    data = []
    for file_path in tqdm(list(dir_path.iterdir()), desc='Processing images...'):
        if file_path.is_file():
            match = pattern.match(file_path.name)

            if match:
                row = {
                    'jpeg_variant': match.group(1),
                    'target_size_kb': match.group(2),
                    'image_name': match.group(3),
                    'decoded_size_kb': file_path.stat().st_size / 1024,
                }

                encoded_file_path = Path(encoded_path) / (file_path.stem + '.' + row['jpeg_variant'])
                row['encoded_size_kb'] = encoded_file_path.stat().st_size / 1024

                for iqm_name, metric in IQMS.items():
                    try:
                        score_tensor = metric(str(file_path))
                        row[iqm_name] = score_tensor.item() # Extract the scalar float value from the PyTorch tensor
                    except Exception as e:
                        print(f"Error computing {iqm_name} on {file_path.name}: {e}")
                        row[iqm_name] = None
                
                data.append(row)

    return pd.DataFrame(data)

decoded_path = "../imgs/decoded"
encoded_path = "../imgs/encoded"
df = extract_file_info(decoded_path, encoded_path)
df.to_csv('data.csv', index=False)
