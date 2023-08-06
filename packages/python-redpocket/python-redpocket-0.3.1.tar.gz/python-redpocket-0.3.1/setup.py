# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redpocket']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'python-redpocket',
    'version': '0.3.1',
    'description': 'A Python API Interface for RedPocket Mobile',
    'long_description': '# python-redpocket\n\n[![python38|39](https://img.shields.io/pypi/pyversions/python-redpocket)](https://pypi.org/project/python-redpocket/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![codecov](https://codecov.io/gh/mbillow/python-redpocket/branch/main/graph/badge.svg?token=Q88GID8SSQ)](https://codecov.io/gh/mbillow/python-redpocket) [![pypi downloads](https://img.shields.io/pypi/dm/python-redpocket)](https://pypi.org/project/python-redpocket/)\n\nA simple, fully tested, Pythonic wrapper around RedPocket Mobile\'s API.\n\n## Example Usage\n\n```python\nfrom getpass import getpass\nfrom redpocket import RedPocket\n\nusername = input("RedPocket Username: ")\npassword = getpass("Password:")\n\nrp = RedPocket(username=username, password=password)\n\nlines = rp.get_lines()\nprint(lines)\n# [\n#     RedPocketLine(\n#         account_id=\'12345\',\n#         number=1234567890,\n#         plan=\'Annual- Unlimited Everything + 8GB high speeds\',\n#         expiration=datetime.date(2022, 1, 2),\n#         family=False\n#     )\n# ]\n\nline_details = lines[0].get_details()\nprint(line_details)\n# RedPocketLineDetails(\n#     number=1234567890, \n#     product_code=\'GSMA\', \n#     status=\'Active\', \n#     plan_id=\'355\', \n#     plan_code=\'E240GSMA\', \n#     expiration=datetime.date(2021, 5, 12), \n#     last_autorenew=datetime.date(2021, 12, 3), \n#     last_expiration=datetime.date(2022, 1, 2), \n#     main_balance=-1, \n#     voice_balance=-1, \n#     messaging_balance=-1, \n#     data_balance=7657, \n#     phone=RedPocketPhone(model=\'Apple iPhone 12 A2172\', imei=\'\', sim=\'\', esn=\'\')\n\nprint(line_details.remaining_days_in_cycle)\n# 11\n\nprint(line_details.remaining_months_purchased)\n# 8\n```\n\nThere is also a helper function to get all the lines and line details in one call:\n\n```python\nfrom redpocket import RedPocket\n\nrp = RedPocket(username="", password="")\nlines = rp.get_all_line_details()\n\nprint(lines)\n# [\n#     (\n#         RedPocketLine(\n#             account_id=\'12345\', \n#             number=1234567890, \n#             plan=\'Annual- Unlimited Everything + 8GB high speeds\', \n#             expiration=datetime.date(2022, 1, 2), \n#             family=False), \n#         RedPocketLineDetails(\n#             number=1234567890, \n#             product_code=\'GSMA\', \n#             status=\'Active\', \n#             plan_id=\'355\', \n#             plan_code=\'E240GSMA\', \n#             expiration=datetime.date(2021, 5, 12), \n#             last_autorenew=datetime.date(2021, 12, 3), \n#             last_expiration=datetime.date(2022, 1, 2), \n#             main_balance=-1, \n#             voice_balance=-1, \n#             messaging_balance=-1, \n#             data_balance=7657, \n#             phone=RedPocketPhone(model=\'Apple iPhone 12 A2172\', imei=\'\', sim=\'\', esn=\'\')\n#         )\n#     )\n# ]\n```\n\nIf you know the hash or account number of the specific account you want to retrieve, you can do that as well:\n\n```python\nfrom redpocket import RedPocket\n\nrp = RedPocket(username="", password="")\n\nmy_line_hash = rp.get_lines()[0].account_hash\nprint(my_line_hash)\n# \'MTIzNDU2\'\n\ndetails = rp.get_line_details(account_hash=my_line_hash)\nprint(details)\n# RedPocketLineDetails(\n#     ...\n# )\n```\n',
    'author': 'Marc Billow',
    'author_email': 'marc@billow.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbillow/python-redpocket',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
