# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['watermark']
setup_kwargs = {
    'name': 'watermark.py',
    'version': '0.0.3.post1',
    'description': 'A convenient python wrapper around FFmpeg to apply watermarks to images, gifs, and videos.',
    'long_description': '# watermark.py\n\n![PyPI](https://img.shields.io/pypi/v/watermark.py)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/watermark.py)\n\nA convenient python wrapper around FFmpeg to apply watermarks to images, gifs,\nand videos.\n\n## Installation\n\n```shell\npip install watermark.py\n```\n\nYou need to install  [`ffmpeg`](https://ffmpeg.org/) seperately.\n\n## Usage\n\n```python\nfrom watermark import File, Watermark, apply_watermark, Position\n\nvideo = File("vid.mp4")\nwatermark = Watermark(File("im.png"), pos=Position.bottom_right)\n\napply_watermark(video, watermark)\n```\n\n## Used by\n\n- [telewater](https://github.com/aahnik/telewater)\nA telegram bot that applies watermark on images, gifs, and videos.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/watermark.py',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
