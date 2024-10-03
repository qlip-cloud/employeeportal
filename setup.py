from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in employee_portal/__init__.py
from employee_portal import __version__ as version

setup(
	name='employee_portal',
	version=version,
	description='Employee portal for managing information and services.',
	author='Ashley Mercado Defort',
	author_email='ashley.mercado@mentum.com.co',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
