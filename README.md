# Multimedial Datenformate PS

**Thema**: JPEG, JPEG2000, JPEG XR, JPEG XL, JPEG AI compression to a fixed file size; evaluation with no reference image quality metrics (IQM).

## Running

There are two run scripts that start a docker container with all JPEG tools installed and that runs `src/main.py` with the given arguments. You would typically pass in an array of path to images that should get compressed. Both scripts assume that the docker image is called `mmdf:latest`, where `mmdf` is short for the lecture title "Multimediale Datenformate". 

**Linux**: `$ ./run.sh <image_folder>/*.png`

**Windows (CMD)**: `run.bat <image_folder>/*.png`

## Tools  

**JPEG**: `cjpeg -quality [0..100] fox.ppm > fox.jpeg`, formats: PPM (PBMPLUS color format), PGM (PBMPLUS gray-scale format), BMP, Targa

**JPEG2000**: `opj_compress -r [1..] -i fox.ppm -o fox.j2k`, formats: PBM, PGM, PPM, PNM, PAM, PGX, PNG, BMP, TIF, TIFF, RAW, YUV, RAWL, TGA

**JPEG XL**: `cjxl fox.ppm fox.jxl -q [1..100]`, formats: JXL, PPM, PNM, PFM, PAM, PGX, PNG, APNG, GIF, JPEG, EXR

**JPEG XR**: `JxrEncApp -q [0.0 .. 1.0] -i fox.ppm -o fox.jxr`, formats: BMP, PNM, TIF, HDR

**JPEG AI**: TBD

## Image Quality Metrics (no-reference)

General Information: [nfdi4ing.de](https://quality.nfdi4ing.de/en/latest/index.html), all IQMs are implemented in MATLAB.

**NIQE**: *Naturalness Image Quality Evaluator* ([link](https://quality.nfdi4ing.de/en/latest/image_quality/NIQE.html))

**BRISQUE**: *Blind/Referenceless Image Spatial Quality Evaluator* ([link](https://zenodo.org/records/11104461)) ([library](pypi.org/project/brisque/))

**PIQE**: *Perception based Image Quality Evaluator* ([link](https://quality.nfdi4ing.de/en/latest/image_quality/PIQE.html))

## Building Docker Image

The docker image consists of a debian python installation and several JPEG conversion tool, as well as all the python packages listed in `requirements.txt`.

**Build Image**: `docker buildx build -t mmdf:latest .`

## Dataset

Possible image dataset candidates, pay attention to similiar original image file sizes.
- [test_images](https://github.com/jhcloos/test_images) by jhcloos. HQ PPM images, ~50 images
- TBD