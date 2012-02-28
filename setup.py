from setuptools import setup, find_packages
import os

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='mlmmj_archiver',
	version = '0.1',
	author = 'Mate Gabri',
	author_email = 'mate@gabri.hu',
	description = ('Wrapper script for Hypermail to manage the archives of mlmmj lists.'),
	license = 'BSD',
	keywords = 'mlmmj archive hypermail',
	url = 'http://packages.python.org/mlmmj_archiver',
	long_description = read('README.md'),
	classifiers = [
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: BSD License",
		"Topic :: System :: Archiving",
		"Topic :: Utilities",
	],
	packages = find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=["PyYAML"],
	entry_points={
		'console_scripts': [
			'mlmmj_archiver = mlmmj_archiver.main:main',
			],
		},
)
