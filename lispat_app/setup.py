import lispat

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    import os
    import re

    def find_packages(path=''):
        ret = []

        for root, dirs, files, in os.walk(path):
            if '__init__.py' in files:
                ret.append(re.sub('^[^A-z0-9_]+', '', root.replace('/', '.')))
        return ret

install_requires = [
    'chardet==2.3.0',
    'nltk',
    'pdfminer.six',
    'pygogo',
    'python-docx',
    'docopt',
    ]

setup(
    name='lispat',
    install_requires=install_requires,
    author='Joshua Brummet, Zeke, Eric',
    entry_points={
        'console_scripts': [
            'lispat = lispat.run:main',
        ],
    },
    packages=find_packages(),
)
