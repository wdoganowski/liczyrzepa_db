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

export DEFAULT_AWS_REGION=eu-north-1
export PHOTOS_BUCKET=liczyrzepa-s3-bucket-01
export SHOW_ADMIN_TOOLS=1

cd /root
wget https://raw.githubusercontent.com/wdoganowski/liczyrzepa_db/main/ec2/node-app
cp node-app /etc/init.d
chmod +x /etc/init.d/node-app
/sbin/update-rc.d node-app defaults
/etc/init.d/node-app start