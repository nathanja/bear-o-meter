#!/bin/bash

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install python-dev python-pip nodejs build-essential

sudo pip install --upgrade pip
sudo pip install virtualenv virtualenvwrapper

mkdir ~/.virtualenvs
export WORKON_HOME=~/.virtualenvs
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv bear
deactivate

sudo npm cache clean -f
sudo npm install -g n
sudo n stable
sudo ln -sf /usr/local/n/versions/node/*/bin/node /usr/bin/nodejs
npm install twitter

cd ~/Downloads
wget -O Hamachi.tgz https://www.vpn.net/installers/logmein-hamachi-2.1.0.174-armhf.tgz
tar -xvf Hamachi.tgz
cd logmein*

sudo ./install.sh
sudo hamachi login
sudo hamachi set-nick bear-o-meter
