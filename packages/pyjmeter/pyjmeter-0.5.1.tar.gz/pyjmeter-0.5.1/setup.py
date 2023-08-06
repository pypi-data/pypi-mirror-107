#!/usr/bin/env python

from setuptools import setup, find_packages
import os
from os.path import join

def create_manifest():
    manifest_data = ['include README.md LICENSE', 'include recursive-include tests *.py']
    for root, dirs, files in os.walk("jmeter_api"):
        for file in files:
            if file.endswith(".xml"):
                manifest_data.append(f'include {os.path.join(root, file)}')
    with open('MANIFEST.in', 'w', encoding='utf-8') as manifest_file:
        for line in manifest_data:
            manifest_file.write(f'{line}\n')

with open('README.md', 'r') as f:
    README = f.read()

create_manifest()
setup(
    name='pyjmeter',
    version='0.5.1',
    description='JMeter test plan builder',
    long_description_content_type='text/markdown',
    long_description=README,
    author='Alexey Svetlov',
    author_email='alexeysvetlov92@gmail.com',
    url='https://github.com/lanitgithub/jmeter_api',
    # license='MIT',
    include_package_data=True,
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'atomicwrites', 'attrs', 'colorama',
        'importlib-metadata', 'Jinja2', 'MarkupSafe',
        'more-itertools', 'packaging', 'pluggy',
        'py', 'pytest', 'pyparsing', 'python-dateutil', 'six',
        'wcwidth', 'xmltodict', 'zipp',
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        # 'Documentation': 'https://requests.readthedocs.io',
        'Source': 'https://github.com/lanitgithub/jmeter_api',
    },
)
