from setuptools import setup, find_packages

setup(
    name='sensorbucket',
    version='0.1.0',
    author='Tim van Osch',
    author_email='timvosch@pollex.nl',
    package_dir={"": "sensorbucket"},
    packages=find_packages(where="sensorbucket"),
    url='http://pypi.python.org/pypi/Sensorbucket/',
    license='LICENSE',
    description='Provides interaction with the SensorBucket API'
)
