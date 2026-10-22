# 3. Contrato de la API (backend Lapticon)

Fuentes: `referencias/Lapticon.postman_collection.json`, `referencias/Lapticon.postman_environment.json`,
diapositivas "Mapa de endpoints" de *session 10.pdf* y pruebas reales a los endpoints públicos (22-oct-2026).

Leyenda de verificación: ✅ comprobado contra el servidor · 📄 documentado (Postman/PDF), forma de la respuesta **sin confirmar** · ⚠️ inconsistencia.

## 3.1 Datos de conexión

| Variable | Valor | Nota |
|---|---|---|
| `base_url` | `https://lapticon-backend.onrender.com` | Render (plan gratuito → arranque en frío) |
| Proyecto Firebase | `lapticon-eba31` (project number `919252353880`) | Auth + Firestore |
| `firebase_api_key` | ver environment de Postman | Solo para la prueba en Postman; en la app la toma `google-services.json` |
| Usuario de prueba | `test30@gmail.com` / ver environment | Compartido por todo el curso: **no usarlo como cuenta propia** |
| `other_uid` | `e6GUAvw1cFY7VGSwUQkrTPIrAre2` | Usuario ajeno para probar los 403 |

**Autenticación:** todas las rutas, salvo `/api/ratings/{uid}` (GET) y `/api/ciudades/*`, exigen
`Authorization: Bearer <idToken>`. Sin token o con token inválido → **401** (middleware `VerificarToken.js` con Firebase Admin SDK).
El backend identifica al usuario por `req.user.uid`, por eso **nunca enviamos el uid propio en el body**.

> En Postman el token se obtiene con `POST identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=…`.
> En la app **no** se llama ese endpoint: se usa `FirebaseAuth.signInWithEmailAndPassword()` y luego `user.getIdToken()`.

## 3.2 Endpoints

### Usuarios

| Método | Ruta | Body | Respuesta esperada | Estado |
|---|---|---|---|---|
| POST | `/api/users/register` | `{ nombre, apellido, telefono, nacionalidad }` | 200/201 con el perfil (crea o actualiza) | 📄 |
| GET | `/api/users/{uid}` | — | 200 si es mi uid · **403** si es de otro | 📄 |
| PUT | `/api/users/{uid}` | campos parciales, p. ej. `{ nombre }` | 200 si es mío · **403** si es de otro | 📄 |

Probar si acepta un campo extra `rol` (`"remitente"`/`"viajero"`) para el reto 1.

### Viajes

| Método | Ruta | Body / query | Notas | Estado |
|---|---|---|---|---|
| POST | `/api/viajes` | `{ numeroVuelo: "AA123", ciudadOrigen, ciudadDestino, fechaViaje: "2026-12-01" }` | **400** si ya tengo un viaje `disponible` (un viaje activo a la vez). Puede validar el vuelo con AeroDataBox. | 📄 |
| GET | `/api/viajes` | — | Mis viajes | 📄 |
| GET | `/api/viajes/disponible` | — | Mi viaje activo (probablemente 404 o `null` si no hay) | 📄 |
| GET | `/api/viajes/buscar?ciudad=Bogota` | `ciudad` = ciudad origen | Viajeros que salen de esa ciudad | 📄 |
| GET | `/api/vuelos/{numero}/{fecha}` | — | Validación del vuelo (AeroDataBox) | ⚠️ solo en el PDF |

### Encomiendas

| Método | Ruta | Body / query | Notas | Estado |
|---|---|---|---|---|
| POST | `/api/encomiendas` | `{ ciudadOrigen, ciudadDestino, observaciones, moneda: "USD", valor: 10 }` | Devuelve el objeto con `_id` (Mongo). Queda `disponible`. | 📄 |
| GET | `/api/encomiendas` | — | Mis encomiendas (como remitente). Dispara `actualizarEncomiendasVencidas()` | 📄 |
| GET | `/api/encomiendas/disponibles?origen=Bogota&destino=Miami` | `origen`, `destino` | Encomiendas que un viajero puede tomar | 📄 |
| PUT | `/api/encomiendas/{id}/estado` | `{ estado: "cancelada" \| "entregada" … }` | Solo remitente dueño o viajero asignado | 📄 |
| PUT | `/api/encomiendas/tomar/{id}` | — (el uid sale del token) | Pasa a `tomada` y la vincula al viajero | ⚠️ solo en el PDF |

⚠️ El PDF dice que el remitente define una **fecha límite** (`fechaVencimiento`), pero el body de Postman no la incluye.
Hay que probar si el backend la acepta (nombre exacto del campo y formato).

### Calificaciones

| Método | Ruta | Body | Respuesta | Estado |
|---|---|---|---|---|
| POST | `/api/ratings` | `{ usuarioDestino: uid, rolDestino: "viajero" \| "remitente", calificacion: 1-5, comentario }` | — | 📄 |
| GET | `/api/ratings/{uid}` *(pública)* | — | `{ "total": 0, "promedio": null, "calificaciones": [] }` | ✅ |

