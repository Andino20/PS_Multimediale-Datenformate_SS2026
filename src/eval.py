import pyiqa
from pathlib import Path
import pandas as pd
from tqdm import tqdm

IQMS = {
    'brisque': pyiqa.create_metric('brisque'),
    'niqe': pyiqa.create_metric('niqe'),
    'nima': pyiqa.create_metric('nima'),
    'clip': pyiqa.create_metric('clipiqa')
}

FORMATS = ['jpeg', 'j2k', 'jxl', 'jxr']
SIZES = [25000, 50000, 75000, 100000, 125000, 150000, 175000]

IMG_DIR = Path('../imgs')

data_rows = []

for fmt in FORMATS:
    format_path = IMG_DIR / f'{fmt}_dec'

    for size in SIZES:
        format_size_path = format_path / str(size)
        
        # Ensure the directory exists before attempting to glob
        if not format_size_path.exists():
            print(f"Skipping missing directory: {format_size_path}")
            continue
            
        # Get all PNG files in the subfolder
        img_paths = list(format_size_path.glob('*.png'))
        
        for img_path in tqdm(img_paths, desc=f'Running IQMs on {fmt.capitalize()}@{size} images'):
            image_id = img_path.stem  # e.g., 'image_001'
            
            # Base row dictionary containing our metadata
            row = {
                'image_id': image_id,
                'format': fmt,
                'target_size': size,
                'file_path': str(img_path)
            }
            
            # Run every metric on the current single image
            for iqm_name, metric in IQMS.items():
                try:
                    score_tensor = metric(str(img_path))
                    # Extract the scalar float value from the PyTorch tensor
                    row[iqm_name] = score_tensor.item()
                except Exception as e:
                    print(f"Error computing {iqm_name} on {img_path.name}: {e}")
                    row[iqm_name] = None
            
            data_rows.append(row)

df = pd.DataFrame(data_rows)

print("\nFirst few rows of the collected data:")
print(df.head())

df.to_csv('metrics.csv', index=False)
