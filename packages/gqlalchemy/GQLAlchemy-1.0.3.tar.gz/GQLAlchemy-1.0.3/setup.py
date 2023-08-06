# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0', 'pymgclient>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'gqlalchemy',
    'version': '1.0.3',
    'description': 'GQLAlchemy is library developed with purpose of assisting writing and running queries on Memgraph.',
    'long_description': '# GQLAlchemy\n\n![Github Action build-and-test](https://github.com/memgraph/gqlalchemy/workflows/Build%20and%20Test/badge.svg)\n[![GitHub license](https://img.shields.io/github/license/memgraph/gqlalchemy)](https://github.com/memgraph/gqlalchemy/master/LICENSE)\n[![PyPi release version](https://img.shields.io/pypi/v/gqlalchemy)](https://pypi.org/project/gqlalchemy)\n\nGQLAlchemy is a library developed to assist in writing and running queries on Memgraph. GQLAlchemy supports high-level connection to Memgraph as well as modular query builder.\n\nGQLAlchemy is built on top of Memgraph\'s low-level client `pymgclient`\n([pypi](https://pypi.org/project/pymgclient/) /\n[documentation](https://memgraph.github.io/pymgclient/) /\n[GitHub](https://github.com/memgraph/pymgclient)).\n\n## Installation\n\nTo install `gqlalchemy`, simply run the following command:\n```\npip install gqlalchemy\n```\n\n## Build & Test\n\nThe project uses [poetry](https://python-poetry.org/) to build the GQLAlchemy. To build and run tests execute the following commands:\n`poetry install`\n\nBefore running tets make sure you have an active memgraph instance, then you can run:\n`poetry run pytest .`\n\n## GQLAlchemy example\n\n\nWhen working with the `gqlalchemy`, Python developer can connect to database and execute `MATCH` cypher query with following syntax:\n\n```python\nfrom gqlalchemy import Memgraph\n\nmemgraph = Memgraph("127.0.0.1", 7687)\nmemgraph.execute_query("CREATE (:Node)-[:Connection]->(:Node)")\nresults = memgraph.execute_and_fetch("""\n    MATCH (from:Node)-[:Connection]->(to:Node)\n    RETURN from, to;\n""")\n\nfor result in results:\n    print(result[\'from\'])\n    print(result[\'to\'])\n```\n\n## Query builder example\n\nAs we can see, the example above can be error-prone, because we do not have abstractions for creating a database connection and `MATCH` query.\n\nNow, rewrite the exact same query by using the functionality of gqlalchemys query builder..\n\n```python\n\nfrom gqlalchemy import Match, Memgraph\n\nmemgraph = Memgraph()\n\nresults = Match().node("Node",variable="from")\n                 .to("Connection")\n                 .node("Node",variable="to")\n                 .execute()\n\nfor result in results:\n    print(result[\'from\'])\n    print(result[\'to\'])\n```\n\n## License\n\nCopyright (c) 2016-2021 [Memgraph Ltd.](https://memgraph.com)\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use\nthis file except in compliance with the License. You may obtain a copy of the\nLicense at\n\n     http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n',
    'author': 'Jure Bajic',
    'author_email': 'jure.bajic@memgraph.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/memgraph/gqlalchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
