import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name='pycryptostring',
	version='1.0.0',
	description='A text format for easily interacting with cryptographic hashes and keys',
	long_description=read('README.md'),
	long_description_content_type="text/markdown",
	url='https://github.com/darkwyrm/pycryptostring',
	project_urls={
		"Bug Tracker": "https://github.com/darkwyrm/pycryptostring/issues"
	},
	author='Jon Yoder',
	author_email='jon@yoder.cloud',
	license='MIT',
	py_modules=['pycryptostring'],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development",
		"Programming Language :: Python",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=['retval>=1.0.0']
)
