from setuptools import setup 
  
# reading long description from file 
with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 
  
  
# specify requirements of your package here 
REQUIREMENTS = ['numpy','numba','matplotlib','scipy'] 
  
# some more details 
CLASSIFIERS = [ 
    'Development Status :: 4 - Beta', 
    'Intended Audience :: Developers', 
    'Topic :: Internet', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.6', 
    ] 
  
# calling the setup function  
setup(name='pycabanas', 
      version='0.0.11', 
      description='Spin Glass Analysis', 
      long_description=long_description, 
      url='https://github.com/ocabanas/pycabanas', 
      author='Oriol Cabanas', 
      author_email='oriol.cabanas@gmail.com', 
      license='MIT', 
      packages=['pycabanas'], 
      classifiers=CLASSIFIERS, 
      install_requires=REQUIREMENTS, 
      keywords=''
      ) 