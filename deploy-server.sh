#!/usr/bin/env bash

## mount secure Virtual Block Device
sudo cryptsetup luksOpen secure-file secret-data
mkdir -p /tmp/storage-mount
sudo mount /dev/mapper/secret-data /tmp/storage-mount
echo "Secure files mounted with success..."

# run server
echo "Running SSL server..."
cd IEDCSServer
python manage.py runsslserver 0.0.0.0:8000
