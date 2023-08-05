# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pupalink']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'beautifulsoup4>=4.9.3,<5.0.0', 'lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'pupalink',
    'version': '0.1.0a4',
    'description': 'Springer Link Download Module for Python',
    'long_description': '<img align="right" src="https://user-images.githubusercontent.com/14788425/119204060-d10abc80-ba94-11eb-91a0-72b0d0ab3649.png" height="300px">\n\n# ♞ pupalink\n\nA simple Python module to search and download books from SpringerLink.\n\n---\n\n> 🧪 **This project is still in an early stage of development. Expect breaking\n> changes**.\n\n---\n\n## Features\n\n- Search and download books from Springer Link\n\n## Prerequisites\n\n- An active SpringerLink account with premium access.\n\n## Getting started\n\nSign in to your SpringerLink account and copy the `idp_session` cookie and paste it like below:\n\n```python\nfrom pupalink import Session\n\nsession = Session("YOUR_IDP_SESSION")\n```\n\n### Example \n\n```python\nfrom pupalink import Session\nfrom asyncio import get_event_loop\n\nasync def main():\n    session = Session("YOUR_KEY")\n    books = await session.search_book("Rust")\n\n    for book in books:\n        await session.download_book(book)\n\n    await session.close()\n\n\nloop = get_event_loop()\nloop.run_until_complete(main())\n\n```',
    'author': 'Jimmy Nelle',
    'author_email': 'jimmy.nelle@hsw-stud.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pupagang/pupalink',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
