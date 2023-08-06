from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='helloworld-pkg-tut',
	version='0.0.1',
	description='Simply prints hello <name>',
	py_modules=["helloworld"],
	package_dir={'': 'src'},
	long_description=long_description,
	long_description_content_type="text/markdown",
	install_requires = [
			"numpy ~= 1.18",
		],
	classifiers=[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
			"Operating System :: OS Independent",
		],
	url="https://https://github.com/QuantumSystems/quantum-computing",
	author="Atul Varshneya",
	author_email="atul.varshneya@gmail.com",
	)
