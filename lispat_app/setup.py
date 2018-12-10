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
    'nltk',
    'pdfminer.six',
    'pygogo',
    'python-docx',
    'docopt',
    'gensim',
    'cld2-cffi',
    'joblib'
    'spacy',
    'chardet==3.0.4',
    'textblob',
    'matplotlib==2.1.0',
    'sklearn'
    'scattertext'
    'empath',
    'mpdl3'
    'git+https://github.com/javadba/mpld3@display_fix'
]

setup(
    name='lispat',
    install_requires=install_requires,
    author='Joshua Brummet, Zeke Moreland, Eric Holguin',
    entry_points={
        'console_scripts': [
            'lispat = lispat.run:main',
        ],
    },
    packages=find_packages(),
)
