package client

import (
	"crypto/tls"
	"fmt"
	"sync"

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

	buf := make([]byte, 1024)
	var readBytes int
	for {
		n, err := s.Read(buf)
		if err != nil {
			fmt.Printf("[SID: %d] Error: %s\n", s.StreamID(), err)
			break
		}
		readBytes += n
	}

	fmt.Printf("[SID: %d] Finished, bytes read: %d\n", s.StreamID(), readBytes)
	wg.Done()
}

// Client connects to addr, opens n streams and downloads all data it can receive from a stream
func Client(addr string, streams int) error {
	session, err := quic.DialAddr(addr, &tls.Config{InsecureSkipVerify: true}, &quic.Config{
		CreatePaths: true,
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
