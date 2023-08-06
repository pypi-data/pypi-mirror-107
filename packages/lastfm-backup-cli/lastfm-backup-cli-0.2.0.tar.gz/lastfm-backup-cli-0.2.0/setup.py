# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lastfm_backup_cli']

package_data = \
{'': ['*']}

install_requires = \
['pylast>=4.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['lastfm-backup = lastfm_backup_cli.main:cli_main']}

setup_kwargs = {
    'name': 'lastfm-backup-cli',
    'version': '0.2.0',
    'description': 'Super-simple CLI tool for backing up Last.fm scrobbling data',
    'long_description': '# lastfm-backup-cli\nSuper-simple CLI tool for backing up Last.fm scrobbling data into CSV file\n\n### installation\n- pre-requisites: Python 3.7 or newer, pip\n- installation: `pip install --user lastfm-backup-cli`\n  - or, if your default Python is 2.x: `python3 -m pip install --user lastfm-backup-cli`\n\n### usage\n- get your LastFM API key [here](https://www.last.fm/api)\n- run: `lastfm-backup <PATH TO BACKUP CSV FILE> --user <YOUR LASTFM USERNAME> --api-key <YOUR API KEY> --time-from <DATE OF FIRST SCROBBLE IN BACKUP FILE> --time-to <DATE OF LAST SCROBBLE IN BACKUP FILE>`\n  - example: `lastfm-backup lastfm-backup-2021-01.csv --user Rezult --api-key <YOUR API KEY> --time-from 2021-01-01 --time-to 2021-02-01`\n- you can also set env variables: `LASTFM_API_KEY` and `LASTFM_USER`\n\n### output\n- output CSV file structure is:\n```csv\n<SCROBBLE DATE>,<SCROBBLE TIME (UTC)>,<ARTIST>,<TITLE>\n...\n```\n- output CSV example:\n```csv\n2021-05-26,06:05:49,Alice Coltrane,Journey in Satchidananda\n2021-05-25,14:16:08,London Music Works,"S.T.A.Y. (From ""Interstellar"")"\n2021-05-25,13:18:39,Pantha du Prince,Silentium Larix\n2021-05-25,13:11:10,Avenade,Have It Your Way\n2021-05-25,13:03:51,Four Tet,Planet\n2021-05-25,12:57:58,Songs: Ohia,Steve Albini\'s Blues\n2021-05-25,12:52:31,Andy Stott,It Should Be Us\n```\n\n### options\n```\nusage: lastfm-backup [-h] [--user USER] [--api-key API_KEY] [--time-from TIME_FROM] [--time-to TIME_TO] [-d] file\n\nSuper-simple CLI tool for backing up Last.fm scrobbling data\n\npositional arguments:\n  file                  CSV file path where backup should be written to. Defaults to lastfm.csv\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --user USER           The last.fm username to fetch the recent tracks of.Might be provided by env variable LASTFM_USER\n  --api_key API_KEY     A Last.fm API key. Might be provided by env variable LASTFM_API_KEY\n  --time-from TIME_FROM\n                        Beginning timestamp of a range - only display scrobbles after this time. Must be in UTC. Example: 2021-05-13\n  --time-to TIME_TO     End timestamp of a range - only display scrobbles before this time. Must be in UTC. Example: 2021-05-15\n  -d, --debug           Enable more verbose logging\n```\n',
    'author': 'emkor93',
    'author_email': 'emkor93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emkor/lastfm-backup-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
