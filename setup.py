from setuptools import find_packages
from setuptools import setup

VERSION = "0.1.4"
DESCRIPTION = "DnD Engine"

# Setting up
setup(
    name="dnd_engine",
    version=VERSION,
    description=DESCRIPTION,
    include_package_data=True,
    packages=find_packages(exclude=["conf", "data", "db", "sample", "team", "test"]),
    install_requires=[
        "pydantic",
    ],
    python_requires=">=3.10",
)
