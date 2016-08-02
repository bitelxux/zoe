title Envío de mensaje

A->A: create_message(data)
A->+Protocol: format_message(data)
Protocol->-A: msg
A->A: register_message(msg)
loop hasta mensaje entregado o timeout
  A->A: get_info(B)
alt No se conocen los datos de B
  A-->A: search_remote(B)
else Se conocen los datos de B
  A->B: send_message(B, msg)
  note right of B: B recibe el mensaje
  B->+Protocol: parse_msg()
  Protocol->-B: parsed message
  B->+Protocol: prepare_ack()
  Protocol->-B: prepared ack
  B->A: ack_message(msg)
  A->A: ackd_message(msg)
end
end

