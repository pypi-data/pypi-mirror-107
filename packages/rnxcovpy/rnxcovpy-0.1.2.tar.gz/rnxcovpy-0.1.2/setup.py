from setuptools import setup


def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()

LICENSE = "MIT License"

setup(name="rnxcovpy",
      version="0.1.2",
      description="This package can be used to convert betueen different versions of the RINEX format.",
      packages=["rnxcovpy"],
      author="MingGao",
      author_email="2752889603@qq.com",
      long_description=readme_file(),
      license="MIT",
      classifiers=["Programming Language :: Python :: 3",
            f"License :: OSI Approved :: {LICENSE}"],
      python_requires='>=3.6'
      )
