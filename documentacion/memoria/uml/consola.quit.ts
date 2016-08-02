participant Usuario

title Quit

Usuario->Consola: quit
alt Si se está en consola python
    Consola->Consola: Abandona python
    Consola->Usuario: prompt de comandos
else Si se está en consola de comandos 
    Consola->Consola: Cierra conexión
    Usuario->Usuario: Cliente telnet termina
