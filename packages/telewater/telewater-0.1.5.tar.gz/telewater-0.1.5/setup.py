# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telewater']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Telethon>=1.21.1,<2.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cryptg>=0.2.post2,<0.3',
 'hachoir>=3.1.2,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.16.0,<0.17.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'watermark.py>=0.0.3,<0.0.4']

entry_points = \
{'console_scripts': ['telewater = telewater.cli:app']}

setup_kwargs = {
    'name': 'telewater',
    'version': '0.1.5',
    'description': 'A telegram bot that applies watermark on images, gifs and videos.',
    'long_description': "# telewater\n\nA telegram bot that applies watermark on images, gifs and videos.\n\n## Features\n\n- **Fast** because it is made using async libraries.\n- **Simple** to use.\n- Any one who uses an instance of the bot will have to use the same watermark and position. This is meant to be used by **single person/organization** (by only you or your team), as configuration is stored at a global level instead of per user basis.\n- **No database** connection required.\n- It **does not store media** (photos/videos/gifs) on the server. Media is deleted immediately after the watermarked version is sent to the user.\n\n## Usage\n\nUsing the bot is very simple. Just send a photo, video or gif to the bot. The bot will reply with the watermarked media.\n\nThe bot commands `/set` and `/get` can set and get the value of the configuration variables. The commands are simple and intuitive. The bot will show you the usage if you send an incorrect argument.\n\n## Deploy\n\nThis application can be easily deployed to Heroku, which is extremely good if you want to enjoy a free tier.\n\nYou may [read further](#further-reading) to learn about more more deployment options.\n\n[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/aahnik/telewater)\n\nClick on the above button. A form will appear, where you need to enter the credentials for the bot. After the app is deployed sucessfully, [turn on the woker dyno](https://user-images.githubusercontent.com/66209958/117938593-d6de0080-b324-11eb-9c0f-9bcc6d975808.png) to start the bot.\n\n## Installation\n\nThe following is the guide to install `telewater` on your computer, or VPS.\n\nIf you are a beginner, don't bother yourself with these. Just go ahead with the heroku method described abvoe.\n\nIf you are familiar with **Docker** then [click here](https://github.com/aahnik/telewater/wiki/Install-and-run-using-docker) otherwise, continue reading.\n\n#### Requirements\n\nMake sure to have these installed in your system.\n\n- [python3.9+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) (the bot is built with the telethon library)\n- [ffmpeg](https://ffmpeg.org/) (used by the bot for applying watermark)\n\n#### Verification\n\nOpen you terminal to check if you have all basic requirements properly installed.\n\n1. Run `python --version` and you should get something like this `Python 3.9.2` (or above).\n2. Run `pip --version` and you should get `pip 20.2.2` (or above).\n\n    > Some systems may require to use `python3` and `pip3` instead of the above.\n\n3. Run `ffmpeg -h` and it should display a help message and version above `4.2.4`.\n\n#### Install via pip\n\n```shell\npip install telewater\n```\n\n#### Starting `telewater`\n\nTelewater has a simple command line interface to start the bot.\n\nSimply open your terminal and run `telewater`. It will prompt you to enter the required information.\n\n## Further reading\n\n- [Environment Variables](https://github.com/aahnik/telewater/wiki/Environment-Variables)\n- [Telewater CLI usage](https://github.com/aahnik/telewater/wiki/Telewater-CLI-usage)\n- [Install and run using docker](https://github.com/aahnik/telewater/wiki/Install-and-run-using-docker)\n- [Deploy to Digital Ocean](https://github.com/aahnik/telewater/wiki/Deploy-to-Digital-Ocean)\n- [Run multiple instances](https://github.com/aahnik/telewater/wiki/Run-multiple-instances)\n\nFor any further help, feel free to [create an issue](https://github.com/aahnik/telewater/issues) in the GitHub repo.\n\n<!-- AAHNIK 2021 -->\n",
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/telewater',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
