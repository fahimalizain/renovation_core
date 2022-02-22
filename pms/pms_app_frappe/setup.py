from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pms_app_frappe/__init__.py
from pms_app_frappe import __version__ as version

setup(
	name="pms_app_frappe",
	version=version,
	description="PMS Frappe App",
	author="Leam Technology Systems",
	author_email="info@leam.ae",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
