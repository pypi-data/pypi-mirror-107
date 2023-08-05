from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="helloworld-jammer",
    version="0.0.2",
    description="Returns 'Hello, World!'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jammer42/helloworld-package",
    packages=find_packages(where="src", include=["helloworld"]),
    package_dir={"": "src"},
    extras_require={"dev": ["pytest"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
