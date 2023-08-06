from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  "Operating System :: Unix",
  "Operating System :: MacOS :: MacOS X",
  "Operating System :: Microsoft :: Windows",
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='PythonDatabaseModule',
  version='1.5.3',
  description="""A database for python.It is offline and it is still in testing phase!""",
  long_description=open('README.txt').read(),
  url='',  
  author='Jonian Bicaku',
  author_email='joni.bicaku@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='database', 
  packages=find_packages(),
  install_requires=['os'] 
)
