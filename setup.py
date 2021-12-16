import setuptools

import os
import sys

with open("README.md", "r") as f:
  long_description = f.read()

with open("LICENSE", "r") as f:
  license = f.read()

setuptools.setup(
    name="logdog-TheTimmoth",
    version="1.0.0b1",
    author="Tim Schlottmann",
    author_email="coding@timsc.de",
    license=license,
    description="A stdout event sniffer and handler",
    long_description=long_description,
    url="https://github.com/TheTimmoth/logdog",
    keywords=["logdog", "log", "events"],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    scripts=["bin/logdog", "bin/log2mail"],
    install_requires=["cryptography"],
    platforms=["Linux"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
    ],
)
