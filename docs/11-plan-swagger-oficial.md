# 11. Plan de trabajo: Swagger oficial y observaciones del profesor

> **Estado:** en desarrollo (28-oct-2026). Pasos 1 (2H), 2 (Fase 0), 3 (Fase 1), 4 (2A) y 5 (2B) hechos; sigue 2G.
>
> **Fuentes:**
> - el Swagger oficial: https://lapticon-backend.onrender.com/api-docs/ (copia en `referencias/swagger-oficial.json`);
> - una verificación contra el servidor real el 28-oct-2026, con las dos cuentas propias. Solo hubo lecturas y
>   peticiones que no cambian nada: id inexistente o estado inválido;
> - la **revisión del profesor** (§1.1): no queda claro cuándo un viajero tomó la encomienda, y "verificar vuelo" no
>   funciona, así que no debe mostrarse.
>
> **Bloqueado:** **cancelar encomienda.** Esperamos que el profesor la agregue (Fase 4).

## 0. Para quien desarrolle esto (otro agente o persona)

Este documento basta para trabajar sin la conversación en la que se escribió.

**Repositorios.** Son tres, anidados en `proyecto_2_corte/`. Cada uno tiene su propio git:

| Carpeta | Repositorio | Qué es |
|---|---|---|
| `./` | `…-lapicon` | Documentación (`docs/`, `referencias/`, `CLAUDE.md`). Ignora las otras dos carpetas. |
| `lapticon_app/` | `…-lapicon-flutter` | App Flutter (Riverpod 3, go_router). Arquitectura en `CLAUDE.md` y `docs/04`. |
| `aplicacion_pwa/` | `…-lapicon-pwa` | PWA (React 19 + TS + Vite + TanStack Query + Tailwind). Uso en su `README.md`; plan en `docs/10`. |

**Reglas que no se negocian**

- **El mismo cambio va en las dos apps**, con los mismos nombres de componentes, las mismas claves locales
  (`viajero_…_{uid}`) y los mismos textos. Cada sección de la Fase 2 dice los archivos de cada una.
- Las pantallas **nunca** llaman a `http`/`fetch`/Firebase directo:
  - en la PWA, todo pasa por `src/datos/repositorios/index.ts`;
  - en Flutter, por `lib/data/repositories/*`.
- Diseño y accesibilidad según `docs/07` y `docs/09`:
  - áreas táctiles ≥ 48 dp;
  - nada se comunica solo con color (siempre texto + ícono);
  - textos en español de "tú";
  - las acciones irreversibles se confirman escribiendo una palabra (`ENTREGAR`, `RETIRAR`…).
- **Comandos de verificación (deben quedar en verde antes de cada commit)**
  - PWA:

    ```bash
    npm run typecheck && npm run lint && npm test && npm run e2e
    ```

  - Flutter:

    ```bash
    flutter analyze && flutter test
    ```

- **Commits pequeños en español** (`feat:`, `fix:`, `test:`, `docs:`), con commit **dentro de cada carpeta**.
- **No hacer push sin el OK de Harold.** Un push al repo de la PWA **despliega a producción**
  (lapticon.haroldsoftware.com, Cloudflare Pages).
- **Nunca** escribir en un archivo ni en la salida: claves, tokens ni contraseñas.
  - La clave de Firebase de la PWA está en `aplicacion_pwa/.env.local`, que no se sube.
  - Los tokens de prueba están en `~/.lapticon/` (`token.json` = remitente, `token2.json` = viajero).
- **Datos de prueba:** solo las dos cuentas propias. No tocar el viaje **AV10 Bogota → Miami** ni las encomiendas de la
  demo; crear datos desechables para cada prueba que escriba en el servidor.
- **Al terminar cada fase:**
  1. marcarla en la tabla de §5 de este documento;
  2. agregar un paso a `docs/BITACORA.md`;
  3. actualizar `docs/03` y `docs/api/` si cambió el contrato.

## 1. Lo más importante

