import setuptools
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'piglr'))
from version import VERSION as __version__

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

setuptools.setup(
    name='piglr',
    version=__version__,
    author='Christian Lang',
    author_email='me@christianlang.io',
    description='A Pig Reinforcement Learning Environment.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/christianwlang/piglr',
    download_url='https://pypi.org/project/piglr/',
    project_urls={
        'Documentation': 'https://piglr.readthedocs.io/en/latest/',
        'Source': 'https://github.com/christianwlang/piglr',
        'Tracker': 'https://github.com/christianwlang/piglr/issues'
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    license=license,
    extras_require={
        'testing': ['pytest', 'pytest-cov', 'flake8'],
        'docs': ['sphinx']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
