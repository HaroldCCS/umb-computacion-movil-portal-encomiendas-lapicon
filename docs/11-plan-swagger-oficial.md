# 11. Plan de trabajo: ajustar todo al Swagger oficial del profesor

> **Estado:** plan, sin desarrollar (28-oct-2026).
>
> **Fuentes:**
> - el Swagger oficial: https://lapticon-backend.onrender.com/api-docs/ (copia en `referencias/swagger-oficial.json`);
> - una verificación contra el servidor real el 28-oct-2026, con las dos cuentas propias. Solo hubo lecturas y
>   peticiones que no cambian nada: id inexistente o estado inválido.
>
> **Bloqueado:** **cancelar encomienda.** Esperamos que el profesor la agregue (§5).

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
- Vuelos: llamar sin token, que es pública.
- **No** mezclar `ciudades-por-pais` (con tildes) con las ciudades de los formularios (sin tildes): los filtros
  comparan texto exacto. Solo se usaría para sugerir ciudades según la nacionalidad, normalizando a la lista de
  `/ciudades`.

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

| Paso | Qué | Depende de | Tiempo aprox. |
|---|---|---|---|
| 1 | Fase 0 (verificación) | — | 1 h |
| 2 | Fase 1 (docs + Swagger propio) | Paso 1 | 2 h |
| 3 | 2A Cancelar viaje (Flutter y PWA) | Paso 1 | 6 h |
| 4 | 2B Viajero con remitente conocido | Paso 1 | 8 h |
| 5 | 2C, 2D, 2E | Paso 1 | 10 h |
| 6 | Fase 3 en cada paso (no al final) | — | incluido |
| 7 | 2F IA (si responde) | Paso 1 | 3 h |
| ⏸ | Fase 4 Cancelar encomienda | El profesor | 4 h |

Commits pequeños por paso y por repo (`feat:`, `fix:`, `test:`, `docs:`).

**Despliegue:** push al repo de la PWA = producción en lapticon.haroldsoftware.com, así que solo se sube con tu OK.
**Flutter:** nueva Release con el APK.

## 6. Preguntas para el profesor

1. El Swagger dice `lapticon-backend-ed.onrender.com`, pero ese servidor no existe y las rutas están en
   `lapticon-backend.onrender.com`. ¿Cuál debemos usar para la entrega?
2. **¿Cuándo estará cancelar encomienda?** ¿Será el estado `cancelada` o un `DELETE`?
3. El enum oficial de encomienda no tiene `entregada`, pero el servidor la acepta. ¿El flujo correcto es
   `tomada → entregada → recibida` o `tomada → recibida`?
4. `GET /api/chats/estado/{chatId}`: ¿qué `chatId` espera el backend y quién crea ese documento?
5. Viaje `contactado`: ¿quién lo pone y cuándo?
6. `GET /api/encomiendas/vencidas` devuelve las de todos los usuarios. ¿Es intencional?
7. ¿Hay endpoint para subir la foto (`fotoUrl`)?