| # | Hallazgo | Consecuencia |
|---|---|---|
| 1 | **Ya se puede cancelar un viaje:** `PATCH /api/viajes/{id}/estado` con `{ estado: "cancelado" }`. Verificado que la ruta existe y valida el estado (400 "Estado inválido" con un estado falso). | Se puede construir ya (Fase 2A). Resuelve "Ya tienes un viaje disponible… debes cerrarlo". |
| 2 | **El viajero ya puede saber quién es el remitente:** `GET /api/encomiendas/buscar` y `/disponibles2` devuelven el `uid` del remitente (`/disponibles` no lo daba). | Arregla "Podrás escribirle cuando te escriba primero" (Fase 2B): el viajero abre el chat y califica sin esperar. |
| 3 | **El viajero ya puede ver lo que tomó desde el servidor:** `GET /api/encomiendas/buscar` → `{ disponibles, tomadas }`. | "Mis entregas" deja de depender solo del celular (Fase 2B). |
| 4 | **El remitente ya ve el nombre de los viajeros:** `GET /api/viajes/disponibles?ciudadOrigen&ciudadDestino` (pública) → `nombreUsuario` + `uid` por ruta. | Mejor búsqueda de viajeros y nombre en el chat (Fase 2C). |
| 5 | El Swagger oficial apunta a **`lapticon-backend-ed.onrender.com`, que no existe** (404 en todo). Todas las rutas nuevas **sí están en nuestro servidor** (`lapticon-backend.onrender.com`). | No cambiar la URL de las apps. Preguntarle al profesor (§6). |
| 6 | `GET /api/chats/estado/{chatId}` ya **no da 500**: responde **404 "Chat no encontrado"** para nuestro par, y según el oficial devuelve `{ estado, fechaCierre }` con 200. | Falta saber qué `chatId` espera (Fase 0). La app ya trata el 404 como abierto. |
| 7 | El oficial **no incluye `entregada`** en los estados de encomienda (`disponible, tomada, vencida, recibida`), pero el servidor todavía la acepta. | Mantener `entregada` mientras el servidor la acepte. Preguntar (§6). |

### 1.1 Observaciones del profesor sobre la experiencia de usuario

| # | Lo que dijo | Diagnóstico en el código actual (igual en las dos apps) | Dónde se resuelve |
|---|---|---|---|
| P1 | **No queda claro si el viajero tomó la encomienda** | Ver el detalle abajo | Fase 2G |
| P2 | **"Verificar vuelo" no sirve; si no sirve, no se muestra** (Harold está de acuerdo) | El servidor responde siempre 500 (`RAPIDAPI_KEY` no configurada). La app igual muestra el botón "Verificar vuelo", el aviso "Verificación no disponible", el subtítulo "Lo verificamos con la aerolínea…" y la insignia **"Sin verificar"** en Mi viaje. Promete algo que no cumple y siembra desconfianza. | Fase 2H |

**Diagnóstico de P1:**
- `tomada` se muestra como **"En camino"** para los dos roles:
  - PWA: `src/datos/modelos/estado.ts`;
  - Flutter: `lib/data/models/estado.dart`.

  "En camino" suena a "ya viaja", no a "alguien aceptó llevarla", y no dice **quién**.
- El remitente **no recibe ningún aviso** cuando se la toman: solo cambia la insignia en la lista. Ya existe un aviso
  así para "por calificar", pero no para "te la tomaron".
- En el detalle del remitente, "Quién la lleva" va **al final**, debajo de "Qué envías", y sin nombre: el backend no lo
  da. El paso se llama solo "Tomada".
- El viajero, al tomarla, solo ve un *toast* que desaparece. El detalle muestra la misma insignia "En camino", y no
  hay nada arriba que diga **"Tú llevas esta encomienda"** ni qué sigue. El chat con el remitente aparece
  deshabilitado (ver 2B), lo que lo empeora.

## 2. Imprecisiones que teníamos, corregidas

