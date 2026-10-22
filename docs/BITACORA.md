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
