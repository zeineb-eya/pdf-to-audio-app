#!/bin/bash

echo "Installing Python..."
curl -o python.tar.gz https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xzf python.tar.gz
cd Python-3.10.0
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
cd ..

python3.10 --version
pip3.10 --version

pip3.10 install -r requirements.txt