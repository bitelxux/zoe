participant Core
participant Storage

title Almacenar Mensaje

Core->Storage: Almacenar(mensaje)
Storage->Storage: Encriptar mensaje
Storage->Storage: Almacenar mensaje
Storage->Core: Resultado: 
