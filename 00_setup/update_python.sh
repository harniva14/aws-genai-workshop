#!/bin/bash

wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz
tar -xf Python-3.9.9.tgz
cd Python-3.9.9
sudo yum install bzip2-devel
./configure --enable-optimizations
sudo make altinstall

sudo mv /usr/bin/python3 /usr/bin/python3_backup
sudo ln -s $(which python3.9) /usr/bin/python3
python3 --version

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py

python3 --version

echo "Python successfully updated to 3.9.9!"