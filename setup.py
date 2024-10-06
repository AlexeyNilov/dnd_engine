from setuptools import find_packages
from setuptools import setup

VERSION = "0.2.17"
DESCRIPTION = "DnD Engine"

# Setting up
setup(
    name="dnd_engine",
    version=VERSION,
    description=DESCRIPTION,
    include_package_data=True,
    packages=find_packages(exclude=["conf", "db", "sample", "team", "test"]),
    install_requires=["pydantic", "fastlite", "pyyaml"],
    python_requires=">=3.10",
)
