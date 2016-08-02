participant A
participant NatA
participant Presentador
participant NatB
participant B

title Discover

note left of A 
dirección LAN: 192.168.1.20:33333
Inaccesible desde internet
end note

A --> NatA: Presentador:SEA(B)
NatA --> Presentador: SEA(B)
note right of NatA
El router otorga un puerto UDP de salida desconocido
para A: 234.235.18.3:44334

El Presentador recibe un paquete UDP de A con la dirección
que expone el gateway 234.235.18.3:44334
end note

note left of Presentador: Presentador no conoce a B. No hace nada

note right of B
dirección LAN: 192.168.4.10:22222
Inaccesible desde internet
end note

B --> NatB: Presentador:HEL(direccion privada de B)
note right of NatB
El router otorga un puerto UDP de salida desconocido
para B: 117.45.65.234:66551

El Presentador recibe un paquete UDP de B con la dirección
que expone el gateway 117.45.65.234:66551

El presentador registra las ips privadas reportadas por B
y la direcció pública expuesta por su GW.
end note

A --> NatA: Presentador: SEA(B)
NatA --> Presentador: SEA(B)

note left of Presentador
  El NAT de A se seguirá dando el mismo puerto de salida
  hasta que expire por inactividad.

  El presentador conoce ambos nodos.
  Y envía un mensaje CAL a cada uno de ellos.
end note

Presentador --> NatA: CAL(direcciones B)
NatA --> A: CAL(direcciones B)

Presentador --> NatB: CAL(direcciones A)
NatB --> B: CAL(direcciones A)

A --> NatA:HEL
note left of NatA: 
mensaje de dirección publica de A a dirección pública de B
234.235.18.3:44334->117.45.65.234:66551
source: 
end note

NatA --> NatB:HEL
note right of NatB
El NAT de B no tiene inicio de comunicación
UDP con la dirección pública de A.
Descarta el paquete
end note

B --> NatB:HEL(direccion publica de A)
NatB --> NatA:HEL

note left of NatA: 
mensaje de dirección publica de B a dirección pública de A
117.45.65.234:66551->234.235.18.3:44334

El NatA sí tiene un puerto UDP escuchando una posible respuesta
de B. Envía en mensaje a la dirección interna de A.
end note

NatA --> A: HEL de B

note left of A
A sigue intentando hasta que expire el tiempo de punching
o se localice a B.
end note

A --> NatA:HEL
NatA --> NatB:HEL
note right of NatB
El NAT de B si tiene ahora un puerto listo para recibir una
respuesta de la dirección pública de A.
Envía el mensaje a la dirección interna de B.
end note

NatB --> B: HEL de B

note left of A
Ambos nodos están conectados P2P y se pueden enviar mensajes
UDP directamente aunque sus IPs internas fueran inaccesibles
y sus NATs no tuvieran enrutamientos fijos para puertos determinados.
end note

A --> NatA: mensaje para B
NatA --> NatB: mensaje para B
NatB --> B: mensaje para B

B --> NatB: mensaje para A
NatB --> NatA: mensaje para A
NatA --> A: mensaje para A
