# Multimedial Datenformate PS

**Thema**: JPEG, JPEG2000, JPEG XR, JPEG XL, JPEG AI compression to a fixed file size; evaluation with no reference image quality metrics (IQM).

## Running

**Linux**: `$ ./run.sh images/in/*.png`

**Windows (CMD)**: `run.bat images/in/*.png`

## Tools  

**JPEG**: `cjpeg -quality X`

**JPEG2000**: `opj_compress -r 20`

**JPEG XL**: `cjxl --target_size=51200`

**JPEG XR**: `JxrEncApp -q 0.5`

**JPEG AI**: TBD

## Image Quality Metrics (no-reference)

General Information: [nfdi4ing.de](https://quality.nfdi4ing.de/en/latest/index.html), all IQMs are implemented in MATLAB.

**NIQE**: *Naturalness Image Quality Evaluator* ([link](https://quality.nfdi4ing.de/en/latest/image_quality/NIQE.html))

**BRISQUE**: *Blind/Referenceless Image Spatial Quality Evaluator* ([link](https://zenodo.org/records/11104461)) ([library](pypi.org/project/brisque/))

**PIQE**: *Perception based Image Quality Evaluator* ([link](https://quality.nfdi4ing.de/en/latest/image_quality/PIQE.html))

## Building Docker Image

`docker buildx build -t mmdf:latest .`