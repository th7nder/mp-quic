package server

import (
	"math/rand"
	"sync"
	"time"

	quic "github.com/lucas-clemente/quic-go"
	"github.com/lucas-clemente/quic-go/example/multistream/common"
	"github.com/lucas-clemente/quic-go/internal/utils"
	"github.com/pkg/errors"
)

// Server listens on addr, waits on n streams and sends 100MB random file over each stream
func Server(addr string, streams int, size int, game bool) error {
	utils.Infof("Generating random data")
	data := make([]byte, size*1000*1000)
	_, err := rand.Read(data)
	if err != nil {
		return errors.Wrap(err, "failed to generate 100MB of data")
	}

	utils.Infof("Starting server")
	listener, err := quic.ListenAddr(addr, common.GenerateTLSConfig(), nil)
	if err != nil {
		return errors.Wrap(err, "failed to listen on addr")
	}

	for {
		utils.Infof("Waiting for a session")
		sess, err := listener.Accept()
		if err != nil {
			return errors.Wrap(err, "failed to start session")
		}
		if game {
			go handleGameSession(sess, data)
		} else {
			go handleSession(sess, data, streams)
		}
	}
}

func handleGameSession(session quic.Session, data []byte) {
	utils.Infof("Accepting game streams")
	var wg sync.WaitGroup

	rand.Seed(time.Now().UnixNano())

	// 4 streams!
	// Background download
	go stream(session, &wg, data)
	wg.Add(1)
	// Boss casts, pool on the floors (0.3-1s, 100-200B)
	go customStream(session, func(s quic.Stream) (error, bool) {
		_, err := s.Write(data[:100+rand.Intn(100)])
		if err != nil {
			return err, false
		}
		time.Sleep(time.Duration(300+rand.Intn(700)) * time.Millisecond)
		return nil, true
	})
	// Player chat (0.5-3s), random 20-250B
	go customStream(session, func(s quic.Stream) (error, bool) {
		_, err := s.Write(data[:20+rand.Intn(230)])
		if err != nil {
			return err, false
		}
		time.Sleep(time.Duration(500+rand.Intn(2500)) * time.Millisecond)
		return nil, true
	})
	// Character movement (0.1s), random 50B
	go customStream(session, func(s quic.Stream) (error, bool) {
		_, err := s.Write(data[:50])
		if err != nil {
			return err, false
		}
		time.Sleep(100 * time.Millisecond)
		return nil, true
	})

	wg.Wait()
	err := session.Close(nil)
	if err != nil {
		panic(errors.Wrap(err, "failed to close the game session"))
	}
	utils.Infof("Finished game session")
}

func handleSession(session quic.Session, data []byte, streams int) {
	utils.Infof("Accepting streams")
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
	utils.Infof("Finished session")
}

func stream(session quic.Session, wg *sync.WaitGroup, data []byte) {
	utils.Infof("Waiting for stream")
	s, err := session.AcceptStream()
	if err != nil {
		panic(errors.Wrap(err, "failed to accept a stream"))
	}

	helo := make([]byte, len("HELO"))
	_, err = s.Read(helo)
	if err != nil {
		panic(errors.Wrap(err, "failed to read HELO packet"))
	}

	start := time.Now()
	utils.Infof("[SID: %d] Accepted stream, starting to send data", s.StreamID())
	n, err := s.Write(data)
	if err != nil {
		utils.Infof("[SID: %d] Wrote: %d, failed to write data: %s", s.StreamID(), n, err)
	}
	elapsed := time.Since(start)
	utils.Infof("[SID: %d] Elapsed: %s\n", s.StreamID(), elapsed)

	if err := s.Close(); err != nil {
		utils.Infof("[SID: %d] Failed to close a stream", err)
	}

	utils.Infof("[SID: %d] Successfully wrote: %d data", s.StreamID(), n)
	wg.Done()
}

func customStream(session quic.Session, write func(s quic.Stream) (error, bool)) {
	utils.Infof("Waiting for stream")
	s, err := session.AcceptStream()
	if err != nil {
		panic(errors.Wrap(err, "failed to accept a stream"))
	}

	helo := make([]byte, len("HELO"))
	_, err = s.Read(helo)
	if err != nil {
		panic(errors.Wrap(err, "failed to read HELO packet"))
	}

	start := time.Now()
	utils.Infof("[SID: %d] Accepted stream, starting to send data", s.StreamID())
	for {
		err, cont := write(s)
		if err != nil {
			utils.Infof("[SID: %d] Wrote: %d, failed to write data: %s", s.StreamID(), err)
			break
		}

		if !cont {
			break
		}
	}
	elapsed := time.Since(start)
	utils.Infof("[SID: %d] Elapsed: %s\n", s.StreamID(), elapsed)

	if err := s.Close(); err != nil {
		utils.Infof("[SID: %d] Failed to close a stream", err)
	}

	utils.Infof("[SID: %d] Successfully wrote data", s.StreamID())
}
