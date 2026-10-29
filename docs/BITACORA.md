# Bitácora de trabajo — Lapticon

Una entrada por paso: qué se hizo, qué errores aparecieron, cómo se resolvieron y qué queda pendiente.

---

## 2026-10-22 13:10 — Paso 1: entorno de desarrollo

**Qué se hizo**
- Revisión con `flutter --version` y `flutter doctor -v`.
- Instalación de Android SDK Command-line Tools: `brew install --cask android-commandlinetools` y luego
  `sdkmanager --sdk_root=~/Library/Android/sdk "cmdline-tools;latest"` (así quedan dentro del SDK que usa Flutter).
- Aceptación de licencias con `flutter doctor --android-licenses`.
- `flutter upgrade`: de 3.41.9 (Dart 3.11.5) a **3.47.7**, la versión contra la que se escribió el código.

**Errores encontrados**
- `✗ cmdline-tools component is missing` y `✗ Android license status unknown` en `flutter doctor`.
- Flutter 3.41.9 era más viejo que el 3.47 que asume el código.

**Cómo se resolvieron**
- Con las instalaciones de arriba. Resultado: `flutter doctor` → *No issues found!*

**Entorno final**
- Flutter 3.47.7 stable, Android SDK 36.1 (platforms 34 y 36.1), Java 21 (Corretto), Xcode 16.4.
- AVD disponible: `Medium_Phone` (Android 37, arm64).

**Pendiente**
- El `.gitignore` de la raíz no excluye `lapticon_app/lib/firebase_options.dart`: se corrige en el paso de Git.

---

## 2026-10-22 13:18 — Paso 2: `bash setup.sh`

**Qué se hizo**
- `bash setup.sh` en `lapticon_app/`: generó `android/` (Kotlin DSL), dejó `applicationId = "com.lapticon.app"`,
  `minSdk = maxOf(flutter.minSdkVersion, 23)`, permiso de Internet y etiqueta "Lapticon"; agregó dependencias y generó
  `lib/firebase_options.dart` para `lapticon-eba31`.
- Versiones resueltas: firebase_core 5.0, firebase_auth 7.0, cloud_firestore 7.0, flutter_riverpod 3.4.3,
  go_router 18.1.1, google_fonts 9.0, http 1.6, intl 0.20.3, shared_preferences 2.5.6.

**Errores encontrados**
- Ninguno en el script (terminó en la primera corrida). `flutter analyze`: *No issues found*.
- `flutter test`: 83 pasan, 1 falla (`RouteTicket muestra la ruta y es accesible`) → se atiende en el paso 3.

**Pendiente**
- El test que falla. El build de Android todavía no se ha probado (paso 4).

---

## 2026-10-22 13:13 — Paso 3: `flutter analyze` y `flutter test`

**Qué se hizo**
- `flutter analyze`: sin errores ni warnings.
- `flutter test`: 84/84 en verde después de la corrección.
- Git inicializado en `proyecto_2_corte` (rama `main`). Al `.gitignore` de la raíz se le agregaron
  `lapticon_app/lib/firebase_options.dart` y `lapticon_app/android/app/google-services.json`, aunque ya estaban
  en `lapticon_app/.gitignore`. Se verificó que ningún archivo con API key quede en el índice.

**Errores encontrados**
- `RouteTicket muestra la ruta y es accesible`: el test buscaba un nodo con etiqueta exacta
  "Ruta de Bogota a Miami", pero el nodo real era
  "Ruta de Bogota a Miami / ORIGEN / Bogota / DESTINO / Miami / FECHA / 1 dic".

**Cómo se resolvió (el error estaba en el código)**
- TalkBack habría leído la ruta dos veces. En `lib/core/widgets/route_ticket.dart` la parte superior se envuelve en
  `ExcludeSemantics`, porque la etiqueta "Ruta de X a Y" ya la describe.
- El test pasa a comparar la etiqueta completa (`Ruta de Bogota a Miami\nFECHA\n1 dic`), así se detecta si la
  ruta vuelve a repetirse.

**Pendiente**
- Compilar y ejecutar en Android (paso 4).

---

## 2026-10-22 13:21 — Paso 4: ejecución en el emulador

**Qué se hizo**
- Emulador `Medium_Phone` (Android 37, arm64, 1080×2400) y `flutter run -d emulator-5554`.
- Primer `flutter build apk --debug` en ~5 min: Gradle descargó por su cuenta Build-Tools 36, Platform 35/36 y CMake 3.22.1
  (las licencias ya estaban aceptadas).
