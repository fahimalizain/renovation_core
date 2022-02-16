from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in school_app_frappe/__init__.py
from school_app_frappe import __version__ as version

setup(
	name="school_app_frappe",
	version=version,
	description="School App",
	author="Leam",
	author_email="info@leam.ae",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
