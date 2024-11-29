#!/bin/bash

# -- enable root console login

cat <<EOF > /etc/securetty
ttyS0
ttyS1
ttyS2
ttyS3
ttyS4
ttyS5
ttyS6
ttyS7
EOF

cp /etc/pam.d/login /tmp/login
cat <<EOF >/etc/pam.d/login
auth [success=ok auth_err=1] pam_succeed_if.so user = root
auth [success=done default=ignore] pam_securetty.so
EOF
cat /tmp/login >> /etc/pam.d/login

# -- stop netplan from configuring our interface

cat <<EOF >/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
network:
  config: disabled
EOF

apt purge -y netplan.io libnetplan0
rm -rf /run/systemd/network

# 172.31.16.16/28

cat <<EOF > /etc/systemd/network/ens5.network
[Match]
Name=ens5

[Network]
DHCP=no
Gateway=172.31.16.1
DNS=172.31.0.2
NTP=169.254.169.123
IPForward=yes

Address=172.31.16.5/20

Address=172.31.16.17/20
Address=172.31.16.18/20
Address=172.31.16.19/20
Address=172.31.16.20/20
Address=172.31.16.21/20
Address=172.31.16.22/20
Address=172.31.16.23/20
Address=172.31.16.24/20
Address=172.31.16.25/20
Address=172.31.16.26/20
Address=172.31.16.27/20
Address=172.31.16.28/20
Address=172.31.16.29/20
Address=172.31.16.30/20
EOF

systemctl enable --now systemd-networkd
networkctl reload
networkctl reconfigure ens5

# -- public ip needs assignment for this to work

apt update
apt install -y wireguard tcpdump vim

PRIVATE_KEY=$(wg genkey)

cat <<EOF >/etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
ListenPort = 443
PrivateKey = ${PRIVATE_KEY}
EOF

systemctl enable --now wg-quick@wg0
