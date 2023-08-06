# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['watermark']
setup_kwargs = {
    'name': 'watermark.py',
    'version': '0.0.2',
    'description': 'A convinient python wrapper around ffmpeg to apply watermarks to images, gifs and videos.',
    'long_description': '# watermark.py\n\nA convinient python wrapper around `ffmpeg` to apply\nwatermarks to images, gifs and videos.\n\n## Installation\n\n```shell\npip install watermark.py\n```\n\nYou need to install  [`ffmpeg`](https://ffmpeg.org/) seperately.\n\n## Usage\n\n<!-- ### GUI\n\nVisit watermark.py.aahnik.dev to experience the web app.\n\n### CLI\n\nYou can use the command-line interface to easily apply watermark.\n\n```shell\nwatermark --help\n``` -->\n\n<!-- ### Python -->\n\n```python\nfrom watermark import File, Watermark, apply_watermark\n\nvideo = File("vid.mp4")\nwatermark = Watermark("im.png")\n\napply_watermark(video, watermark)\n```\n\n<!-- ## Used by\n\n- tgcf\n- telewater -->\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/watermark.py',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
