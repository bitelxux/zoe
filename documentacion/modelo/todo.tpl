@startuml

skinparam class {
        BackgroundColor <BGCOLOR>
        ArrowColor <ARROWCOLOR>
        BorderColor <BORDERCOLOR>
}

namespace UtilsMod <COLOR>
  ZThread <|-- TServer
  class Singleton
  class ZLogger
  class ConfigManager
end namespace

namespace NetMod <COLOR>
  Net -down-> Router
  Net -right-> Transport
  UDP --|> Transport
  OtherTransport --|> Transport
  Net -up-> Protocol
  Zoe --|> Protocol
  OtherProtocol --|> Protocol
  Router *- Peer
end namespace

namespace StatsMod <COLOR>
end namespace

namespace ConsoleMod <COLOR>
  Console -> TelnetConsoleProvider
  Console -down-> PythonConsole
  TelnetConsoleProvider --> TelnetConsole
  TelnetConsole <|-- ZoeConsole
  Console <|-- DjangoConsole
  Console <|-- OtherConsole
end namespace

namespace ContactsMod <COLOR>
  class Contact
end namespace

namespace StorageMod <COLOR>
  MySQLStorage --|> Storage
  SqliteStorage --|> Storage
  OtherStorage --|> Storage
end namespace

namespace CoreMod <COLOR>
  CoreMod.Core -left-> StatsMod.Stats
  CoreMod.Core -right-> NetMod.Net
  CoreMod.Core -down-> ConsoleMod.Console
  CoreMod.Core -down-> StorageMod.Storage
  CoreMod.Core -left-> ContactsMod.Contact
  CoreMod.Publisher -> NetMod.Net
  CoreMod.Publisher -> ContactsMod.Contact
  CoreMod.Publisher -> StatsMod.Stats
  CoreMod.Publisher -> StorageMod.Storage
  CoreMod.Publisher -> ConsoleMod.Console
end namespace

@enduml
