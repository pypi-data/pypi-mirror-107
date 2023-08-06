from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Almost all Searching and Sorting Algorithms for python'
LONG_DESCRIPTION = """
A package that allows you to :-
1. Search an element in an array using various searching techniques.
2. Sort an array using various sorting algorithms.
"""

# Setting up
setup(
    name="searchsort",
    version=VERSION,
    author="Programmin-in-Python (MK)",
    author_email="<kalanithi6014@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python3', 'sort', 'search', 'sorting', 'searching', 'sorting-algorithms',
                'searching-algorithms', 'search-sort', 'searchsort'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)