import os
from setuptools import setup, find_packages

VERSION = '1.0.0' 
DESCRIPTION = 'An Open-Source Nature-Inspired Optimization Clustering Framework in Python'
LONG_DESCRIPTION = 'An Open-Source Nature-Inspired Optimization Clustering Framework in Python'

# Setting up
setup(
       # the name must match the folder name 'EvoCC'
        name="EvoCluster", 
        version=VERSION,
        author="Dang Trung Anh, Raneem Qaddoura",
        author_email="dangtrunganh@gmail.com, raneem.qaddoura@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        # package_dir={"": "EvoCluster"},
        packages=find_packages(),
        # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        install_requires=[], 
        url='https://github.com/housecricket/Evo-Cluster',
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],
        package_data = {'': ['datasets/*.csv']},
)