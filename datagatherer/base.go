package datagatherer

import (
	"bufio"
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/lucas-clemente/quic-go/internal/protocol"
	"github.com/lucas-clemente/quic-go/internal/wire"
)

type Base struct {
	chunks      map[protocol.StreamID]map[protocol.ByteCount]time.Time
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
		chunks:      make(map[protocol.StreamID]map[protocol.ByteCount]time.Time),
		rttFile:     rttFile,
		rttWriter:   bufio.NewWriterSize(rttFile, 100*1000*1000),
		pathsFile:   pathsFile,
		pathsWriter: bufio.NewWriterSize(pathsFile, 100*1000*1000),
	}
}

func (b *Base) OnPacketSent(pathID protocol.PathID, frames []wire.Frame) {
	b.mut.Lock()
	defer b.mut.Unlock()

	now := time.Now()
	for _, frame := range frames {
		switch frame := frame.(type) {
		case *wire.StreamFrame:
			// given that offset + datalen are not overlapping
			if _, ok := b.chunks[frame.StreamID]; !ok {
				b.chunks[frame.StreamID] = make(map[protocol.ByteCount]time.Time)
			}
			b.chunks[frame.StreamID][frame.Offset] = now
		default:
		}
	}
}

func (b *Base) OnAckReceived(pathID protocol.PathID, frames []wire.Frame) {
	b.mut.Lock()
	defer b.mut.Unlock()

	now := time.Now()
	for _, frame := range frames {
		switch frame := frame.(type) {
		case *wire.StreamFrame:
			difference := now.Sub(b.chunks[frame.StreamID][frame.Offset])
			// streamID || offset || delay (ns)
			b.rttWriter.WriteString(
				fmt.Sprintf(
					"%d,%d,%d\n",
					frame.StreamID,
					frame.Offset,
					difference.Nanoseconds(),
				),
			)
			delete(b.chunks[frame.StreamID], frame.Offset)
		default:
		}
	}
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
	for streamID, stream := range b.chunks {
		for offset := range stream {
			b.rttWriter.WriteString(
				fmt.Sprintf(
					"%d,%d,%d\n",
					streamID,
					offset,
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