| Tema | Lo que creíamos (docs/03, docs/api) | Lo que dice el oficial / el servidor hoy | Verificado |
|---|---|---|---|
| Cerrar/cancelar viaje | No existía (propuesta 🆕 `PUT /api/viajes/{id}/estado`) | **Existe:** `PATCH` (no PUT), estados `disponible, completado, cancelado` | ✅ ruta y validación |
| Estados de viaje | `disponible, completado` | `disponible, completado, cancelado, contactado` | 📄 solo el oficial |
| Encomiendas tomadas por mí | No existía (propuesta 🆕 `/api/encomiendas/viajero`) | `GET /api/encomiendas/buscar?origen&destino` → `{ disponibles, tomadas }`, **por ruta** | ✅ forma; `tomadas` venía vacío (falta probar con una `tomada`) |
| uid del remitente al viajero | Imposible | `buscar` y `disponibles2` traen `uid` | ✅ |
| Perfil público | No existía (propuesta 🆕 `/users/{uid}/publico`) | No existe, pero `GET /api/viajes/disponibles` da `nombreUsuario` del viajero | ✅ parcial |
| Mis encomiendas disponibles | Solo `GET /api/encomiendas` | También `GET /api/encomiendas/mis-encomiendas` → `{ disponibles }` | ✅ |
| Encomiendas vencidas | — | `GET /api/encomiendas/vencidas`: **las de todos** los usuarios, con `remitenteNombre` | ✅ (no sirve para la app) |
| Ciudades por país | — | `GET /api/ciudades/ciudades-por-pais?nombre=Colombia`: **con tildes** (`Bogotá`), distinto de `/ciudades` (`Bogota`) | ✅ |
| Perfil de usuario | `{ nombre, apellido, telefono, nacionalidad, email }` | Además `fechaNacimiento` (fecha) y `correo`. El `PUT` da **400** si se intenta cambiar `uid` o `email` | 📄 |
| Ver perfil ajeno | 403 | El oficial dice 403 o 404; el servidor sigue dando **403** también para uid inexistente | ✅ |
| Quién cambia el estado de una encomienda | "No valida roles" | Oficial: **solo remitente o viajero asignado** (403 a terceros) | 📄 falta probar con un tercero |
| Encomienda | Sin foto | Campo `fotoUrl` (siempre `null`; no hay endpoint para subirla) | ✅ |
| Estado del chat | 500 siempre | 404 "Chat no encontrado"; con 200 → `{ estado, fechaCierre }` | ✅ 404 |
| Vuelos | Ruta protegida | **Pública** (sin token); sigue con 500 por `RAPIDAPI_KEY` | ✅ 500 |
| IA de emparejamiento | — | `POST /api/encomiendas/emparejar-viajes` (OpenRouter) y `/evaluar-emparejamiento` (necesita `MATCHING_API_URL`) | ❓ sin probar |
| Tarea de vencidas | Se aplica al consultar | También `POST /api/encomiendas/actualizar-vencidas` (pública, para tarea programada) | 📄 (no la llama la app) |

## 3. Fases

### Fase 0 — Verificar lo que falta (con datos de prueba desechables, ~1 h)

Todo con las dos cuentas propias. Antes de cada escritura se crea un **dato nuevo solo para la prueba**; nunca se
tocan el viaje AV10 ni las encomiendas de la demo.

1. Crear un viaje de prueba (después de cerrar el actual o con una tercera cuenta) y hacer `PATCH … { estado: "cancelado" }`:
   - ¿qué responde?
   - ¿`GET /api/viajes/disponible` da 404 después?
   - ¿se puede registrar otro viaje?
   - Repetir con `completado`.
2. Remitente publica una encomienda de prueba → viajero la toma → `GET /api/encomiendas/buscar`. Comprobar:
   - ¿aparece en `tomadas`, con `uid`?
   - ¿sigue apareciendo después de `entregada` y de `recibida`?
3. ¿`buscar` o `disponibles2` excluyen las encomiendas propias? (Hay rastros de un arreglo de "self-deal" en el
   servidor.) Si sí, la app deja de cruzar listas.
4. `PUT /{id}/estado` desde una tercera cuenta → ¿403?
5. Estado del chat: probar el `chatId` actual (uids ordenados con `_`) frente a otras formas (id de la encomienda, orden
   inverso) para encontrar el que da 200.
6. `POST /api/encomiendas/emparejar-viajes`: ¿responde o da 500?
7. Guardar todas las respuestas en `referencias/respuestas/` (con teléfono y correo ocultos), como en docs/03.

#### Resultados de la Fase 0 (28-oct-2026) ✅

Con las dos cuentas propias y datos desechables (ruta **Cali → Lima**, valor USD 1). Respuestas en
`referencias/respuestas/fase0_*.json`.

