# 10. Plan de migración — Lapticon como PWA

> **Estado: plan, sin código todavía.** La app Flutter (`lapticon_app/`) **no se toca**: la PWA vive aparte en
> `aplicacion_pwa/` y comparte el mismo backend, el mismo proyecto de Firebase y los mismos datos.
> Base de diseño: el sistema v2 (`docs/07`), las lecciones del rediseño (`docs/09`, §8 "Llevarlo a una PWA") y la
> guía de *Cuentas Claras*. Contrato de la API: `docs/03`.

## 10.1 Objetivo y criterios de "terminado"

Una PWA que haga **todo lo que hace la app Flutter**, con el **mismo diseño v2**, pensada primero para el celular
(iPhone Safari y Android Chrome, instalada en la pantalla de inicio), consumiendo **todos los endpoints** del backend.

Se considera terminada cuando:

1. Cada pantalla y flujo del inventario (§10.6) funciona en un celular real, instalada como app.
2. Cada endpoint de la matriz (§10.5) se llama desde la PWA y su respuesta (o su error conocido) se maneja como en Flutter.
3. Un chat abierto desde la PWA se ve en la app Flutter y al revés (mismo esquema de Firestore).
4. Lighthouse móvil: PWA instalable, Accesibilidad ≥ 95, Rendimiento ≥ 85, Buenas prácticas ≥ 95.
5. Pruebas en verde: unidad, componentes, accesibilidad (claro/oscuro, texto al 200 % en 360 px) y E2E en
   viewports de iPhone y Android.
6. Desplegada en una URL HTTPS pública, con la API funcionando desde esa URL.

## 10.2 Hallazgos que condicionan el plan (verificados el 24-oct-2026)

| Hallazgo | Cómo se comprobó | Consecuencia |
|---|---|---|
| **El backend tiene CORS con lista blanca y solo permite `http://localhost:5500` y `http://127.0.0.1:5500`** | Peticiones con `Origin:` de 20 orígenes; solo esos dos reciben `Access-Control-Allow-Origin` | Una PWA en cualquier dominio público **no puede llamar a la API desde el navegador**. Hace falta un **proxy en el mismo dominio** (§10.4) o que el profesor agregue el origen |
| La clave de Firebase (`google-services.json`) funciona desde la web, desde cualquier origen | `accounts:createAuthUri` con `Origin` de localhost y de un dominio público → respuesta válida | Firebase Auth y Firestore con el **mismo proyecto** `lapticon-eba31`, sin registrar nada nuevo |
| No hay app web registrada en Firebase (solo dos apps Android) | `google-services.json` y `firebase_options.dart` | Se inicializa con `apiKey`, `authDomain`, `projectId` (Auth y Firestore no exigen `appId` web). Registrar una app web es opcional |
| El chat va directo a Firestore con un esquema propio | `lib/features/chat/chat_service.dart` | La PWA debe leer y escribir **exactamente** `chats/{uidA_uidB}` y `mensajes/{autoId}` (§10.7.6) |
| Tres endpoints fallan en el servidor (no en la app) | `docs/03` | `/api/vuelos` → 500, `/api/chats/estado` → 500, `/api/chatbot` → 500. La PWA los llama y los trata igual que Flutter; no puede hacerlos funcionar |
| El backend gratuito de Render tarda hasta ~60 s en despertar | `docs/03`, pruebas | Tiempo de espera de 75 s, aviso "Despertando el servidor…", y el proxy no debe cortar antes |
| *Cuentas Claras* ya resolvió lo mismo | `prestamo-frontend`: Cloudflare Pages + `functions/api/[[ruta]].js` + service worker propio | Se reutiliza ese patrón probado (stack, proxy, SW, cabeceras) |

## 10.3 Arquitectura y stack

Mismo stack que *Cuentas Claras* (ya probado por Harold en producción como PWA):

