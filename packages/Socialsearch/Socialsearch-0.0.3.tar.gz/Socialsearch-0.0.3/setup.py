from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 2'
]
 
setup(
  name='Socialsearch',
  version='0.0.3',
  description='A very Special Searcher',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Borys Kostka',
  author_email='borys.kostka09@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Searcher', 
  packages=find_packages(),
  install_requires=[''] 
)