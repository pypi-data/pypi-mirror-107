import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="allneo4j-pkg-ronidas39",
    version="0.0.1",
    author="RONI DAS",
    author_email="roni@totaltechnology.in",
    description="complete package for neo4j",
    long_description="neo4j operations",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "allneo4j"},
    packages=setuptools.find_packages(where="allneo4j"),
    install_requires=["neo4j"],
    python_requires=">=3.7",
)