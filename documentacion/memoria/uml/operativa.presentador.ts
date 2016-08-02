title Punching entre nodos

note left of A
A publica sus datos en el Presentador
Durante toda la vida de A, este enviará sus datos al
Presentador.
end note

A-->Presentador: HEL(A)

note over Presentador: El presentador conoce los datos de A.

note left of A
A se quiere conectar a B
A sigue enviando SEA(B) al Presentador
hasta que recibe algún mensaje de B o expira el timeout.
end note

A-->Presentador: SEA(B) 

note over Presentador: El Presentador no conoce a B. No hace nada.

note right of B: B se une a la red y publica sus datos en el Presentador.

B-->Presentador: HEL(B)

A-->Presentador: SEA(B)

note over Presentador: El Presentador envía sendos mensajes CAL cruzados a A y B

Presentador-->A: CAL(B,coordinates)
Presentador-->B: CAL(A,coordinates)

A-->B: HEL(A)
note right of B: Este primer paquete es rechazado puesto que el NAT no lo espera.

B-->A: HEL(B)
note left of A: A sí acepta este paquete, puesto que envió uno previamente.

A-->B: HEL(A)
note right of B: Ahora el paquete de A si es admitido y enrutado.

note over A, B: En este punto el NAT está perforado y A y B pueden enviarse mensajes directamente.

note over Presentador: El Presentador ya no interviene a no ser que se necesite recuperar la conexión.