| # | Pregunta | Resultado | Qué cambia en el plan |
|---|---|---|---|
| 1 | Cancelar viaje | `PATCH { estado: "cancelado" }` → **200** `{ message, viaje }`. Después, `GET /disponible` → 404 y `POST /api/viajes` → 201. Con `completado` pasa lo mismo. Acepta solo `disponible`, `completado` y `cancelado`: **`contactado` da 400**. Otro usuario → **404** "Viaje no encontrado o no autorizado". **Un viaje cancelado se puede volver a `disponible`.** | 2A se puede construir. La app no ofrece reactivar. `contactado` solo se muestra si llega. |
| 2 | `buscar` y `tomadas` | Al tomarla, sale en `tomadas` con `uid`, `viajeroId` y **`remitenteNombre`**. Con `entregada` o `recibida` **desaparece de las dos listas.** Tomar **no exige** que la ruta coincida con el viaje del viajero. | 2B: el nombre del remitente viene en `buscar`. "Mis entregas" = `tomadas` + lo guardado en el celular, que sigue haciendo falta para `entregada` y `recibida`. |
| 3 | ¿Excluyen las propias? | `buscar` **no** las excluye. `disponibles2` **sí** (las del remitente: `[]`). | 2B: mantener el filtro por `uid` (ya no hace falta cruzar con `GET /api/encomiendas`, porque `buscar` trae el `uid`). |
| 4 | Estado desde un tercero | `PUT /{id}/estado` desde una cuenta que no es remitente ni viajero asignado → **403** "No autorizado para modificar esta encomienda". | Ninguno. |
| 5 | `chatId` del estado del chat | **Uids ordenados con `_`** (el que ya usa la app) → **200 `{ estado: "activo", fechaCierre: null }`**. En orden inverso, o con el id de la encomienda → 404. Al **tomar** queda `activo`. Al marcar **`entregada`** pasa a **`cerrado`** con `fechaCierre`. **Tomar otra encomienda del mismo par lo reabre.** | 2E: tratar `cerrado` como bloqueado, y `activo`, 404 o 500 como abierto. El valor es `activo`, no `abierto`. El chat es por par, no por encomienda. |
| 6 | `emparejar-viajes` | El primer intento se quedó sin respuesta (más de 120 s). El segundo: **200** en 0,5 s → `[{ viajeId, uid, afinidad, ciudadOrigen, ciudadDestino, fechaViaje }]`. `evaluar-emparejamiento` → 500 "Error al consultar motor de emparejamiento". | 2F se puede construir (con tiempo de espera y sin bloquear la publicación). |
| 7 | Respuestas guardadas | 31 archivos `fase0_*.json`, con teléfono y correo ocultos. | — |

**Datos que quedaron en el servidor:**
- Encomiendas de prueba Cali → Lima: **A** `recibida`, **B** `entregada` y **C** `tomada` por el viajero. C deja abierto
  el chat del par de la demo, porque B lo había cerrado.
- Viaje de prueba **LA2401** Cali → Lima `completado` (cuenta remitente).
- El viaje **A777** Bogota → Medellin de la cuenta remitente se canceló y se dejó otra vez en `disponible`, como estaba.

### Fase 1 — Documentación (repo de documentación, ~2 h)

| Archivo | Cambio |
|---|---|
| `docs/api/openapi.yaml` | Partir del oficial y conservar nuestras marcas ✅/⚠️/🆕, roles y ejemplos reales. Mover a ✅ lo que ya existe y sacar de 🆕 cerrar viaje, encomiendas tomadas y uid del remitente. Dejar 🆕 solo lo que sigue faltando (§4). Corregir `servers`. |
| `docs/03-contrato-api.md` | Rehacer las tablas con §2; agregar `PATCH viajes`, `buscar`, `disponibles2`, `mis-encomiendas`, `vencidas`, `viajes/disponibles` y `ciudades-por-pais`. |
| `docs/entregables/00`, `06`, `09` | Actualizar hallazgos y limitaciones (ya no "imposible cancelar viaje" ni "no se sabe el remitente"), y las respuestas de la sustentación. |
| `CLAUDE.md` | Sección "Contrato del backend" al día. |
| `docs/06-riesgos-y-preguntas.md` | Marcar respondidas las preguntas que resuelve el oficial y agregar las de §6. |

### Fase 2 — Apps (el mismo cambio en Flutter y en la PWA)

Archivos base:
- PWA: `src/datos/repositorios/index.ts`, `src/datos/modelos/*`, `src/funciones/viajero|remitente/*`;
- Flutter: `lib/data/repositories/*`, `lib/data/models/*`, `lib/features/*`.

