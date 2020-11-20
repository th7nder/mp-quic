package datagatherer

import (
	"net"
	"time"

	"github.com/lucas-clemente/quic-go/internal/protocol"
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
	OnPacketSent(pathID protocol.PathID, packetNumber protocol.PacketNumber)
	OnAckReceived(pathID protocol.PathID, packetNumber protocol.PacketNumber)
	OnPathGatherSentStats(args *GatherSentStatsArgs)

	Close()
}
