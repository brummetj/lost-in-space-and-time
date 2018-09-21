from setuptools import setup

setup(
    name='lispat',
    entry_points={
        'console_scripts': [
            'lispat = lispat.__main__:main',
        ],
    }
)
