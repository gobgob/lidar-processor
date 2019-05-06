#!/usr/bin/env bash

# https://www.nyayapati.com/srao/2014/06/how-to-pip-install-python-packages-offline/
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
source ~/.bashrc

pyenv install 3.7.3

mkdir lidar_env
pip install --download -r requirements.txt lidar_env