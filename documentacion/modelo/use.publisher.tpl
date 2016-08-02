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

(Some) --> (Publisher) : Publish(Some/*)
(Other) --> (Publisher) : Publish(Other/)
(Other) --> (Publisher) : Subscribe(A/*)
(A) --> (Publisher): Subscribe(Some/*)
(A) --> (Publisher): Publish(A/*)
(B) --> (Publisher): Subscribe(Other/something/*)
Publisher -up-> A: Notifies(Some/*)
Publisher --> B: Notifies(Other/something/*)
Publisher --> Other: Notifies(A/*)

@enduml
