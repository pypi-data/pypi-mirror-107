import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="undeniable",
    version="0.0.2",
    author="drbh",
    author_email="david.richard.holtz@gmail.com",
    description="A no nonsense NFT minting protocol built on Solana and IPFS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drbh/undeniable",
    data_files=[('undeniable/protocol/', ['undeniable/protocol/spec.json'])],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)