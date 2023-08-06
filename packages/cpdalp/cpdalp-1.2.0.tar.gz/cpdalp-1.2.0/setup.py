from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='cpdalp',
      version='1.2.0',
      description=' ALPACA-centered Pure Numpy Implementation of the Coherent Point Drift Algorithm',
      long_description=readme(),
      url='https://github.com/agporto/pycpd',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
      ],
      keywords='image processing, point cloud, registration, mesh, surface',
      author='Arthur Porto',
      author_email='agporto@gmail.com',
      license='MIT',
      packages=['cpdalp'],
      install_requires=['numpy'],
      zip_safe=False)
