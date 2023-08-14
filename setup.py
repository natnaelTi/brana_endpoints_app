from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in brana_endpoints_app/__init__.py
from brana_endpoints_app import __version__ as version

setup(
	name="brana_endpoints_app",
	version=version,
	description="This Frappe application is Brana Audiobooks\' server-side application.",
	author="Natnael Tilaye",
	author_email="natnaeltilaye30@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
