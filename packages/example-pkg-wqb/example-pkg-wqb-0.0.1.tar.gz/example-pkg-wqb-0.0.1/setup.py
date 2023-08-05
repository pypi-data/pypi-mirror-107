import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="example-pkg-wqb",
  version="0.0.1",
  author="wangqibo6",
  author_email="wangqibo6@jd.com",
  description="离线任务日志系统",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url=" http://artifactory.jd.com/libs-py/rec/nrt/toolkit/offline/",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)