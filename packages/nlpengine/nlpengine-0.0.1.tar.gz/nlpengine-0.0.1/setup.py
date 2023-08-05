#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Sudheesh Sudevan",
    author_email='sudheesh_sudevan@live.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A collection of Natural Language Processing tools to make your life easier.",
    entry_points={
        'console_scripts': [
            'nlpengine=nlpengine.cli:main',
        ],
    },
    # install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nlpengine',
    name='nlpengine',
    packages=find_packages(include=['nlpengine', 'nlpengine.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sudheesh_sudevan/nlpengine',
    version='0.0.1',
    zip_safe=False,
    install_requires=[
          'scikit-learn', 
          'pandas',
          'fasttext==0.9.2',
          'wget',
          'docx'],
)
