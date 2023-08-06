# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab2nextclouddeck']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'progress>=1.5,<2.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-gitlab>=2.7.1,<3.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['gitlab2nextclouddeck = gitlab2nextclouddeck.main:app']}

setup_kwargs = {
    'name': 'gitlab2nextclouddeck',
    'version': '0.1.11',
    'description': '',
    'long_description': "![PyPI - Implementation](https://img.shields.io/pypi/implementation/gitlab2nextclouddeck) ![PyPI - Status](https://img.shields.io/pypi/status/gitlab2nextclouddeck) ![PyPI - License](https://img.shields.io/pypi/l/gitlab2nextclouddeck) ![PyPI](https://img.shields.io/pypi/v/gitlab2nextclouddeck) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitlab2nextclouddeck)\n\n# gitlab2NextcloudDeck Importer\n\nImports Issues from gitlab to Nextcloud Deck\n\n## Introduction\n\nImports Issues from selected Project in gitlab to targeted Nextcloud Deck Stack. You can choose which Project and which Stack.\n\n## Installation\n\n```bash\n$ pip3 install gitlab2nextclouddeck\n```\n\n## Usage\n\n```bash\n$ python3 -m gitlab2nextclouddeck\n```\n\n## Changelog\n\n### [0.1.10] - 2021-05-22\n\n#### Fixed\n\n- README fixed\n\n### [0.1.9] - 2021-05-22\n\n#### Fixed\n\n- running in CLI when installed from pip\n\n### [0.1.6] - 2021-05-22\n\n#### Fixed\n\n- gitlab-ci build and publish fix\n\n### [0.1.5] - 2021-05-22\n\n#### Fixed\n\n- gitlab-ci fix removing artifact\n\n### [0.1.4] - 2021-05-22\n\n#### Fixed\n\n- running as name in CLI\n\n### [0.1.2] - 2021-05-21\n\n#### Fixed\n\n- Badges fixed for Markdown\n\n### [0.1.0] - 2021-05-21\n\n#### Added\n\n- Reading Issue from Gitlab\n- linked issues will right shown\n- will created in create date order\n- gitlab api extended with url\n- labels will set to issues\n- get linked issues from gitlab\n- organize linked issues\n- writing in description for NextcloudDeck\n- Creates Cards from readed Gitlab Issues\n- poetry template\n- README, License\n- toml config for building and publishing\n\n#### Removed\n\n- README.rst\n\n#### Fixed\n\n- update card fixed\n\n## Contributor Covenant Code of Conduct\n\n### Our Pledge\n\nIn the interest of fostering an open and welcoming environment, we as\ncontributors and maintainers pledge to making participation in our project and\nour community a harassment-free experience for everyone, regardless of age, body\nsize, disability, ethnicity, gender identity and expression, level of experience,\nnationality, personal appearance, race, religion, or sexual identity and\norientation.\n\n### Our Standards\n\nExamples of behavior that contributes to creating a positive environment\ninclude:\n\n- Using welcoming and inclusive language\n- Being respectful of differing viewpoints and experiences\n- Gracefully accepting constructive criticism\n- Focusing on what is best for the community\n- Showing empathy towards other community members\n\nExamples of unacceptable behavior by participants include:\n\n- The use of sexualized language or imagery and unwelcome sexual attention or\n  advances\n- Trolling, insulting/derogatory comments, and personal or political attacks\n- Public or private harassment\n- Publishing others' private information, such as a physical or electronic\n  address, without explicit permission\n- Other conduct which could reasonably be considered inappropriate in a\n  professional setting\n\n### Our Responsibilities\n\nProject maintainers are responsible for clarifying the standards of acceptable\nbehavior and are expected to take appropriate and fair corrective action in\nresponse to any instances of unacceptable behavior.\n\nProject maintainers have the right and responsibility to remove, edit, or\nreject comments, commits, code, wiki edits, issues, and other contributions\nthat are not aligned to this Code of Conduct, or to ban temporarily or\npermanently any contributor for other behaviors that they deem inappropriate,\nthreatening, offensive, or harmful.\n\n### Scope\n\nThis Code of Conduct applies both within project spaces and in public spaces\nwhen an individual is representing the project or its community. Examples of\nrepresenting a project or community include using an official project e-mail\naddress, posting via an official social media account, or acting as an appointed\nrepresentative at an online or offline event. Representation of a project may be\nfurther defined and clarified by project maintainers.\n\n### Enforcement\n\nInstances of abusive, harassing, or otherwise unacceptable behavior may be\nreported by contacting the project team at developers@whiteoctober.co.uk. All\ncomplaints will be reviewed and investigated and will result in a response that\nis deemed necessary and appropriate to the circumstances. The project team is\nobligated to maintain confidentiality with regard to the reporter of an incident.\nFurther details of specific enforcement policies may be posted separately.\n\nProject contributors who do not follow or enforce the Code of Conduct in good\nfaith may face temporary or permanent repercussions as determined by\nmembers of the project's leadership.\n\nActions we may take in such instances include (but are not limited to) the following:\n\n- [Locking conversations](https://help.github.com/articles/locking-conversations/)\n- [Blocking users](https://github.com/blog/2146-organizations-can-now-block-abusive-users)\n- [Reporting users to Github](https://help.github.com/articles/reporting-abuse-or-spam/)\n\nAs an individual user on Github, you also have the option to [block a user from your personal account](https://help.github.com/articles/blocking-a-user-from-your-personal-account/) or to [report a user to Github](https://help.github.com/articles/reporting-abuse-or-spam/) yourself, but the existence of these functions will not be used as a reason for inaction on our part.\n\n### Attribution\n\nThis Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,\navailable at [http://contributor-covenant.org/version/1/4][version]\n\n[homepage]: http://contributor-covenant.org\n[version]: http://contributor-covenant.org/version/1/4/\n",
    'author': 'Ferit Cubukcuoglu',
    'author_email': 'info@yazcub.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://yazcub.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
