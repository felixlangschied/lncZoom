from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lncZoom",
    version="0.0.1",
    python_requires='>=3.7.0',
    description=" Extend LncLOOM Motifs across species tree ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Felix Langschied",
    author_email="langschied@bio.uni-frankfurt.de",
    # url="https://github.com/felixlangschied/ncortho",
    packages=find_packages(),
    package_data={'': ['*']},
    install_requires=[
        'beautifulsoup4',
        'pyfaidx',
        'taxOrder',
        'ete3',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': ["lncZoom = lncZoom.main:main"]
    },
    license="GPL-3.0",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)