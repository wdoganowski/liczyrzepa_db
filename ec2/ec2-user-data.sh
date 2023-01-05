#!/bin/bash -ex
cd /root
apt-get -y update
apt-get -y upgrade

apt-get install -y unzip

curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/ILT-TF-100-TECESS-5/app/app.zip
mkdir -p /var/app
unzip -o app.zip -d /var/app

cd /var/app
npm install

cd /root
wget https://raw.githubusercontent.com/wdoganowski/liczyrzepa_db/main/ec2/node-app
cp node-app /etc/init.d
chmod +x /etc/init.d/node-app
/sbin/update-rc.d node-app defaults
/etc/init.d/node-app start