| Capa | Elección | Por qué |
|---|---|---|
| Lenguaje y build | **TypeScript + Vite** | Tipos como en Dart; build rápido y code-splitting |
| UI | **React 19** | Igual que Cuentas Claras |
| Rutas | **React Router 7** | URLs reales: botón atrás del sistema, deep links (`?accion=`), recargar sin perder la pantalla |
| Datos del servidor | **TanStack Query 5** | Equivale a los `FutureProvider` + `invalidate` de Riverpod: caché, reintento, refrescar al volver a la app |
| Estado local | Hooks + contextos pequeños (sesión, pestaña, avisos) | Lo mínimo; nada de Redux |
| Estilos | **CSS con variables (tokens v2) + Tailwind 3** mapeado a esas variables | Los tokens viven en un solo archivo, con claro/oscuro, como `tema.dart` |
| Validación de respuestas | Lectores tolerantes propios (como los `fromJson` de Dart) | El backend devuelve formas variables; mismas reglas que Flutter |
| Firebase | SDK web **modular** (`firebase/auth`, `firebase/firestore`) | Mismo proyecto; Firestore se carga solo en las rutas de chat |
| Pruebas | **Vitest** + Testing Library + `vitest-axe`; **Playwright** (iPhone 13, Pixel 7) | Unidad, componentes, accesibilidad y E2E en móvil |
| PWA | Manifest + **service worker propio sin dependencias** (plantilla de Cuentas Claras) | Control total del caché; la API nunca se cachea |
| Hosting | **Cloudflare Pages** (`lapticon-pwa.pages.dev`) | Decisión §10.14. La API se llama **directo** cuando el profesor agregue el origen al CORS; mientras tanto, plan B con una Pages Function como proxy de `/api/*` (§10.4) |

### Estructura de carpetas

```text
aplicacion_pwa/
├── index.html                  meta de iOS/Android, viewport-fit=cover, theme-color claro/oscuro
├── public/                     manifest.webmanifest, íconos (192, 512, maskable, apple-touch), _headers, _redirects
├── functions/api/[[ruta]].js   plan B: proxy de Cloudflare Pages → https://lapticon-backend.onrender.com/api/*
├── src/
│   ├── main.tsx / App.tsx      proveedores (Query, sesión, avisos), rutas
│   ├── core/
│   │   ├── tema/               tokens.css (claro/oscuro), medidas, movimiento, vocabulario.ts
│   │   ├── red/                cliente API (Bearer, 401→reintento, 75 s, aviso de servidor lento), errores
│   │   ├── firebase.ts         init + auth + firestore (perezoso)
│   │   ├── rutas.ts            rutas, AccionPendiente (?accion=), redirectFor()
│   │   ├── formato.ts          Fmt (fechas, dinero, relativo, hora)
│   │   ├── validadores.ts      Validators de Dart, mismos mensajes
│   │   └── componentes/        sistema v2 (§10.8)
│   ├── datos/
│   │   ├── modelos/            Usuario, Rol, Viaje, Encomienda, Estados, Calificación, Conversación, Mensaje
│   │   ├── repositorios/       usuarios, viajes, encomiendas, calificaciones, ciudades, chats, chatbot
│   │   └── local.ts            localStorage con las mismas claves que Flutter (§10.7.5)
│   ├── funciones/              sesion, auth, onboarding, inicio, remitente, viajero, chat, calificaciones, perfil, asistente
│   └── pwa/                    sw.js (plantilla), registro.ts (actualizar), instalar.ts (Android/iOS)
├── pruebas/e2e/                Playwright (móvil)
└── README.md
```

Regla igual que en Flutter: **las pantallas nunca llaman a `fetch` ni a Firebase directo**, solo a repositorios y hooks.

## 10.4 La API desde el navegador (CORS)

**Decisión (24-oct-2026): pedir al profesor que agregue el origen de la PWA a la lista blanca de CORS** (pregunta
P12 en `docs/06`). El cliente toma la URL de la API de una variable de build, `VITE_API_URL`, y funciona en tres modos:

