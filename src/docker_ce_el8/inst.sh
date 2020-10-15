#!/bin/bash

yum --disablerepo=* localinstall pkg/*.rpm

systemctl start docker
docker --version  