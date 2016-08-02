participant Usuario

title Accept

Usuario<-Consola: Invitación pendiente de usuarioB
alt Usuario Acepta
    Consola->Consola: Registra usuarioB como contacto
    Consola-->UsuarioB: accept(invitación)
else Usuario rechaza la invitación
    note right of Usuario: la invitación desaparece de pendientes
    note right of Usuario: No pasa nada
else Usuario no hace nada 
    note right of Usuario: No pasa nada


