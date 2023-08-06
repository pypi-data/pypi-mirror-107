# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jfaleiro_pqueue']

package_data = \
{'': ['*']}

extras_require = \
{'coverage': ['pytest>=6.2.2,<7.0.0',
              'coverage>=5.4,<6.0',
              'PyHamcrest>=2.0.2,<3.0.0'],
 'interactive-dev': ['pre-commit>=2.10.1,<3.0.0',
                     'autopep8>=1.5.5,<2.0.0',
                     'isort>=5.7.0,<6.0.0',
                     'flake8>=3.8.4,<4.0.0',
                     'rope>=0.18.0,<0.19.0'],
 'tests': ['pytest>=6.2.2,<7.0.0',
           'PyHamcrest>=2.0.2,<3.0.0',
           'behave>=1.2.6,<2.0.0']}

setup_kwargs = {
    'name': 'jfaleiro.pqueue',
    'version': '0.0.2',
    'description': 'A simple priority queue for use cases in computational finance',
    'long_description': '# pqueue\n\nA simple priority queue for use cases in computational finance.\n\nPriority queues are one of the most commonly used structures in computational finance. One example are Central Limit Orders Books, or [CLOBS](https://en.wikipedia.org/wiki/Central_limit_order_book), in which the priority of the execution of orders is given by an orders\' price. This specific implementation uses a [heap structure](https://en.wikipedia.org/wiki/Heap_(data_structure)) where the priority is prepended to the search key. For CLOB orders the priority is the price of an order.\n\nThe original implementation of this library was done over an afternoon far back in 2016 to support agent simulations in my [doctorate thesis](https://repository.essex.ac.uk/21782/).\n\nSee _LICENSE_ for important licensing information.\n\n## Instalation\n\n```bash\npip install jfaleiro.pqueue\n```\n\nOr as a dependency in [`poetry`](https://python-poetry.org/):\n\n```bash\npoetry add jfaleiro.pqueue\npoetry update\n```\n\n## Use\n\nSay for example you have any structure, like this one, to represent an order:\n\n```python\nclass NewOrder(NamedTuple):\n    """ based on https://www.fixglobal.com/home/trader-fix-tags-reading/ """\n    side: OrderSideEnum\n    symbol: str\n    quantity: int\n    price: Decimal\n    id: str = None\n    instruction: OrderExecutionInstruction = OrderExecutionInstruction.ALL_OR_NONE\n    time_in_force: OrderTimeInForceEnum = OrderTimeInForceEnum.GOOD_TIL_CANCEL\n    type: OrderTypeEnum = OrderTypeEnum.LIMIT\n```\n\nAnd a book with orders falling on either bid (buy orders) or asks (sell orders) side:\n\n```python\nbids = Heap()\nasks = Heap(reverse=True)\n```\n\nAs you probably know, the `reverse=True` is used because orders in an "asks" side are reversed, i.e. lower prices cross before higher prices.\n\nYou can add new orders in either side by using a `push`. You need do specify an `id` and a `priority`. For example, to book a new buy order the `item` is of course the order, the `priority` is the price, and the `id` is the order\'s id:\n\n```python\nbids.push(id=order.id, priority=order.price, item=order)\n```\n\nAdding a sell order is exactly the same. The `reverse=True` takes care of the reverse priority:\n\n```python\nasks.push(id=order.id, priority=order.price, item=order)\n```\n\nIf you have an `id` of a previously booked order, you can cancel orders as easily with a `remove`:\n\n```python\nbids.remove(id=action.id)\n```\n\nYou can verify crosses with a `peek`, for example, if want to verify if a cross occurred:\n\n```python\nif asks.peek().price <= bids.peek().price:\n  print(\'a cross happened!!\')\n```\n\nAfter which you might want to cross (execute) orders on the top of each side:\n\n```python\nask_order = asks.pop()\n...\nbid_order = bids.pop()\n```\n\nAnd that does it. It is so simple and short that you can see it as just another proof that finding the adequate patterns is 99% of any solution in engineering. Computational finance is of course no exception.\n\nYou can check this [implementation of an order book](https://gitlab.com/jfaleiro/orderbook) for a full example of use of `pqueue`.\n',
    'author': 'Jorge M Faleiro Jr',
    'author_email': 'j@falei.ro',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/jfaleiro.open/pqueue',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
