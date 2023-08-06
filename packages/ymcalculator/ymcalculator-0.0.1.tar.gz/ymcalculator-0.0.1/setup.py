from setuptools import setup, find_packages
 
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 2.7',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ymcalculator',
  version='0.0.1',
  description='The very zimple calculato',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  # the URL of your package's home page e.g. github link
  author='Yam',
  author_email='ymgchbrtv0095@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='calculator', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=[''] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)
