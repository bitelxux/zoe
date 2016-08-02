participant Usuario

title Consola Telnet

Usuario->App: telnet
alt telnet operativo
  App->Usuario: Mensaje bienvenida
  App->Usuario: Ayuda
  App->Usuario: Prompt
else telnet no responde
  Operativo->Usuario: Error telnet
