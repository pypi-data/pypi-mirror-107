# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guap', 'guap.metrics']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0', 'numpy>=1.20.2,<2.0.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'guap',
    'version': '0.1.3',
    'description': '',
    'long_description': '<h1 align="center">\n  guap\n</h1>\n\n<h3 align="center">\n From algorithms outputs to business outcomes.\n</h3>\n<p align="center">\nguap is an open-source python package that helps data team to get an ML evaluation metrics everyone can agree on by converting your model output to business outcomes, a.k.a. profits.</p>\n\n<h3 align="center">\n 🤖 \U0001fa84 📈\n</h3>\n\n\n<p align="center">\n  <img src="https://i.imgur.com/sCfpF6d.png">\n</p>\n\n<p align="center">\n    <a href="https://github.com/chetanraj/awesome-github-badges">\n        <img alt="Made with love" src="https://img.shields.io/badge/Made%20With-Love-orange.svg">\n    </a>\n\t<a href="https://github.com/chetanraj/awesome-github-badges">\n        <img alt="py version" src="https://img.shields.io/badge/python-3.6_|_3.7_|_3.8-blue">\n    </a>\n\t    </a>\n\t<a href="https://github.com/chetanraj/awesome-github-badges">\n        <img alt="version" src="https://img.shields.io/badge/version-0.1.0-gree">\n    </a>\n</p>\n\n\n## 🧞\u200d♂️ Why should I use guap?\nOur mission with guap is to align all stakeholders with measurable business outcomes by including the three core teams — business, data science and IT — throughout the life cycle of the AI models.\n\n- Make collaboration healthier and clearer between tech and non-tech people\n- Make better decisions at every stage of the ML project lifecycle\n\nWant to know more? Read [Why guap exist](https://ulyssebottello.com/why-guap/).\n\n## ✨ Features\nWe\'re on the journey to make sure every ML use-case that go to production is a valuable one. And it starts with a simple way to estimate the expected profit/cost of a model based on its confusion matrix.\n\n- **Get the total profit** Based on the test set, guap will give you the total expected profit based on the cost matrix. A great way to have an overview of the model profitability.\n- **Average profit per prediction** Along the total profit score, guap will give you the average profit/cost per prediction. Perfect if you have costs per prediction, or if you need to estimate the profitability while scaling.\n\nThat\'s it...for now! Keep up-to-date with release announcements on Twitter [@guap_ml](https://twitter.com/guap_ml)!\n\n## \U0001fa84 Quickstart Install\nFirst install the package using pip\n\n```\npip install guap\n```\n\nThen, you can follow our instructions using the Google Colab demo. We\'re writing the documentation right now.\n\n## ⌛ Status\n- [x] Alpha: We are demoing guap to users and receiving feedback\n- [ ] Private Beta\n- [ ] Public Beta\n- [ ] Official Launch\n\nWatch "releases" of this repo to get notified of major updates, and give the star button a click whilst you\'re there.\n\n## 🙏 Contributing\nPull requests are welcome. You don\'t know where to start? let\'s talk [@guap_ml](https://twitter.com/guap_ml)!\n\n## 💖 License\n[Apache License 2.0](http://www.apache.org/licenses/)\n',
    'author': 'Ulysse Bottello',
    'author_email': 'ulysse@guap.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guap-ml/guap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
