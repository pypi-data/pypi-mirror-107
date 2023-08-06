from setuptools import setup

setup(
    name = 'imvickykumar999', # while installing pacakge, change name to something unique on pypi.org
    version = '0.1.0', # use different version if updated, like '0.0.2'
    description = 'Website : https://github.com/imvickykumar999/100th-Repository-Morsetor-python-Package',
    long_description = open('README.md').read(),
    url = 'https://imvickykumar999.herokuapp.com',
    author = 'Vicky Kumar',
    keywords = ['Chatting', 'Firebase', 'GitHub Uploader','Morse','custom','python package','function and class','3D line',
    '3D plane', 'angle bw planes or line', 'distance bw point and plane'],
    license = 'MIT',
    packages = ['multivicks', 'vicksbase'], # while importing package
    install_requires = ['']
)
