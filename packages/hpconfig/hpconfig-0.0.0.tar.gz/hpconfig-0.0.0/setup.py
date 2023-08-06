#!/bin/env python3

version="0.0.0"

# Get long description from README.md:
with open('README.md', 'r') as fh:
    long_description = fh.read()


from setuptools import setup
setup(
    name='hpconfig',
    description='A Python module to configure heat-pump systems for sustainable heating',
    author='Marc van der Sluys, Paul van Kan, Martin Buitink, Chris Gieling',
    url='https://github.com/MarcvdSluys/HPConfig',
    
    packages=['hpconfig'],
    install_requires=['numpy'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    version=version,
    license='EUPL 1.2',
    keywords=['heat pump','heating','energy'],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
    ]
)

