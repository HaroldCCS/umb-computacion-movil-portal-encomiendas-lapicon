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
