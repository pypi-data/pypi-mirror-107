# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openeditor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'openeditor',
    'version': '0.3.1',
    'description': 'Edit files with your $EDITOR, like git commit does.',
    'long_description': '# `openeditor`\nEdit files with your `$EDITOR`, like git commit does.\n\n## Usage\nInstall with: `pip install openeditor`\n\n```\n# Let user edit file\ns = openeditor.edit_file("path/to/my/file.txt")\nprint("The file now contains:\\n" + s)\n\n# Use a temp file\ns = openeditor.edit_file(\n    "# Please edit this file, save and close editor when done", \n    "path/to/my/file.txt"\n)\nprint("The file now contains:\\n" + s) \n```\n\nThe editor is obtained from, in order of precedence:\n\n* `$VISUAL`\n* `$EDITOR`\n\nIf neither of these provide a useful editor, an exception will be thrown.\n\n## Limitations\n`openeditor` expects an editor string similar to `EDITOR=cmd` such that:\n\n1. `cmd file.txt` (filename as the final argument) is a correct way of editing `file.txt`.\n2. `cmd` is not too complex. Simple things like space-separated flags (eg. `EDITOR="vim -n"`) are fine but advanced shell magic may break.\n\nIf your `cmd` **does** need to be more complex, one possible workaround is to write a wrapper script that presents a compatible command-line interface to `openeditor` and invokes the full command as appopriate.',
    'author': 'Azat Akhmetov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/metov/openeditor',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
