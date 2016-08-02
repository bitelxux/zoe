title console

participant Any
participant TelnetConsole
participant Console
participant Peer

Peer->+TelnetConsole: init()
TelnetConsole->+Console: init()
Console->-TelnetConsole: console
TelnetConsole->TelnetConsole: prepare_listener()
TelnetConsole->-Peer: telnet_console

Any->TelnetConsole: telnet
TelnetConsole->Any: hello()
Any->+TelnetConsole: do_something()
TelnetConsole->TelnetConsole: parse_command(cmd)
TelnetConsole->TelnetConsole: check_permissions(cmd)
TelnetConsole->TelnetConsole: do_helper(cmd)
TelnetConsole->+Peer: do_something()
Peer->-TelnetConsole: result
TelnetConsole->-Any: result

