# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

packages = \
['uppaalpy',
 'uppaalpy.classes',
 'uppaalpy.classes.class_tests',
 'uppaalpy.path_tests']

package_data = \
{'': ['*'],
 'uppaalpy.classes.class_tests': ['constraint_cache_xml_files/*',
                                  'constraint_xml_files/*',
                                  'label_xml_files/*',
                                  'nta_xml_files/*',
                                  'template_xml_files/*'],
 'uppaalpy.path_tests': ['testcases/epsilon_tests/*',
                         'testcases/good_nta/*',
                         'testcases/path_concatenation/*',
                         'testcases/path_exists/*',
                         'testcases/path_not_exists/*',
                         'testcases/path_not_realizable/*',
                         'testcases/path_realizable/*']}

install_requires = \
['lxml>=4.6.2', 'networkx>=2.5', 'ortools>=8.1.8487']

setup_kwargs = {
    'name': 'uppaal-py',
    'version': '0.0.3',
    'description': 'UPPAAL wrapper for Python.',
    'long_description': '# uppaal-py\nPython library for reading, writing, analyzing, and modifying UPPAAL timed automata files. Works with Python >= 3.8.\n\n## Disclaimer\nuppaal-py is a work-in-progress library. For bugs, missing features or documentation please create an issue or send me an email. API is subject to change.\n\n## Dependencies\n* [lxml](https://lxml.de/)\n* [NetworkX](https://github.com/networkx/networkx)\n* [ortools](https://developers.google.com/optimization)\n\n## Installation\nVia pip:\n```\npip install uppaal-py\n```\n\n## License\n[MIT](https://mit-license.org/)\n\n## Features\n- Reading and writing UPPAAL files.\n- LP based path realizability analysis.\n- Working with variables of type `int` and a subset of expressions involving `ints` for guards, invariants, and updates during transitions allowed in UPPAAL in addition to clocks during computations.\n\n## TODO:\n- [ ] Methods for calling UPPAAL/verifyta.\n- [ ] Migrate to [libutap](https://github.com/MASKOR/libutap) for parsing files.\n- [ ] Parameter synthesis for safety property.\n- [ ] [lxml type annotations](https://github.com/lxml/lxml-stubs) and type annotations for the remaining functions.\n- [ ] Auto-generated documentation.\n\n## Non-features\n- Analysis involving network of TA — product of two or more TA can be implemented in the future, though.\n- Symbolic model checking, UPPAAL does that.\n',
    'author': 'Deniz Koluaçık',
    'author_email': 'koluacik@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/koluacik/uppaal-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
