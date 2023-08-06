import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="spsshrunner",
    version="0.0.0",
    author="Stevie Py",
    author_email="st3v13py@gmail.com",
    description="Facilitate SSH expect flows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steviepy/spsshrunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
