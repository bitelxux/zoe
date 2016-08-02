participant Usuario

title Register

Usuario->Consola: register <email>
Consola-->Autoridad: register <email>
Autoridad->Autoridad: calcula código único de activación
Autoridad-->eMail: código de activación
Usuario->eMail: obtener código
eMail->Usuario: Código
