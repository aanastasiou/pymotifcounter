import sys

from setuptools import setup, find_packages

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
    packages=find_packages(exclude=('test', 'test.*')),
    keywords='',
    # scripts=['scripts/neomodel_install_labels', 'scripts/neomodel_remove_labels'],
    # setup_requires=['pytest-runner'] if any(x in ('pytest', 'test') for x in sys.argv) else [],
    # tests_require=['pytest', 'shapely', 'neobolt'],
    install_requires=['pandas', 'networkx', 'pyparsing'],
    # classifiers=[]
    )
