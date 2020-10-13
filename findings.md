# Lodz University of Technology Server, Throttling 2.5Mbps

## 2 PATHS, 1 stream, 100 MB file
```
2020/10/13 23:00:21 [SID: 3] Accepted stream, starting to send data
2020/10/13 23:00:48 [SID: 3] Elapsed: 27.73099431s
2020/10/13 23:00:48 [SID: 3] Successfully wrote: 104857600 data
2020/10/13 23:00:48 Info for stream 3 of 822e4fcac5914c99
2020/10/13 23:00:48 Path 0: from: [::]:5201, to: 5.x.x.x:59332
2020/10/13 23:00:48 Path 0: sent 6 retrans 0 lost 0; rcv 7 rtt 694.44ms
2020/10/13 23:00:48 Path 1: from: [::]:5201, to: 5.x.x.x:59333
2020/10/13 23:00:48 Path 1: sent 49073 retrans 6 lost 6; rcv 24528 rtt 122.402ms
2020/10/13 23:00:48 Path 3: from: [::]:5201, to: 8.x.x.x:57374
2020/10/13 23:00:48 Path 3: sent 30962 retrans 61 lost 60; rcv 15862 rtt 178.905ms
2020/10/13 23:00:48 Closing connection 822e4fcac5914c99
2020/10/13 23:00:48 Finished session
```

## 1 PATH, 1 stream, 100 MB file

```
2020/10/13 23:07:40 Accepting streams
2020/10/13 23:07:40 Waiting for stream
2020/10/13 23:07:40 [SID: 3] Accepted stream, starting to send data
2020/10/13 23:08:26 [SID: 3] Elapsed: 46.309485265s
2020/10/13 23:08:26 [SID: 3] Successfully wrote: 104857600 data
2020/10/13 23:08:26 Info for stream 3 of 21a01af13f67d55c
2020/10/13 23:08:26 Path 0: from: [::]:5201, to: 5.x.x.x:64652
2020/10/13 23:08:26 Path 0: sent 80504 retrans 22 lost 22; rcv 41798 rtt 129.617ms
2020/10/13 23:08:26 Closing connection 21a01af13f67d55c
2020/10/13 23:08:26 Finished session
```

## 2 PATHS, 100MB file, drop one path in the middle

```
2020/10/13 23:45:56 [SID: 3] Accepted stream, starting to send data
2020/10/13 23:46:32 [SID: 3] Elapsed: 36.254934031s
2020/10/13 23:46:32 [SID: 3] Successfully wrote: 104857600 data
2020/10/13 23:46:32 Info for stream 3 of 656925c0e45f2a33
2020/10/13 23:46:32 Path 3: from: [::]:5201, to: 83.20.194.106:57744
2020/10/13 23:46:32 Path 3: sent 2154 retrans 100 lost 93; rcv 1097 rtt 40.926ms
2020/10/13 23:46:32 Path 1: from: [::]:5201, to: 5.173.109.234:64664
2020/10/13 23:46:32 Path 1: sent 78206 retrans 8 lost 6; rcv 40000 rtt 168.981ms
2020/10/13 23:46:32 Path 0: from: [::]:5201, to: 5.173.109.234:59333
2020/10/13 23:46:32 Path 0: sent 6 retrans 0 lost 0; rcv 7 rtt 449.561ms
2020/10/13 23:46:32 Closing connection 656925c0e45f2a33
2020/10/13 23:46:32 Finished session
```

# Google Cloud, Zurich, No throttling

## 2 PATHS, 1 stream, 100 MB file
```
2020/10/13 21:26:56 [SID: 3] Accepted stream, starting to send data
2020/10/13 21:27:41 [SID: 3] Elapsed: 45.154265946s
2020/10/13 21:27:41 [SID: 3] Successfully wrote: 104857600 data
2020/10/13 21:27:41 Info for stream 3 of 897ecf6dfde2f241
2020/10/13 21:27:41 Path 0: from: [::]:6121, to: 5.173.109.234:64649
2020/10/13 21:27:41 Path 0: sent 6 retrans 1 lost 0; rcv 7 rtt 2.605322s
2020/10/13 21:27:41 Path 1: from: [::]:6121, to: 5.173.109.234:64657
2020/10/13 21:27:41 Path 1: sent 79358 retrans 3 lost 3; rcv 41119 rtt 228.347ms
2020/10/13 21:27:41 Path 3: from: [::]:6121, to: 83.20.194.106:43946
2020/10/13 21:27:41 Path 3: sent 1306 retrans 135 lost 128; rcv 609 rtt 1.832414s
2020/10/13 21:27:41 Closing connection 897ecf6dfde2f241
2020/10/13 21:27:41 Finished session
```
```
2020/10/13 21:32:33 [SID: 3] Accepted stream, starting to send data
2020/10/13 21:33:11 [SID: 3] Elapsed: 37.266455521s
2020/10/13 21:33:11 [SID: 3] Successfully wrote: 104857600 data
2020/10/13 21:33:11 Info for stream 3 of f7406ef697606e03
2020/10/13 21:33:11 Path 0: from: [::]:6121, to: 5.173.109.234:59351
2020/10/13 21:33:11 Path 0: sent 6 retrans 0 lost 0; rcv 7 rtt 246.188ms
2020/10/13 21:33:11 Path 1: from: [::]:6121, to: 5.173.109.234:59329
2020/10/13 21:33:11 Path 1: sent 49605 retrans 2 lost 2; rcv 25854 rtt 71.732ms
2020/10/13 21:33:11 Path 3: from: [::]:6121, to: 83.20.194.106:44591
2020/10/13 21:33:11 Path 3: sent 30625 retrans 47 lost 47; rcv 15280 rtt 96.252ms
2020/10/13 21:33:11 Closing connection f7406ef697606e03
2020/10/13 21:33:11 Finished session
```

## 1 PATH, 1 stream, 100 MB file
```
2020/10/13 21:30:25 [SID: 3] Accepted stream, starting to send data
2020/10/13 21:31:04 [SID: 3] Elapsed: 38.493458311s
2020/10/13 21:31:04 [SID: 3] Successfully wrote: 104857600 data
2020/10/13 21:31:04 Info for stream 3 of 21cbc4682a081988
2020/10/13 21:31:04 Path 0: from: [::]:6121, to: 5.173.109.234:59336
2020/10/13 21:31:04 Path 0: sent 80568 retrans 20 lost 20; rcv 42051 rtt 112.156ms
2020/10/13 21:31:04 Closing connection 21cbc4682a081988
2020/10/13 21:31:04 Finished session
```

# Errors
1. Server, Client -> AcceptStream; without any HELO from client, server is unable to send data
2. When an interface is disabled or firewalled whole session goes down
3. On Linux, two default gateways. Each of the paths go through the same gateway, need to add custom routing rule.
```
konrad@stormheim:~/go/src/github.com/th7nder/mp-quic$ sudo ip rule add from 192.168.1.0/24 table 777
konrad@stormheim:~/go/src/github.com/th7nder/mp-quic$ sudo ip route add 0.0.0.0/0 via 192.168.1.1 dev wlp41s0 table 777 
```
4. Closing session is not verified? Sometimes PeerGoingAway, sometimes EOF
5. Server closed session and finished, client has NetworkIdleTimeout and no file

#  Conclusions
1. Different way of writing software, multi-threaded, error handling
2. Scheduler affects packets A LOT. RTT matters.
3. Without throttling, it's shit