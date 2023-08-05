# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='py-toolkit',
    version='0.0.4',
    packages=find_packages(exclude=("tests",)),
    url='https://github.com/DewMaple/toolkit',
    description='python toolkit for common usage',
    author='DewMaple',
    author_email='dewmaple@gmail.com',
    license='',
    keywords=['python', "schema meta"],
    classifiers=['Programming Language :: Python :: 3.6'],
    project_urls={
        'Bug Reports': 'https://github.com/DewMaple/toolkit/issues',
        'Source': 'https://github.com/DewMaple/toolkit',
    },
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-xprocess",
    ],
    zip_safe=True
)