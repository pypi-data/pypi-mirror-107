import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="beCoditive",
  version="0.0.1",
  author="beCoditive",
  author_email="becoditive@gmail.com",
  description="The official pip package for beCoditive API.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/becoditive/becoditive-pip",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License ",
    "Operating System :: OS Independent"
  ],
  python_requires=">=3.6"
)