- Recorrido sin cuenta: pantalla de inicio de sesión, "Crear cuenta", volver e intentar entrar con campos vacíos
  (aparecen "Escribe tu correo." y "Escribe tu contraseña."). Sin excepciones ni overflows en el log.
- Nuevo `lapticon_app/tool/obtener_token.sh`: pide correo y contraseña por teclado y guarda el idToken en
  `~/.lapticon/token.json` (fuera del repo, permisos 600) para probar la API con curl.

**Errores encontrados**
- Ninguno de compilación ni de ejecución en las pantallas públicas.
- Aviso (no es error): `firebase_auth` y `firebase_core` aplican Kotlin Gradle Plugin; Flutter avisa que en versiones
  futuras eso dejará de compilar. Se arregla cuando los plugins se actualicen, no en nuestro código.

**Pendiente**
- Las pantallas con sesión (completar perfil, elegir rol, perfil, remitente, viajero, chat) necesitan una cuenta
  nueva → paso 5.

---

## 2026-10-22 14:19 — Paso 5: contrato real de la API y pruebas en el emulador

**Qué se hizo**
- Cuentas propias: remitente y viajero (las creó Harold; tokens en `~/.lapticon/`, fuera del repo).
- Todos los endpoints probados con curl; las respuestas están en `referencias/respuestas/` con teléfono y correo
  enmascarados. `docs/03` y `CLAUDE.md` actualizados con lo confirmado.
- En el emulador, como viajero: Mi viaje, Explorar, tomar encomienda, chat en Firestore (en los dos sentidos),
  marcar entregada, calificar al remitente y Perfil. Todo quedó verificado contra el servidor.

**Errores encontrados y cómo se resolvieron**
- El backend no tiene el estado `cancelada` (daba 400) → se agregó `recibida` y cancelar ahora deja la encomienda `vencida`.
- El backend ignora `fechaVencimiento` (vence al mes) → se quitó el selector y se muestra la fecha automática.
- `/disponibles` trae `remitenteNombre` y no el uid → el modelo lo lee; el viajero ya no ve sus propias encomiendas.
- `/api/chats/estado` responde 500 siempre → la app trata el chat como abierto.
- Las calificaciones traen la fecha en `timestamp` → el modelo la lee.
- Aserción de `ListTile` dentro de `DecoratedBox` (Mi viaje y Perfil) → se envolvió en un `Material` transparente.
- La fecha del pase salía cortada, se perdía el nombre del remitente al entregar y se podía calificar dos veces → corregido.

**Pendiente / para el profesor**
- Fallas del servidor: `/api/vuelos` (falta RAPIDAPI_KEY), `/api/chatbot` (key de OpenRouter inválida) y
  `/api/chats/estado` (500). Calificaciones inválidas dan 500 en vez de 400 y `POST /api/encomiendas` no valida el body.
- Seguridad: las reglas de Firestore dejan que cualquier usuario autenticado liste todos los chats.
- No hay endpoint para "encomiendas que tomé": la app las recuerda localmente, así que solo aparecen las tomadas en ese teléfono.
- Falta probar en el emulador: el flujo del remitente (requiere iniciar sesión con esa cuenta), el asistente IA,
  cambiar de rol y registrar un viaje nuevo.
- Detalle visual: la etiqueta "TE PAGAN" se parte en dos líneas en las tarjetas de Explorar.

---

## 2026-10-23 01:39 — Paso 6: rediseño UI/UX v2

**Qué se hizo**
- Se replanteó el diseño con la guía de UI/UX de *Cuentas Claras*: plan y decisiones en `docs/08-plan-rediseno-ui.md`
  (paleta Lapticon, fuente del sistema + Space Grotesk, pestaña Inicio para el remitente, estilo iOS completo).
- Fases: 1 tokens y tema · 2 componentes base · 3 barra flotante, pantalla iOS, hero y pase · 4 inicio por rol con
  contadores y avisos que llevan a la acción · 5a–5d todas las pantallas · 6 limpieza, accesibilidad y documentos.
- Se borraron los widgets y alias del sistema v1; `docs/07` describe el sistema v2.
- Pruebas: de 105 a 218, entre ellas `test/accesibilidad_test.dart` (claro/oscuro y letra al doble en 360 dp).
- Cada fase se revisó en el emulador con datos reales (o con una galería temporal cuando la pantalla necesitaba otra
  cuenta o no estaba alcanzable). Tag `pre-rediseno-v2` antes de empezar y `rediseno-v2` al terminar.

