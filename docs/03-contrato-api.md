# 3. Contrato de la API (backend Lapticon)

Fuentes: `referencias/Lapticon.postman_collection.json`, `referencias/Lapticon.postman_environment.json`,
diapositivas "Mapa de endpoints" de *session 10.pdf* y **pruebas reales con dos cuentas propias** (remitente y viajero,
22-oct-2026). Las respuestas están en `referencias/respuestas/` (teléfono y correo enmascarados).

> **Versión Swagger/OpenAPI** de este contrato, con bodies, esquemas y los endpoints que faltan: [`docs/api/`](api/README.md).

Leyenda de verificación: ✅ comprobado contra el servidor · 📄 documentado (Postman/PDF), forma de la respuesta **sin confirmar** · ⚠️ falla o se comporta distinto a lo documentado.

## 3.1 Datos de conexión

| Variable | Valor | Nota |
|---|---|---|
| `base_url` | `https://lapticon-backend.onrender.com` | Render (plan gratuito → arranque en frío) |
| Proyecto Firebase | `lapticon-eba31` (project number `919252353880`) | Auth + Firestore |
| `firebase_api_key` | ver environment de Postman | Solo para la prueba en Postman; en la app la toma `google-services.json` |
| Usuario de prueba | `test30@gmail.com` / ver environment | Compartido por todo el curso: **no usarlo como cuenta propia** |
| `other_uid` | `e6GUAvw1cFY7VGSwUQkrTPIrAre2` | Usuario ajeno para probar los 403 |

**Autenticación:** todas las rutas, salvo `/api/ratings/{uid}` (GET) y `/api/ciudades/*`, exigen
`Authorization: Bearer <idToken>`. ✅ Sin token → **401** `{ "error": "Token no proporcionado" }`; token inválido → **401**
`{ "error": "Token inválido" }`.

**Formato de respuestas ✅:** los errores siempre son `{ "error": "…" }` (a veces con `detalle`). Los éxitos usan
`{ message, user }` en usuarios y `{ mensaje, … }` en encomiendas, calificaciones y viajes. `ApiClient.extractMessage`
lee `message`, `mensaje` y `error`.
El backend identifica al usuario por `req.user.uid`, por eso **nunca enviamos el uid propio en el body**.

> En Postman el token se obtiene con `POST identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=…`.
> En la app **no** se llama ese endpoint: se usa `FirebaseAuth.signInWithEmailAndPassword()` y luego `user.getIdToken()`.

## 3.2 Endpoints

### Usuarios ✅

| Método | Ruta | Body | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/users/register` | `{ nombre, apellido, telefono, nacionalidad }` | **201** `{ message: "Usuario guardado correctamente", user }` (crea o actualiza) | ✅ |
| GET | `/api/users/{uid}` | — | **200** `{ user }` si es mi uid · **403** `{ error: "No autorizado para consultar este usuario" }` si es de otro (también para uids que no existen) | ✅ |
| PUT | `/api/users/{uid}` | campos parciales | **200** `{ message: "Usuario actualizado correctamente", user }` | ✅ |

`user = { _id, uid, nombre, apellido, telefono, nacionalidad, email, createdAt, updatedAt, __v }`.
El backend guarda el `email` del token. **No acepta `rol`:** `PUT { rol }` responde 200 pero no lo guarda → el rol vive
solo en la app (`shared_preferences`), como ya hacía `UsuarioRepository.guardarRol` (devuelve `false`).

### Viajes ✅

| Método | Ruta | Body / query | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/viajes` | `{ numeroVuelo, ciudadOrigen, ciudadDestino, fechaViaje: "2026-12-01" }` | **201** con el viaje (`uid` = viajero, `fechaViaje` en ISO `…T00:00:00.000Z`, `estado: "disponible"`) | ✅ |
| POST | `/api/viajes` (2.º activo) | — | **400** `{ error: "Ya tienes un viaje disponible. Debes cerrarlo o cambiar su estado antes de registrar uno nuevo." }` | ✅ |
| GET | `/api/viajes` | — | **200** arreglo (vacío `[]` si no hay) | ✅ |
| GET | `/api/viajes/disponible` | — | **200** el viaje (objeto directo) · **404** `{ mensaje: "No hay viajes disponibles" }` | ✅ |
| GET | `/api/viajes/buscar?ciudad=Bogota` | `ciudad` = origen | **200** arreglo de viajes (incluye `uid` del viajero) | ✅ |
| GET | `/api/vuelos/{numero}/{fecha}` | — | **500** `{ error: "RAPIDAPI_KEY no está configurada en el servidor" }` | ⚠️ existe, pero falla en el servidor |