| Modo | `VITE_API_URL` | Cuándo |
|---|---|---|
| **Directo** (objetivo) | `https://lapticon-backend.onrender.com` | Producción en `https://lapticon-pwa.pages.dev` **cuando el profesor agregue ese origen**. También en desarrollo con Vite en el puerto **5500**, que ya está en la lista blanca |
| **Proxy de desarrollo** | vacío (mismo origen) | Probar desde el celular en la red local (`http://192.168.x.x:5500` no está en la lista): el `server.proxy` de Vite reenvía `/api` a Render |
| **Plan B: proxy en Cloudflare** | vacío (mismo origen) | Mientras el profesor no responda, o si dice que no, y en las vistas previas por rama (`<rama>.lapticon-pwa.pages.dev`, que nunca estarán en la lista) |

```text
Directo:   Celular ──► https://lapticon-backend.onrender.com/api/…   (requiere el origen en la lista CORS)
Plan B:    Celular ──► https://lapticon-pwa.pages.dev/api/…  ──Pages Function──►  Render  (mismo origen: sin CORS)
```

- La Pages Function (`functions/api/[[ruta]].js`, patrón de *Cuentas Claras*) reenvía método, ruta, query, cuerpo y
  `Authorization`, sin caché. Cloudflare no cuenta como CPU el tiempo esperando al backend: aguanta los ~60 s del
  arranque en frío. Se incluye desde la fase 0 aunque el modo objetivo sea el directo: pasar de uno a otro es
  cambiar la variable y volver a desplegar.
- **Cómo se verifica que el profesor lo agregó:** `curl -I -H "Origin: https://lapticon-pwa.pages.dev"
  https://lapticon-backend.onrender.com/api/ciudades/paises` debe traer `Access-Control-Allow-Origin`.

## 10.5 Matriz de endpoints (todos)

| # | Endpoint | Pantalla / momento | Estado del servidor | Cómo lo maneja la PWA |
|---|---|---|---|---|
| 1 | `POST /api/users/register` | Completar perfil | ✅ | Crea o actualiza; error junto al botón |
| 2 | `GET /api/users/{uid}` | Arranque de sesión, Perfil | ✅ | 404/403 → "sin perfil" → Completar perfil |
| 3 | `PUT /api/users/{uid}` | Editar perfil | ✅ | Toast "Perfil actualizado" |
| 4 | `POST /api/viajes` | Registrar viaje | ✅ / 400 si ya hay uno | 400 → hoja "Ya tienes un viaje activo · Ver mi viaje" |
| 5 | `GET /api/viajes` | Historial de viajes | ✅ | Lista agrupada; no se muestra si está vacía |
| 6 | `GET /api/viajes/disponible` | Mi viaje, Explorar, "+" | ✅ / 404 sin viaje | 404 → "sin viaje activo" (no es error) |
| 7 | `GET /api/viajes/buscar?ciudad=` | Buscar viajeros | ✅ | Viajero + calificación + pase |
| 8 | `GET /api/vuelos/{numero}/{fecha}` | Registrar viaje → Verificar | ⚠️ 500 | "Verificación no disponible… aparecerá como *sin verificar*" |
| 9 | `POST /api/encomiendas` | Nueva encomienda | ✅ (no valida body) | Validación completa antes de enviar |
| 10 | `GET /api/encomiendas` | Inicio, Envíos, filtro de propias | ✅ | Agrupado por estado; contadores |
| 11 | `GET /api/encomiendas/disponibles?origen=&destino=` | Explorar | ✅ | Excluye las propias cruzando con #10 |
| 12 | `PUT /api/encomiendas/tomar/{id}` | Tomar (viajero) | ✅ / 400 | Hoja de responsabilidad; 400 → error junto a la acción |
| 13 | `PUT /api/encomiendas/{id}/estado` | Retirar (vencida), Entregar | ✅ / 400 / 403 | Escribir RETIRAR / ENTREGAR |
| 14 | `POST /api/ratings` | Calificar | ✅ (500 si inválida) | Solo 1–5 y con destino; recuerda "calificada" localmente |
| 15 | `GET /api/ratings/{uid}` (pública) | Perfil, filas de confianza, Reseñas | ✅ | Promedio, barras por estrella |
| 16 | `GET /api/chats/estado/{chatId}` | Chat (antes de enviar) | ⚠️ 500 | 500/404 → chat abierto (igual que Flutter) |
| 17 | `GET /api/ciudades/paises` | Completar/editar perfil | ✅ | Caché local 7 días |
| 18 | `GET /api/ciudades/ciudades` | Origen/destino en formularios | ✅ | Caché local 7 días; nombres exactos ("Bogota") |
| 19 | `POST /api/chatbot` | Asistente | ⚠️ 500 | Error en la burbuja con "Reintentar" |
| — | Firestore `chats/…` | Chats y chat | ✅ (reglas por confirmar) | Tiempo real con `onSnapshot`; mismo esquema que Flutter |
| — | Firebase Auth | Login, registro, recuperar, token | ✅ | `getIdToken()` para el Bearer; renovar ante 401 |

