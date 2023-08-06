# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manim_rubikscube']

package_data = \
{'': ['*']}

install_requires = \
['kociemba-manim-rubikscube', 'manim']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['manim-rubikscube = manim_rubikscube.__main__:main'],
 'manim.plugins': ['manim_rubikscube = manim_rubikscube']}

setup_kwargs = {
    'name': 'manim-rubikscube',
    'version': '0.1.0',
    'description': "A Manim implementation of the classic Rubik's Cube",
    'long_description': "Manim RubiksCube\n============================================\n\n\nThis plugin for `Manim Community <https://www.manim.community/>`_ provides an implementation of the classic Rubik's Cube.\n\nInstallation\n============\n\nThis plugin is `available on PyPi. <https://pypi.org/project/manim-rubikscube/>`_\nUsage of this plugin assumes that Python and Manim are both correctly installed. Manim is listed as a dependency, but no version is specified. This is because the plugin will work with any version of Manim Community that does not have breaking changes to the plugin. Some releases of this plugin have been tested with certain versions of Manim. To see what versions of Manim are confirmed to be compatible with this plugin (to the best of my testing), `see Releases. <https://github.com/WampyCakes/manim-rubikscube/releases>`_ By no means is this exclusive. Most releases of this plugin will work, more or less, on all versions of Manim Community.\n\nTo install the RubiksCube plugin run:\n\n.. code-block:: bash\n\n   pip install manim-rubikscube\n\n\nTo see what version of manim-rubikscube you are running:\n\n.. code-block:: bash\n\n    manim-rubikscube\n\nor\n\n.. code-block:: bash\n\n    pip list\n\nImporting\n=========\n\nTo use the RubiksCube, you can either:\n\n\n* Add ``from manim_rubikscube import *`` to your script\n* Follow the `Manim steps for using plugins <https://docs.manim.community/en/stable/installation/plugins.html#using-plugins-in-projects>`_\n\nOnce the RubiksCube is imported, you can use the RubiksCube as any other mobject.\n\nDocumentation and Examples\n==========================\nDocumentation and examples are `available here. <https://manim-rubikscube.readthedocs.io/en/stable/>`_\n\nLicense\n=======\nThis plugin is licensed under the MIT license. See the ``LICENSE`` file for more information.",
    'author': 'KingWampy',
    'author_email': 'fake-noreply@email.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WampyCakes/manim-rubikscube',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