Con `/api/vuelos` caído, la app muestra "No pudimos verificar el vuelo" y deja registrar el viaje igual.

### Encomiendas ✅

| Método | Ruta | Body / query | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/encomiendas` | `{ ciudadOrigen, ciudadDestino, observaciones, moneda: "USD", valor: 10 }` | **201** con la encomienda | ✅ |
| GET | `/api/encomiendas` | — | **200** arreglo de mis encomiendas (como remitente) | ✅ |
| GET | `/api/encomiendas/disponibles?origen=Bogota&destino=Miami` | `origen`, `destino` | **200** arreglo con `remitenteNombre` y **sin** `uid`; incluye las propias | ✅ |
| PUT | `/api/encomiendas/tomar/{id}` | — (uid del token) | **200** `{ mensaje: "Encomienda tomada exitosamente" }` (sin la encomienda) · **400** `{ error: "Esta encomienda ya fue tomada o vencida" }` | ✅ |
| PUT | `/api/encomiendas/{id}/estado` | `{ estado }` | **200** `{ mensaje: "Estado actualizado", encomienda }` · **400** estado inválido · **403** `{ error: "No autorizado para modificar esta encomienda" }` | ✅ |

Encomienda real:

```json
{ "_id": "6ada5d86…", "uid": "<remitente>", "ciudadOrigen": "Bogota", "ciudadDestino": "Miami",
  "observaciones": "…", "moneda": "USD", "valor": 15, "estado": "disponible", "viajeroId": null,
  "fechaCreacion": "2026-10-22T19:01:26.915Z", "fechaVencimiento": "2026-11-22T19:01:26.915Z",
  "fechaDisponibleDesde": "2026-10-22T19:01:26.915Z", "fechaLimiteEntrega": null, "__v": 0 }
```

**Estados válidos** (texto exacto del 400): `disponible, tomada, vencida, entregada, recibida`.

⚠️ Comportamientos del backend que la app debe tener en cuenta:
- **No existe `cancelada`.** Para retirar una encomienda, la app la pasa a `vencida`.
- **`fechaVencimiento` se ignora:** siempre vence un mes después de creada. La app ya no pide fecha límite.
- **No valida el body:** `POST {}` crea una encomienda vacía con 201 → la app valida todo antes de enviar.
- **No valida roles:** el remitente puede tomar su propia encomienda y marcarla `entregada`. `/disponibles` no trae el uid,
  así que la app cruza la lista con `GET /api/encomiendas` (mis encomiendas) para no ofrecerle al viajero las propias.
- Volver a `disponible` no limpia `viajeroId`.

### Calificaciones ✅

| Método | Ruta | Body | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/ratings` | `{ usuarioDestino, rolDestino: "viajero" \| "remitente", calificacion: 1-5, comentario }` | **201** `{ mensaje: "Calificación guardada", data: { usuarioOrigen, usuarioDestino, rolDestino, calificacion, comentario, timestamp, _id } }` | ✅ |
| GET | `/api/ratings/{uid}` *(pública)* | — | **200** `{ total, promedio (num \| null), calificaciones: [ … ] }`; la fecha viene en `timestamp` | ✅ |

⚠️ `encomiendaId` **se ignora** (no se guarda). Tampoco se valida que la encomienda esté entregada (se puede calificar
antes). Body vacío o `calificacion` fuera de 1-5 → **500** `{ error: "Error interno al guardar calificación" }` (no 400),
por eso la app limita a 1-5 antes de enviar.

### Chats

| Método | Ruta | Respuesta real | Estado |
|---|---|---|---|
| GET | `/api/chats/estado/{chatId}` | **500** `{ error: "Error interno del servidor" }`, incluso para un par real remitente/viajero, en cualquier orden y después de calificar | ⚠️ |

- `chatId = ([uidA, uidB]..sort()).join('_')` (Dart) → el mismo par de usuarios siempre usa el mismo documento.
- Mientras el endpoint falle, la app trata el chat como **abierto** (500 o 404 → abierto).
- **Los mensajes no pasan por el backend**: van directo a Firestore, `chats/{chatId}/mensajes/{autoId}` con
  `{ texto, emisorUid, creadoEn: serverTimestamp }`. Esquema y reglas de Firestore **por confirmar** desde la app.
- El backend debería cerrar el chat (`chatService.cerrarChatSiEntregaConfirmada`) cuando ambas partes califican tras la
  entrega; no se pudo comprobar por el 500.

### Ciudades (públicas) ✅

