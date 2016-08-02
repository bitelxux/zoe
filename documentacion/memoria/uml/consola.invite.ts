participant Usuario

title Invite

Usuario->Consola: invite <email>
Consola-->UsuarioB: invite <from>
alt UsuarioB acepta
    UsuarioB-->Consola: Acepta
    Consola->Consola: Registra nuevo contacto
else UsuarioB no hace nada:
    note right of UsuarioB: No pasa nada
else UsuarioB rechaza invitación:
    note right of UsuarioB: No pada nada

