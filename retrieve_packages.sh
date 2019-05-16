#!/usr/bin/env bash

# https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/
# https://www.ibm.com/support/knowledgecenter/en/SSWTQQ_2.0.3/install/t_si_pythonpackagesoffline.html
# https://stackoverflow.com/questions/11091623/python-packages-offline-installation
# https://www.nyayapati.com/srao/2014/06/how-to-pip-install-python-packages-offline/

download_python37()
{
    # for Python 3.7
    apt-get download build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev \
        libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

    wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
}
install_python37()
{
    # on target
    dpkg -i download build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev \
        libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
    tar xzf Python-3.7.3.tgz

    cd Python-3.7.3
    sudo ./configure --enable-optimizations
    sudo make altinstall
}

install_venv_python37()
{
    curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
    source ~/.bashrc

    pyenv install 3.7.3
}

download_packages_for_lidar()
{
    mkdir lidar_env
    pip install --download lidar_env -r requirements.txt
}

install_packages_for_lidar()
{
    cd
    pip install --no-index --find-links=file:/$HOME/.mypypi ipython

}