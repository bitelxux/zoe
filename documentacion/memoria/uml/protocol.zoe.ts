participant NetA
participant Protocol

title Zoe Protocol

alt Codificación de mensaje
  NetA->Protocol: encode message
  Protocol->NetA: encoded message
else Decodificación de mensaje
  NetA->Protocol: decode message
  Protocol->NetA: decoded message
end
