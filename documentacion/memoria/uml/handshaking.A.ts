participant NodoA
participant NodoB

title Handshaking

NodoA<-NodoB: Respuesta a conexión ( con desafío )
NodoA->NodoA: Parsea mensaje y comprueba autoría
alt Fallo de mensaje o autoría
    note right of NodoA: No se hace nada
else Mensaje correcto y autoría validada
   NodoA->NodoA: Comprueba desafío
   alt Desafio correcto
       note right of NodoA: Se establece la sesión
   else 
       note right of NodoA: No se hace nada
   end
end
