from setuptools import setup
from setuptools import find_packages
import os

def readme():
    with open('README.md') as file:
        return(file.read())

def versionNumber():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poissonDiskSampling/_version.py')) as versionFile:
        return(versionFile.readlines()[-1].split()[-1].strip("\"'"))

setup(name='poissonDiskSampling',
      version=versionNumber(),
      description='Poisson Disk Sampling Algorithm with Variable Sampling Radius',
      long_description_content_type="text/markdown",
      long_description=readme(),
      classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
      ],
      url='https://gitlab.com/abittner/poissonDiskSampling',
      author='Adrian Bittner',
      author_email='adrian.bittner@eso.org',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'matplotlib>=3.1',
        'numpy>=1.17',
      ],
      python_requires='>=3.6',
      entry_points={
      },
      include_package_data=True,
      zip_safe=False)
