#!/bin/bash

yum --disablerepo=* localinstall pkg/*.rpm

#rpm -ivh pkg/audit-libs-python-2.8.5-4.el7.x86_64.rpm
#rpm -ivh pkg/checkpolicy-2.5-8.el7.x86_64.rpm
#rpm -ivh pkg/libcgroup-0.41-21.el7.x86_64.rpm
#rpm -ivh pkg/libsemanage-python-2.5-14.el7.x86_64.rpm
#rpm -ivh pkg/python-IPy-0.75-6.el7.noarch.rpm
#rpm -ivh pkg/setools-libs-3.3.8-4.el7.x86_64.rpm
#rpm -ivh pkg/policycoreutils-python-2.5-34.el7.x86_64.rpm
#rpm -ivh pkg/libseccomp-2.3.1-4.el7.x86_64.rpm
#rpm -ivh pkg/container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
#rpm -ivh pkg/containerd.io-1.3.7-3.1.el7.x86_64.rpm
#rpm -ivh pkg/docker-ce-cli-19.03.9-3.el7.x86_64.rpm
#rpm -ivh pkg/docker-ce-selinux-17.03.2.ce-1.el7.centos.noarch.rpm
#rpm -ivh pkg/docker-ce-19.03.9-3.el7.x86_64.rpm


systemctl start docker
docker --version  
