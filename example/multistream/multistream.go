package main

import (
	"flag"

	"github.com/lucas-clemente/quic-go/example/multistream/client"
	"github.com/lucas-clemente/quic-go/example/multistream/server"
)

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
var (
	addr    = flag.String("addr", "", "host:port of client/server")
	t       = flag.String("type", "client", "client|server")
	streams = flag.Int("streams", 1, "number of streams to be opened")
)

func main() {
	flag.Parse()
	if *addr == "" {
		flag.Usage()
		return
	}

	switch *t {
	case "client":
		err := client.Client(*addr, *streams)
		if err != nil {
			panic(err)
		}
	case "server":
		err := server.Server(*addr, *streams)
		if err != nil {
			panic(err)
		}
	default:
		flag.Usage()
	}
}
