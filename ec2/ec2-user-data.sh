#!/bin/bash -ex
sudo apt-get update

apt install unzip

curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

apt-get update
apt-get upgrade

wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/ILT-TF-100-TECESS-5/app/app.zip
mkdir -p /var/app
unzip app.zip -d /var/app

cd /var/app
npm install

cd
wget https://raw.githubusercontent.com/wdoganowski/liczyrzepa_db/main/ec2/node-app
cp node-app /etc/init.d
/sbin/update-rc.d node-app defaults

cd /var/app
npm start