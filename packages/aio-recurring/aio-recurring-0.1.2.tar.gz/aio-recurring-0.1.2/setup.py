# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_recurring']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aio-recurring',
    'version': '0.1.2',
    'description': 'Schedule recurring coroutines using asyncio',
    'long_description': '# aio-recurring\nRecurring coroutines using asyncio\n\n## Usage:\n\n```python\nimport asyncio\nfrom datetime import datetime\n\nfrom aio_recurring.job import (\n    recurring,\n    run_recurring_jobs,\n)\n\n\n@recurring(every=5)\nasync def print_info_5():\n    print(f"[{datetime.now()}] This coroutine is rescheduled every 5 seconds")\n\n\n@recurring(every=10)\nasync def print_info_10():\n    print(f"[{datetime.now()}] This coroutine is rescheduled every 10 seconds")\n\n\nasync def main():\n    run_recurring_jobs()\n\n\nif __name__ == \'__main__\':\n    loop = asyncio.get_event_loop()\n    loop.create_task(main())\n    loop.run_forever()\n\n```',
    'author': 'Sergey Konik',
    'author_email': 's.konik.job@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skonik/aio-recurring',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
