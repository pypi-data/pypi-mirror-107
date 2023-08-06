from setuptools import setup, find_packages, Extension

README= open("README.md").read()

VERSION = '0.0.1' 
DESCRIPTION = 'RF-PHATE'
LONG_DESCRIPTION = README

# Setting up
setup(
        name="rf_phate", 
        version=VERSION,
        author="Jake Rhodes",
        author_email="jakerhodes@aggiemail.usu.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
	long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[],
        
        keywords=['random forest', 'proximities', 'dimensionality reduction'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ],

	license="GNU General Public License Version 2",
)