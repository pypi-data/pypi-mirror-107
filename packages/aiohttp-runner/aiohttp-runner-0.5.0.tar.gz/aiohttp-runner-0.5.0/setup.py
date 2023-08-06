# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_runner']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3,<4', 'async-exit-stack>=1,<2', 'async_generator>=1,<2']

setup_kwargs = {
    'name': 'aiohttp-runner',
    'version': '0.5.0',
    'description': 'Wraps aiohttp or gunicorn server for aiohttp application.',
    'long_description': "Install\n---\n```\npip install aiohttp-runner\n```\n\nExample usage\n---\n\n```python\nimport asyncio\nimport aiohttp.web\nfrom async_generator import asynccontextmanager\nfrom aiohttp_runner import (\n    simple_http_runner, gunicorn_http_runner,\n    HttpRequest, HttpResponse,\n    create_http_app, wait_for_interrupt,\n)\n\n\n@asynccontextmanager\nasync def app_factory():\n    yield create_http_app(routes=[\n        ('GET', '/', http_handler),\n    ])\n\n\nasync def http_handler(_req: HttpRequest) -> HttpResponse:\n    return aiohttp.web.Response(status=204)\n\n\nasync def main() -> None:\n    bind = '127.0.0.1:8080'\n\n    runner = gunicorn_http_runner(app_factory, bind, workers=2)\n    # OR\n    runner = simple_http_runner(app_factory, bind)\n\n    async with runner:\n        await wait_for_interrupt()\n\n\nif __name__ == '__main__':\n    asyncio.get_event_loop().run_until_complete(main())\n```\n",
    'author': 'xppt',
    'author_email': '21246102+xppt@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
