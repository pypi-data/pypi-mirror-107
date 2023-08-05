import setuptools
from setuptools import setup

setup(
    name='FileHandler',
    version='v1.0.13',
    url='',
    license='',
    author='chienaeae',
    author_email='chienaeae@gmail.com',
    description='file processor package',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["requests==2.25.1"],
)
