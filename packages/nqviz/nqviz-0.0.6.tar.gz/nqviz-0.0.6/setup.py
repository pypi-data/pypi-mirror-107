from setuptools import setup
from os import path

# read the contents of README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='nqviz',
      version='0.0.6',
      description='N Queen Visualizer',
      url='https://github.com/jhan15/nqviz',
      author = 'Jianming Han',
      author_email = 'hjma810@126.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
      ],
      packages=['nqviz'],
      install_requires=['pygame>=2.0.1'],
      python_requires='>=3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
