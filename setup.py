from setuptools import setup

version = '19.7.0'

setup(
   name = 'ephemerides',
   version = version,
   author = 'R. Thomas, T. Berg',
   packages = ['ephemerides'],
   description = 'ESO official ephemerides in Python',
   python_requires = '>=3.6',
   install_requires = [
        "requests >= 2.22.0",
        "bs4 >= 0.0.1",
       ],
   include_package_data=True,
)
