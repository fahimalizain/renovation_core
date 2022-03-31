from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pms_manager/__init__.py
from pms_manager_frappe import __version__ as version

setup(
    name="pms_manager_frappe",
    version=version,
    description="Frappe app for PMS Manager",
    author="Leam Technology Systems",
    author_email="info@leam.ae",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
