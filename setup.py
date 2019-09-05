from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pynami',
      version='0.1.0',
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
      install_requires=['requests', 'marshmallow', 'tabulate', 'pytoml'],
      include_package_data=True)
