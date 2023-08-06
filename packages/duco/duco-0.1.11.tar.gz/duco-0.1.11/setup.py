import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='duco',  
    version='0.1.11',
    author="Dan Sinclair",
    author_email="dansinclair@me.com",
    description="A python package for the Duino Coin REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dansinclair25/duco-py",
    packages=setuptools.find_packages(),
    install_requires = [
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )