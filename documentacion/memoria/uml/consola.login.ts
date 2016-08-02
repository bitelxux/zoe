participant Usuario

title login

Usuario->Consola: login <pass>
alt Si pass correcto
  Consola->Usuario: Login correcto.
else Si pass incorrecto
  Consola->Usuario: Login incorrecto.
  Consola->Usuario: Muestra ayuda.
  Consola->Usuario: Prompt.
