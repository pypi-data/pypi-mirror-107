import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="allneo",
    author="RONI DAS",
    version="15.0.0",
    author_email="roni@totaltechnology.in",
    description="complete package for neo4j developed by Roni Das",
    long_description=long_description,
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