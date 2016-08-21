#!/usr/bin/env bash

echo "=== Begin Vagrant Provisioning using 'config/vagrant/python_setup.sh'"
PYTHON_VERSION='3.5.2'
apt-get -y update
apt-get -y python3.5 python3-pip

cd ~

sudo pip3 install --upgrade pip
sudo pip3 install virtualenv

virtualenv venv
. venv/bin/activate

pip3 install -r requirements.txt

deactivate
