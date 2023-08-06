
from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

def requirements():
    with open('requirements.txt') as f:
        return f.read().split('\n')

setup(name='SocketFactory',
      version='1.0.7',
      url='https://github.com/LindaGuiducci/SocketFactory.git',
      description=('Python library to analyze how the shape of the stump evolves,'
      ' from the cast to the finished socket, based on the three-dimensional digitization of the surfaces.'),
      author='Linda Guiducci and Ioana Madalina Raileanu',
      author_email='ioanamadalina.raileanu@mail.polimi.it',
      long_description=readme(),
      long_description_content_type='text/markdown',
      include_package_data=True,
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3.8',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering'
      ],
      py_modules=["SocketFactory"],
      install_requires=requirements(),
      python_requires='>=3.8',  # Your supported Python ranges
)