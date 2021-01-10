# Errors
1. Server, Client -> AcceptStream; without any HELO from client, server is unable to send data
2. When an interface is disabled or firewalled whole session goes down
3. On Linux, two default gateways. Each of the paths go through the same gateway, need to add custom routing rule.
```
sudo ip rule add from 192.168.1.0/24 table 1
sudo ip rule add from 192.168.8.0/24 table 2
sudo ip route add 192.168.1.0/24 dev enp39s0 scope link table 1
sudo ip route add default via 192.168.1.1 dev enp39s0 table 1
sudo ip route add 192.168.8.0/24 dev wlp41s0 scope link table 2
sudo ip route add default via 192.168.8.1 dev wlp41s0 table 2
sudo ip route add default scope global nexthop via 192.168.1.1 dev enp39s0
```
4. Closing session is not verified? Sometimes PeerGoingAway, sometimes EOF
5. Server closed session and finished, client has NetworkIdleTimeout and no file