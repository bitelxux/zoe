@startuml

skinparam usecase {
	BackgroundColor <BGCOLOR>
	BorderColor <BORDERCOLOR>

	BackgroundColor<< Main >> YellowGreen
	BorderColor<< Main >> YellowGreen
	
	ArrowColor <ARROWCOLOR>
	ActorBorderColor black
	ActorFontName Courier

	ActorBackgroundColor<< Human >> Gold
}

Some -> (Start)

Some --> (Telnet) : telnets app

Telnet --> (TelnetProvider) : queries new session
TelnetProvider --> (ZoeConsole)
(ZoeConsole) ---> Some

Other --> (Telnet) : telnets app

Telnet --> (TelnetProvider) : queries new session
TelnetProvider --> (ZoeConsole)
(ZoeConsole) ---> Other

Other --> (Quit) 
Quit->ZoeConsole: Destroyes console

@enduml
