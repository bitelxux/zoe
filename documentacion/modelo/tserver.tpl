@startuml

skinparam class {
        BackgroundColor <BGCOLOR>
        ArrowColor <ARROWCOLOR>
        BorderColor <BORDERCOLOR>
}

ZThread <|-- TServer

class ZThread{
  - running
  - run()
  + start()
  + stop()
  }

class TServer{
  - activities
  - run()
  + start()
  + stop()
  }

@enduml
