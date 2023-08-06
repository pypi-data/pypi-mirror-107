import pathlib
from setuptools import setup, find_packages


PATH = pathlib.Path(__file__).parent
README = (PATH / 'README.md').read_text()

setup(
    name='hexbuilder',
    version='1.0.3',
    description='Command line tool that converts a text file '
                'to its representing hex code.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/davidmaamoaix/HexBuilder',
    author='David Ma',
    author_email='davidma@davidma.cn',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['hexbuilder=hexbuilder.builder:main']
    }
)