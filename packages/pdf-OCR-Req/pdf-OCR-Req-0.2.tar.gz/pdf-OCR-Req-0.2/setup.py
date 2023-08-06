
from setuptools import setup, find_packages

setup(
    name='pdf-OCR-Req',
    version='0.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=open('README.txt').read(),
    install_requires=['numpy','fitz'],
    author='Vardhani k ',
    author_email='myemail@example.com'
)
