#!/bin/bash

NAME=$1

lxc-create --name $NAME --template download -- --dist debian --release trixie --arch amd64
lxc-start $NAME

echo "lxc.start.auto = 1" > /etc/lxc/autostart.conf
