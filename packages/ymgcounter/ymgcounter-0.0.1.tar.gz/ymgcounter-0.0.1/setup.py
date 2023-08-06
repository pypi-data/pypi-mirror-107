from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'very basic counter'

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ymgcounter',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Yam',
    author_email='ymgchbrtv0095@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['math', 'counter'],
    packages=find_packages(),
    install_requires=[]
)
