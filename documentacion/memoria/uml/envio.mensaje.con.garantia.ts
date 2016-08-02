title Envío de mensje con garantía

CoreA->StorageA: almacenar mensaje
loop Mientras el mensaje siga pendiente, cada x tiempo
    CoreA->RouterA: pide coordenadas de B
    alt Si se tienen coordenadas de B
        CoreA->NetA: despachar mensaje
        NetA-->NodoB: despachar mensaje
    end
end





