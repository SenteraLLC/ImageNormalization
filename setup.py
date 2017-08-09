from setuptools import setup

setup(name='ImageNormalization',
	version='0.1',
	description='Tools for normalizing the reflectance of multispectral imagery.',
	url='',
	author='John Jackson',
	author_email='john.jackson@sentera.com',
	license='',
	packages=['multispectral',],
	install_requires=[
			'Pillow',
	],
	zip_safe=False)