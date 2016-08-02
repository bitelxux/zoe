participant Core
participant Storage
participant NodoB

title Envío de mensaje sin garantía

alt Si se requiere histórico
    Core-->Storage: Almacenar mensaje
    Core->Net: Enviar mensaje
    Net->Core: Resultado
    Core->Storage: Actualizar estado mensaje

else Si no se requiere histórico
    note at right of Core: No se almacena
    Core->Net: Enviar mensaje

end





