from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='Dev_WordList_Gen',
  version='0.0.3',
  description='Create a Wordlist Easily.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Logendher Gunasekaran',
  author_email='logendher@bytfort.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='wordlist', 
  packages=find_packages(),
  install_requires=[''] 
)
