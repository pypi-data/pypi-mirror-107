from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="SearchFile",
      version="0.2.0",
      long_description=long_description,
      long_description_content_type="text/markdown",
      description="Search for files by the specified path.",
      author="Prudnikov Artem",
      url="https://github.com/Artemik1/SearchFile-package",
      author_email="artem_prudnikov_2002@mail.ru",
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent"
      ],
      python_requires='>=3.9')
