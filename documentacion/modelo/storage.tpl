@startuml

skinparam class {
	BackgroundColor <BGCOLOR>
	ArrowColor <ARROWCOLOR>
	BorderColor <BORDERCOLOR>
}

class Messages{
  - id
  - to
  - from
  - ts
  - tries
  - ack_ts
  - type
  - payload
  }

class Contacts{
  - id
  - name
  - description
  }

class Groups{
  - id
  - name
  - description
  - admins
  }

class ContactsGroups{
  - group_id
  - contact_id
  - ack_ts
  - is_admin
  }

Contacts "0..n" -up- "0..m" Groups
(Contacts, Groups) . ContactsGroups

Contacts "1" -down- "0..n" Messages
Messages "1" -down- "n" Groups

@enduml
