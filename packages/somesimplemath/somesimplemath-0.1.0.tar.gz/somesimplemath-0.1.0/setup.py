from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Module for simple math.'

setup(
	name="somesimplemath", 
	version=VERSION,
	author="Felix Ou",
	author_email="felixcou@outlook.com",
	description=DESCRIPTION,
	long_description="Simple math module similar to the built-in MATH module.",
	packages=find_packages(),
	install_requires=[],
	keywords=['math'],
	classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