| Método | Ruta | Respuesta | Estado |
|---|---|---|---|
| GET | `/api/ciudades/paises` | Arreglo plano de strings (`["Afghanistan","Albania",…]`), en inglés, con algunos nombres mal codificados y duplicados | ✅ |
| GET | `/api/ciudades/ciudades` | Arreglo plano de strings (~1.800–2.000 ciudades de América, p. ej. `"Bogota"`, `"Miami"`, sin tildes) | ✅ |

Uso: autocompletar en formularios y **cachear localmente**. Enviar los nombres **exactamente** como vienen (`Bogota`,
no `Bogotá`), porque los filtros por ciudad comparan texto.

### Chatbot

| Método | Ruta | Body | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/chatbot` | `{ mensajeUsuario: "…" }` | **500** `{ error: "Error al generar respuesta con OpenRouter", detalle: { error: { message: "User not found.", code: 401 } } }` · vacío → **400** `{ error: "Mensaje vacío" }` | ⚠️ la key de OpenRouter del servidor no es válida |

## 3.3 Modelos de datos (Dart)

```text
Usuario      { uid, nombre, apellido, telefono, nacionalidad, email, createdAt }   // envuelto en { user }; sin rol
Viaje        { _id, uid (viajero), numeroVuelo, ciudadOrigen, ciudadDestino, fechaViaje (ISO),
               estado: disponible | completado, createdAt }
Encomienda   { _id, uid (remitente), viajeroId, ciudadOrigen, ciudadDestino, observaciones, moneda, valor (num),
               estado: disponible | tomada | entregada | recibida | vencida,
               fechaCreacion, fechaVencimiento (creación + 1 mes), fechaDisponibleDesde, fechaLimiteEntrega,
               remitenteNombre (solo en /disponibles) }
Rating       { _id, usuarioOrigen, usuarioDestino, rolDestino: viajero | remitente, calificacion (1-5), comentario, timestamp }
ResumenRating{ total, promedio (num | null), calificaciones: [Rating] }
EstadoChat   { abierto | cerrado }   // endpoint caído → abierto
MensajeChat  { id, texto, emisorUid, creadoEn }          // Firestore, por confirmar
```

Los modelos siguen siendo tolerantes (`_id` o `id`, objetos envueltos o directos); los tests de
`test/contrato_test.dart` → grupo "Respuestas reales" usan estas respuestas.

## 3.4 Ciclo de vida de la encomienda

```text
            POST /api/encomiendas        PUT /api/encomiendas/tomar/:id      PUT /:id/estado (entregada)     PUT /:id/estado (recibida)
  (nueva) ───────────────────────► DISPONIBLE ───────────────────────► TOMADA ──────────────────────────► ENTREGADA ─────────────────────────► RECIBIDA
                                       │  └── PUT /:id/estado (vencida) = el remitente la retira
                                       └── un mes después de creada ──► VENCIDA  (se aplica "lazy" al consultar)
  Calificaciones: POST /api/ratings (ambos), sin depender del estado en el backend.
```

Viajes: `disponible` → `completado` cuando pasa `fechaViaje` (también *lazy*). Solo un viaje `disponible` a la vez.
Consecuencia en la app: **los estados pueden estar desactualizados hasta que alguien consulta** → siempre refrescar al entrar a la lista.

## 3.5 Verificación del contrato (22-oct-2026)

Con dos cuentas propias (remitente y viajero), nunca con la compartida:

- [x] Forma de `POST/GET/PUT /api/users` → `{ message?, user }`. **No acepta `rol`.**
- [x] Forma de `POST /api/encomiendas`. **Ignora `fechaVencimiento`** (vence al mes).
- [x] `PUT /api/encomiendas/tomar/:id` existe → `{ mensaje }`.
- [x] `GET /api/vuelos/:numero/:fecha` existe, pero da 500 (falta `RAPIDAPI_KEY` en el servidor).
- [x] `GET /api/viajes/disponible` sin viaje → 404 `{ mensaje }`.
- [x] `POST /api/ratings` **no necesita ni guarda `encomiendaId`**.
- [ ] `GET /api/chats/estado/:chatId` → 500 siempre. Falta confirmar la estructura de Firestore y las reglas, desde la app.
- [x] Formato de errores: `{ error }`.
- [x] Estados de encomienda: `disponible, tomada, vencida, entregada, recibida` (sin `cancelada`).

Para repetir las pruebas: `bash lapticon_app/tool/obtener_token.sh` (una vez por cuenta) y `curl` con
`Authorization: Bearer <idToken>`; renovar con `RENOVAR=1 bash lapticon_app/tool/obtener_token.sh`.
