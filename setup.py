from setuptools import setup, find_packages

from pynami import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pynami',
      version=__version__,
      description='Python wrapper forthe NaMi API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: Freeware',
                   'Intended Audience :: Science/Research',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering :: Physics'],
      author='Sebastian Scholz',
      author_email='sebastian.scholz@pfadfinder-weeg.de',
      packages=find_packages(),
      install_requires=['marshmallow', 'tabulate', 'sphinxcontrib-httpdomain',
                        'sphinx-rtd-theme', 'sphinx-jsonschema', 'schwifty',
                        'openpyxl'],
      include_package_data=True)