Probablemente también requiera el id de la encomienda para cerrar el chat ("cuando las dos partes califican después de la entrega"): **por confirmar**.

### Chats

| Método | Ruta | Respuesta | Estado |
|---|---|---|---|
| GET | `/api/chats/estado/{chatId}` | Si el chat está abierto o cerrado | 📄 |

- `chatId = ([uidA, uidB]..sort()).join('_')` (Dart) → el mismo par de usuarios siempre usa el mismo documento.
- **Los mensajes no pasan por el backend**: van directo a Firestore, colección `chats/{chatId}`.
  Falta confirmar la subcolección y el esquema del mensaje (propuesta: `chats/{chatId}/mensajes/{autoId}` con
  `{ texto, emisorUid, creadoEn: serverTimestamp }`) y las reglas de seguridad de Firestore.
- El backend cierra el chat (`chatService.cerrarChatSiEntregaConfirmada`) cuando ambas partes califican tras la entrega.

### Ciudades (públicas)

| Método | Ruta | Respuesta | Estado |
|---|---|---|---|
| GET | `/api/ciudades/paises` | Arreglo plano de strings (`["Afghanistan","Albania",…]`), en inglés, con algunos nombres mal codificados y duplicados | ✅ |
| GET | `/api/ciudades/ciudades` | Arreglo plano de strings (~1.800–2.000 ciudades de América, p. ej. `"Bogota"`, `"Miami"`, sin tildes) | ✅ |

Uso: autocompletar en formularios y **cachear localmente** (la lista es grande y casi no cambia). Enviar los nombres
**exactamente** como vienen (`Bogota`, no `Bogotá`), porque los filtros por ciudad comparan texto.

### Chatbot

| Método | Ruta | Body | Notas | Estado |
|---|---|---|---|---|
| POST | `/api/chatbot` | `{ mensajeUsuario: "…" }` | Requiere token; depende de que el backend tenga `OPENROUTER_API_KEY` | 📄 |

## 3.3 Modelos de datos propuestos (Dart)

Campos confirmados por los bodies de Postman; los marcados con `?` son supuestos a validar con la primera respuesta real.

```text
Usuario      { uid, nombre, apellido, telefono, nacionalidad, email?, rol? }
Viaje        { _id, numeroVuelo, ciudadOrigen, ciudadDestino, fechaViaje (YYYY-MM-DD),
               estado: disponible | completado, viajeroUid?, createdAt? }
Encomienda   { _id, ciudadOrigen, ciudadDestino, observaciones, moneda, valor (num),
               estado: disponible | tomada | entregada | vencida | cancelada,
               remitenteUid?, viajeroUid?, fechaVencimiento?, createdAt? }
Rating       { usuarioDestino, rolDestino: viajero | remitente, calificacion (1-5), comentario,
               usuarioOrigen?, fecha? }
ResumenRating{ total, promedio (num | null), calificaciones: [Rating] }
EstadoChat   { estado: abierto | cerrado ? }
MensajeChat  { id, texto, emisorUid, creadoEn }          // Firestore
```

Regla de implementación: los modelos usan `fromJson` tolerante (campos opcionales, `_id` o `id`) hasta confirmar el contrato.

## 3.4 Ciclo de vida de la encomienda

```text
            POST /api/encomiendas        PUT /api/encomiendas/tomar/:id      PUT /:id/estado (entregada)     POST /api/ratings (ambos)
  (nueva) ───────────────────────► DISPONIBLE ───────────────────────► TOMADA ──────────────────────────► ENTREGADA ─────────────────────────► chat CERRADO
                                       │  └── PUT /:id/estado (cancelada) ──► CANCELADA
                                       └── fechaVencimiento pasada ──► VENCIDA  (se aplica "lazy" al consultar)
```

Viajes: `disponible` → `completado` cuando pasa `fechaViaje` (también *lazy*, `actualizarViajesCompletados()`).
Consecuencia en la app: **los estados pueden estar desactualizados hasta que alguien consulta** → siempre refrescar al entrar a la lista.

## 3.5 Primera tarea técnica: verificar el contrato

Antes de escribir los modelos, ejecutar la colección en Postman **con una cuenta propia** (no la compartida) y guardar
cada respuesta real en `referencias/respuestas/`. Lista de verificación:

- [ ] Forma de la respuesta de `POST/GET /api/users` y si acepta `rol`.
- [ ] Forma de `POST /api/encomiendas` y si acepta `fechaVencimiento`.
- [ ] Que existan `PUT /api/encomiendas/tomar/:id` y `GET /api/vuelos/:numero/:fecha` y qué devuelven.
- [ ] Qué devuelve `GET /api/viajes/disponible` cuando no hay viaje.
- [ ] Si `POST /api/ratings` necesita `encomiendaId`.
- [ ] Respuesta de `GET /api/chats/estado/:chatId` y estructura de la colección `chats` en Firestore.
- [ ] Formato de los errores (`{ message }`, `{ error }`, `{ msg }`…) para unificar el manejo en `ApiClient`.
