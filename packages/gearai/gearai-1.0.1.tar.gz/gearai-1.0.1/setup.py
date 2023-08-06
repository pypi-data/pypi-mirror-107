 
# IMPORTING REQUIRED LIBRARIES
import os
from codecs import open
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

# SETUP PARAMETERS
setup(
  name = 'gearai',         
  packages = ['gearai','gearai.ga','gearai.ga.tf','gearai.ga.tf.keras'],
  version = '1.0.1',
  license='GNU General Public Version 3',
  description = 'Gear AI is the open source Python Library for solving various AI needs',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = ['Vigneshwar K R'],
  author_email = 'vicky.pcbasic@gmail.com',
  url = 'https://github.com/ToastCoder/gearai',
  download_url = 'https://github.com/ToastCoder/gearai/archive/master.zip',
  keywords = ['ARTIFICIAL INTELLIGENCE', 'TENSORFLOW'],
  install_requires=['tensorflow'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Education',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)