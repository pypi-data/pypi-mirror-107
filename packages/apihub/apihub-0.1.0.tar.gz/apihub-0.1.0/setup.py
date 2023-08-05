# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apihub', 'apihub.common', 'apihub.security', 'apihub.subscription']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.37.4,<0.38.0',
 'SQLAlchemy>=1.4.15,<2.0.0',
 'fastapi-jwt-auth>=0.5.0,<0.6.0',
 'fastapi>=0.65.1,<0.66.0',
 'prometheus-client>=0.7.0,<0.8.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'python-multipart>=0.0.5,<0.0.6',
 'redis>=3.5.3,<4.0.0',
 'tanbih-pipeline[redis]>=0.11.0,<0.12.0',
 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['apihub_result = apihub.result:main',
                     'apihub_server = apihub.server:main']}

setup_kwargs = {
    'name': 'apihub',
    'version': '0.1.0',
    'description': 'a API gateway on top of Redis',
    'long_description': '<!-- PROJECT SHIELDS -->\n<!--\n*** I\'m using markdown "reference style" links for readability.\n*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).\n*** See the bottom of this document for the declaration of the reference variables\n*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.\n*** https://www.markdownguide.org/basic-syntax/#reference-style-links\n-->\n[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n[![LinkedIn][linkedin-shield]][linkedin-url]\n\n\n\n<!-- PROJECT LOGO -->\n<br />\n<p align="center">\n  <a href="https://github.com/yifan/apihub">\n    <img src="https://raw.githubusercontent.com/yifan/apihub/master/images/APIHub.png" alt="Logo" width="600" height="400">\n  </a>\n\n  <h3 align="center">APIHub</h3>\n\n  <p align="center">\n    APIHub is a platform to dynamically serve API services on-fly. API service workers can be deployed when needed.\n    <br />\n    <a href="https://github.com/yifan/apihub"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/yifan/apihub">View Demo</a>\n    ·\n    <a href="https://github.com/yifan/apihub/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/yifan/apihub/issues">Request Feature</a>\n  </p>\n</p>\n\n\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#prerequisites">Prerequisites</a></li>\n        <li><a href="#installation">Installation</a></li>\n      </ul>\n    </li>\n    <li><a href="#usage">Usage</a></li>\n    <li><a href="#roadmap">Roadmap</a></li>\n    <li><a href="#contributing">Contributing</a></li>\n    <li><a href="#license">License</a></li>\n    <li><a href="#contact">Contact</a></li>\n    <li><a href="#acknowledgements">Acknowledgements</a></li>\n  </ol>\n</details>\n\n\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\n\n[![Product Name Screen Shot][product-screenshot]](https://raw.githubusercontent.com/yifan/apihub/master/images/APIHub.png)\n\nHere\'s a blank template to get started:\n**To avoid retyping too much info. Do a search and replace with your text editor for the following:**\n`yifan`, `apihub`, `yifan2019`, `email`, `APIHub`, `project_description`\n\n### Features & TODOs\n\n    [X] Security\n        [X] authenticate\n        [X] admin, manager, user\n        [X] user management\n        [X] rate limiter\n        [ ] register\n        [ ] social login\n    [ ] Subscription\n        [-] subscription\n        [-] quota\n        [X] application token\n        [-] daily usage record in redis\n    [ ] Async/sync API calls\n        [ ] api worker reports input/output: describe\n        [X] generic worker deployment \n        [ ] auto scaler for api workers\n\n\n### Built With\n\n* [fastapi](https://fastapi.tiangolo.com/)\n* [SQLAlchemy](https://www.sqlalchemy.org/)\n* [pydantic](https://pydantic-docs.helpmanual.io/)\n* [tanbih-pipeline](https://github.com/yifan/pipeline)\n* [psycopg2](https://pypi.org/project/psycopg2/)\n* [redis](https://pypi.org/project/redis/)\n* [poetry](https://python-poetry.org/)\n\n\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nTo get a local copy up and running follow these simple steps.\n\n### Prerequisites\n\nThis is an example of how to list things you need to use the software and how to install them.\n\n### Installation\n\n1. Clone the repo\n   ```sh\n   git clone https://github.com/yifan/apihub.git\n   ```\n2. Install python packages\n   ```sh\n   poetry install\n   ```\n\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nUse this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.\n\n_For more examples, please refer to the [Documentation](https://example.com)_\n\n\n\n<!-- ROADMAP -->\n## Roadmap\n\nSee the [open issues](https://github.com/yifan/apihub/issues) for a list of proposed features (and known issues).\n\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n\n## Testing\n\n1. Start postgres and redis\n   ```sh\n   docker compose up\n   ```\n2. Setup environment variables in a local .env file\n   ```sh\n   cat >.env <<EOF\n   DB_URI="postgresql://dbuser:dbpass@localhost:5432/test"\n   JWT_SECRET="nosecret"\n   REDIS="redis://localhost:6379/1"\n   IN_REDIS="redis://localhost:6379/1"\n   OUT_REDIS="redis://localhost:6379/1"\n   SECURITY_TOKEN_EXPIRES_DAYS=1\n   SUBSCRIPTION_TOKEN_EXPIRES_DAYS=1\n   EOF\n   ```\n3. Run tests\n   ```sh\n   poetry run test\n   ```\n4. Shutdown docker services\n   ```sh\n   docker compose down\n   ```\n\n\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the MIT License. See `LICENSE` for more information.\n\n\n\n<!-- CONTACT -->\n## Contact\n\nYifan Zhang - [@yifan2019](https://twitter.com/yifan2019) - yzhang@hbku.edu.qa\n\nProject Link: [https://github.com/yifan/apihub](https://github.com/yifan/apihub)\n\n\n\n<!-- ACKNOWLEDGEMENTS -->\n## Acknowledgements\n\n* []()\n* []()\n* []()\n\n\n\nCopyright (C) 2021, Qatar Computing Research Institute, HBKU\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/yifan/apihub.svg?style=for-the-badge\n[contributors-url]: https://github.com/yifan/apihub/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/yifan/apihub.svg?style=for-the-badge\n[forks-url]: https://github.com/yifan/apihub/network/members\n[stars-shield]: https://img.shields.io/github/stars/yifan/apihub.svg?style=for-the-badge\n[stars-url]: https://github.com/yifan/apihub/stargazers\n[issues-shield]: https://img.shields.io/github/issues/yifan/apihub.svg?style=for-the-badge\n[issues-url]: https://github.com/yifan/apihub/issues\n[license-shield]: https://img.shields.io/github/license/yifan/apihub.svg?style=for-the-badge\n[license-url]: https://github.com/yifan/apihub/blob/master/LICENSE\n[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555\n[linkedin-url]: https://linkedin.com/in/yifanzhang\n',
    'author': 'Yifan Zhang',
    'author_email': 'freqyifan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
