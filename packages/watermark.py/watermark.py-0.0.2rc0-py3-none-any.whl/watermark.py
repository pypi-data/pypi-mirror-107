from enum import Enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module
import logging
import os

from PIL import Image


def to_png(file: str) -> str:
    im = Image.open(file)
    if not file.endswith(".png"):
        png_file = f"{file}.png"
        im.save(png_file)
    else:
        png_file = file

    return png_file


def _open_image(file: str):
    im = Image.open(file)
    logging.info(
        f"""Opened Image {file}
        Image format {im.format}
        Mode {im.mode}
        Size {im.size}
            Height {im.height}
            Width {im.width}
    """
    )
    im = im.convert("RGBA")

    return im


def watermark_image(
    image_file: str, watermark_file: str = "image.png", x_off: int = 10, y_off: int = 10
):
    png = to_png(image_file)
    im = _open_image(png)
    wt = _open_image(watermark_file)
    im.alpha_composite(im=wt, dest=(x_off, y_off))
    output_file = f"watered_{png}"
    im.save(output_file)
    try:
        os.remove(png)
    except:
        pass
    return output_file


def watermark_video(
    video_file: str,
    watermark_file: str = "image.png",
    frame_rate: int = 15,
    preset: str = "ultrafast",
    x_off: int = 10,
    y_off: int = 10,
) -> None:
    """Apply watermark to video or gifs"""
    output_file = f"watered_{video_file}"
    command = f'ffmpeg -i {video_file} \
        -i {watermark_file} \
        -an -dn -sn -r {frame_rate} \
        -preset {preset} \
        -tune zerolatency  -tune fastdecode \
        -filter_complex "overlay={x_off}:{y_off}" \
        {output_file}'

    logging.info(f"Running command {command}")
    os.system(command)
    return output_file


class XOff(str, Enum):
    left = "left"
    mid = "mid"
    right = "right"


class YOff(str, Enum):
    top = "top"
    mid = "mid"
    bottom = "bottom"


class Preset(str, Enum):
    ultrafast = "ultrafast"


class Watermark(BaseModel):
    image: str = "image.png"
    x_off: XOff = XOff.mid
    y_off: YOff = YOff.mid
    preset: Preset = Preset.ultrafast
    frame_rate: int = 15
    # only applicable if the object to be watermarked is a video


class File:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def apply(self, watermark: Watermark):
        pass
