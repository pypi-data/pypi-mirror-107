import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tarcom",
    version="0.1.0",
    author="Tarek Moghrabi",
    author_email="tarexmo@outlook.com",
    description="TarCo Communication (tarcom) - Communicate with network devices using TCP (Server and Client). Internal Use Only (Use at your own risk)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://tarcosolutions.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
