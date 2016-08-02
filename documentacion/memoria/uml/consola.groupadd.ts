participant Usuario

title GroupAdd

Usuario->Consola: groupadd <group> [email1,..]
alt Existe grupo
    note right of Consola: No se hace nada
else No existe grupo:
    Consola->Consola: Crear grupo
end

alt Por cada contacto
    Consola->Consola: Agregar contacto a grupo
end

Consola->Usuario: Resultado

