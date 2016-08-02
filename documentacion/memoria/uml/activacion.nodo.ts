participant Usuario
participant Consola
participant Nodo

title Activación de nodo

Usuario->Consola: Solicitar codigo activación
Consola->Nodo: Enviar mensaje
Nodo-->Presentador: Mensaje de activación con email
Presentador-->eMail: Código de activación
Usuario->eMail: Obtiene el código
Usuario->Consola: Comando activación con código
Consola->Nodo: Activar nodo
alt Código OK 
    note right of Nodo: Nodo queda activado
else Código Incorrecto:
    note right of Nodo: Nodo no se activa
end
Consola->Usuario: Resultado 



