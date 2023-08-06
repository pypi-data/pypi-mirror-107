from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()
# delete the url info if error, also change version in an update
setup(
  name = "replapiit_python_parser",
  version = "0.0.2",
  description = "Parser for replapi-it-python",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "darkdarcool30",
  url = "https://github.com/darkdarcool/ReplAPI-Python-Parser",
  author_email = "darkdarcool@gmail.com",
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "GNU General Public License v3 (GPLv3)",
  packages=['replapiit_python_parser'],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)