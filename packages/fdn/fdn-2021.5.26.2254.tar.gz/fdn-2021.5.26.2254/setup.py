from setuptools import find_packages
from setuptools import setup

import fnx

setup(
    name='fdn',
    version=fnx.__version__,
    packages=find_packages('.'),
    url='https://github.com/hobbymarks/fnx',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    author='hobbymarks',
    author_email='ihobbymarks@gmail.com',
    description="uniformly change file or directory names",
    long_description=
    "xfn used to uniformly change file or directory names and also support "
    "rollback these operations. ",
    include_package_data=True,
    install_requires=[
        "click>=8.0.0", "setuptools>=49.6.0", "unidecode>=1.2.0",
        "cryptography>=3.4.7", "colorama>=0.4.4", "pandas>=1.2.4",
        "wcwidth>=0.2.5"
    ],
    entry_points={
        'console_scripts': [
            'fdn = fnx:run_main',
        ],
    },
)
