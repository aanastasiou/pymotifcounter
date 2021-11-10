import os
import json
import warnings

from setuptools import setup, find_packages


def get_pymotifcounter_binaries():
    """
    Autodiscovers which binaries the user may have configured and installs them in the current Python interpreter's bin/
    directory.

    :returns: A list of relative path binaries that will be installed in the local interpreter's bin/ directory.
    :rtype: list
    """
    try:
        with open("binaries/binaries_to_install.json") as fd:
            default_binaries = json.load(fd)

        existing_binaries = list(filter(lambda x: os.path.exists(x), default_binaries))
    except FileNotFoundError:
        existing_binaries = []

    if len(existing_binaries)<1:
        warnings.warn("!!!None of the core binaries are installed in the local Python interpreter's bin/ as part of this "
                      "installation!!!")

    return existing_binaries


setup(
    name='pymotifcounter',
    version='0.0.1',
    description='A simple wrapper for graph motif counting algorithms',
    long_description=open('README.rst').read(),
    author='Athanasios Anastasiou',
    author_email='athanastasiou@gmail.com',
    zip_safe=True,
    url='',
    license='',
    # packages=find_packages(exclude=('test', 'test.*')),
    packages=["pymotifcounter",],
    keywords='',
    data_files=[("bin", get_pymotifcounter_binaries()), ],
    # scripts=['scripts/neomodel_install_labels', 'scripts/neomodel_remove_labels'],
    # setup_requires=['pytest-runner'] if any(x in ('pytest', 'test') for x in sys.argv) else [],
    tests_require=['pytest'],
    install_requires=['pandas', 'networkx', 'pyparsing'],
    # classifiers=[]
    )
