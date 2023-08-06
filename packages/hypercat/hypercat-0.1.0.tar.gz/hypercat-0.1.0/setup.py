# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypercat']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=3.1.2',
 'h5py>=2.9.0',
 'matplotlib>=3.0.3',
 'numpy>=1.16.2',
 'scikit-image>=0.15.0',
 'scipy>=1.2.1',
 'urwid>=2.0.1']

setup_kwargs = {
    'name': 'hypercat',
    'version': '0.1.0',
    'description': 'Hypercube of clumpy AGN tori',
    'long_description': 'hypercat\n========\nHypercubes of (clumpy) AGN tori\n\n**Authors:** Robert Nikutta [\\<robert.nikutta@gmail.com\\>](mailto:robert.nikutta@gmail.com), Enrique Lopez-Rodriguez, Kohei Ichikawa\n\n**Version:** 2021-05-31\n\n**License:** BSD-3-Clause, please see [LICENSE](./LICENSE) file\n\n**Attribution:** Please cite this repository, and the following papers:\n\n[R. Nikutta, E. Lopez-Rodriguez, K. Ichikawa, N. A. Levenson, C. Packham, A. Alonso-Herrero, S. F. Hönig; "Hypercubes of AGN Tori (HYPERCAT) -- I. Models and Image Morphology"; ApJ 2021, accepted for publication](TODO: link)\n\n[Nikutta, Lopez-Rodriguez, Ichikawa, Levenson, Packham, Alonso-Herrero, Hönig; "Hypercubes of AGN Tori (HYPERCAT) -- II. Reolving the Torus with with Extremely Large Telescopes"; ApJ 2021, under review](TODO: link)\n\n**Synopsis:**\nHandle a hypercube of CLUMPY brightness maps. Easy-to-use classes and\nfunctions are provided to interpolate images in many dimensions\n(spanned by the model parameters), extract monochromatic or\nmulti-wavelength images, as well as rotate images, zoom in and out,\napply PSFs, extract interferometric signals, etc.\n\n**User Manual and Examples:**\nFor installation instructions and many usage examples, please see the\nHYPERCAT User Manual [User Manual](./docs/manual/) and the [example\nJupyter notebooks](./examples/)\n',
    'author': 'Robert Nikutta',
    'author_email': 'robert.nikutta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rnikutta/hypercat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
