Design
======

The vpn system is a management layer overtop of wireguard.

Wireguard interfaces may be configured to host private networks of any size,
and can allow communication of any nodes within that network's scope so long as
the remote ends allow it.

We could potenetially pipe wireguard over socat

e.g.

....
        A
       / \
      B   C
....
If A is the HUB, B may ping C through A so long as C is configured to allow B's
private address on its wireguard interface, and vice versa for B.

A must not specify more than /32 for a peer unless that peer is also a router.
Overlapping network addresses between peers will cause one to be overridden and
the other to receive no address.

e.g.

....
[Peer]
PublicKey = pB=
AllowedIPs = 10.0.0.2/24

[Peer]
PublicKey = pC=
AllowedIPs = 10.0.0.3/24
....
This would cause B to receive `(none)` for `allowed ips`.

The appropriate configuration for clients to talk through the hub is as follows

A's config
....
[Interface]
Address = 10.0.0.1/24
ListenPort = 9999
PrivateKey = PA=
[Peer]
PublicKey = pB=
AllowedIPs = 10.0.0.2/32
[Peer]
PublicKey = pC=
AllowedIPs = 10.0.0.3/32
....

B's config
....
[Interface]
Address = 10.0.0.2/24
PrivateKey = PB=
[Peer]
PublicKey = pA=
Endpoint = my.vpn.example.com:9999
AllowedIPs = 10.0.0.1/24
PersistentKeepalive = 25
....

C's config
....
[Interface]
Address = 10.0.0.3/24
PrivateKey = PC=
[Peer]
PublicKey = pA=
Endpoint = my.vpn.example.com:9999
AllowedIPs = 10.0.0.1/24
PersistentKeepalive = 25
....

following this configuration, bring all of the wireguard interfaces up,
verify both machines can ping the hub, the hub can ping both machines, and that
B can ping C via A.

This "ping across" may not be desirable in all circumstances, and may require
interesting rules to prevent or control.
