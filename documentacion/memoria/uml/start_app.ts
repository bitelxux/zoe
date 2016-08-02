title Inicio

App->App: parse_arguments()
App->+ConfigParser: init()
ConfigParser->-App: config_parser
App->+ConfigParser: read_config()
ConfigParser->-App: config
App->+Peer: init()
Peer->-App: peer
App-->Peer: wakeup()

