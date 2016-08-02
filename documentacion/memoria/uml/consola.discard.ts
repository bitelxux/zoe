participant Usuario

title Discard

Usuario->Consola: obtener invitación pendiente
Consola->Usuario: invitación pendiente
Usuario->+Consola: discard(invitación)
Consola->Consola: eliminar invitación
Consola->-Usuario: Resultado
