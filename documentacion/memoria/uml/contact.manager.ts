title Contact Manager

Peer->+ContactManager: init()
ContactManager->-Peer: contact_manager

Peer->+ContactManager: get_contacts()
ContactManager->-Peer: contacts_list

Peer->+ContactManager: get_groups()
ContactManager->-Peer: groups_list

Peer-->+ContactManager: invite_contact()
alt Invitación Aceptada
  Peer-->-ContactManager: invitation_accepted()
  ContactManager->-Peer: result
end

Peer->+ContactManager: accept_invitation()
ContactManager->-Peer: result

Peer->+ContactManager: add_contact_to_group(contact_list)
ContactManager->-Peer: result

Peer->+ContactManager: remove_contact_from_group(contact_list)
ContactManager->-Peer: result

Peer->+ContactManager: create_group(group)
ContactManager->-Peer: result

Peer->+ContactManager: remove_group(group)
ContactManager->-Peer: result

