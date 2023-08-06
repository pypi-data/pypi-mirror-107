import pathlib
import os
import subprocess

from setuptools import find_packages, setup

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
with open(here / 'README.md', 'r') as readme:
    long_description = readme.read()


def get_latest_tag():
    os.system('git fetch --tags')
    return subprocess.check_output(['git', 'describe', '--tags']).decode().strip()


def bump_patch(vers):
    major, minor, patch = vers.split('.')
    if not patch.isnumeric():
        return vers
    bumped_patch = str(int(patch) + 1)
    return '.'.join([major, minor, bumped_patch])


VERSION = '0.0.0'
if 'DEPLOY' in os.environ:
    VERSION = os.environ['GITHUB_REF'].split('/')[-1]


setup(
    name='fit-tracker',
    version=VERSION,
    description='A lightweight experiment tracker for numerical optimization problems.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/atraders/fit-tracker',
    author='@genziano',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='ml, operation research, optimization, logging',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=[],
    extras_require={'dev': ['pylint', 'pytest', 'mypy', 'isort'],},
)
