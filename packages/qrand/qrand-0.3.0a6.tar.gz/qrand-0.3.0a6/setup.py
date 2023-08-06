# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qrand',
 'qrand.caches',
 'qrand.errors',
 'qrand.helpers',
 'qrand.platforms',
 'qrand.platforms.cirq',
 'qrand.platforms.qiskit',
 'qrand.platforms.qsharp',
 'qrand.protocols',
 'qrand.validation']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0', 'randomgen>=1.19.3,<2.0.0']

extras_require = \
{'cirq': ['cirq>=0.10.0,<0.11.0'],
 'qiskit': ['qiskit>=0.25.0,<0.26.0'],
 'qsharp': ['qsharp>=0.15.2103,<0.16.0']}

setup_kwargs = {
    'name': 'qrand',
    'version': '0.3.0a6',
    'description': 'A multiprotocol and multiplatform quantum random number generation framework',
    'long_description': '[![Unitary Fund](https://img.shields.io/badge/Supported_By-UNITARY_FUND-FFF000.svg?style=flat)](http://unitary.fund)\n[![YouTube](https://img.shields.io/badge/PR-qrand-FF0000.svg?style=flat&logo=YouTube&logoColor=white)](https://youtu.be/CG7BxuWFpME)\n[![PyPI](https://img.shields.io/pypi/v/qrand?label=PyPI&style=flat&color=3776AB&logo=Python&logoColor=white)](https://pypi.org/project/qrand/)\n[![Coverage](https://img.shields.io/badge/Coverage-67%25-green.svg?style=flat)](http://pytest.org)\n[![Apache-2.0 License](https://img.shields.io/github/license/pedrorrivero/qrand?label=License&style=flat&color=1D1D1D)](https://github.com/pedrorrivero/qrand/blob/master/LICENSE)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4755731.svg)](https://doi.org/10.5281/zenodo.4755731)\n\n\n# qrand\n\n> A multiprotocol and multiplatform quantum random number generation framework\n\nRandom numbers are everywhere.\n\nComputer algorithms, data encryption, physical simulations, and even the arts use them all the time. There is one problem though: it turns out that they are actually very difficult to produce in large amounts. Classical computers can only implement mathematical tricks to emulate randomness, while measuring it out of physical processes turns out to be too slow. Luckily, the probabilistic nature of quantum computers makes these devices particularly useful for the task.\n\nQRAND is a free and open-source framework for quantum random number generation. Thanks to its loosely coupled design, it offers seamlessly compatibility between different [quantum computing platforms](#supported-quantum-platforms) and [QRNG protocols](#implemented-qrng-protocols). Not only that, but it also enables the creation of custom cross-compatible protocols, and a wide range of output formats (e.g. bitstring, int, float, complex, hex, base64).\n\nTo boost its efficiency, QRAND makes use of a concurrent cache to reduce the number of internet connections needed for random number generation; and for quality checks, it incorporates a suite of classical entropy validation tests which can be easily plugged into any base protocol.\n\nAdditionally, QRAND introduces an interface layer for [NumPy](https://numpy.org/) that enables the efficient production of quantum random numbers (QRN) adhering to a wide variety of probability distributions. This is ultimately accomplished by transforming uniform probability distributions produced in cloud-based real quantum hardware, through NumPy\'s random module.\n\n```python3\nfrom qrand import QuantumBitGenerator\nfrom qrand.platforms import QiskitPlatform\nfrom qrand.protocols import HadamardProtocol\nfrom numpy.random import Generator\nfrom qiskit import IBMQ\n\nprovider = IBMQ.load_account()\nplatform = QiskitPlatform(provider)\nprotocol = HadamardProtocol()\nbitgen = QuantumBitGenerator(platform, protocol)\ngen = Generator(bitgen)\n\nprint(f"Random Raw: {bitgen.random_raw()}")\nprint(f"Random Bitstring: {bitgen.random_bitstring()}")\nprint(f"Random Unsigned Int: {bitgen.random_uint()}")\nprint(f"Random Double: {bitgen.random_double()}")\n\nprint(f"Random Binomial: {gen.binomial(4, 1/4)}")\nprint(f"Random Exponential: {gen.exponential()}")\nprint(f"Random Logistic: {gen.logistic()}")\nprint(f"Random Poisson: {gen.poisson()}")\nprint(f"Random Std. Normal: {gen.standard_normal()}")\nprint(f"Random Triangular: {gen.triangular(-1, 0, 1)}")\n# ...\n```\n\n## Supported quantum platforms\nAs of May 2021, only [`Qiskit`](https://qiskit.org/) is supported. However, support for [`Cirq`](https://quantumai.google/cirq) and [`Q#`](https://docs.microsoft.com/en-us/azure/quantum/user-guide/?view=qsharp-preview) is under active development.\n\n## Implemented QRNG protocols\nAs of May 2021, only the basic `HadamardProtocol` is available. We are also working on implementing this [`EntaglementProtocol`](https://www.nature.com/articles/s41598-019-56706-2), as well as a version of [Google\'s Sycamore routine](https://arxiv.org/abs/1612.05903) (patent permitting).\n\n## Authors and citation\nQRAND is the work of many people who contribute to the project at\ndifferent levels. If you use QRAND, please cite as per the included\n[BibTeX file](QRAND.bib).\n\n<!-- ## Documentation -->\n\n## Contribution guidelines\nIf you\'d like to contribute to QRAND, please take a look at the\n[contribution guidelines](CONTRIBUTING.md). This project adheres to the following [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.\n\nWe use [GitHub issues](https://github.com/pedrorrivero/qrand/issues) for tracking requests and bugs. Please use Unitary Fund\'s [Discord](http://discord.unitary.fund/) for discussion and simple questions.\n\n## Acknowledgements\nParts of this software\'s source code have been borrowed from the [qRNG](https://github.com/ozanerhansha/qRNG) project, which is licensed under the [GNU GPLv3](https://github.com/ozanerhansha/qRNG/blob/master/LICENSE) license. Copyright notice and specific changes can be found as a docstring wherever this applies.\n\n## License\n[Apache License 2.0](LICENSE)\n\n---\n(c) Copyright 2021 Pedro Rivero\n',
    'author': 'Pedro Rivero',
    'author_email': 'pedro.rivero.ramirez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pedrorrivero/qrand',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
