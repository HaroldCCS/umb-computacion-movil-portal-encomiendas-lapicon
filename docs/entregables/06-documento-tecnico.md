# Documento técnico — Lapticon

> Entregable del tablero: **"Doc técnico"**, con sus tres partes: **Requerimientos**, **Definición y alcance de la
> app** y **Arquitectura**. Versión del 26-oct-2026, con el estado real de lo construido.
> Proyecto del 2.º corte de Computación Móvil (UMB, Ingeniería de Software). Estudiante: Harold Camargo.

---

## 1. Definición de la app

### 1.1 Problema

Enviar un paquete pequeño entre ciudades o países por un courier es caro y lento. Al mismo tiempo, muchas personas
viajan con espacio libre en su equipaje.

### 1.2 Propuesta

**Lapticon** une a un **remitente** que quiere enviar un paquete con un **viajero** que ya va a ese destino. El
remitente publica la encomienda con lo que paga; el viajero registra su vuelo, ve las encomiendas de su ruta, toma una,
coordinan por chat, la entrega y ambos se califican.

> *"Tu paquete viaja con alguien que ya va para allá."*

### 1.3 Actores

| Actor | Qué hace |
|---|---|
| **Remitente** | Publica encomiendas, sigue su estado, habla con el viajero, retira o califica. |
| **Viajero** | Registra su vuelo, explora encomiendas de su ruta, las toma, las entrega y califica al remitente. |
| Backend Lapticon | API REST compartida por el curso (Node/Express + MongoDB en Render). No se modifica. |
| Firebase `lapticon-eba31` | Identidad (Auth) y mensajes del chat (Firestore). |
| Servicios externos | AeroDataBox (vuelos) y OpenRouter (asistente), consumidos a través del backend. |

Una misma cuenta puede usar los dos roles y cambiar entre ellos.

### 1.4 Ciclo de vida de una encomienda

```text
DISPONIBLE ──tomar (viajero)──► TOMADA ──entregar (viajero)──► ENTREGADA ──► RECIBIDA
     └── retirar (remitente) o un mes sin tomarla ──► VENCIDA
Después de la entrega, remitente y viajero se califican (1–5 estrellas y comentario).
```

---

## 2. Alcance

### 2.1 Dentro del alcance (construido)

