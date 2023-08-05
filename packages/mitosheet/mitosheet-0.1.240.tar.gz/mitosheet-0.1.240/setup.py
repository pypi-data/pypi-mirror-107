#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
The mitosheet package is distributed under the mitosheet and mitosheet3
package names on pip. The package.json will tell you all you need to 
know about which one we are in currently using.

As such, this setup.py script reads in the package.json and sets up
the proper package.
"""

from __future__ import print_function
from glob import glob
from os.path import join as pjoin
import json
import setuptools
from pathlib import Path


from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    skip_if_exists,
    ensure_python,
)

from setuptools import setup

HERE = Path(__file__).parent.resolve()

package_json = json.loads(open('package.json').read())
lab_path = Path(pjoin(HERE, 'mitosheet', 'labextension'))


# The name of the project
name = package_json['name']

# Ensure a valid python version
ensure_python('>=3.4')


if name == 'mitosheet':
    # Get our version, which we just read 
    version = package_json['version']

    # Representative files that should exist after a successful build
    jstargets = [
        pjoin(HERE, 'lib', 'plugin.js'),
    ]

    package_data_spec = {
        name: [
            'labextension/*.tgz'
        ]
    }

    data_files_spec = [
        ('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ]


    cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
        data_files_spec=data_files_spec)
    cmdclass['jsdeps'] = combine_commands(
        install_npm(HERE, build_cmd='build:all'),
        ensure_targets(jstargets),
    )

    setup_args = dict(
        name            = name,
        description     = 'The Mito Spreadsheet',
        version         = version,
        scripts         = glob(pjoin('scripts', '*')),
        cmdclass        = cmdclass,
        packages        = setuptools.find_packages(exclude=['deployment']),
        author          = 'Mito',
        author_email    = 'naterush1997@gmail.com',
        license         = package_json["license"],
        url             = 'https://github.com/mito/mito',
        platforms       = "Linux, Mac OS X, Windows",
        keywords        = ['Jupyter', 'Widgets', 'IPython'],
        classifiers     = [
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: ' + package_json["license"],
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Framework :: Jupyter',
        ],
        include_package_data = True,
        # NOTE: this should be the same as the INSTALL_REQUIRES variable in
        # the mitoinstaller package
        install_requires = [
            # We require jupyterlab 2.0
            'jupyterlab>=2.0,<3.0,!=2.3.0,!=2.3.1', # there are css incompatabilities on version 2.3.1 and 2.3.0
            'ipywidgets>=7.0.0',
            'pandas>=1.1.0',
            # We don't need to lock an analytics-python version, as this library
            # is stabilized and mature
            'analytics-python',
            # Graphing libraries
            'plotly==4.14.3'
        ],
        extras_require = {
            'test': [
                'pytest',
                'flake8',
            ],
            'deploy': [
                'wheel', 
                'twine',
                "jupyter_packaging"
            ]
        },
        entry_points = {
        },
        long_description="""
            To learn more about Mito, checkout out our documentation: https://docs.trymito.io/getting-started/installing-mito\n\n
            Before installing Mito \n\n
            1. Check that you have Python 3.6 or above. To check your version of Python, open a new terminal, and type python3 --version. If you need to install or update Python, restart your terminal after doing so.\n\n
            2. Check that you have Node installed.To check this, open a new terminal, and type node -v.  It should print a version number. If you need to install Node, restart your terminal after doing so.\n\n
            3. Mito works in Jupyter Lab 2.0 only. We do not yet support Google Collab, VSCode, or Jupyter Lab 3.0.\n\n
            4. Checkout our terms of service and privacy policy. By installing Mito, you're agreeing to both of them. Please contact us at aarondr77 (@) gmail.com with any questions.\n\n
            Installation Instructions \n\n
            For more detailed installation instructions, see our documentation: https://docs.trymito.io/getting-started/installing-mito\n\n
            1. pip install mitosheet\n\n
            2. jupyter labextension install @jupyter-widgets/jupyterlab-manager@2\n\n
            3. jupyter lab
            """,
        long_description_content_type='text/markdown'
    )
elif name == 'mitosheet3':
    # Representative files that should exist after a successful build
    jstargets = [
        str(lab_path / "package.json"),
    ]

    package_data_spec = {
        'mitosheet': ["*"],
    }

    labext_name = "mitosheet3"

    data_files_spec = [
        ("share/jupyter/labextensions/%s" % labext_name, str(lab_path), "**"),
        ("share/jupyter/labextensions/%s" % labext_name, str(HERE), "install.json"),
    ]

    cmdclass = create_cmdclass("jsdeps",
        package_data_spec=package_data_spec,
        data_files_spec=data_files_spec
    )

    js_command = combine_commands(
        install_npm(HERE, build_cmd="build:prod", npm=["jlpm"]),
        ensure_targets(jstargets),
    )

    is_repo = (HERE / ".git").exists()
    if is_repo:
        cmdclass["jsdeps"] = js_command
    else:
        cmdclass["jsdeps"] = skip_if_exists(jstargets, js_command)

    setup_args = dict(
        name                    = name,
        version                 = package_json["version"],
        url                     = package_json["homepage"],
        author                  = package_json["author"]["name"],
        author_email            = package_json["author"]["email"],
        description             = package_json["description"],
        license                 = package_json["license"],
        long_description="""
            To learn more about Mito, checkout out our documentation: https://docs.trymito.io/getting-started/installing-mito\n\n
            Before installing Mito \n\n
            1. Check that you have Python 3.6 or above. To check your version of Python, open a new terminal, and type python3 --version. If you need to install or update Python, restart your terminal after doing so.\n\n
            2. Checkout our terms of service and privacy policy. By installing Mito, you're agreeing to both of them. Please contact us at aarondr77 (@) gmail.com with any questions.\n\n
            Installation Instructions \n\n
            For more detailed installation instructions, see our documentation: https://docs.trymito.io/getting-started/installing-mito\n\n
            1. pip install mitosheet3\n\n
            2. jupyter lab
        """,
        long_description_content_type = "text/markdown",
        cmdclass                 = cmdclass,
        packages                 = setuptools.find_packages(exclude=['deployment']),
        install_requires=[
            "jupyterlab~=3.0",
            'ipywidgets>=7.0.0',
            'pandas>=1.1.0',
            'analytics-python',
            # Graphing libraries
            'plotly==4.14.3'
        ],
        extras_require = {
            'test': [
                'pytest',
                'flake8',
            ],
            'deploy': [
                'wheel', 
                'twine',
                "jupyter_packaging"
            ]
        },
        zip_safe                = False,
        include_package_data    = True,
        python_requires         = ">=3.6",
        platforms               = "Linux, Mac OS X, Windows",
        keywords                = ["Jupyter", "JupyterLab", "JupyterLab3"],
        classifiers             = [
            "License :: " + package_json["license"],
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Framework :: Jupyter",
        ],
    )

if __name__ == '__main__':
    setup(**setup_args)
