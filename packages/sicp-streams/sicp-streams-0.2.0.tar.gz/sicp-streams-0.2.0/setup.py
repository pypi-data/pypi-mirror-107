# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['more_streamtools', 'sicp_streams', 'streamdemo', 'streamtools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sicp-streams',
    'version': '0.2.0',
    'description': 'Replace iterator with stream and enjoy immutable. ',
    'long_description': '# Streams\n\nHonor [SICP 3.5 Streams](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-24.html). It shows a\nway to see "changing" data differently.\n\n## Introduction\n\nIterators actually irrecoverably consumes the data in it. This is not acceptable for (not pure but Lisp-like) functional\nprogramming. This package is built for solve this.\n\nStream is designed to be immutable, but not enforced by codes. Prevent doing anything with `s._head` or `s._tail`.\n\n## Usage (all codes are complete)\n\n```python\n## Importing and Constructing a Stream\nfrom sicp_streams import Stream\n\ns = Stream("axolotl", "barnacle", "coral")\n\n# Equivalently, use another stream as last element means "rest"\n# s = Stream("axolotl", Stream("barnacle", Stream("coral", None)))\n\n# Equivalently, use a callable as last element also means "rest", and will not be called until it is necessary\n# s = Stream("axolotl", lambda: Stream("barnacle", lambda: Stream("coral", lambda: None)))\n\n# Therefore, it is possible to construct a stream that never ends\nones = Stream(1, lambda: ones)\n\n## Get Data from It\nassert s.head == "axolotl"\nassert s.tail.head == "barnacle"\nassert s.tail.tail.head == "coral"\nassert s.tail.tail.tail is None  # end of stream is None\n\n## Get Data by subscripting\nassert (s[0], s[1], s[2]) == ("axolotl", "barnacle", "coral")\n\n## Turn into an Iterator\nit = iter(s)\nassert next(it) == "axolotl"\nassert next(it) == "barnacle"\nassert next(it) == "coral"\n\n## Construct from an iterable\nStream.from_iterable([1, 2, 3])\n\n\n## Construct from generator function\n@Stream.from_generator_function\ndef counts(n):\n    while True:\n        yield n\n        n += 1\n\n\nintegers = counts(1)\n```\n\n## Toolbox Analog to `itertools` and Iterator-related Built-in Functions\n\n```python\nfrom sicp_streams import Stream\nimport streamtools\n\n# some of them have different name (for obvious but unnecessary reason)\n# map -> smap\nstreamtools.smap(lambda x: x + 1, Stream(1, 2, 3))\n# filter -> sfilter\nstreamtools.sfilter(lambda x: x % 2 == 0, Stream(1, 2, 3))\n# zip -> szip\nstreamtools.szip(Stream(1, 2, 3), Stream(4, 5, 6))\n# islice -> sslice\nstreamtools.sslice(Stream(1, 2, 3, 4, 5), 2, 4)\n```\n\n## Demo, reimplementing SICP 3.5 (Not all of it)\n\n```python\nimport streamdemo\n```\n',
    'author': 'Xu Siyuan',
    'author_email': 'inqb@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/no1xsyzy/sicp-streams',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
