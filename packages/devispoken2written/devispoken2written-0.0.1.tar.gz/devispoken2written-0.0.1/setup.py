from os import name
from setuptools import _install_setup_requires, setup, find_packages, version


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    "Operating System :: OS Independent"
]

setup(name='devispoken2written',
   version='0.0.1',
   description='A module to converts spoken english to written english',
   long_description=open('readme.txt').read() + '\n\n' + open('changelog.txt').read(),
   author='Devi Prasad', 
   author_email='dp.devi03@gmail.com',
   license='MIT',
   classifiers=classifiers,
   keywords='spoken to written english', 
   packages=['devispoken2written'], 
   install_requires=['setuptools', 'wheel'])


