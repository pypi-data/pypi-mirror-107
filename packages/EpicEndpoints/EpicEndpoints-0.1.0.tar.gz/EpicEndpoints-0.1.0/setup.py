from setuptools import setup

setup(
   name='EpicEndpoints',
   version='0.1.0',
   author='AtomicXYZ',
   packages=['EpicEndpoints'],
   url='http://pypi.python.org/pypi/EpicEndpoints/',
   license='LICENSE',
   description='An awesome package that does something',
   long_description=open('README.md').read(),
   install_requires=[
       "requests",
   ],
)