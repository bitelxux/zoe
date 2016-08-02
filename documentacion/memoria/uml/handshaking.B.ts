participant NodoA
participant NodoB

title Handshaking

NodoA->NodoB: Petición de conexión
NodoB->NodoB: Comprueba mensaje y autoría
alt Correcto 
    NodoB->NodoA: Respuesta a petición de conexión
    NodoB->NodoB: Registra la sesión
else Incorrecto 
    note right of NodoB: No se hace nada
end
