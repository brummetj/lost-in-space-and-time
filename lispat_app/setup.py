from setuptools import setup

setup(
    name='snek',
    entry_points={
        'console_scripts': [
            'lispat = lispat:main',
        ],
    }
)
