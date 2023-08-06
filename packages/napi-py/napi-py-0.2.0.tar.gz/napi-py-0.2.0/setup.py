# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['napi']

package_data = \
{'': ['*']}

install_requires = \
['pylzma>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['napi-py = napi.main:cli_main']}

setup_kwargs = {
    'name': 'napi-py',
    'version': '0.2.0',
    'description': 'CLI tool for downloading subtitles from napiprojekt.pl',
    'long_description': '# napi-py ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/napi-py) ![CI](https://github.com/emkor/napi-py/workflows/CI/badge.svg)\nCLI tool for downloading subtitles from napiprojekt.pl, fork of [gabrys/napi.py](https://github.com/gabrys/napi.py)\n\n## prerequisites\n- Python 3.6.2 or newer\n- on Linux, `python3-dev` package:\n  - for Debian-based systems, use `sudo apt-get install python3-dev`\n\n## installation\n- `pip install napi-py` for user-wide installation\n\n## usage as CLI tool\n- `napi-py ~/Downloads/MyMovie.mp4` will download and save subtitles under `~/Downloads/MyMovie.srt`\n\n## usage as lib\n```python\nfrom napi import NapiPy\n\nmovie_path = "~/Downloads/MyMovie.mp4"\n\nnapi = NapiPy()\nmovie_hash = napi.calc_hash(movie_path)\nsource_encoding, target_encoding, tmp_file = napi.download_subs(movie_hash)\nsubs_path = napi.move_subs_to_movie(tmp_file, movie_path)\nprint(subs_path)\n```\n\n## in case of issues\n- if there are no subs for your movie, there\'s still hope:\n    - open the movie web page on `napiprojekt.pl` in your browser, as in example: `https://www.napiprojekt.pl/napisy1,1,1-dla-55534-Z%C5%82odziejaszki-(2018)`\n    - choose subtitles that might match your movie, right-click them and select "Copy link" on link containing hash, which looks like this `napiprojekt:96edd6537d9852a51cbdd5b64fee9194`\n    - use flag `--hash YOURHASH` in this tool, i.e. `--hash 96edd6537d9852a51cbdd5b64fee9194` or `--hash napiprojekt:96edd6537d9852a51cbdd5b64fee9194`\n\n## development\n- `make install` installs poetry virtualenv\n- `make test` runs tests\n- `make build` creates installable package\n',
    'author': 'emkor93',
    'author_email': 'emkor93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emkor/napi-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
