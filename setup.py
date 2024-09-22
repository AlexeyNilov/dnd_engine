from setuptools import find_packages
from setuptools import setup

VERSION = '0.1.2'
DESCRIPTION = 'DnD Engine'

# Setting up
setup(
    name="dnd_engine",
    version=VERSION,
    description=DESCRIPTION,
    include_package_data=True,
    packages=find_packages(include=['dnd_engine']),
    install_requires=[
        'pydantic',
    ],
    python_requires='>=3.10',
)
