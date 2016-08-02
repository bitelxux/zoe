participant A
participant A.pub
participant A.priv
participant B.pub
participant B.priv
participant B

title Encriptación

A --> B.pub: Encripta mensaje (B.pub)
A --> A.priv: Firma mensaje (A.priv)

B --> B.priv: Desencripta mensaje(B.priv)
B --> A.pub: Comprueba firma(A.pub)
