from setuptools import setup
from setuptools import find_packages

setup(
    name='lidarproc',
    version='1.0.0',
    packages=find_packages(exclude=['docs', 'samples', 'logs']),
    url='https://www.clementbesnier.fr/projets/cdr2019',
    license='LICENSE.txt',
    author='Clément Besnier',
    author_email='clemsciences@aol.com',
    description='Code used by GobGob Senpai during the France robotics cup 2019',
    long_description=open("README.md").read(),
    install_requires=['matplotlib', 'numpy', 'scipy', 'scikit-image'],
)
