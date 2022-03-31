from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='pms_manager',
    version='0.0.1',
    install_requires=install_requires,
    url='https://github.com/leam-tech/pms_backend',
    license='MIT',
    author='Fahim Ali Zain',
    author_email='fahimalizain@gmail.com',
    description='School App',
    packages=find_packages(""),
    package_dir={"": "src"}
)
