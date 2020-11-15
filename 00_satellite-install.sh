#!/bin/bash

### INFO ######################################################
#
# BaseOs Repo must be available (e.g. from installation dvd)
# Tutorial: https://access.redhat.com/solutions/1355683
#
###############################################################

#-Script Vars-------------------------------------------------#
FQDN=satellite.dpp.dev
EXTIP=127.0.0.1
PREPKGS="sos chrony python2"
DVDISOPATH=/root/satellite-6.8.0-rhel-7-x86_64-dvd.iso
MOUNTPOINT=/mnt/iso
INSTPKSCRIPT=install_packages
INSTSATSCRIPT=/usr/sbin/satellite-installer --scenario satellite -v -s --disable-system-checks 
SRCPATH=$PWD
#--------------------------------------------------------------

if [[ -z "${ISOPATH}" ]]; then
  DVDISOPATH=$DVDISOPATH
else
  DVDISOPATH="${ISOPATH}"
fi

if [[ -f "$DVDISOPATH" ]]; then
    echo "$DVDISOPATH exists. Continuing..."
else
    echo "$DVDISOPATH does not exist. Exiting"
    exit 0
fi

if [[ -n "$(grep $FQDN /etc/hosts)" ]]; then
    echo "$FQDN already in /etc/hosts"
else
    echo "$EXTIP $FQDN" >> /etc/hosts
fi

for pkg in $PREPKGS; do
    yum install -y $pkg
done

if [[ ! -f "/usr/bin/python" ]]; then
    ln -s /usr/bin/python2.7 /usr/bin/python
fi

if [[ ! -d "$MOUNTPOINT" ]]; then
    mkdir -p $MOUNTPOINT
fi

mount -t iso9660 -o loop $DVDISOPATH $MOUNTPOINT
cd $MOUNTPOINT
#echo $PWD
(exec $MOUNTPOINT/$INSTPKSCRIPT)

#$INSTSATSCRIPT -> Geht irgendwie nicht. Muss ich noch checken
satellite-installer --scenario satellite -v -s --disable-system-checks

cd $SRCPATH
#umount $MOUNTPOINT --force
echo "You can now unmount the iso via umount $MOUNTPOINT"
