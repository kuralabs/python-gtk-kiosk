#!/usr/bin/env python3

"""
Installation script for the Python GTK Kiosk.
"""

from pathlib import Path
from setuptools import setup, find_packages


def check_directory():
    """
    You must always change directory to the parent of this file before
    executing the setup.py script. setuptools will fail reading files,
    including and excluding files from the MANIFEST.in, defining the library
    path, etc, if not.
    """
    from os import chdir

    here = Path(__file__).parent.resolve()
    if Path.cwd().resolve() != here:
        print('Changing path to {}'.format(here))
        chdir(str(here))


check_directory()


#####################
# Utilities         #
#####################

def read(filename):
    """
    Read the content of a file.

    :param str filename: The file to read.

    :return: The content of the file.
    :rtype: str
    """
    return Path(filename).read_text(encoding='utf-8')


def find_files(search_path, include=('*', ), exclude=('.*', )):
    """
    Find files in a directory.

    :param str search_path: Path to search for files.
    :param tuple include: Patterns of files to include.
    :param tuple exclude: Patterns of files to exclude.

    :return: List of files found that matched the include collection but didn't
     matched the exclude collection.
    :rtype: list
    """
    from os import walk
    from fnmatch import fnmatch
    from os.path import join, normpath

    def included_in(fname, patterns):
        return any(fnmatch(fname, pattern) for pattern in patterns)

    files_collected = []

    for root, folders, files in walk(search_path):
        files_collected.extend(
            normpath(join(root, fname)) for fname in files
            if included_in(fname, include) and not included_in(fname, exclude)
        )

    files_collected.sort()
    return files_collected


#####################
# Finders           #
#####################

def find_version(filename):
    """
    Find version of a package.

    This will read and parse a Python module that has defined a __version__
    variable. This function does not import the file.

    ::

        setup(
            ...
            version=find_version('lib/package/__init__.py'),
            ...
        )

    :param str filename: Path to a Python module with a __version__ variable.

    :return: The version of the package.
    :rtype: str
    """
    import re

    content = read(filename)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M
    )
    if not version_match:
        raise RuntimeError('Unable to find version string.')

    version = version_match.group(1)

    print('Version found:')
    print('  {}'.format(version))
    print('--')

    return version


def find_requirements(filename):
    """
    Finds PyPI compatible requirements in a pip requirements.txt file.

    In this way requirements needs to be specified only in one, centralized
    place:

    ::

        setup(
            ...
            install_requires=find_requirements('requirements.txt'),
            ...
        )

    Supports comments and non PyPI requirements (which are ignored).

    :param str filename: Path to a requirements.txt file.

    :return: List of requirements with version.
    :rtype: list
    """
    import string

    content = read(filename)
    requirements = []
    ignored = []

    for line in (
        line.strip() for line in content.splitlines()
    ):
        # Comments
        if line.startswith('#') or not line:
            continue

        if line[:1] not in string.ascii_letters:
            ignored.append(line)
            continue

        requirements.append(line)

    print('Requirements found:')
    for requirement in requirements:
        print('  {}'.format(requirement))
    print('--')

    print('Requirements ignored:')
    for requirement in ignored:
        print('  {}'.format(requirement))
    print('--')

    return requirements


def find_data(package_path, data_path, **kwargs):
    """
    Find data files in a package.

    ::

        setup(
            ...
            package_data={
                'package': find_data(
                    'lib/package',
                    'data',
                )
            },
            ...
        )

    :param str package_path: Path to the root of the package.
    :param str data_path: Relative path from the root of the package to the
     data directory.
    :param kwargs: Function supports inclusion and exclusion patterns as
     specified in the find_files function.

    :return: List of data files found.
    :rtype: list
    """
    from os.path import join, relpath

    files_collected = find_files(join(package_path, data_path), **kwargs)
    data_files = [relpath(fname, package_path) for fname in files_collected]

    print('Data files found:')
    for data_file in data_files:
        print('  {}'.format(data_file))
    print('--')

    return data_files


setup(
    name='python_gtk_kiosk',
    version=find_version('python_gtk_kiosk/__init__.py'),
    packages=find_packages(),

    # Dependencies
    install_requires=find_requirements('requirements.txt'),

    # Data files
    package_data={
        'python-gtk-kiosk': find_data(
            'python_gtk_kiosk',
            'data',
        )
    },

    # Metadata
    author='KuraLabs S.R.L',
    author_email='info@kuralabs.io',
    description=(
        'This application is an example of how to use CSS and custom fonts '
        'with GTK and how to start the application in kiosk mode.'
    ),
    url='https://github.com/kuralabs/python-gtk-kiosk',

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],

    python_requires='>=3.5.0',

    entry_points={
        'console_scripts': [
            'python-gtk-kiosk = python_gtk_kiosk.__main__:main',
        ]
    },
)