**Verificación de la matriz:** un script `npm run humo` (§10.11) recorre los 19 endpoints **a través del proxy desplegado**
con un token de prueba de Harold (el que deja `lapticon_app/tool/obtener_token.sh` fuera del repo), en modo solo
lectura por defecto y con escrituras opcionales sobre las cuentas propias.

## 10.6 Inventario de pantallas y rutas

Cada pantalla de Flutter tiene su ruta web. Las pestañas pasan a ser rutas (el botón atrás y los enlaces funcionan).

| Flutter | Ruta PWA | Notas de migración |
|---|---|---|
| Splash / sesión | `/` | Decide con `redirectFor(estado, ruta)` (misma regla que `app_router.dart`) |
| Login · Registro · Recuperar | `/login` · `/registro` · `/recuperar` | Errores de Firebase traducidos (mismos textos) |
| Completar perfil · Elegir rol | `/completar-perfil` · `/elegir-rol` | Paso 1 y 2 de 2; país en hoja |
| Inicio (remitente) | `/inicio` | Encabezado, tarjeta Medianoche, avisos, Vista rápida |
| Envíos | `/envios?pestana=entregadas` | El chip va en la URL (Inicio puede abrir uno concreto) |
| Nueva encomienda | `/remitente/nueva` | Hoja de ciudad, `CampoMonto`, chips de moneda, vista previa |
| Detalle (remitente) | `/remitente/encomienda/:id?accion=calificar` | Ver "detalles con id" abajo |
| Buscar viajeros | `/remitente/viajeros` | |
| Mi viaje · Explorar | `/mi-viaje` · `/explorar` | Pestañas del viajero |
| Registrar viaje | `/viajero/registrar` | Fecha con selector nativo en hoja |
| Encomienda (viajero) | `/viajero/encomienda/:id?accion=entregar` | Ver "detalles con id" |
| Chats · Chat | `/chats` · `/chat/:otroUid` | El chatId sale de los dos uids |
| Calificar · Reseñas | `/calificar` · `/resenas/:uid` | |
| Perfil · Editar perfil | `/perfil` · `/perfil/editar` | |
| Asistente | `/asistente` | |

**Detalles con id (diferencia con Flutter):** Flutter pasa la encomienda completa al navegar; en la web la pantalla
debe poder abrirse **recargando o desde un enlace**, y el backend **no tiene `GET /encomiendas/{id}`**. Solución: el
detalle usa el objeto que llega por `state` de navegación; si no llega, lo busca en la caché de TanStack Query y,
si tampoco está, en `GET /api/encomiendas` (remitente) o en "mis entregas" + disponibles de mi ruta (viajero). Si no
aparece: estado vacío "No encontramos esta encomienda" con vuelta atrás.

## 10.7 Lógica a portar (mismo comportamiento que Flutter)

Se porta **con sus pruebas**: cada prueba de Dart tiene su equivalente en Vitest.

1. **Sesión** (`session_controller.dart`): estados `cargando · sinSesion · sinPerfil · sinRol · listo · error`, la
   máquina de transiciones y `redirectFor()` (prueba de cada combinación).
