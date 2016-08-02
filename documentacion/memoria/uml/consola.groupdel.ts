participant Usuario

title groupdel

Usuario->Consola: groupdel <grupo> <email>

alt Si contacto en grupo
    Consola->Consola: eliminar contacto de grupo 
    note right of Consola: Resultado: OK
else Si contacto no en grupo o grupo no existe
    note right of Consola: Resultado: Error
end

Consola->Usuario: Resultado

