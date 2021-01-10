# Używanie programu

Zbudowanie programu - `go build .`
Zależności i modyfikacje - `go.mod` w głównym katalogu.

Uruchomienie programu z flagą `-v` zaczyna generować logi protokołu na stderr.
*Uwaga*, podczas transmisji wielościeżkowej czasami się pojawia bug (protokołu), transmisja zrywa się na początku i trzeba jeszcze raz.
Program wypluwa w katalogu uruchomienia .csv w następującym formacie.
- `<DATETIME>_paths.csv` - plik z danymi ścieżek, format: `unixNano | localAddr | remoteAddr | inFlight (bytes) | SRTT (microsecs) | num packets | num retransmissions | num losses | cwnd (bytes)`
- `<DATETIME>_delays.csv` - plik z danymi strumienim, format: `streamID | offset | sentTime - unixNano (ns) | delay (ns)`
- `<DATETIME>_rtt.csv` - plik z rtt pakietów, format: `streamID | offset | sentTime - unixNano (ns) | rtt (ns)`

1. Transmisja jednego strumienia po QUIC

Po stronie klienta
```
./multistream -addr "212.51.220.78:5201" -type "client" -streams 1 -multipath=false
```
Po stronie serwera
```
./multistream -type server -addr "0.0.0.0:5201" -streams 1 -size 100
```

2. Transmisja jednego strumienia po MPQUIC

Po stronie klienta
```
./multistream -addr "212.51.220.78:5201" -type "client" -streams 1 -multipath=true
```
Po stronie serwera
```
./multistream -type server -addr "0.0.0.0:5201" -streams 1 -size 100
```

3. Transmisja dwóch strumieni po MPQUIC

Po stronie klienta
```
./multistream -addr "212.51.220.78:5201" -type "client" -streams 2 -multipath=true
```
Po stronie serwera
```
./multistream -type server -addr "0.0.0.0:5201" -streams 2 -size 50
```

3. Transmisja "growa"
Modyfikacja parametrów - `server/server.go:handleGameSession` 


Po stronie klienta
```
./multistream -addr "212.51.220.78:5201" -type "client" -streams 2 -game -multipath=true
```
Po stronie serwera
```
./multistream -type server -addr "0.0.0.0:5201" -streams 2 -game -size 50
```

# Wykresy

`plot.py`, dość kiepsko napisany, ale potrafi ładnie generować opóźnienie odbioru.
`plot_normal.py`, SRTT, throughput, inFlights. Napisany dość ładnie, można się bawić.
`plot_parser.py`, parser CSVk, olewa plik z rtt.csv.


# Pliki protokołu 

Ogólnie to zbieranie danych było dodawane w `session.go`, `sent_packet_handler.go` oraz `scheduler.go`, można sprawdzić po referencjach do DataGatherera.

`session.go` - tworzenie nowego "połączenia" (sesji) QUIC. taki kontener na strumienie itd,
`datagatherer/{base.go, interface.go}` - instrumentacja do zbierania danych.  
`ackhandler/sent_packet_handler.go` - każda ścieżka ma swój. Można tu zmienić kontrole zatorów, trafiają tutaj potwierdzenia odbioru, wykonywana jest obsługa strat itd. 
`ackhandler/received_packet_handler.go` - każda ścieżka ma swój. Jak pakiet dotrze do odbiornika, to tutaj jest obsługa.
`scheduler.go` - planista pakietów, jeden na sesje. 
`streams_map.go` - jeden na sesję. planista ramek strumieni, chociaż ciężko to tak nazwać. funkcja `RoundRobinIterate`
`congestion/{olia.go, olia_sender.go, cubic.go, cubic_sender.go}` - algorytmy kontroli zatorów.
`pconn_manager.go` - obsługa socketów UDP. Zakomentowane ustawienie bufora UDP.
`path_manager.go` - zarządca ścieżek.
`interal/flow_control/flow_controller.go` - kontrola przepływu. 

