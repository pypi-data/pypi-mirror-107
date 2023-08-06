from setuptools import setup
import os
from setuptools import setup

# with open('requirements.txt') as f:
#     required = f.read().splitlines()

setup(name='test_data_lake',
      version='0.0.0.11',
      description='processes Datalake to Bronze-Silver_Gold',
      url='https://upload.pypi.org/test_alex',
      author='Imparnert',
      author_email='alex-12-04@hotmail.com',
      license='MIT',
      packages=['delta_lake'],
      # entry_points={'console_scripts': ['Package = Package.__main__:main'], },
      # install_requires=required,
      classifiers=["Programming Language :: Python :: 3"],
      python_requires='>=3',
      zip_safe=False,
      # scripts=[
      #           'requirements.txt',
      #           'README.md',
      #          ],
      long_description=open('README.md').read(),
      # include_package_data=True,
      )
