participant NetA
participant Router
participant Presenters

title Query Address

NetA->Router: query address
alt Router conoce la direccion
   Router->NetA: dirección
else Router no conoce la direccion
   NetA->Router: get known peers
   Router->NetA: known peers
   NetA->Presenters: SEA to each known
end
