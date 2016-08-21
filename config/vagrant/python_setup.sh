#!/usr/bin/env bash

echo "=== Begin Vagrant Provisioning using 'config/vagrant/python_setup.sh'"
PYTHON_VERSION='3.5.2'

sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get -y update
sudo apt-get install -y python3.5 python3.5-dev python3-pip

cd ~

sudo pip3 install --upgrade pip
sudo pip3 install virtualenv


virtualenv -p /usr/bin/python3.5 venv
. venv/bin/activate

pip3 install -r /vagrant/requirements.txt

deactivate