Mantener los mismos nombres y claves locales en las dos apps, como siempre.

**2A. Cancelar viaje (prioridad alta, ~3 h por app)**
- Repositorio: `viajes.cambiarEstado(id, 'cancelado' | 'completado')` con `PATCH`. Hay que revisar que el cliente HTTP
  de cada app soporte `PATCH`; hoy solo se usa GET/POST/PUT.
- "Mi viaje": botón **Cancelar viaje**, con confirmación escribiendo `CANCELAR` (mismo patrón que `ENTREGAR`). Si hay
  encomiendas tomadas sin entregar, avisar antes y no dejar continuar.
- Modelo `Viaje`: estados `cancelado` y `contactado`, con etiqueta, ícono y color, sin depender solo del color.
- Al cancelar: invalidar el viaje disponible y llevar a registrar uno nuevo.

**2B. Viajero: remitente conocido y "Mis entregas" desde el servidor (prioridad alta, ~4 h por app)**
- Explorar usa `GET /api/encomiendas/buscar` en lugar de `/disponibles`. Así cada encomienda trae el `uid` del
  remitente; `remitenteNombre` se completa con `/disponibles` o se muestra "Remitente".
- Detalle de la encomienda: se habilita **"Abrir chat con el remitente"** y calificarlo sin esperar a que escriba
  primero. Se quita el texto "Podrás escribirle cuando te escriba primero".
- "Mis entregas": mezclar `tomadas` del servidor con lo guardado en el celular. Lo local queda solo como respaldo para
  `entregada`/`recibida`, si la Fase 0 confirma que `tomadas` no las incluye.
- Si `buscar` ya excluye las propias, quitar el cruce con `GET /api/encomiendas`.

**2C. Remitente: viajeros con nombre (prioridad media, ~2 h por app)**
- Búsqueda de viajeros con `GET /api/viajes/disponibles?ciudadOrigen&ciudadDestino` (ruta completa + `nombreUsuario`)
  en lugar de `/viajes/buscar?ciudad`.
- Chat del remitente: tomar el nombre del viajero de esa lista cuando esté (hoy sale "Chat").

**2D. Perfil (prioridad media, ~2 h por app)**
- Campo opcional **fecha de nacimiento** (`fechaNacimiento`, `YYYY-MM-DD`), validando la mayoría de edad en la app.
- No mandar `uid`/`email` en el `PUT`, para no recibir el 400 nuevo. Hoy no se mandan, pero hay que cubrirlo con una
  prueba.
- `rol` sigue sin guardarse en el servidor: no cambia.

**2E. Robustez (prioridad media, ~1 h por app)**
- Modelos tolerantes a `fotoUrl` y a estados de viaje desconocidos (se muestran como texto, sin romper).
- Chat: leer `{ estado, fechaCierre }`. Con `cerrado`, bloquear la barra de escribir y mostrar la fecha. Con 404 o 500,
  sigue abierto.
- Vuelos: en `validarVuelo`, llamar sin token, que es pública. Solo lo usa `humo`: la interfaz ya no lo muestra (2H).
- **No** mezclar `ciudades-por-pais` (con tildes) con las ciudades de los formularios (sin tildes): los filtros
  comparan texto exacto. Solo se usaría para sugerir ciudades según la nacionalidad, normalizando a la lista de
  `/ciudades`.

**2G. Que quede claro que el viajero tomó la encomienda (observación P1, prioridad alta, ~4 h por app)**

Objetivo: los dos roles saben, sin dudar y en el primer vistazo, que la encomienda tiene viajero, quién es y qué sigue.
Depende de 2B y 2C para mostrar nombres; si no hay nombre, el texto genérico también cumple.

1. **Etiquetas según el rol.** `tomada` deja de decir "En camino":

   | Rol | Insignia (texto + ícono) | En listas e inicio |
   |---|---|---|
   | Remitente | **"Tomada"** + ícono de persona con maleta | "Tomada por {nombre}" o "Un viajero la tomó" |
   | Viajero | **"La llevas tú"** | "Por entregar" (ya existe en Mi viaje) |

   - Implementar como función `etiquetaEstado(estado, rol)`, en lugar de un mapa fijo:
     - PWA: `src/datos/modelos/estado.ts`, `src/core/componentes/Insignia.tsx`;
     - Flutter: `lib/data/models/estado.dart` y el widget de insignia.
   - Los demás estados no cambian.
   - En Inicio del remitente, la subtarjeta "En camino" pasa a **"Tomadas"**:
     - PWA: `InicioRemitente.tsx`, `remitente/logica.ts` (`enCamino`);
     - Flutter: `inicio_remitente_screen.dart`, `envios_logic.dart`.
