
import io
import os
from setuptools import setup, find_packages

DEPENDENCIES = ["matplotlib", "numpy", "scipy", "scikit-image"]
EXCLUDE_FROM_PACKAGES = ['docs', 'samples', 'logs']
CURDIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name='lidarproc',
    version='1.0.1',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    url='https://www.clementbesnier.fr/projets/cdr2019',
    keywords=[],
    scripts=[],
    zip_safe=False,
    license='License :: OSI Approved :: MIT License',
    author='Clément Besnier',
    author_email='clemsciences@aol.com',
    install_requires=DEPENDENCIES,
    description='Code used by GobGob Senpai during the France robotics cup 2019',
    long_description=open("README.md").read(),
)
