from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()
# delete the url info if error, also change version in an update
setup(
  name = "ChitChatPY",
  version = "0.0.1",
  description = "Unit test for python",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "darkdarcool30",
  url = "https://github.com/darkdarcool/ChitChatPY",
  author_email = "darkdarcool@gmail.com",
#To find more licenses or classifiers go to: https://pypi.org/classifiers/
  license = "GNU General Public License v3 (GPLv3)",
  packages=['ChitChatPY'],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)