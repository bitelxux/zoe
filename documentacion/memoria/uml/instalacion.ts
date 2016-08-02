participant Usuario

title Instalación de Nodo

Alguien->Usuario: Envía instalador por email
Usuario->WEB: Descarga instalador
WEB->Usuario: Recibe instalador
Alguien->Usuario: Suministra instalador en soporte digital
Usuario->Torrent: Descarga instalador
Torrent->Usuario: Recibe instalador
Usuario->Otro medio: Solicita instalador
Otro medio->Usuario: Recibe instalador

Usuario->Equipo: Ejecuta instalador 
Equipo->Equipo: Resuelve dependencias e instala
Equipo->Usuario: Comunica resultado instalación

