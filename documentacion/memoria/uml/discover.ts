participant NodoA
participant Presentador
participant NodoB

title Discover

while A recibe cualquier mensaje de B or Timeout
  NodoA-->Presentador: search(B)
  alt Presentador conoce a B
    Presentador-->NodoA: Coordenadas de B
    NodoA-->NodoB: inicio handshaking
  else Presentador no conoce a B
    note right of Presentador: No se hace nada
end
end
