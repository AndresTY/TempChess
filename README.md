# API Resevas



**register(request)** 

Entra un request con la informacion pertinente al registro

_output_
```console
http code(406 o 201)
```

---

**AddVehiculo(placa,style,gamma)**

Crea el vehiculo con la informacion suministrada

_output_
```console
http code (406 o 201)
```

---

**Catalogo(User, Filter)**

Muestra un array con todos vehiculos creados

_output_
```Json
{
   "Vehiculos":{
      "placa":"",
      "gamma":"",
      "style":{
         "marca":"",
         "polarizado":"",
         "Demas atributos":""
      }
   }
}
```

---

**reservar(User, Vehiculo, horas)**

Se genera la reserva para que un admin lo confirme

_output POST_
```console
http code(406 o 201)
```

_output GET_
```Json
{
   "reserva_espera":{
      "starttime":"",
      "endtime":"",
      "actualtime":"",
      "renter":"",
      "vehicule":"",
      "isAccepted":"Espera"
   }
}
```

---

**login(username, hash_password)**

se crea una cuenta

_output POST_
```console
http code(406 o 201)
```

_output GET_
```txt
TOKEN
```

---

**acceptReserva(user_admin)**

permite unicamente a usuario administradores aceptar reservas

_output_

```Json
{
   "reserva_espera":{
      "starttime":"",
      "endtime":"",
      "actualtime":"",
      "renter":"",
      "vehicule":"",
      "isAccepted":"Espera"
   },
   "reserva_cancelado":{
      "starttime":"",
      "endtime":"",
      "actualtime":"",
      "renter":"",
      "vehicule":"",
      "isAccepted":"Cancelado"
   }
}
```