2. **Cliente API** (`api_client.dart`): Bearer con `getIdToken()`, rutas públicas sin token, ante 401 renovar el token
   y reintentar una vez, tiempo de espera 75 s, aviso "despertando" a los 5 s, errores `{ error }` con
   `message | mensaje | error` y mensajes por defecto por código (400/401/403/404/5xx), error de red sin internet.
3. **Modelos tolerantes** (`fromJson`): las mismas llaves alternativas (`_id`/`id`, `uid`/`viajeroId`, objetos
   envueltos o directos, fechas en `timestamp`). **Las pruebas usan las respuestas reales de
   `referencias/respuestas/`** — las mismas que usa `contrato_test.dart`.
4. **Lógica pura**: `agruparEnvios`, `ResumenEnvios` (+ nota), `pasoActual`, `parseValor`/`validarValor` (enteros),
   `validarObservaciones`, `validarRuta`, `normalizarVuelo`, `validarNumeroVuelo`, `combinarEntregas`,
   `paraTomar`, `tomadaPorMi`, `porEntregar`, `porCalificarViajero`, `gananciasPorMoneda`, `ordenarDisponibles`,
   `resumenVuelo`, `agruparPorDia`, `etiquetaDia`, `inicialesDe`, `Conversacion.ordenar`, `distribucion`,
   `sugerenciasPara`, `componerComentario`, `etiquetaPuntaje`, `Fmt.*`, `Validators.*`, `Vocabulario`.
5. **Almacenamiento local** con **las mismas claves** que Flutter, en `localStorage`:
   `rol_{uid}`, `calificadas_{uid}`, `viajero_entregas_{uid}`, `viajero_vuelos_verificados_{uid}`,
   `cache_paises` / `cache_ciudades` (+ `_at`, 7 días). Todo con try/catch: en modo privado puede fallar.
   *Nota:* el teléfono y el navegador no comparten este almacenamiento; el rol y lo "calificado" se recuerdan por
   dispositivo, igual que en Flutter.
6. **Chat en Firestore**, idéntico a `chat_service.dart`:
   - `chatId = [uidA, uidB].sort().join('_')`.
   - Resumen `chats/{chatId}` (merge): `participantes` (ordenados), `nombres{uid: nombre}`, `encomiendaId`, `ruta`,
     `ultimoMensaje`, `ultimoEmisorUid`, `actualizadoEn: serverTimestamp()`.
   - Mensaje `chats/{chatId}/mensajes/{autoId}`: `texto`, `emisorUid`, `creadoEn: serverTimestamp()`,
     `creadoLocal: Date.now()`. Envío en **un batch** (resumen + mensaje).
   - Mensajes con `onSnapshot(includeMetadataChanges)` ordenados en el cliente; "Enviando…" con `hasPendingWrites`.
   - Conversaciones: `where('participantes', 'array-contains', uid)`, orden en el cliente (sin índice compuesto).
   - Antes de enviar consulta `/api/chats/estado` (hoy 500 → abierto). Errores de Firestore traducidos.
7. **Asistente** (`asistente_controller.dart`): historial, escribiendo, error con reintento, reiniciar, sugerencias
   por rol.

## 10.8 Sistema de diseño en web (aplicando el v2)

Los **mismos tokens, componentes y reglas** de `docs/07`, traducidos con la tabla de `docs/09 §8`:

### Tokens
- `src/core/tema/tokens.css`: las variables de `Colores` (`--fondo`, `--superficie`, `--texto2`, `--marca-solido`,
  `--exito-suave`…) en `:root` y en `@media (prefers-color-scheme: dark)`; `Degradados`, `Pastel`, `TonosVidrio`.
- `Medidas` y `Movimiento` como variables (`--radio-tarjeta: 24px`, `--entrada: cubic-bezier(.22,1,.36,1)`…).
- Tailwind configurado **solo con esos tokens** (sin colores sueltos); una prueba busca `#` hexadecimales fuera de
  `tokens.css`.
