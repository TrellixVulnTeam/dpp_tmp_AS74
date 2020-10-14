#!/bin/bash

yum --disablerepo=* localinstall pkg/*.rpm

#rpm -ivh pkg/sshpass-1.06-2.el7.x86_64.rpm
#rpm -ivh pkg/python-ply-3.4-11.el7.noarch.rpm
#rpm -ivh pkg/python-pycparser-2.14-1.el7.noarch.rpm
#rpm -ivh pkg/python-cffi-1.6.0-5.el7.x86_64.rpm
#rpm -ivh pkg/python-enum34-1.0.4-1.el7.noarch.rpm
#rpm -ivh pkg/python-idna-2.4-1.el7.noarch.rpm
#rpm -ivh pkg/python2-pyasn1-0.1.9-7.el7.noarch.rpm
#rpm -ivh pkg/python2-cryptography-1.7.2-2.el7.x86_64.rpm
#rpm -ivh pkg/python-paramiko-2.1.1-9.el7.noarch.rpm
#rpm -ivh pkg/python-babel-0.9.6-8.el7.noarch.rpm
#rpm -ivh pkg/python-markupsafe-0.11-10.el7.x86_64.rpm
#rpm -ivh pkg/libyaml-0.1.4-11.el7_0.x86_64.rpm
#rpm -ivh pkg/python-jinja2-2.7.2-4.el7.noarch.rpm
#rpm -ivh pkg/PyYAML-3.10-11.el7.x86_64.rpm
#rpm -ivh pkg/ansible-2.9.9-1.el7.ans.noarch.rpm

ansible --version

