import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ZxSci",
    version="0.0.9",
    author="Larry",
    author_email="1140091006@qq.com",
    description="一个帮助理工科本科学生进行简化计算的库",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    license="MIT Licence",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet']
)