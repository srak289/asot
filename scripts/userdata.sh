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

apt purge -y netplan.io libnetplan1 netplan-generator python3-netplan
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
IPv4Forwarding=yes
IPv6Forwarding=yes

Address=172.31.0.5/20
Address=172.31.0.5/20
EOF

systemctl enable --now systemd-networkd
networkctl reload
networkctl reconfigure ens5

# -- public ip needs assignment for this to work

apt-get update
apt-get install -y wireguard tcpdump vim git man-db nftables bridge-utils bind9-dnsutils strongswan openssl podman python3 wireguard

PRIVATE_KEY=$(wg genkey)

cat <<EOF >/etc/wireguard/wg0.conf
[Interface]
Address = 100.64.0.1/24
ListenPort = 443
PrivateKey = ${PRIVATE_KEY}
EOF

systemctl enable --now wg-quick@wg0

useradd -m srak
usermod -aG sudo srak
echo -e 'srak\tALL=(ALL)\tNOPASSWD:ALL' > /etc/sudoers.d/srak
mkdir /home/srak/.ssh
cp /home/admin/.ssh/authorized_keys /home/srak/.ssh/authorized_keys
chmod 700 /home/srak/.ssh
chmod 600 /home/srak/.ssh/authorized_keys
chown -R srak:srak /home/srak/.ssh
userdel -r admin

hostnamectl set-hostname vpn.ngnh.org
