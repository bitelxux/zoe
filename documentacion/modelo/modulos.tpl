@startuml

skinparam class {
        BackgroundColor <BGCOLOR>
        ArrowColor <ARROWCOLOR>
        BorderColor <BORDERCOLOR>
}

namespace Utils <COLOR>
  note "Todos los objetos\nhacen uso de Utils" as N1
end namespace

namespace Net <COLOR>
end namespace

namespace Console <COLOR>
end namespace

namespace Contacts <COLOR>
end namespace

namespace Storage <COLOR>
end namespace

namespace Plugins <COLOR>
end namespace

namespace Node <COLOR>
end namespace

namespace Core <COLOR>
  Core <-up-> Net
  Console <-> Core
  Core <--> Contacts
  Core <--> Storage
  Core <--> Node
  Core <--> Plugins
end namespace

@enduml
