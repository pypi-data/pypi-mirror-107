# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['watermark_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'watermark.py',
    'version': '0.0.1rc0',
    'description': 'A convinient python library to apply watermarks to images, gifs and videos.',
    'long_description': '# watermark.py\n\nA convinient python library to apply watermarks to images, gifs and videos.\n\n## Installation\n\n```shell\npip install watermark.py\n```\n\n## Dependancies\n\nYou need to install these seperately.\n\n- `ffmpeg` for watermarking videos.\n- `Pillow` for watermarking images.\n\n## Usage\n\n```python\nfrom watermark_py import File,Watermark\n\nfile = File("path to file")\nwatermark = Watermark("path to image",x_off,y_off)\n\nfile.apply(watermark)\n```\n\n## Used by\n\n- tgcf\n- telewater\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/watermark.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
