package main

import (
	"flag"
	"time"

	"github.com/lucas-clemente/quic-go/example/multistream/client"
	"github.com/lucas-clemente/quic-go/example/multistream/server"
	"github.com/lucas-clemente/quic-go/internal/utils"
)

// We start a server echoing data on the first stream the client opens,
// then connect with a client, send the message, and wait for its receipt.
var (
	addr      = flag.String("addr", "", "host:port of client/server")
	t         = flag.String("type", "client", "client|server")
	game      = flag.Bool("game", false, "is game session")
	streams   = flag.Int("streams", 1, "number of streams to be opened")
	size      = flag.Int("size", 30, "size of data in MB")
	multipath = flag.Bool("multipath", false, "enable/disable multipath")
	verbose   = flag.Bool("v", false, "verbose logging")
)

func main() {
	flag.Parse()
	if *addr == "" {
		flag.Usage()
		return
	}

	utils.SetLogTimeFormat(time.StampMicro)
	if *verbose {
		utils.SetLogLevel(utils.LogLevelDebug)
	} else {
		utils.SetLogLevel(utils.LogLevelInfo)
	}

	switch *t {
	case "client":
		err := client.Client(*addr, *streams, *multipath, *game)
		if err != nil {
			panic(err)
		}
	case "server":
		err := server.Server(*addr, *streams, *size, *game)
		if err != nil {
			panic(err)
		}
	default:
		flag.Usage()
	}
}
