import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connect-4-cli",
    version="0.0.1",
    author="Germán Mené Santa Olaya",
    author_email="german.mene@gmail.com",
    description="A CLI implementation of the classic connect 4 game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmso/connect-4-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Games/Entertainment :: Board Games"
    ],
)