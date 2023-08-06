# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['watermark']
install_requires = \
['Pillow>=8.2.0,<9.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'watermark.py',
    'version': '0.0.2rc0',
    'description': 'A convinient python library to apply watermarks to images, gifs and videos.',
    'long_description': '# watermark.py\n\nA convinient python library to apply watermarks to images, gifs and videos.\n\n## Installation\n\n```shell\npip install watermark.py\n```\n\n## Dependancies\n\nYou need to install these seperately.\n\n- `ffmpeg` for watermarking videos.\n\n## Usage\n\n```python\nfrom watermark import File,Watermark\n\nfile = File("path to file")\nwatermark = Watermark("path to image",x_off,y_off)\n\nfile.apply(watermark)\n```\n\n## Used by\n\n- tgcf\n- telewater\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/watermark.py',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
