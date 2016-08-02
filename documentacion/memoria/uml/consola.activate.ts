participant Usuario

title Activate

Usuario->Consola: activate <codigo de activación>
alt código correcto
 Consola->Usuario: OK. Nodo activado
else código incorrecto
 Consola->Usuario: Error. Código inválido
