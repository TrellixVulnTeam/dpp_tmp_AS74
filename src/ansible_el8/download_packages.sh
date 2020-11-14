#!/bin/bash

PKGDIR="pkg"
EPELURL="https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm"
YUMPKGNAME="epel-release"

if [ -d "$PWD/$PKGDIR" ] 
then
  echo "folder $PKGDIR already exists."
else
  mkdir $PWD/$PKGDIR
fi

#yum install -y epel-release
yum install -y $EPELURL 
yum install -y yumdownloader

#yum install -y --downloadonly --downloaddir=$PWD/$PKGDIR ansible
yumdownloader --resolve --destdir=$PWD/$PKGDIR ansible

yum erase -y $YUMPKGNAME