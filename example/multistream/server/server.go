package server

import (
	"crypto/rand"
	"fmt"
	"sync"

	quic "github.com/lucas-clemente/quic-go"
	"github.com/lucas-clemente/quic-go/example/multistream/common"
	"github.com/pkg/errors"
)

// Server listens on addr, waits on n streams and sends 100MB random file over each stream
func Server(addr string, streams int, size int) error {
	fmt.Println("Generating random data")
	data := make([]byte, size*1024*1024)
	_, err := rand.Read(data)
	if err != nil {
		return errors.Wrap(err, "failed to generate 100MB of data")
	}

	fmt.Println("Starting server")
	listener, err := quic.ListenAddr(addr, common.GenerateTLSConfig(), nil)
	if err != nil {
		return errors.Wrap(err, "failed to listen on addr")
	}

	for {
		fmt.Println("Waiting for a session")
		sess, err := listener.Accept()
		if err != nil {
			return errors.Wrap(err, "failed to start session")
		}
		go handleSession(sess, data, streams)
	}
}

func handleSession(session quic.Session, data []byte, streams int) {
	fmt.Println("Accepting streams")
	var wg sync.WaitGroup
	for i := 0; i < streams; i++ {
		wg.Add(1)
		go stream(session, &wg, data)
	}

	wg.Wait()

	err := session.Close(nil)
	if err != nil {
		panic(errors.Wrap(err, "failed to close the session"))
	}
	fmt.Println("Finished session")
}

func stream(session quic.Session, wg *sync.WaitGroup, data []byte) {
	fmt.Println("Waiting for stream")
	s, err := session.AcceptStream()
	if err != nil {
		panic(errors.Wrap(err, "failed to accept a stream"))
	}

	helo := make([]byte, len("HELO"))
	_, err = s.Read(helo)
	if err != nil {
		panic(errors.Wrap(err, "failed to read HELO packet"))
	}

	var written int

	fmt.Printf("[SID: %d] Accepted stream, starting to send data\n", s.StreamID())
	for written != len(data) {
		n, err := s.Write(data)
		if err != nil {
			// fmt.Printf("[SID: %d] Wrote: %d, failed to write data: %s\n", s.StreamID(), n, err)
		} else {
			written += n
		}
		if n%1024*1024 == 0 {
			fmt.Printf("[SID: %d] Wrote: %d", s.StreamID(), n)
		}
	}

	if err := s.Close(); err != nil {
		fmt.Printf("[SID: %d] Failed to close a stream", err)
	}

	fmt.Printf("[SID: %d] Successfully wrote: %d data\n", s.StreamID(), written)
	wg.Done()
}
