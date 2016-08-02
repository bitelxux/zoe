participant NodoB
participant NodoA

title Aceptación de contacto

NodoB<--NodoA: Recibe invitación
alt Usuario Acepta
    NodoB-->NodoA: Envía confirmación
else Usuario No hace nada
    note right of NodoB: Invitación queda pendiente
else Usuario Rechaza
    note right of NodoB: No se hace nada. a A le queda como pendiente
end

