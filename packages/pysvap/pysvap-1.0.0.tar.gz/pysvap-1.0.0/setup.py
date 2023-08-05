"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = open('README.md').read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name='pysvap',  # Required

    version='1.0.0',  # Required

    description='A python library for image Manipulation which implements different algorithm designs on rgb values of each individual pixel ',
    # Optional

    long_description=long_description,  # Optional

    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://github.com/shubh-vashisht/PySvap',  # Optional

    author='Shubh Vashisht and Aman Priyadarshi',  # Optional

    author_email='shubhv2@gmail.com, aman19294@iiitd.ac.in',  # Optional

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='imageManipulation, image, pixels',
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['Pillow'],
    project_urls={
        'Source': 'https://github.com/shubh-vashisht/PySvap',
    },
)