- Dos clientes de la misma app, con el mismo diseño y los mismos datos:
  - **App Flutter** para Android e iOS (lo que pide el curso).
  - **PWA** instalable desde el navegador del celular (https://lapticon.haroldsoftware.com).
- Las seis prácticas del proyecto: autenticación, roles y navegación, encomiendas, viajes, chat, entrega y calificación.
- Retos del frontend: rol persistido (en el dispositivo, porque el backend no lo acepta) y chat que se bloquea si
  está cerrado.
- Extras: asistente con IA, caché de ciudades y países, aviso de servidor dormido, modo oscuro, accesibilidad, avisos
  que llevan a la acción pendiente y, en la PWA, uso sin conexión.

### 2.2 Fuera del alcance

| Excluido | Motivo |
|---|---|
| Inicio de sesión con Google | Requiere registrar el SHA-1 del equipo en el Firebase del curso (decisión 22-oct). |
| Matching con IA (reto 2) y vencimientos programados (reto 3) | Son cambios del backend; no tenemos su repositorio. |
| Pagos dentro de la app | El backend no los tiene; el valor es lo que el remitente ofrece. |
| Notificaciones push | Ni el backend ni el enunciado las piden. |
| Publicar en Play Store / App Store | Se entrega como APK (Android), IPA sin firmar (iPhone) y PWA. |

### 2.3 Supuestos y restricciones

- El backend es **compartido** por todo el curso y está en un plan gratuito que "se duerme" (hasta ~60 s).
- Dos endpoints fallan **en el servidor** (`/api/vuelos` y `/api/chatbot` → 500). La verificación del vuelo se quitó
  de la interfaz y el asistente muestra el error sin bloquear el flujo. `/api/chats/estado` daba 500 hasta el
  22-oct; desde el 28-oct responde (docs/03).
- El CORS del backend solo permite `localhost:5500`; la PWA publicada usa un **proxy propio** en Cloudflare.

---

## 3. Requerimientos

Prioridad: **M** obligatorio · **D** deseable · **O** opcional. Estado: ✅ cumplido · 🟡 parcial o adaptado · ❌ no.
La versión original (antes de programar) está en [`docs/02-requerimientos.md`](../02-requerimientos.md).

### 3.1 Funcionales

| ID | Requerimiento | Prioridad | Estado |
|---|---|---|---|
| **RF-A** | **Autenticación y perfil** | | |
| A1–A2 | Registro e inicio de sesión con correo y contraseña (Firebase Auth) | M | ✅ |
| A3 | Inicio con Google | O | ❌ pospuesto |
| A4 | Recuperar contraseña | D | ✅ |
| A5 | Sesión persistente y cerrar sesión | M | ✅ |
| A6–A7 | Completar perfil (`POST /api/users/register`), ver y editar (`GET`/`PUT /api/users/{uid}`) | M | ✅ |
| A8–A9 | Bearer idToken en cada llamada; ante 401, renovar el token y reintentar una vez | M/D | ✅ |
| **RF-B** | **Roles y navegación** | | |
| B1–B2 | Elegir rol y navegación distinta por rol (barra de pestañas) | M | ✅ |
| B3 | Guardar el rol en el backend | M | 🟡 el backend lo ignora: se guarda en el dispositivo y se avisa |
| B4 | Cambiar de rol desde el perfil | D | ✅ |
| **RF-C** | **Encomiendas (remitente)** | | |
| C1 | Crear encomienda con validación completa | M | ✅ (sin fecha límite: el backend la fija a un mes) |
| C2–C3 | Mis encomiendas agrupadas por estado y detalle (maestro-detalle) | M | ✅ |
| C4 | Cancelar mientras esté disponible | M | 🟡 el backend no tiene "cancelada": se retira como `vencida` |
| C5–C6 | Buscar viajeros por ruta y ver su nombre y calificación | D | ✅ con `GET /api/viajes/disponibles` (docs/11 §2C) |
| C7 | Viajes sugeridos por el matching IA | O | ❌ no existe en el backend |
| **RF-D** | **Viajes (viajero)** | | |
| D1 | Registrar viaje | M | ✅ |
| D2 | Validar el vuelo con AeroDataBox | M | 🟡 retirado de la interfaz: el servidor responde 500 (`RAPIDAPI_KEY`); queda listo en el repositorio (docs/11 §2H) |
| D3 | Un viaje activo a la vez (400) | M | ✅ hoja con "Ver mi viaje" |
| D4–D5 | Mi viaje, historial y encomiendas disponibles de la ruta | M | ✅ |
| D6–D7 | Tomar una encomienda y ver las que tomé | M | ✅ las tomadas vienen de `buscar`; las entregadas se recuerdan en el dispositivo |
| **RF-E** | **Chat** | | |
| E1–E2 | Chat por encomienda en tiempo real sobre Firestore (id `uidA_uidB` ordenado) | M | ✅ |
| E3 | Consultar el estado y bloquear el envío si está cerrado | M | ✅ el endpoint responde desde el 28-oct; el chat se cierra al marcar `entregada` |
| E4–E5 | Lista de conversaciones; hora y "Enviando…" | D/O | ✅ (sin contador de no leídos) |
| **RF-F** | **Entrega y calificación** | | |
| F1 | Marcar entregada | M | ✅ escribiendo ENTREGAR |
| F2–F3 | Calificar (1–5 + comentario) y ver calificaciones recibidas | M | ✅ |
| F4 | Chat cerrado tras calificar | M | 🟡 la app bloquea la barra y dice desde cuándo; el backend lo cierra antes, al marcar `entregada` (pregunta P16 al profesor) |
| **RF-G** | **Extras** | | |
| G1 | Asistente con IA | D | ✅ (error con "Reintentar" mientras el servidor falle) |
| G2 | Caché local de ciudades y países (7 días) | D | ✅ |
| G3 | Aviso sin conexión | D | ✅ PWA · 🟡 Flutter (mensaje de error de red) |
| G4 | Ciudad de origen por GPS | O | ❌ |
| G5 | Ícono y splash propios | D | ✅ PWA (íconos e instalación) · 🟡 Flutter (splash propio dentro de la app) |

### 3.2 No funcionales

| ID | Requerimiento | Cómo se cumple |
|---|---|---|
| RNF-1 | Seguridad | Contraseñas solo en Firebase; token en memoria; claves fuera del repositorio (`.gitignore`, secretos de GitHub y variables de Cloudflare); CSP y HSTS en la PWA. |
| RNF-2 | Arquitectura por capas | Presentación → datos (repositorios) → red/servicios. Las pantallas nunca llaman a `http` ni a Firebase. |
| RNF-3 | Manejo de errores | Mensaje humano por código (400, 401, 403, 404, 5xx, sin red, tiempo agotado), junto a la acción que falló. |
| RNF-4 | Arranque en frío | Tiempo de espera de 75 s y aviso "Despertando el servidor…" a los 5 s. |
| RNF-5 | Estados de carga, vacío y error | Esqueletos, vacíos con acción, "Reintentar" y jalar para actualizar en todas las listas. |
| RNF-6 | Usabilidad y accesibilidad | Español de "tú", contraste AA, toques ≥ 48, letra al doble sin desbordes, claro y oscuro, "reducir movimiento". |
| RNF-7 | Plataformas | Android (APK), iPhone (IPA sin firmar) y cualquier celular con la PWA. |
| RNF-8 | Calidad | `flutter analyze` limpio y 184 pruebas en Flutter; 123 unitarias y 26 E2E en la PWA; CI en cada push. |
| RNF-9 | Control de versiones | Tres repositorios en GitHub, commits pequeños en español, historial conservado. |
| RNF-10 | Documentación | README en cada repo, `docs/` y esta carpeta de entregables. |

---

## 4. Arquitectura

### 4.1 Vista de contexto

```text
                ┌───────────────────── Celular ──────────────────────┐
                │  App Flutter (Android/iOS)   o   PWA (navegador)    │
                └───────┬────────────────────────┬───────────────────┘
          idToken (Auth) │                        │ HTTPS + Authorization: Bearer <idToken>
                         ▼                        ▼
             ┌────────────────────┐   ┌──────────────────────────────┐      ┌───────────────┐
             │  Firebase          │   │  Backend Lapticon (Render)   │────► │ MongoDB Atlas │
             │  Auth · Firestore  │   │  Node/Express · REST /api/*  │      └───────────────┘
             └────────────────────┘   └──────────┬───────────────────┘
               (chat en tiempo real)              ├──► AeroDataBox (vuelos)
                                                  └──► OpenRouter (asistente IA)

  Solo la PWA publicada: Navegador ──► Cloudflare Pages ──(Function /api/*)──► Backend   (por el CORS)
```

- **Identidad:** Firebase Auth emite el idToken; el backend solo lo verifica.
- **Datos de negocio:** API REST del backend (usuarios, viajes, encomiendas, calificaciones, catálogo).
- **Chat:** directo a Firestore; el backend solo informa si un chat está cerrado.

### 4.2 Capas (iguales en las dos apps)

| Capa | Responsabilidad | Flutter | PWA |
|---|---|---|---|
| Presentación | Pantallas, componentes del sistema de diseño, navegación | `lib/features/*`, `lib/core/widgets/` | `src/funciones/*`, `src/core/componentes/` |
| Estado | Sesión, datos del servidor en caché, estado de pantalla | Riverpod 3 | TanStack Query + contexto |
| Datos | Modelos tolerantes y repositorios = contrato de la API | `lib/data/models`, `lib/data/repositories` | `src/datos/modelos`, `src/datos/repositorios` |
| Red y servicios | Cliente HTTP, Firebase Auth, Firestore, almacenamiento local | `lib/core/network`, `lib/data/services`, `lib/data/local` | `src/core/red`, `src/core/auth*.ts`, `src/funciones/chat/servicio*` |

**Regla:** las pantallas nunca llaman a `http`/`fetch` ni a Firebase; siempre a un repositorio o servicio.

### 4.3 App Flutter

```text
lib/
├── core/         config (URL, tiempos) · network (ApiClient, excepciones) · router (go_router, redirectFor)
│                 theme (tokens v2, claro/oscuro) · utils (formatos, validadores) · widgets (sistema de diseño)
├── data/         models (Usuario, Viaje, Encomienda, Calificaciones…) · repositories · services (Auth) · local (Prefs)
└── features/     session · splash · auth · onboarding · home · remitente · viajero · catalogo
                  chat · calificaciones · perfil · asistente
```

Paquetes: `firebase_core`, `firebase_auth`, `cloud_firestore`, `flutter_riverpod`, `go_router`, `http`,
`shared_preferences`, `intl`, `google_fonts`. `applicationId = com.lapticon.app`.

### 4.4 PWA

React 19 + TypeScript + Vite, React Router (cada pestaña es una URL), TanStack Query, Tailwind mapeado a los
mismos tokens, Firebase web modular (Firestore se descarga solo al abrir el chat) y un **service worker propio** que
guarda la interfaz para abrir sin conexión pero **nunca** guarda respuestas de la API.

### 4.5 Flujos clave

**Autenticación y primera llamada protegida**

```text
Login ─► Firebase Auth ─► idToken ─► GET /api/users/{uid} (Bearer)
   ├─ 200 con perfil completo y rol ─► Inicio del rol
   ├─ 404 / perfil incompleto ───────► Completar perfil ─► POST /api/users/register
   ├─ 401 ─► renovar token y reintentar una vez
   └─ red / 5xx ─► Splash con el error y "Reintentar"
```

**Chat**

```text
chatId = [uidA, uidB].sort().join('_')
Enviar:  GET /api/chats/estado/{chatId}  → cerrado: bloquear │ activo, 404 o 500: seguir
         lote atómico ─► chats/{chatId}        (participantes, nombres, ruta, último mensaje, actualizadoEn)
                     └► chats/{chatId}/mensajes/{auto}  (texto, emisorUid, creadoEn, creadoLocal)
Recibir: escucha en tiempo real, orden por fecha; "Enviando…" hasta que el servidor confirma.
```

### 4.6 Persistencia

| Dónde | Qué | Por qué |
|---|---|---|
| Backend (MongoDB) | Perfil, viajes, encomiendas, calificaciones | Fuente de verdad compartida |
| Firestore | Chats y mensajes | Tiempo real |
| Dispositivo (`SharedPreferences` / `localStorage`) | Rol, entregas calificadas, encomiendas tomadas, caché de ciudades (7 días) | El backend no guarda esos datos o no hace falta pedirlos cada vez |

### 4.7 Manejo de errores

| Situación | Qué hace la app |
|---|---|
| Sin red / tiempo agotado | Mensaje claro y "Reintentar"; la PWA muestra además "Sin conexión" |
| Servidor dormido (> 5 s) | Aviso "Despertando el servidor… puede tardar hasta un minuto" |
| 400 regla de negocio | Hoja que explica y ofrece el camino ("Ver mi viaje") |
| 401 | Renueva el token y reintenta una vez |
| 403 / 404 | "No tienes permiso…" / estado vacío cuando "no hay" es normal |
| 500 de vuelos, chat o asistente | Mensaje específico; el flujo sigue (vuelos: no se muestra; chat abierto; asistente con "Reintentar") |

### 4.8 Despliegue e integración continua

| Repositorio | CI (GitHub Actions) | Entrega |
|---|---|---|
| …-lapicon-flutter | Análisis y pruebas · APK · IPA sin firmar | Release "última versión" con enlace fijo al APK |
| …-lapicon-pwa | Tipos, lint, pruebas, build · E2E en iPhone y Android | Cloudflare Pages: cada push a `main` publica en https://lapticon.haroldsoftware.com |
| …-lapicon (este) | — | Documentación |

---

## 5. Decisiones técnicas

| Decisión | Alternativas | Por qué |
|---|---|---|
| Flutter | Kotlin nativo, React Native | Es el material del curso; un código para Android e iOS |
| Riverpod 3 + go_router | Provider + Navigator | Estado con caché y redirecciones declarativas según la sesión |
| Modelos "tolerantes" | Modelos estrictos | El backend devuelve formas variables (`_id`/`id`, objetos envueltos) |
| Rol en el dispositivo | Rol en el backend | El backend ignora el campo (verificado) |
| Validar todo en el cliente | Confiar en el backend | El backend acepta cuerpos vacíos y da 500 en vez de 400 |
| PWA además de Flutter | Solo Flutter | Probar desde cualquier celular sin instalar un APK; mismo diseño y datos |
| Proxy en Cloudflare | Pedir el CORS | El CORS solo permite localhost; el proxy no depende del profesor |

## 6. Calidad

| | Flutter | PWA |
|---|---|---|
| Análisis estático | `flutter analyze` sin errores ni warnings | TypeScript estricto + ESLint |
| Unidad y contrato | modelos con respuestas reales, lógica, validadores, cliente HTTP | ídem, más repositorios con `fetch` falso |
| Interfaz | widget tests y accesibilidad (contraste, 48 dp, letra al doble) | componentes con `axe-core`; contraste de tokens |
| Extremo a extremo | prueba manual en el emulador con cuentas reales | 26 E2E en iPhone y Android, con dos personas a la vez |
| Contra el servidor real | — | `npm run humo`: 15/15 endpoints (28-oct) |

## 7. Limitaciones conocidas

- Fallas del servidor: `/api/vuelos` y `/api/chatbot` (500).
- El backend no guarda el rol ni qué encomiendas califiqué, y solo lista las que tomé mientras siguen `tomada`: eso se
  recuerda **por dispositivo**.
- No hay cancelar encomienda: "retirar" la deja `vencida` (pedido al profesor).
- Las reglas de Firestore permiten listar chats a cualquier usuario autenticado (reportado).
- Pendiente: prueba en un celular físico con las dos cuentas y chat Flutter ↔ PWA en vivo.
