Model
=====

One network per tunnel interface
Can do routes via using systemd
Perhaps we construct our model as leaves reachable by a series of edges
Perhaps there is a core "node" or multiple core "nodes"
How does freeIPA user/group membership / machine accounts fit into this model?
Is there a way that identity could adjust the allowed paths to be tuned on a core set of nodes such that
group membership dictates the path of traversal and access within the backbone network
I want to generate my NF tables ruleset from freeIPA or some other kind of identity manager that states what can and cannot be accessed.
I think this modeling layer is an abstraction of the implementation, whether that is bare metal, VM, or AWS.
The "core" or "hub" still definitely needs to be reachable from "the internet"
The "core" may be more than one node, and listen on more than one interface/port in order to circumnavigate firewalling
The model should account for passthrough of arbitrary elastic addresses from AWS via the core or other ingress node to arbitrary
machines or services behind NAT / on the other end of a WG tunnel.
These tunnels should likely still be provisioned by the model

there may be an agent that exists on the endpoint to configure the wireguard tunnel