- Tipografía: fuente del sistema (`-apple-system, Roboto…`) + **Space Grotesk autoalojada** (sin Google Fonts:
  CSP `'self'` y funciona sin conexión) solo en ciudades y cifras grandes. `font-variant-numeric: tabular-nums`.

### Componentes (mismos nombres que en Flutter, para poder seguirlos)
`Pantalla` (título grande que se compacta con `IntersectionObserver`, jalar para actualizar, pie fijo) ·
`BarraPestanas` (fija, `backdrop-filter`, `env(safe-area-inset-bottom)`, contadores) · `EncabezadoApp` ·
`TarjetaHero` / `SubTarjetaVidrio` / `EtiquetaVidrio` · `Mosaico` / `GrillaMosaicos` · `RouteTicket` (muescas con
máscara CSS) · `Tarjeta` · `Grupo` / `Fila` / `FilaAccion` / `TarjetaAccion` · `Boton` / `BotonIcono` / `Enlace` ·
`Campo` / `CampoContrasena` / `CampoMonto` · `Chips` / `ChipsMultiples` · `Insignia` · `Avatar` · `IconoEnCaja` ·
`Progreso` · `Monto` · `Aviso` / `Vacio` / `ErrorCarga` / `AvisoServidor` · `Esqueleto` · `Entrada` ·
`mostrarToast` (región `aria-live`) · `Hoja` / `confirmarConHoja` (`<dialog>` abajo, foco atrapado, Esc, arrastrar
para cerrar) · `ConfirmacionEscrita` · `AccionResaltada` (`scrollIntoView` + foco) · `Presionable`
(`:active { transform: scale(.97) }`, sin resaltado de toque).

### Reglas que se mantienen (de `docs/09`)
Acción principal en pie fijo · avisos con deep link `?accion=` · contadores sin ceros · error junto a la acción y
éxito en toast arriba · regla del negocio en hoja con camino · fricción proporcional (un toque / hoja / escribir
palabra) · "Sin verificar" siempre visible · no mezclar monedas · etiqueta y acción en el mismo nodo (elementos
nativos `<button>`/`<a>`) · 48 px de área táctil · letra al 200 % sin desbordes · `prefers-reduced-motion`.

## 10.9 Lo específico de una PWA móvil

| Tema | Qué se hace |
|---|---|
| Instalable | `manifest.webmanifest` (nombre, `display: standalone`, `theme_color`, `background_color`, íconos 192/512 + **maskable**, `start_url: /`, `scope: /`, `lang: es`), `apple-touch-icon` 180 |
| Invitar a instalar | Android/Chrome: botón propio con `beforeinstallprompt`. iPhone: hoja con "Compartir → Agregar a inicio" (Safari no tiene el evento). Solo después de iniciar sesión y una vez; se recuerda si se descarta |
| Pantalla completa en iPhone | `viewport-fit=cover`, `apple-mobile-web-app-capable`, barra de estado `black-translucent` **con relleno de `safe-area-inset-top`** (lección: nada difuminado detrás de la barra) |
| Alto real | `100dvh` y `env(safe-area-inset-*)`; la barra de pestañas respeta el indicador de inicio |
| Teclado | Campos de **≥ 16 px** (Safari no hace zoom); `inputmode`/`enterkeyhint`/`autocomplete` correctos; el pie fijo sube con el teclado (`visualViewport`) |
| Gestos | `overscroll-behavior: contain` (sin rebote de toda la página en el chat), jalar para actualizar propio, sin resaltado gris al tocar |
| Sin conexión | El service worker guarda la interfaz: la app **abre sin señal** y muestra "Sin conexión"; **la API nunca se cachea** (datos privados que cambian); Firestore muestra lo último recibido y envía al volver la red |
| Actualizaciones | Plantilla de SW con versión por build; aviso "Hay una versión nueva · Actualizar" (no recarga sola en medio de un formulario) |
| Sesión | Firebase Auth persiste en IndexedDB. En iPhone, la app instalada **no comparte sesión con Safari**: se inicia sesión una vez dentro de la app |
| Rendimiento | Code-splitting por ruta, Firestore solo en chat, imágenes nulas (íconos SVG), objetivo LCP < 2,5 s en 4G |
| Seguridad | `_headers` con CSP: `connect-src 'self'` + `https://lapticon-backend.onrender.com` (modo directo) + Firebase (`identitytoolkit`, `securetoken`, `firestore.googleapis.com`); HSTS, `nosniff`, `frame-ancestors 'none'`; nada de secretos en el código (la clave de Firebase es pública por diseño) |
| Notificaciones push | **Fuera de alcance** (la app Flutter tampoco las tiene). Se anota como mejora futura |