**Errores encontrados y cómo se resolvieron**
- Inicio en blanco en Android: el primer cuadro mide 0 y la grilla de mosaicos calculaba un ancho negativo → piso en 0.
- El detalle quedaba sin contenido: la acción resaltada ocupaba todo el alto del pie → `MainAxisSize.min`.
- La flecha de volver de la barra iOS salía como un cuadro → faltaba `cupertino_icons`.
- Contraste: el verde de éxito y el degradado Cielo no llegaban a AA con texto pequeño → tonos más oscuros.
- Grupos con contenido corto se encogían y centraban → se estiran a todo el ancho.
- El botón seguía cargando debajo de la hoja de una regla del backend → deja de cargar antes de abrirla.
- Con letra grande desbordaban el pase, la cabecera del hero, `Fila`, las estrellas y la marca → `Wrap`/`Flexible`.
- El hero de Inicio tenía la acción y la etiqueta en nodos distintos del lector de pantalla → un solo nodo.
- Esos arreglos de letra grande descentraron los detalles del pase y despegaron el valor de `Fila` de la derecha
  (se vio en el emulador) → corregido y con pruebas de alineación.

**Pendiente**
- Lo calificado antes del rediseño no quedó registrado en el teléfono: esa entrega aparece una vez "por calificar".
- No se vieron en el emulador (sí en pruebas): el detalle del remitente con envíos reales y Registrar viaje con un
  viajero sin viaje activo.
- Dos documentos con número 08 (`08-plan-rediseno-ui.md` y `08-compilacion-y-pruebas-ios.md`, de otra sesión).
- Otra sesión de Claude usó el mismo emulador en paralelo; conviene usar uno por sesión.

---

## 2026-10-24 — Paso 7: Lapticon como PWA (`aplicacion_pwa/`)

**Qué se hizo**
- Plan en `docs/10-plan-migracion-pwa.md` (stack de *Cuentas Claras*: React 19 + TypeScript + Vite + TanStack Query +
  React Router + Tailwind mapeado a los tokens v2; Cloudflare Pages; proxy como plan B por el CORS del backend).
- Fase 0: andamiaje, proxy y CI (`.github/workflows/pwa.yml`). Fases 1–8: núcleo, componentes, todas las pantallas,
  chat en Firestore con el mismo esquema que Flutter, service worker, íconos e instalación.
- Pruebas: 122 unitarias (portadas de Dart, contrato con `referencias/respuestas/`, componentes con axe, contraste de
  tokens), 26 E2E en iPhone y Android con dos personas a la vez, y `npm run humo` contra el servidor real (13/13).

**Errores encontrados y cómo se resolvieron**
- La tarjeta principal del viajero salía sin degradado: Tailwind no ve clases armadas con plantillas
  (`hero-${rol}`) → mapa de clases literales y una prueba que lo vigila.
- Fechas de viaje un día antes en Colombia (medianoche UTC leída como instante) → se leen como fecha del calendario.
- Los campos de ciudad/país solo anunciaban la etiqueta → ahora "Origen: Bogota".
- E2E intermitentes por escribir antes de que la pantalla montara → esperar la pantalla antes de llenar.
- `npm audit` marcaba `@grpc/grpc-js` (solo Node) → `overrides` a 1.14.6.

**Pendiente**
- Conectar Cloudflare Pages (con `VITE_FIREBASE_API_KEY`), probar instalada en iPhone y Android y el chat con Flutter.
- Respuesta del profesor a P12 (CORS) para pasar del proxy al modo directo.

---

## 2026-10-24 — Paso 8: un repositorio por aplicación

**Qué se hizo**
- La app Flutter pasó a [umb-computacion-movil-portal-encomiendas-lapicon-flutter](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter) y la PWA a [umb-computacion-movil-portal-encomiendas-lapicon-pwa](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-pwa), **con su historial**
  (`git subtree split` de `lapticon_app/` y `aplicacion_pwa/`). Cada una tiene su workflow en la raíz.
- Este repositorio queda como documentación; el código se quitó de aquí (sigue en su historial).
- Localmente, los dos repos se clonan dentro de esta carpeta con los mismos nombres, ignorados por este repo.
- El repo de Flutter recibió los secretos `GOOGLE_SERVICES_JSON` y `ANDROID_DEBUG_KEYSTORE_BASE64` (los mismos de antes);
  el enlace del APK ahora apunta a sus Releases. La PWA lleva su copia de `referencias/respuestas/` para las pruebas.

---

## 2026-10-26 — Paso 9: PWA desplegada y entregables del tablero

**Qué se hizo**
- PWA desplegada en Cloudflare Pages desde el panel (Git), proyecto `lapticon-pwa`, dominio
  https://lapticon.haroldsoftware.com. Humo contra el servidor a través del proxy desplegado: 13/13.
