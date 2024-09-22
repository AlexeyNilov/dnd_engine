from setuptools import find_packages
from setuptools import setup

VERSION = '0.1.1'
DESCRIPTION = 'DnD Engine models'

# Setting up
setup(
    name="dnd-engine",
    version=VERSION,
    description=DESCRIPTION,
    include_package_data=True,
    packages=find_packages(include=['model']),
    install_requires=[
        'pydantic',
    ],
    python_requires='>=3.10',
)
