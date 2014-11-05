from setuptools import setup, find_packages

with open('README.md') as f:
    description = f.read()

setup(name = "peggy",
      version = "0.1",
      packages = find_packages(),
      description = description,
      author = "Alistair Lynn",
      author_email = "alistair@alynn.co.uk",
      install_requires = 'nose >=1.3, <2',
      license = 'MIT',
      zip_safe = True)