2. **Aviso al remitente cuando se la toman.**
   - Al cargar Inicio y Envíos, comparar el estado de cada encomienda con el último visto, guardado en la clave local
     nueva `remitente_estados_vistos_{uid}` (mapa `id → estado`).
   - Si alguna pasó de `disponible` a `tomada`, mostrar arriba una tarjeta destacada con el mismo patrón de los avisos
     "por calificar":
     - texto: **"¡{nombre} tomó tu encomienda {origen} → {destino}!"** (sin nombre: "Un viajero tomó…");
     - botones **"Escribirle"** (abre el chat) y **"Ver envío"**.
   - Se marca como vista al abrir el detalle o al tocar "Entendido".
   - En la pestaña Envíos, contador "1 nueva" junto al de "por calificar":
     - PWA: `src/app/estructura.tsx`;
     - Flutter: el equivalente en la barra de navegación.
3. **Detalle del remitente.**
   - PWA: `remitente/DetalleEnvio.tsx`; Flutter: `encomienda_detalle_screen.dart`.
   - Con `tomada`:
     - va **justo debajo del ticket** un bloque "**Quién la lleva**" con nombre, calificación (`FilaConfianza` /
       `trust_row.dart`) y botón **"Escribirle"**;
     - el bloque se quita del final;
     - el pie del grupo Estado dice: "**{nombre} aceptó llevarla.** Coordinen por chat dónde y cuándo se la entregas.";
     - en la línea de tiempo, el paso 2 se llama **"Tomada por un viajero"** (`PASOS_ENCOMIENDA` / `pasosEncomienda`).
4. **Detalle del viajero.**
   - PWA: `viajero/EncomiendaViajero.tsx`; Flutter: `encomienda_viajero_screen.dart`.
   - Si `mia && tomada`, arriba del ticket va un aviso fijo de éxito (no un *toast*):
     - título: **"Tú llevas esta encomienda"**;
     - pasos numerados: "1. Escríbele a {remitente} para recibir el paquete · 2. Llévalo en tu viaje {vuelo} · 3. Al
       entregarlo, márcala como entregada".
   - Después de tomarla, la pantalla se queda en el detalle mostrando ese aviso, y se mantiene el *toast*.
   - El botón principal pasa a **"Escribir al remitente"** (habilitado gracias a 2B). "Marcar como entregada" queda
     como segundo botón, porque entregar es lo último.
5. **Explorar del viajero.** Las que tomé salen en una sección propia **"Las que llevas"**, arriba de las disponibles,
   con la insignia "La llevas tú". Hoy van mezcladas y ordenadas por estado (`viajero/logica.ts` → orden).
6. **Pruebas.**
   - Unitarias:
     - `etiquetaEstado` por rol;
     - detección de "nueva tomada" con la clave local (primera vez sin mapa = no avisa todo de golpe; disponible →
       tomada = avisa; ya vista = no avisa).
   - E2E PWA: el viajero toma → el remitente entra y ve el aviso y "Tomada"; el viajero ve "Tú llevas esta encomienda".
   - Flutter: pruebas de widget de los dos detalles y del aviso.
7. **Criterio de aceptación**
   - En la PWA no queda ningún "En camino" para `tomada` (`grep -rn "En camino" src` sin resultados de estado), y en
     Flutter tampoco.
   - Con la cuenta remitente, al entrar después de que el viajero tomó una encomienda, se ve el aviso con su nombre sin
     tocar nada.

**2H. Quitar "Verificar vuelo" de la interfaz (observación P2, prioridad alta, ~2 h por app)**

Objetivo: el viajero registra su viaje con número de vuelo, ruta y fecha, sin ninguna mención de verificación. El
número de vuelo **se sigue pidiendo y mostrando**: le sirve al remitente.

