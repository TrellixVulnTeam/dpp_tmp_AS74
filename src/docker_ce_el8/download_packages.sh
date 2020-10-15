#!/bin/bash

PKGDIR="pkg"
DOCKERURL="https://download.docker.com/linux/centos/docker-ce.repo"

if [ -d "$PWD/$PKGDIR" ] 
then
  echo "folder $PKGDIR already exists."
else
  mkdir $PWD/$PKGDIR
fi

yum install -y yum-utils
yum-config-manager --add-repo $DOCKERURL

yum install -y --downloadonly --downloaddir=$PWD/$PKGDIR docker-ce docker-ce-cli containerd.io

yum-config-manager --disable $DOCKERURL