## 10.10 Fases de trabajo

Cada fase termina con: `typecheck` y `lint` sin errores, pruebas en verde, **revisión en un celular real** (o en
viewport móvil si aún no hay despliegue) y commit pequeño en español. Se crea el tag `pwa-inicio` antes de empezar.

| Fase | Contenido | Criterio de listo |
|---|---|---|
| **0. Andamiaje y conectividad** | Vite + React + TS en `aplicacion_pwa/`; ESLint, Vitest, Playwright; Vite en el puerto 5500 y su proxy; Pages Function (plan B); `_headers`/`_redirects`; workflow de CI; **despliegue de prueba** en Cloudflare Pages; enviar P12 al profesor | Desde el **celular**, la URL pública llama a `/api/ciudades/paises` y muestra el resultado (directo si el profesor ya agregó el origen; si no, por el plan B) |
| **1. Núcleo** | Tokens y tema claro/oscuro; cliente API; modelos tolerantes + pruebas con `referencias/respuestas/`; Firebase; sesión + `redirectFor`; almacenamiento local; formato y validadores (pruebas portadas de Dart) | Pruebas de contrato y lógica en verde; login real abre la sesión y resuelve el estado |
| **2. Componentes base** | Presionable, Tarjeta, Grupo/Fila, Boton, Campo*, Insignia, Avatar, Chips, Aviso/Vacio, Esqueleto, Entrada, Toasts, Hoja, ConfirmacionEscrita; galería en `/dev/galeria` (solo desarrollo) | Pruebas de cada componente (axe, 48 px, teclado, reduce-motion) |
| **3. Estructura** | Pantalla iOS, BarraPestanas, EncabezadoApp, TarjetaHero, Mosaico, RouteTicket, AccionResaltada, jalar para actualizar | Navegación por pestañas con atrás del sistema; se ve bien en iPhone y Android |
| **4. Autenticación y onboarding** | Login, registro, recuperar, completar perfil, elegir rol | Cuenta nueva de punta a punta en el celular |
| **5. Remitente** | Inicio, envíos, nueva encomienda, detalle (retirar, calificar), buscar viajeros | Endpoints 1–3, 7, 9, 10, 13, 15, 17, 18 en uso real |
| **6. Viajero** | Mi viaje, registrar viaje (+ verificar), explorar, tomar, entregar, historial | Endpoints 4–6, 8, 11–13 en uso real |
| **7. Chat, calificaciones, perfil y asistente** | Firestore en tiempo real, calificar, reseñas, perfil, editar, asistente | Chat PWA ↔ Flutter en ambos sentidos; endpoints 14, 16, 19 |
| **8. PWA completa** | Manifest e íconos, service worker, aviso de actualización, invitación a instalar (Android/iOS), sin conexión, meta de iOS | Instalada en iPhone y Android; abre sin conexión; Lighthouse "instalable" |
| **9. Calidad y cierre** | Barrido de accesibilidad, E2E móviles, Lighthouse, `npm run humo` contra el proxy, README, `docs/BITACORA.md`, `CLAUDE.md` | Criterios de §10.1 cumplidos; tag `pwa-v1` |

## 10.11 Estrategia de pruebas

- **Unidad (Vitest):** toda la lógica de §10.7, portando los casos de las pruebas Dart (mismos datos, mismos textos).
- **Contrato:** modelos contra `referencias/respuestas/*.json` (las respuestas reales guardadas).
- **Componentes (Testing Library + `vitest-axe`):** cada componente en claro y oscuro; contraste de cada par de tokens
  (igual que `tema_test.dart`); foco y teclado en hojas y chips.
