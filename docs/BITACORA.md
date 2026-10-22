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
