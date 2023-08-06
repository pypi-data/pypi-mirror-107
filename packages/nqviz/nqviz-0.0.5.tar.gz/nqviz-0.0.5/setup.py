from setuptools import setup
from os import path

# read the contents of README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='nqviz',
      version='0.0.5',
      description='N Queen Visualizer',
      packages=['nqviz'],
      install_requires=['pygame>=2.0.1'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      author = 'Jianming Han',
      author_email = 'hjma810@126.com',
      zip_safe=False)