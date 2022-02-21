from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in todo_app_frappe/__init__.py
from todo_app_frappe import __version__ as version

setup(
	name="todo_app_frappe",
	version=version,
	description="Todo App Frappe",
	author="LEAM",
	author_email="info@leam.ae",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
