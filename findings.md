# HTTP, when a path is significantly slower it does break the connection 
60/32 7/1 -> 09.10.2020 3:29 -> 
```
2020/10/09 03:28:33 GET https://xxx:6121/demo/bigFile
2020/10/09 03:28:33 Starting new connection to xxx ([::]:39600 -> xxx:6121), connectionID ed162c4bd99c9c44, version 512
2020/10/09 03:28:33 Queueing packet 0x6 for later decryption
2020/10/09 03:29:13 Info for stream 5 of ed162c4bd99c9c44
2020/10/09 03:29:13 Path 0: sent 7 retrans 0 lost 0; rcv 8
2020/10/09 03:29:13 Path 1: sent 40083 retrans 0 lost 0; rcv 76823
2020/10/09 03:29:13 40.7865919s
```

# Questions
1. MPQUIC 2017 vs QUIC 2019?

# Errors
1. Server, Client -> AcceptStream; without any HELO from client, server is unable to send data