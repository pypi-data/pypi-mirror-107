# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['venture', 'venture.ui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'arc-cli>=2.3.0,<3.0.0', 'ujson>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['venture = venture.__main__:cli']}

setup_kwargs = {
    'name': 'venture',
    'version': '1.2.2',
    'description': 'Rofi / Wofi based project selector',
    'long_description': "# Venture\n\nA Dmenu / Rofi / Wofi menu to open projects and files in your favorite editor!\n\n\n\n### Dependancies\nVenture supports three UI providers: dmenu, rofi, and wofi. It is expected that you have the one you intend to use installed.\n\n## Installation\n\n```\n$ pip install venture\n```\n\n## Configuration\nWhile not required, you can generate a deafult config with this command\n```\n$ venture dump\n```\nThis will create a file `~/.config/venture.yaml`\n\n\n```yaml\n# The Entry Points for Venture. Venture will list each sub-directory or file\n# for the given directories.\ndirectories:\n- '~' # Simple String syntax for a directory\n# If you have a primary directory you want to list, but then multiple\n# sub-directories within the main directory that need to also be listed,\n# the below syntax can be used\n- base: ~/sourcecode\n  sub:\n    - rust # this would resolve to ~/sourccode/rust/...\n    - python\n    - ruby\n    - work\n# Venture also accepts a simple glob pattern. This would be equivelant to listing out each of the sub-directories as entry points manually.\n- ~/sourcecode/school/*\n# Command To execute when an option is chosen. Recieve the {path} token which is the absolute path to\n# the directory or file that the user selected.\nexec: code -r {path}\n# Whether or not to display files\nshow_files: true\n# Whether or not to display dotfiles\nshow_hidden: false\n# Whether or not to display an icon of the file type\nshow_icons: true\n# What provides the UI, currently supports dmenu, rofi, and wofi\nui_provider: rofi\n# For all 3 ui providers, you can add a dictionary to pass arbitrary arguments to the command\nrofi:\n  theme: ~/.config/rofi/theme.rasi\n\n```\n\n## Quick-launcher\nThe quick-launcher allows you to add specific files / directories to it for easy searchable access.\n\n### Excute\n```\nventure quicklaunch\n```\n\n### Add an entry\nEntries are added to `~/.config/venture.yml`\n```\nventure quicklaunch:add \\\n        name=ARC \\\n        path=~/sourcecode/arc \\\n        icon=\\uF625 \\\n        tags=py,project\n```\nPossible Arguments:\n- `name`: What name to display in the quick-launch menu\n- `path`: Filepath to open on selection\n- `icon`: Icon to display along side the name **optional**\n- `tags`: comma-seperated list of strings to display along with the title. **optional**\n- `--no-default-tags`: Disables Venture's automatic tag detection / creation\n- `--disable-short-tags`: Disables Venture's tag shorthand matching.\n  - enabled: `tags=py` would result in: `[\\uF81F python]`\n  - disabled: `tags=py` would result in: `[py]`",
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seanrcollings/venture',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
