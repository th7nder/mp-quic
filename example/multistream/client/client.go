package client

import (
	"crypto/tls"
	"fmt"
	"io"
	"sync"
	"time"

	quic "github.com/lucas-clemente/quic-go"
	"github.com/pkg/errors"
)

func stream(session quic.Session, wg *sync.WaitGroup) {
	fmt.Println("Waiting for stream")
	s, err := session.OpenStream()
	if err != nil {
		panic(err)
	}
	fmt.Printf("[SID: %d] Opened\n", s.StreamID())

	_, err = s.Write([]byte("HELO"))
	if err != nil {
		panic(errors.Wrap(err, "failed to HELO"))
	}

	fmt.Printf("[SID: %d] Started data stream\n", s.StreamID())
	buf := make([]byte, 1024)
	var readBytes int
	start := time.Now()
	for {
		n, err := s.Read(buf)
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Printf("[SID: %d] Error: %s\n", s.StreamID(), err)
		} else {
			readBytes += n
		}
	}
	elapsed := time.Since(start)

	fmt.Printf("[SID: %d] Elapsed: %s, bytes read: %d\n", s.StreamID(), elapsed, readBytes)
	wg.Done()
}

// Client connects to addr, opens n streams and downloads all data it can receive from a stream
func Client(addr string, streams int, multipath bool) error {
	session, err := quic.DialAddr(addr, &tls.Config{InsecureSkipVerify: true}, &quic.Config{
		CreatePaths: multipath,
	})
	if err != nil {
		return err
	}

	var wg sync.WaitGroup
	for i := 0; i < streams; i++ {
		wg.Add(1)
		go stream(session, &wg)
	}

	wg.Wait()
	return nil
}
