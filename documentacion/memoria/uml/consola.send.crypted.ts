participant Usuario

title Send Crypted

Usuario->Consola: send crypted <to1> <msg>

alt Si no es contacto aceptado
  Consola->Usuario: Error
else contacto aceptado
  Consola->Consola: enviar mensaje a contacto
end

Consola->Usuario: Resultado

