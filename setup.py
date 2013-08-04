from setuptools import setup, find_packages

import sys, os

__version__ = '0.1'

setup(name='haproxyutils',
	version=__version__,
	description="The haproxy utilities.",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX",
		"Environment :: Console",
		"Programming Language :: Python",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries :: Python Modules",
	], 
	keywords='haproxy',
	author='Daniel Myers',
	author_email='dmyers@channeliq.com',
	url='http://github.com/',
	license='MIT',
	packages=['haproxyutils'],
)
