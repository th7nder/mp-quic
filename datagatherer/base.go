package datagatherer

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"sync"
	"time"

	"github.com/lucas-clemente/quic-go/internal/protocol"
	"github.com/lucas-clemente/quic-go/internal/wire"
)

type Base struct {
	chunks       map[protocol.StreamID]map[protocol.ByteCount]*Chunk
	rttFile      *os.File
	rttWriter    *bufio.Writer
	pathsFile    *os.File
	pathsWriter  *bufio.Writer
	delaysFile   *os.File
	delaysWriter *bufio.Writer

	mut sync.Mutex
}

type Chunk struct {
	Sent  time.Time
	Acked bool
}

func NewBase() *Base {
	start := time.Now()

	rttFile, err := os.Create(fmt.Sprintf("g_%s_rtt.csv", start.Format(time.RFC3339)))
	if err != nil {
		panic(err)
	}

	delaysFile, err := os.Create(fmt.Sprintf("g_%s_delays.csv", start.Format(time.RFC3339)))
	if err != nil {
		panic(err)
	}

	pathsFile, err := os.Create(fmt.Sprintf("g_%s_paths.csv", start.Format(time.RFC3339)))
	if err != nil {
		panic(err)
	}

	return &Base{
		chunks:       make(map[protocol.StreamID]map[protocol.ByteCount]*Chunk),
		rttFile:      rttFile,
		rttWriter:    bufio.NewWriterSize(rttFile, 100*1000*1000),
		pathsFile:    pathsFile,
		pathsWriter:  bufio.NewWriterSize(pathsFile, 100*1000*1000),
		delaysFile:   delaysFile,
		delaysWriter: bufio.NewWriterSize(delaysFile, 100*1000*1000),
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
				b.chunks[frame.StreamID] = make(map[protocol.ByteCount]*Chunk)
			}

			b.chunks[frame.StreamID][frame.Offset] = &Chunk{
				Sent: now,
			}
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
			if _, ok := b.chunks[frame.StreamID][frame.Offset]; !ok {
				continue
			}
			difference := now.Sub(b.chunks[frame.StreamID][frame.Offset].Sent)
			// streamID || offset || delay (ns)
			b.rttWriter.WriteString(
				fmt.Sprintf(
					"%d,%d,%d,%d\n",
					frame.StreamID,
					frame.Offset,
					b.chunks[frame.StreamID][frame.Offset].Sent.UnixNano(),
					difference.Nanoseconds(),
				),
			)
			b.chunks[frame.StreamID][frame.Offset].Acked = true

			// sort offsets first
			keys := make([]protocol.ByteCount, len(b.chunks[frame.StreamID]))
			i := 0
			for k := range b.chunks[frame.StreamID] {
				keys[i] = k
				i++
			}
			sort.Slice(keys, func(i, j int) bool { return keys[i] < keys[j] })

			var delayed bool
			for _, offset := range keys {
				chunk := b.chunks[frame.StreamID][offset]

				if offset < frame.Offset {
					delayed = true
					// if this is delayed, it won't release everything later either
					break
				} else if offset > frame.Offset {
					// chunk is not acked, therefore we need to wait.
					// array is sorted, so everything above it will be blocked as well
					if !chunk.Acked {
						break
					}
					// hooray, we're releasing chunks
					diff := now.Sub(chunk.Sent)
					b.delaysWriter.WriteString(
						// stream | offset | sentTime (ns) | delay (ns)
						fmt.Sprintf(
							"%d,%d,%d,%d\n",
							frame.StreamID,
							offset,
							chunk.Sent.UnixNano(),
							diff.Nanoseconds(),
						),
					)

					delete(b.chunks[frame.StreamID], offset)
				}
			}

			// if nothing was blocking current chunk, just delete it and write to CSV as (ack_received - sent)
			if !delayed {
				chunk := b.chunks[frame.StreamID][frame.Offset]
				diff := now.Sub(chunk.Sent)
				b.delaysWriter.WriteString(
					// stream | offset | sentTime (ns) | delay (ns)
					fmt.Sprintf(
						"%d,%d,%d,%d\n",
						frame.StreamID,
						frame.Offset,
						chunk.Sent.UnixNano(),
						diff.Nanoseconds(),
					),
				)

				delete(b.chunks[frame.StreamID], frame.Offset)
			}

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

	if err := b.delaysWriter.Flush(); err != nil {
		panic(err)
	}
	b.delaysFile.Close()
}
