import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="allneo",
    author="RONI DAS",
    version="0.0.1",
    author_email="roni@totaltechnology.in",
    description="complete package for neo4j",
    long_description="Developed By Roni Das ,A complete packing for neo4j operations",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=["neo4j"],
    python_requires=">=3.7",
)