| Qué quitar | PWA (`aplicacion_pwa/`) | Flutter (`lapticon_app/`) |
|---|---|---|
| Botón "Verificar vuelo", estados `Verificacion`, avisos "Verificación no disponible", "No encontramos ese vuelo" y "quedará sin verificar"; subtítulo "Lo verificamos con la aerolínea…" (cambiar por "Los remitentes de tu ruta verán tu vuelo y fecha.") | `src/funciones/viajero/RegistrarViaje.tsx` | `lib/features/viajero/registrar_viaje_screen.dart` (`_Verificacion`, `_verificar`, `_errorVerificar`) |
| Insignia "Vuelo verificado" / "Sin verificar" en Mi viaje (dejar la tarjeta sin insignia o con "Disponible") | `src/funciones/viajero/MiViaje.tsx` | `lib/features/viajero/mi_viaje_screen.dart` |
| Memoria local de vuelos verificados (`viajero_vuelos_verificados_{uid}`) y su clave | `src/datos/local.ts` (`vueloVerificado`, `marcarVueloVerificado`), `src/funciones/viajero/logica.ts` (`claveVuelo`) | `viajero_local_store.dart`, `viajero_logic.dart` |
| Widget de insignia exclusivo | — | `VueloVerificadoBadge` en `widgets/viajero_widgets.dart` |
| Pruebas que lo cubren | `pruebas/e2e/flujos.spec.ts` (líneas ~106 y ~186–202: "Sin verificar", "Verificar vuelo") | `test/viajero/viajero_v2_test.dart` (~264–303), `test/home/inicio_test.dart` (~300–309), `test/viajero/viajero_widgets_test.dart` (~80) |

**Qué se conserva**

- `viajes.validarVuelo` en el repositorio, con un comentario: *"No se usa en la interfaz mientras el servidor responda
  500 (`RAPIDAPI_KEY`); ver docs/11 §2H"*.
- La comprobación `8 verificar vuelo` de `pruebas/humo.mjs`: si algún día responde 200, se sabrá y se podrá volver a
  mostrar.
- `EtiquetaVidrio`, que es genérica y se usa en otros lugares.

**Pruebas nuevas**

- Registrar viaje no muestra ningún texto con "verific".
- Mi viaje no muestra "Sin verificar".

**Criterio de aceptación:** las dos búsquedas siguientes no encuentran ningún texto visible al usuario.

```bash
grep -rni "verific" aplicacion_pwa/src/funciones/viajero
```

```bash
grep -rni "verific" lapticon_app/lib/features/viajero
```

Puede quedar en comentarios.

**Documentos a actualizar en el mismo paso**

- `docs/entregables/07-video-2-minutos.md`: el guion de 0:45 dice "Mi viaje (vuelo, 'Sin verificar')".
- `docs/entregables/09-sustentacion.md`: la pregunta de servicios externos. Ahora se responde: "lo quitamos de la
  interfaz porque el servidor no tiene la clave; lo dejamos listo en el repositorio".
- `docs/entregables/06-documento-tecnico.md`: requisito de verificación de vuelo → "retirado de la interfaz".
- `docs/entregables/02-sem2-registro-viajes.md`.
- `docs/entregables/05-ux-ui.md`.
- `docs/07-diseno-ux-ui.md`.
- `docs/03-contrato-api.md`.

**2F. Opcional — sugerencias de IA (prioridad baja)**
- Si `emparejar-viajes` responde en la Fase 0: al publicar una encomienda, mostrar "Viajeros sugeridos". Si da 500, se
  deja documentado y no se construye.

### Fase 3 — Pruebas (cada app)

- **Pruebas de contrato** con las respuestas nuevas de la Fase 0:
  - `buscar` (`{ disponibles, tomadas }`);
  - `PATCH viajes`;
  - `viajes/disponibles`;
  - chat `{ estado, fechaCierre }`;
  - `fechaNacimiento`;
  - estados `cancelado`/`contactado`.
- **PWA:**
  - `pruebas/e2e/api-falsa.ts` con las rutas nuevas;
  - E2E de "cancelar viaje" y de "viajero escribe primero";
  - `npm run humo` con las rutas nuevas de solo lectura.
- **Flutter:** pruebas de widget del botón cancelar y del chat habilitado.
- **Criterio de listo:** typecheck, lint, unitarias, E2E y `flutter analyze`/`test` en verde, con el CI verde en los
  dos repos.

### Fase 4 — Cancelar encomienda (⏸ bloqueada: esperando al profesor)

