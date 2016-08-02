title peer wakeup

Peer->+Stats: init()
Stats->-Peer: stats
Peer->+DBStorage: init()
DBStorage->-Peer: db
Peer->Peer: setup_presenters
Peer->+Console: init()
Console->-Peer: console
Peer->+Net: init()
Net->-Peer: net
