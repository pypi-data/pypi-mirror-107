from setuptools import setup, find_packages
import MargotRobbie

Classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Natural Language :: English",
  "Programming Language :: Python :: 3.9"
]

setup(
  name=MargotRobbie.__Name__,
  version="1.0.0",
  description=MargotRobbie.__Description__,
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  url=MargotRobbie.__URL__,
  author=MargotRobbie.__Author__,
  author_email=MargotRobbie.__Email__,
  license=MargotRobbie.__License__,
  classifiers=Classifiers,
  packages=find_packages(),
  keywords="MargotRobbie Margot Robbie",
  install_requires=["datetime"]
)