- **E2E (Playwright)** en viewport de iPhone 13 y Pixel 7, con la API **simulada** (intercepción de rutas, sin red):
  flujos de remitente y viajero, deep links `?accion=`, errores junto al botón, palabra para confirmar.
  Repetido con **texto al 200 %** y ancho 360 px (sin desbordes) y en modo oscuro.
- **Humo contra el servidor real (`npm run humo`):** los 19 endpoints a través del proxy desplegado, con el token de
  prueba de Harold leído de `~/.lapticon/` (fuera del repo; nunca se escribe en el código ni en la salida).
- **Manual en celular** al final de cada fase: iPhone (Safari e instalada) y Android (Chrome e instalada).
- **Lighthouse móvil** en CI sobre el build.

## 10.12 CI y despliegue

- Workflow nuevo `.github/workflows/pwa.yml` (solo cuando cambia `aplicacion_pwa/**`): instalar, `typecheck`,
  `lint`, pruebas, E2E y build. No toca el workflow de Flutter.
- Despliegue a Cloudflare Pages, proyecto `lapticon-pwa` (producción: `https://lapticon-pwa.pages.dev`):
  conectando el repositorio en el panel de Cloudflare (raíz `aplicacion_pwa`, build `npm run build`, salida `dist`)
  **o** con `wrangler pages deploy` desde CI con un token. **Lo configura Harold con su cuenta** (yo no creo cuentas
  ni manejo sus credenciales). Si el nombre `lapticon-pwa` está ocupado, cambia el origen que se pide al profesor.
- Variables: `VITE_API_URL` (modo directo o proxy, §10.4), `BACKEND_URL` (función del plan B) y la configuración
  pública de Firebase en el build.

## 10.13 Riesgos

| Riesgo | Mitigación |
|---|---|
| El profesor tarda o no agrega el origen al CORS | Plan B listo desde la fase 0 (proxy en Cloudflare); el desarrollo no se detiene (puerto 5500 y proxy de Vite) |
| Las reglas de Firestore no permiten algo desde la web | Mismo SDK, mismas reglas y mismo usuario que Flutter; se prueba el chat en la fase 7 contra el real |
| Arranque en frío de Render (60 s) | Timeout 75 s, aviso "despertando", reintento; el proxy de Cloudflare no corta la espera |
| iOS limita las PWA (sin `beforeinstallprompt`, almacenamiento aparte de Safari, sin push) | Hoja de instrucciones para instalar; se avisa que se inicia sesión dentro de la app; push fuera de alcance |
| Detalle sin objeto al recargar (no hay `GET /encomiendas/{id}`) | Búsqueda en caché y en listas (§10.6) |
| Dos apps (Flutter y PWA) divergen con el tiempo | Mismos nombres de componentes, mismas pruebas de lógica, mismo `docs/07` como fuente |
| Tamaño del SDK de Firestore | Carga perezosa solo en chat |
| Otra sesión de trabajo usando los mismos recursos | La PWA tiene carpeta, workflow y despliegue propios |

## 10.14 Decisiones (tomadas el 24-oct-2026)

1. **API y CORS:** pedir al profesor que agregue `https://lapticon-pwa.pages.dev` a la lista blanca (P12 en `docs/06`).
   Plan B: proxy en Cloudflare Pages, incluido desde la fase 0.
2. **Hosting:** Cloudflare Pages, proyecto `lapticon-pwa`, con la cuenta de Harold.
3. **Stack:** el mismo de *Cuentas Claras*: React 19 + TypeScript + Vite + TanStack Query + React Router + Tailwind
   (mapeado a los tokens v2), Vitest y Playwright.
4. **Gestor de paquetes:** npm, como Cuentas Claras.
5. **Carpeta:** `aplicacion_pwa` (sin tilde ni espacios: evita problemas en terminal, CI y URLs).
