# watermark.py

A convinient python library to apply watermarks to images, gifs and videos.

## Installation

```shell
pip install watermark.py
```

## Dependancies

You need to install these seperately.

- `ffmpeg` for watermarking videos.
- `Pillow` for watermarking images.

## Usage

```python
from watermark_py import File,Watermark

file = File("path to file")
watermark = Watermark("path to image",x_off,y_off)

file.apply(watermark)
```

## Used by

- tgcf
- telewater