- Hoy el oficial **no tiene** `cancelada` ni un `DELETE`; retirar sigue siendo `PUT /{id}/estado` → `vencida`.
- Lo que hay que preparar sin construir:
  - en los dos modelos, un `cancelada` tolerante;
  - el botón "Retirar" ya existente, aislado detrás de una sola función del repositorio, para cambiar solo el endpoint
    cuando exista.
- Cuando el profesor lo publique:
  1. verificarlo (Fase 0);
  2. cambiar esa función;
  3. etiqueta "Cancelada" distinta de "Vencida";
  4. pruebas;
  5. docs.
- Estimado: ~2 h por app.

## 4. Lo que sigue faltando en el backend (queda como 🆕 en nuestro Swagger)

| Falta | Motivo |
|---|---|
| Cancelar encomienda (`cancelada` o `DELETE`) | Retirar hoy se confunde con vencer. **Pedido al profesor.** |
| Guardar el rol | El `PUT /users` no acepta `rol`; sigue por dispositivo |
| Perfil público (nombre del viajero que tomó *mi* encomienda) | `viajes/disponibles` solo lo da mientras su viaje esté disponible |
| Detalle de una encomienda por id | Sigue sin existir |
| Calificaciones pendientes por encomienda | `encomiendaId` sigue sin guardarse |
| Notificaciones push | No existe |

## 5. Orden propuesto

| Paso | Qué | Depende de | Tiempo aprox. | Estado |
|---|---|---|---|---|
| 1 | **2H Quitar "Verificar vuelo"** (observación del profesor; no depende del servidor) | — | 4 h | ✅ PWA `5c07e21` · Flutter `1854e3b` |
| 2 | Fase 0 (verificación con datos desechables) | — | 1 h | ✅ (ver resultados) |
| 3 | Fase 1 (docs + Swagger propio) | Paso 2 | 2 h | ✅ |
| 4 | 2A Cancelar viaje (Flutter y PWA) | Paso 2 | 6 h | ✅ PWA `a5a30e2` · Flutter `7fb4c48` |
| 5 | 2B Viajero con remitente conocido | Paso 2 | 8 h | ✅ PWA `8562341` · Flutter `cdf1f46` |
| 6 | **2G Que quede claro que la tomaron** (observación del profesor) | Paso 5 (nombres; sin ellos funciona con texto genérico) | 8 h | ⬜ |
| 7 | 2C, 2D, 2E | Paso 2 | 10 h | ⬜ |
| 8 | Fase 3 en cada paso (no al final) | — | incluido | — |
| 9 | 2F IA (si responde) | Paso 2 | 3 h | ⬜ |
| ⏸ | Fase 4 Cancelar encomienda | El profesor | 4 h | ⏸ |

Leyenda: ⬜ pendiente · 🔄 en curso · ✅ hecho (con hash del commit en cada repo) · ⏸ bloqueado.

Commits pequeños por paso y por repo (`feat:`, `fix:`, `test:`, `docs:`).

**Despliegue:** push al repo de la PWA = producción en lapticon.haroldsoftware.com, así que solo se sube con tu OK.
**Flutter:** nueva Release con el APK.

## 6. Preguntas para el profesor

1. El Swagger dice `lapticon-backend-ed.onrender.com`, pero ese servidor no existe y las rutas están en
   `lapticon-backend.onrender.com`. ¿Cuál debemos usar para la entrega?
2. **¿Cuándo estará cancelar encomienda?** ¿Será el estado `cancelada` o un `DELETE`?
3. El enum oficial de encomienda no tiene `entregada`, pero el servidor la acepta. ¿El flujo correcto es
   `tomada → entregada → recibida` o `tomada → recibida`?
4. ~~`GET /api/chats/estado/{chatId}`: ¿qué `chatId` espera el backend?~~ Respondida en la Fase 0 (uids ordenados).
   Nueva: el chat se cierra al marcar `entregada`, antes de calificar. ¿Es intencional?
5. Viaje `contactado`: ¿quién lo pone y cuándo?
6. `GET /api/encomiendas/vencidas` devuelve las de todos los usuarios. ¿Es intencional?
7. ¿Hay endpoint para subir la foto (`fotoUrl`)?
8. Un viaje `cancelado` se puede volver a `disponible`. ¿Debería impedirse?

Copiadas en `docs/06` como P13–P20.
