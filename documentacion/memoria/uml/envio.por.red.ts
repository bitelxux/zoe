participant CoreA
participant NetA
participant Router
participant NodoB

title Envío por red

CoreA->NetA: Enviar mensaje
NetA->NetA: Codifica Mensaje
NetA->Router: Resolver B
Router->NetA: Coordenadas de B
NetA-->NodoB: Envía mensaje
