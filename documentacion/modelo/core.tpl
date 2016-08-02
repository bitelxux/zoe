@startuml

skinparam class {
	BackgroundColor <BGCOLOR>
	ArrowColor <ARROWCOLOR>
	BorderColor <BORDERCOLOR>
}

TServer <|-- Core

class Core{
   -plugins
   -started_at
   -console
   configManager
   -storage
   -node
   -net
   -publisher
   -contacts
   -app_path = None
   my_id = None
   running
   ready
  - run()
  - check_sanity
  - load_plugins_from_dir
  + stop()
  }


@enduml
