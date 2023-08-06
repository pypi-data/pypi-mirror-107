#!/usr/bin/env python

# MIT License
# Copyright (c) 2021 Aahnik Daw

import os

from enum import Enum


class Position(str,Enum):
    top_left = "10:10"
    top_right = "W-w-10:10"
    centre = "(W-w)/2:(H-h)/2"
    bottom_left = "10:H-h-10"
    bottom_right = "W-w-10:H-h-10"


class File:
    def __init__(self, path):
        self.path = path
        self.type = self.find_type()

    def find_type(self):
        ext = self.path.split(".")[-1]
        if ext in ["png", "jpeg", "jpg"]:
            return "image"
        elif ext in ["mp4", "gif"]:
            return "video"
        else:
            raise Exception(f"File type {ext} not supported.")


class Watermark:
    def __init__(
        self,
        overlay: File,
        pos: str = Position.centre,
    ):
        self.overlay = overlay
        self.pos = pos


def apply_watermark(
    file: File,
    wtm: Watermark,
    output_file: str = "",
    frame_rate: int = 15,
    preset: str = "ultrafast",
) -> str:

    if not output_file:
        output_file = f"watered_{file.path}"

    command = f'ffmpeg -i {file.path} \
        -i {wtm.overlay.path} \
        -an -dn -sn -r {frame_rate} \
        -preset {preset} \
        -tune zerolatency  -tune fastdecode \
        -filter_complex "overlay={wtm.pos}" \
        {output_file}'

    print(f"Running command {command}")
    os.system(command)
    return output_file
