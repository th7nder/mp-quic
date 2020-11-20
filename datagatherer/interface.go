package datagatherer

import (
	"net"
	"time"

	"github.com/lucas-clemente/quic-go/internal/protocol"
	"github.com/lucas-clemente/quic-go/internal/wire"
)

type GatherSentStatsArgs struct {
	PathID          protocol.PathID
	SRTT            time.Duration
	LocalAddr       net.Addr
	RemoteAddr      net.Addr
	Packets         uint64
	Retransmissions uint64
	Losses          uint64
	InFlight        protocol.ByteCount
}

type DataGatherer interface {
	OnPacketSent(pathID protocol.PathID, frames []wire.Frame)
	OnAckReceived(pathID protocol.PathID, frames []wire.Frame)
	OnPathGatherSentStats(args *GatherSentStatsArgs)

	Close()
}
