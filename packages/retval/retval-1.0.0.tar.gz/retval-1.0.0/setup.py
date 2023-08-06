import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name='retval',
	version='1.0.0',
	description='a module for easy error-handling without exceptions',
	long_description=read('README.md'),
	long_description_content_type="text/markdown",
	url='https://github.com/darkwyrm/retval',
	project_urls={
		"Bug Tracker": "https://github.com/darkwyrm/retval/issues"
	},
	author='Jon Yoder',
	author_email='jon@yoder.cloud',
	license='MIT',
	packages=find_packages(),
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development",
		"Programming Language :: Python",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
