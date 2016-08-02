
title Autentificación origen

NetA->Proto: Parsear mensaje
alt Mensaje incorrecto
    note right of NetA: descartar mensaje
else Mensaje correcto:
    Proto->Proto: Aplicar clave pública de supuesto remitente a payload
    Proto->Proto: Comprobar checksum
    alt Checksum correcto:
        note right of NodoA: El remitente fue B
    else Checksum incorrecto:
        note right of NodoA: El remitente no fue B
    end
end
Proto->NetA: Resultado
    
