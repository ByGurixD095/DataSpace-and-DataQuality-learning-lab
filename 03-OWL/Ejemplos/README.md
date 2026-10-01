# 🧠 Tres ontologías OWL, tres niveles

Cada ontología usa un modelo de la vida real que ya conoces, para que lo difícil sea OWL y no el dominio.

| Nivel | Fichero | Analogía | Qué se aprende |
|---|---|---|---|
| 🟢 Básico | [`01-biblioteca-basico.ttl`](01-biblioteca-basico.ttl) | Biblioteca del barrio | Clases, subclases, propiedades, domain/range, inversas |
| 🟡 Intermedio | [`02-tienda-intermedio.ttl`](02-tienda-intermedio.ttl) | Pedido de una tienda online | Restricciones, cardinalidad, transitiva, simétrica, clases definidas |
| 🔴 Avanzado | [`03-alquiler-avanzado.ttl`](03-alquiler-avanzado.ttl) | Alquiler de coches ≈ Espacio de Datos | Cadenas de propiedades, cardinalidad cualificada, unión disjunta, complemento |

> Leyenda de los grafos: caja = clase · óvalo = individuo · flecha continua = propiedad · flecha discontinua = `rdf:type` · flecha gruesa = `subClassOf`.

---

## 🟢 Básico · Biblioteca

Un autor escribe libros y un socio los toma prestados. Es el "hola mundo" de OWL.

```mermaid
graph LR
    Persona[Persona]
    Autor[Autor] ==>|subClassOf| Persona
    Socio[Socio] ==>|subClassOf| Persona
    Autor -->|escribió| Libro[Libro]
    Libro -->|escritoPor| Autor
    Socio -->|tomaPrestado| Libro
    Libro -. disjuntos .- Persona

    Cervantes([Cervantes]) -.->|type| Autor
    DonQuijote([Don Quijote]) -.->|type| Libro
    Ana([Ana]) -.->|type| Socio
    Cervantes -->|escribió| DonQuijote
    Ana -->|tomaPrestado| DonQuijote
```

---

## 🟡 Intermedio · Tienda online

Un pedido es como un ticket: tiene un cliente, un estado y líneas que apuntan a productos. Las categorías se anidan como las secciones de unos grandes almacenes.

```mermaid
graph LR
    Cliente[Cliente] -->|realizaPedido| Pedido[Pedido]
    Pedido -->|"realizadoPor (funcional)"| Cliente
    Pedido -->|"tieneLinea (≥1)"| Linea[LineaPedido]
    Linea -->|refiereA| Producto[Producto]
    Pedido -->|"tieneEstado (exactamente 1)"| Estado["EstadoPedido<br/>{Pendiente, Enviado, Entregado}"]
    Fisico[ProductoFisico] ==>|subClassOf| Producto
    Digital[ProductoDigital] ==>|subClassOf| Producto
    Fisico -. disjuntos .- Digital
    Producto -->|perteneceACategoria| Categoria[Categoria]
    Categoria -->|"subcategoriaDe (transitiva)"| Categoria
    Producto <-->|"complementaA (simétrica)"| Producto
    Frecuente["ClienteFrecuente<br/>(≥5 pedidos)"] ==>|"definida ⊑"| Cliente
```

---

## 🔴 Avanzado · Alquiler de coches ≈ Espacio de Datos

Propietario ≈ *Data Provider* · Arrendatario ≈ *Data Consumer* · Vehículo ≈ *Data Asset* · Oferta ≈ oferta del catálogo · Política ≈ ODRL · Contrato ≈ *Contract Agreement*.

Las líneas rojas son propiedades **inferidas** por cadenas: el razonador deduce quién puede usar qué sin que nadie lo escriba.

```mermaid
graph LR
    Prop[Propietario] -->|ofrece| Oferta[Oferta]
    Oferta -->|"ofertaSobreVehiculo (exactamente 1)"| Veh["Vehículo<br/>= Turismo ⊔ Furgoneta ⊔ Moto"]
    Oferta -->|tienePolitica| Pol[Política]
    Pol -->|tieneRegla| Regla["Regla<br/>= Permiso ⊔ Prohibición ⊔ Obligación"]
    Contrato[ContratoAlquiler] -->|contratoDeOferta| Oferta
    Contrato -->|tienePropietario| Prop
    Contrato -->|tieneArrendatario| Arr[Arrendatario]
    Arr -->|firmaContrato| Contrato
    Contrato -->|estado| Est["EstadoContrato<br/>{Borrador, Vigente, Finalizado}"]
    Contrato -->|"renuevaA (asimétrica)"| Contrato

    Arr -.->|"puedeUsar ⟸ cadena"| Veh
    Arr -.->|"contrataCon ⟸ cadena"| Prop
    Veh -.->|"alquiladoEn ⟸ cadena"| Contrato

    linkStyle 10,11,12 stroke:#d33,stroke-width:2px,stroke-dasharray:4
```

---

💡 **Cómo probarlas:** abre los `.ttl` en [Protégé](https://protege.stanford.edu/), activa un razonador (HermiT) y mira los axiomas inferidos. Los comentarios `# Inferencia:` al final de cada fichero te dicen qué debería aparecer.