- Carpeta `docs/entregables/` con un documento por punto del tablero del profesor (semanas 0–4, UX/UI, documento
  técnico, video de 2 minutos, código fuente y sustentación), al día con lo construido.

**Errores encontrados y cómo se resolvieron**
- La primera versión publicada quedó en blanco: el `wrangler.toml` del repo hacía que Cloudflare ignorara las
  variables del panel y el build salió sin `VITE_FIREBASE_API_KEY` → se quitó el archivo (Node 22 con
  `.node-version`) y Harold cargó la clave en el panel.
- Sin la clave, la app se caía sin mostrar nada → ahora muestra "Falta configurar Firebase…" con "Reintentar".
- La cuenta personal de GitHub (HaroldCCS) no aparecía en Cloudflare: estaba vinculada solo la organización
  `haroldsoftware`; Harold la vinculó.

**Pendiente**
- Grabar el video, prueba en celular físico con las dos cuentas y la sustentación.

## 2026-10-26 — Paso 10: contrato de la API en Swagger

**Qué se hizo**
- La colección de Postman se pasó a **OpenAPI 3.1** (`docs/api/openapi.yaml`) con los bodies, esquemas y respuestas
  reales de `referencias/respuestas/`, y un visor **Swagger UI** (`docs/api/index.html`) que abre con doble clic.
- 28 operaciones: 11 ✅, 9 ⚠️ (500 en el servidor o comportamiento distinto) y **8 🆕 que faltan en el backend**
  (rol, perfil público, encomiendas tomadas, detalle, retirar, cerrar viaje, calificaciones pendientes, token push),
  cada una con el motivo.
- Validado con Redocly: 0 errores.

**Errores encontrados y cómo se resolvieron**
- `$ref` dentro de `example` no lo resuelve Swagger → los ejemplos repetidos usan anclas YAML (`x-ejemplos`).
- El backend no envía `Access-Control-Allow-Origin`, así que "Try it out" fallaría en el navegador → el visor es de
  solo lectura y las pruebas siguen en Postman o `curl`.

## 2026-10-28 — Paso 11: quitar "Verificar vuelo" (docs/11 §2H)

**Qué se hizo**
- Observación del profesor: "verificar vuelo" no funciona (el servidor responde siempre 500 por `RAPIDAPI_KEY`), así
  que no debe mostrarse. Se quitó de las dos apps:
  - Registrar viaje: el botón, los avisos ("Verificación no disponible", "Vuelo no encontrado") y el subtítulo. Ahora
    dice "Los remitentes de tu ruta verán tu vuelo y fecha.";
  - Mi viaje: la insignia "Vuelo verificado" / "Sin verificar";
  - la memoria local `viajero_vuelos_verificados_{uid}`, `claveVuelo` y, en Flutter, `VueloVerificadoBadge`.
- Se conservan `validarVuelo` en el repositorio y la comprobación de `humo`, por si el servidor vuelve a responder.
- Pruebas nuevas: Registrar viaje y Mi viaje no muestran ningún texto con "verific".
- Docs al día: video, sustentación, documento técnico, semana 2, UX/UI, docs/07 y docs/03.
- Verificado: PWA typecheck, lint, 123 unitarias y 26 E2E; Flutter analyze sin problemas y 217 pruebas.
  Commits: PWA `5c07e21`, Flutter `1854e3b` (sin push).

## 2026-10-28 — Paso 12: Fase 0 contra el servidor real (docs/11)

**Qué se hizo**
- Se verificó con las dos cuentas propias y datos desechables (Cali → Lima): cancelar y completar viaje, tomar,
  entregar y recibir, `buscar` / `disponibles2` / `mis-encomiendas`, el 403 a un tercero, el estado del chat,
  `viajes/disponibles` (pública) y `emparejar-viajes`. Hay 31 respuestas en `referencias/respuestas/fase0_*.json`.
- Hallazgos principales:
  - `PATCH /api/viajes/{id}/estado` funciona (no acepta `contactado`), y un viaje cancelado se puede reactivar;
  - `buscar` trae `uid` y `remitenteNombre`, pero `tomadas` solo trae las `tomada`;
  - el chat se cierra al marcar `entregada` y se reabre al tomar otra encomienda del mismo par;
  - `emparejar-viajes` responde 200.

**Errores encontrados y cómo se resolvieron**
- Los tokens guardados estaban vencidos → `RENOVAR=1 bash tool/obtener_token.sh`.
- El Python del sistema no tiene certificados SSL → las peticiones se hicieron con `curl`, pasándole el token por la
  entrada estándar para que no aparezca en la salida.
- Marcar `entregada` dejó cerrado el chat del par de la demo → se tomó una tercera encomienda desechable (C) para
  reabrirlo.
