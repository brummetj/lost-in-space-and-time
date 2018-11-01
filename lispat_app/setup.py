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
<<<<<<< HEAD
    'nltk',
=======
    'docx2txt==0.6',
>>>>>>> 87680793a859a1002905c6f8b9191546601d0fe6
    'pdfminer.six',
    'pygogo',
    'python-docx',
    'docopt',
<<<<<<< HEAD
=======
    'nltk',
    'gensim'
>>>>>>> 87680793a859a1002905c6f8b9191546601d0fe6
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
