#!/usr/bin/env bash

sudo umount /tmp/storage-mount
sudo cryptsetup luksClose secret-data
echo "Closed and unmounted secret files with success."
