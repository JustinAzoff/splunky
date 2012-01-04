from setuptools import setup, find_packages
import sys, os
from glob import glob


version = '0.4'

setup(name='splunky',
    version=version,
    description="Simply Splunk interface",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='Splunk',
    author='Justin Azoff',
    author_email='JAzoff@uamail.albany.edu',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "httplib2",
        "lxml",
    ],
    scripts=glob('scripts/*'),
    #entry_points = {
    #    'console_scripts': [
    #    ]
    #},
    )
