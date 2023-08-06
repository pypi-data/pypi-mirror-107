from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='compact',
      version='0.1.2',
      description='PHP compact for Python',
      url='http://github.com/robinvandernoord/compact',
      author='Robin van der Noord',
      author_email='robinvandernoord@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['compact'],
      zip_safe=False)
