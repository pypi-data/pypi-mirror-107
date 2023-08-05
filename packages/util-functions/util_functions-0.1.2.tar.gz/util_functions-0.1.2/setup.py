from setuptools import setup

VERSION = "0.1.2"

setup(
  name="util_functions",
  version=VERSION,
  author="Patryk Palej",
  description="Repository contains utility functions which perform "
              "commonly needed operations ",
  packages=["util_functions"],
  install_requires=["numpy"]
)
