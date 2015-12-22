#!/usr/bin/env bash
cp Certificates/ServerCertificate/IEDCSServer.crt venv/local/lib/python2.7/site-packages/sslserver/certs/
cp Certificates/ServerPrivateKey/IEDCSServer.pem venv/local/lib/python2.7/site-packages/sslserver/certs/
echo Done installing IEDCS Server Certificates
