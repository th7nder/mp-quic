package datagatherer

import (
	"bufio"
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/lucas-clemente/quic-go/internal/protocol"
)

type Base struct {
	packets     map[protocol.PathID]map[protocol.PacketNumber]time.Time
	rttFile     *os.File
	rttWriter   *bufio.Writer
	pathsFile   *os.File
	pathsWriter *bufio.Writer

	mut sync.Mutex
}

func NewBase() *Base {
	start := time.Now()

	rttFile, err := os.Create(fmt.Sprintf("g_%s_rtt.csv", start.Format(time.RFC3339)))
	if err != nil {
		panic(err)
	}

	pathsFile, err := os.Create(fmt.Sprintf("g_%s_paths.csv", start.Format(time.RFC3339)))
	if err != nil {
		panic(err)
	}

	return &Base{
		packets:     make(map[protocol.PathID]map[protocol.PacketNumber]time.Time),
		rttFile:     rttFile,
		rttWriter:   bufio.NewWriterSize(rttFile, 1<<24),
		pathsFile:   pathsFile,
		pathsWriter: bufio.NewWriterSize(pathsFile, 1<<24),
	}
}

func (b *Base) OnPacketSent(pathID protocol.PathID, packetNumber protocol.PacketNumber) {
	if pathID == 0 {
		return
	}
	b.mut.Lock()
	defer b.mut.Unlock()
	if _, ok := b.packets[pathID]; !ok {
		b.packets[pathID] = make(map[protocol.PacketNumber]time.Time)
	}

	b.packets[pathID][packetNumber] = time.Now()
}

func (b *Base) OnAckReceived(pathID protocol.PathID, packetNumber protocol.PacketNumber) {
	if pathID == 0 {
		return
	}
	b.mut.Lock()
	defer b.mut.Unlock()
	difference := time.Now().Sub(b.packets[pathID][packetNumber])

	b.rttWriter.WriteString(
		fmt.Sprintf(
			"%d,%d,%d\n",
			pathID,
			packetNumber,
			difference.Microseconds(),
		),
	)
	delete(b.packets[pathID], packetNumber)
}

func (b *Base) OnPathGatherSentStats(args *GatherSentStatsArgs) {
	b.pathsWriter.WriteString(
		fmt.Sprintf(
			"%d,%d,%s,%s,%d,%d,%d,%d,%d\n",
			time.Now().UnixNano(),
			args.PathID,
			args.LocalAddr.String(),
			args.RemoteAddr.String(),
			args.InFlight,
			args.SRTT.Microseconds(),
			args.Packets,
			args.Retransmissions,
			args.Losses,
		),
	)
}

func (b *Base) Close() {
	for pathID, packets := range b.packets {
		for packetNumber := range packets {
			b.rttWriter.WriteString(
				fmt.Sprintf(
					"%d,%d,%d\n",
					pathID,
					packetNumber,
					-1,
				),
			)
		}
	}
	if err := b.rttWriter.Flush(); err != nil {
		panic(err)
	}
	b.rttFile.Close()

	if err := b.pathsWriter.Flush(); err != nil {
		panic(err)
	}
	b.pathsFile.Close()
}
