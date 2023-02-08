"""Setup script to install lunchbot as a package"""
from setuptools import find_namespace_packages, setup
import os

PROJECT_DIR = os.path.dirname(__file__)

with open(os.path.join(PROJECT_DIR, "requirements.txt")) as f:
    REQUIREMENTS = f.readlines()

setup(
    name="lunchbot",
    packages=find_namespace_packages(),
    install_requires=REQUIREMENTS,
)
