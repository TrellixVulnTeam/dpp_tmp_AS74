#!/bin/bash

### INFO ################################################################
#
# This script is based on the official installation manual:
# https://access.redhat.com/documentation/en-us/red_hat_satellite/6.8/html/installing_satellite_server_from_a_disconnected_network/index 
#
# !!! BaseOs Repo must be available (e.g. from installation dvd) !!!
# Tutorial: https://access.redhat.com/solutions/1355683
#
#########################################################################

#-Script Vars--------------------------------------------------

FQDN=satellite.dpp.dev
EXTIP=127.0.0.1
PREPKGS="sos chrony python2"
DVDISOPATH=/root/satellite-6.8.0-rhel-7-x86_64-dvd.iso
MOUNTPOINT=/mnt/iso
INSTPKSCRIPT=install_packages
INSTSATSCRIPT="/usr/sbin/satellite-installer --scenario satellite -v -s --disable-system-checks" 
SRCPATH=$PWD
FOREMANHOME=/usr/share/foreman-proxy
FOREMANSSHKEY=/usr/share/foreman-proxy/.ssh/id_rsa_foreman_proxy

#--------------------------------------------------------------

if [[ -z "${ISOPATH}" ]]; then
  DVDISOPATH=$DVDISOPATH
else
  DVDISOPATH="${ISOPATH}"
fi


#-Check if DVD Path is correct--------------------------------------------
if [[ -f "$DVDISOPATH" ]]; then
    echo "$DVDISOPATH exists. Continuing..."
else
    echo "$DVDISOPATH does not exist. Exiting"
    exit 0
fi


#-Check if Satellite FQDN is in /etc/hosts--------------------------------
if [[ -n "$(grep $FQDN /etc/hosts)" ]]; then
    echo "$FQDN already in /etc/hosts"
else
    echo "$EXTIP $FQDN" >> /etc/hosts
fi

for pkg in $PREPKGS; do
    yum install -y $pkg
done


#-Check if python2 is standard python interpreter-------------------------
if [[ ! -f "/usr/bin/python" ]]; then
    ln -s /usr/bin/python2.7 /usr/bin/python
fi

if [[ ! -d "$MOUNTPOINT" ]]; then
    mkdir -p $MOUNTPOINT
fi


#-Disable firewalld, if configured---
if [[ ! -f " /usr/sbin/firewalld" ]]; then
    systemctl stop firewalld
    systemctl disable firewalld
fi


#-Install Satellite required packages-------------------------------------
mount -t iso9660 -o loop $DVDISOPATH $MOUNTPOINT
cd $MOUNTPOINT
#echo $PWD
(exec $MOUNTPOINT/$INSTPKSCRIPT)


#-Satellite installation script-------------------------------------------
#$INSTSATSCRIPT -> Geht irgendwie nicht. Muss ich noch checken
satellite-installer --scenario satellite -v -s --disable-system-checks


#-SSH Foreman SSH Keys for remote execution-------------------------------
if [ ! -f "$FOREMANSSHKEY" ] && [ -d "$FOREMANHOME" ]; then
    echo "Do you want to create Foreman SSH Key Pait for remote execution (yes/no)?"
    read CHK 
fi

if [[ $CHK == 'yes' ]]; then
    mkdir -p $FOREMANHOME
    if [[ -f '/tmp/id_rsa' ]]; then
        rm -f /tmp/id_rsa*
    fi
    ssh-keygen -b 2048 -t rsa -f /tmp/id_rsa -q -P ""
    mv /tmp/id_rsa $FOREMANSSHKEY
    mv /tmp/id_rsa.pub $FOREMANSSHKEY.pub
    chown foreman-proxy:foreman-proxy $FOREMANSSHKEY
    chown foreman-proxy:foreman-proxy $FOREMANSSHKEY.pub
fi


#-Clean up and "go home"---------------------------------------------------
cd $SRCPATH
#umount $MOUNTPOINT --force
echo "You can now unmount the iso via: # umount $MOUNTPOINT"
