# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piston',
 'piston.colorschemes',
 'piston.commands',
 'piston.configuration',
 'piston.configuration.validators',
 'piston.utils']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.7.0,<9.0.0',
 'prompt-toolkit>=3.0.18,<4.0.0',
 'pygments>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['piston = piston:main']}

setup_kwargs = {
    'name': 'piston-cli',
    'version': '1.4.0',
    'description': 'A cli tool with an terminal editor to compile over 35 languages instantly using the piston api.',
    'long_description': "# Piston CLI\n\n[![](https://img.shields.io/github/license/Shivansh-007/piston-cli?style=for-the-badge)]()\n[![](https://img.shields.io/github/issues/Shivansh-007/piston-cli?style=for-the-badge)]()\n[![](https://img.shields.io/github/issues-pr/Shivansh-007/piston-cli?style=for-the-badge)]()\n[![](https://img.shields.io/github/workflow/status/Shivansh-007/piston-cli/Linting/main?style=for-the-badge)]()\n[![](https://img.shields.io/pypi/pyversions/piston-cli?style=for-the-badge)]()\n[![](https://img.shields.io/pypi/v/piston-cli?style=for-the-badge)]()\n\nA cli tool which uses the [piston api](https://github.com/engineer-man/piston), developed by Engineerman and his team to compile over 35 languages instantly. Accepts files, paste.pythondiscord.com links and input.\n\n### Installation\n\n#### With pip\n\n```bash\n# Installing the package\npip install piston-cli -U\n# Help Command\npiston -h\n```\n#### With Nix/NixOS\n\nAdd this to your configuration.nix\n\n```nix\n  environment.systemPackages = with pkgs; [\n     piston-cli\n  ];\n```\n\nOr if you're using [home-manager](https://github.com/nix-community/home-manager)\n\n```nix\n  home.packages = with pkgs; [\n     piston-cli\n  ];\n```\n\nAnd finally using nix-env or nix profile\n\n```bash\n# using nix-env\nnix-env -i piston-cli\n# using nix profile (in nixUnstable)\nnix profile install nixpkgs#piston-cli\n```\n#### For Arch/ArchBased\n##### With yay\n```bash\nyay piston-cli\n```\n##### With paru\n```bash\nparu piston-cli\n```\n\nOr any AUR helper you use with doesn't matter. You get the point.\n\n### Example usage\n\n#### Default\n\n![example usage](media/piston-cli.png)\n\n#### Shell\n\n![example shell usage](media/piston-cli-shell.png)\n\n#### File\n\n![example file usage](media/piston-cli-file.png)\n\n#### Link\n\n![example link usage](media/piston-cli-link.png)\n\n### Languages\n\n```bash\npiston --list\n```\n\n## How to run it? (Contributing)\n\n```shell\n# This will install the development and project dependencies.\npoetry install\n\n# This will install the pre-commit hooks.\npoetry run task precommit\n\n# Optionally: run pre-commit hooks to initialize them.\n# You can start working on the feature after this.\npoetry run task pre-commit run --all-files\n\n# Run it\npoetry run task start --help\n```\n\n## Contributing\n\nYou can comment on the issues you would like to work on.\n",
    'author': 'Shivansh-007',
    'author_email': 'shivansh-007@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Shivansh-007/piston-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.4,<4.0.0',
}


setup(**setup_kwargs)
