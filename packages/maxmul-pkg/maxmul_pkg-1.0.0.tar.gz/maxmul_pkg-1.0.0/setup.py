#配置发布信息
import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maxmul_pkg",
    version="1.0.0",
    author="jobi",
    authoremail="jobi@gmail.com", 
    description="an example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),#返回一个需要但是目录没有的包的list
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    )

