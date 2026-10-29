# 3. Contrato de la API (backend Lapticon)

Fuentes: `referencias/Lapticon.postman_collection.json`, `referencias/Lapticon.postman_environment.json`,
diapositivas "Mapa de endpoints" de *session 10.pdf*, el **Swagger oficial del profesor**
(`referencias/swagger-oficial.json`, https://lapticon-backend.onrender.com/api-docs/) y **pruebas reales con dos cuentas
propias** (remitente y viajero, 22-oct y 28-oct-2026). Las respuestas están en `referencias/respuestas/` (teléfono y
correo enmascarados; las del 28-oct empiezan por `fase0_`).

> El Swagger oficial declara el servidor `lapticon-backend-ed.onrender.com`, que **no existe** (404 en todo). Todas sus
> rutas están en `lapticon-backend.onrender.com`, que es el que usan las apps (pregunta al profesor en docs/06).

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

**Autenticación:** todas las rutas, salvo `/api/ratings/{uid}` (GET), `/api/ciudades/*`, `GET /api/viajes/disponibles`,
`GET /api/vuelos/…` y `POST /api/encomiendas/actualizar-vencidas`, exigen
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
| PUT | `/api/users/{uid}` | campos parciales | **200** `{ message: "Usuario actualizado correctamente", user }` · **400** si se intenta cambiar `uid` o `email` (oficial) | ✅ / 📄 400 |

`user = { _id, uid, nombre, apellido, telefono, nacionalidad, email, createdAt, updatedAt, __v }`. Según el oficial
también acepta **`fechaNacimiento`** (fecha, opcional) y `correo` 📄.
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
| GET | `/api/viajes/disponibles?ciudadOrigen&ciudadDestino` *(pública)* | ruta completa | **200** `[{ ciudadOrigen, ciudadDestino, fechaViaje, nombreUsuario, uid }]`: viajeros con viaje disponible en esa ruta, **con nombre** | ✅ |
| PATCH | `/api/viajes/{id}/estado` | `{ estado: "disponible" \| "completado" \| "cancelado" }` | **200** `{ message: "Estado actualizado", viaje }` · **400** `{ error: "Estado inválido" }` (también `contactado`) · **404** `{ error: "Viaje no encontrado o no autorizado" }` (id inexistente o de otro) | ✅ |
| GET | `/api/vuelos/{numero}/{fecha}` *(pública)* | — | **500** `{ error: "RAPIDAPI_KEY no está configurada en el servidor" }` | ⚠️ existe, pero falla en el servidor |

Con `/api/vuelos` caído, la app **no muestra** la verificación del vuelo (docs/11 §2H): se registra con número, ruta y fecha.

**Cancelar o cerrar un viaje ✅:** después de `cancelado` o `completado`, `GET /disponible` da 404 y se puede registrar
otro. Ojo: el servidor **deja volver a `disponible`** un viaje cancelado (la app no lo ofrece) y no revisa si el viaje
tiene encomiendas tomadas (la app avisa antes). El oficial lista también `contactado`, pero el `PATCH` lo rechaza.

### Encomiendas ✅

| Método | Ruta | Body / query | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/encomiendas` | `{ ciudadOrigen, ciudadDestino, observaciones, moneda: "USD", valor: 10 }` | **201** con la encomienda | ✅ |
| GET | `/api/encomiendas` | — | **200** arreglo de mis encomiendas (como remitente) | ✅ |
| GET | `/api/encomiendas/disponibles?origen=Bogota&destino=Miami` | `origen`, `destino` | **200** arreglo con `remitenteNombre` y **sin** `uid`; incluye las propias | ✅ |
| GET | `/api/encomiendas/buscar?origen&destino` | los dos obligatorios | **200** `{ disponibles, tomadas }`: las disponibles de la ruta (**incluye las propias**) y las que **yo tomé** en esa ruta. Cada una con `uid` del remitente **y** `remitenteNombre`. `tomadas` trae **solo** estado `tomada`: con `entregada`/`recibida` desaparece · **400** sin origen o destino | ✅ |
| GET | `/api/encomiendas/disponibles2?ciudadOrigen&ciudadDestino` | opcionales | **200** arreglo con `uid` y sin nombre; **excluye las propias** | ✅ |
| GET | `/api/encomiendas/mis-encomiendas` | — | **200** `{ disponibles }`: solo mis encomiendas aún disponibles | ✅ |
| GET | `/api/encomiendas/vencidas` | — | **200** las vencidas **de todos los usuarios**, con `remitenteNombre` (no sirve para la app) | ✅ |
| POST | `/api/encomiendas/emparejar-viajes` | `{ ciudadOrigen, ciudadDestino, fechaEncomienda, valorEncomienda }` | **200** `[{ viajeId, uid, afinidad (0-1), ciudadOrigen, ciudadDestino, fechaViaje }]`. Una vez tardó más de 120 s; la siguiente, 0,5 s | ✅ |
| POST | `/api/encomiendas/evaluar-emparejamiento` | — | **500** `{ error: "Error al consultar motor de emparejamiento" }` (falta `MATCHING_API_URL`) | ⚠️ |
| POST | `/api/encomiendas/actualizar-vencidas` *(pública)* | — | Para una tarea programada; la app no la llama | 📄 |
| PUT | `/api/encomiendas/tomar/{id}` | — (uid del token) | **200** `{ mensaje: "Encomienda tomada exitosamente" }` (sin la encomienda) · **400** `{ error: "Esta encomienda ya fue tomada o vencida" }` | ✅ |
| PUT | `/api/encomiendas/{id}/estado` | `{ estado }` | **200** `{ mensaje: "Estado actualizado", encomienda }` · **400** estado inválido · **403** `{ error: "No autorizado para modificar esta encomienda" }` si no soy el remitente ni el viajero asignado | ✅ |

Tomar **no exige** que la ruta coincida con el viaje del viajero. Las encomiendas traen además `fotoUrl` (siempre `null`;
no hay endpoint para subir la foto).

Encomienda real:

```json
{ "_id": "6ada5d86…", "uid": "<remitente>", "ciudadOrigen": "Bogota", "ciudadDestino": "Miami",
  "observaciones": "…", "moneda": "USD", "valor": 15, "estado": "disponible", "viajeroId": null,
  "fechaCreacion": "2026-10-22T19:01:26.915Z", "fechaVencimiento": "2026-11-22T19:01:26.915Z",
  "fechaDisponibleDesde": "2026-10-22T19:01:26.915Z", "fechaLimiteEntrega": null, "fotoUrl": null, "__v": 0 }
```

**Estados válidos** (texto exacto del 400): `disponible, tomada, vencida, entregada, recibida`. El oficial **no lista
`entregada`**, pero el servidor la acepta: la app la sigue usando (pregunta al profesor en docs/06).

⚠️ Comportamientos del backend que la app debe tener en cuenta:
- **No existe `cancelada`.** Para retirar una encomienda, la app la pasa a `vencida`.
- **`fechaVencimiento` se ignora:** siempre vence un mes después de creada. La app ya no pide fecha límite.
- **No valida el body:** `POST {}` crea una encomienda vacía con 201 → la app valida todo antes de enviar.
- **No valida roles:** el remitente puede tomar su propia encomienda y marcarla `entregada`. `/disponibles` no trae el uid,
  así que la app cruza la lista con `GET /api/encomiendas`. Con `buscar` (trae `uid`) basta con filtrar por uid, o usar
  `disponibles2`, que ya las excluye.
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
| GET | `/api/chats/estado/{chatId}` | **200** `{ estado: "activo" \| "cerrado", fechaCierre }` · **404** `{ error: "Chat no encontrado" }` si el par nunca tuvo una encomienda tomada (o el id está en otro orden) | ✅ (28-oct; el 22-oct daba 500) |

- `chatId = ([uidA, uidB]..sort()).join('_')` (Dart) → el mismo par de usuarios siempre usa el mismo documento. Es el
  formato que espera el backend: en orden inverso o con el id de la encomienda da 404.
- El documento lo crea el backend: al **tomar** queda `activo`; al marcar **`entregada`** pasa a `cerrado` con
  `fechaCierre`; tomar **otra** encomienda del mismo par lo vuelve a `activo`. El chat es **por par**, no por encomienda.
- La app trata `cerrado` como bloqueado, y `activo`, 404 o 500 como **abierto**.
- **Los mensajes no pasan por el backend**: van directo a Firestore, `chats/{chatId}/mensajes/{autoId}` con
  `{ texto, emisorUid, creadoEn: serverTimestamp }`. Esquema y reglas de Firestore **por confirmar** desde la app.
- El 22-oct pensábamos que se cerraba cuando ambos calificaban; lo comprobado es que se cierra al marcar `entregada`.

### Ciudades (públicas) ✅

| Método | Ruta | Respuesta | Estado |
|---|---|---|---|
| GET | `/api/ciudades/paises` | Arreglo plano de strings (`["Afghanistan","Albania",…]`), en inglés, con algunos nombres mal codificados y duplicados | ✅ |
| GET | `/api/ciudades/ciudades` | Arreglo plano de strings (~1.800–2.000 ciudades de América, p. ej. `"Bogota"`, `"Miami"`, sin tildes) | ✅ |
| GET | `/api/ciudades/ciudades-por-pais?nombre=Colombia` | Arreglo de strings **con tildes** (`"Bogotá"`), distinto de `/ciudades` | ✅ |

Uso: autocompletar en formularios y **cachear localmente**. Enviar los nombres **exactamente** como vienen (`Bogota`,
no `Bogotá`), porque los filtros por ciudad comparan texto. **No mezclar** `ciudades-por-pais` con los formularios.

### Chatbot

| Método | Ruta | Body | Respuesta real | Estado |
|---|---|---|---|---|
| POST | `/api/chatbot` | `{ mensajeUsuario: "…" }` | **500** `{ error: "Error al generar respuesta con OpenRouter", detalle: { error: { message: "User not found.", code: 401 } } }` · vacío → **400** `{ error: "Mensaje vacío" }` | ⚠️ la key de OpenRouter del servidor no es válida |

## 3.3 Modelos de datos (Dart)

```text
Usuario      { uid, nombre, apellido, telefono, nacionalidad, email, fechaNacimiento?, createdAt }   // envuelto en { user }; sin rol
Viaje        { _id, uid (viajero), numeroVuelo, ciudadOrigen, ciudadDestino, fechaViaje (ISO),
               estado: disponible | completado | cancelado | contactado (solo en el oficial), createdAt }
Encomienda   { _id, uid (remitente), viajeroId, ciudadOrigen, ciudadDestino, observaciones, moneda, valor (num),
               estado: disponible | tomada | entregada | recibida | vencida,
               fechaCreacion, fechaVencimiento (creación + 1 mes), fechaDisponibleDesde, fechaLimiteEntrega,
               fotoUrl (null), remitenteNombre (en /disponibles y /buscar) }
Rating       { _id, usuarioOrigen, usuarioDestino, rolDestino: viajero | remitente, calificacion (1-5), comentario, timestamp }
ResumenRating{ total, promedio (num | null), calificaciones: [Rating] }
EstadoChat   { estado: activo | cerrado, fechaCierre }   // 404 o 500 → abierto
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

Viajes: `disponible` → `completado` cuando pasa `fechaViaje` (también *lazy*), o a mano con
`PATCH /api/viajes/{id}/estado` (`completado` o `cancelado`). Solo un viaje `disponible` a la vez.
Chat del par: se abre al tomar y se cierra al marcar `entregada`.
Consecuencia en la app: **los estados pueden estar desactualizados hasta que alguien consulta** → siempre refrescar al entrar a la lista.

## 3.5 Verificación del contrato (22-oct-2026)

Con dos cuentas propias (remitente y viajero), nunca con la compartida:

- [x] Forma de `POST/GET/PUT /api/users` → `{ message?, user }`. **No acepta `rol`.**
- [x] Forma de `POST /api/encomiendas`. **Ignora `fechaVencimiento`** (vence al mes).
- [x] `PUT /api/encomiendas/tomar/:id` existe → `{ mensaje }`.
- [x] `GET /api/vuelos/:numero/:fecha` existe, pero da 500 (falta `RAPIDAPI_KEY` en el servidor).
- [x] `GET /api/viajes/disponible` sin viaje → 404 `{ mensaje }`.
- [x] `POST /api/ratings` **no necesita ni guarda `encomiendaId`**.
- [x] `GET /api/chats/estado/:chatId` → 200 `{ estado, fechaCierre }` con los uid ordenados (28-oct). Falta confirmar las
  reglas de Firestore desde la app.
- [x] Formato de errores: `{ error }`.
- [x] Estados de encomienda: `disponible, tomada, vencida, entregada, recibida` (sin `cancelada`).

### Verificación del 28-oct-2026 (Swagger oficial, docs/11 Fase 0)

- [x] `PATCH /api/viajes/{id}/estado`: `cancelado` y `completado` → 200; `contactado` → 400; viaje ajeno → 404.
- [x] `buscar` → `{ disponibles, tomadas }` con `uid` y `remitenteNombre`; `tomadas` solo trae `tomada`.
- [x] `disponibles2` excluye las propias; `buscar` no.
- [x] `PUT /{id}/estado` desde un tercero → 403.
- [x] Estado del chat: 200 con los uid ordenados; se cierra con `entregada`.
- [x] `emparejar-viajes` → 200; `evaluar-emparejamiento` → 500.
- [x] `viajes/disponibles` es pública y trae `nombreUsuario`.
- [x] `vuelos` es pública, pero sigue en 500; `chatbot` sigue en 500 (key de OpenRouter inválida).

Para repetir las pruebas: `bash lapticon_app/tool/obtener_token.sh` (una vez por cuenta) y `curl` con
`Authorization: Bearer <idToken>`; renovar con `RENOVAR=1 bash lapticon_app/tool/obtener_token.sh`.
