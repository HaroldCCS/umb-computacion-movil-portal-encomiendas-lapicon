# 08 · Compilación en GitHub Actions y pruebas en iPhone

> Informe del 22-oct-2026. Workflow: `.github/workflows/compilar-apps.yml`.

## 1. Qué hace el workflow

Se ejecuta con cada push a `main` que toque `lapticon_app/**`, con cada tag `practica-*` y a mano
(pestaña **Actions → Compilar apps → Run workflow**). Tiene cuatro trabajos:

| Trabajo | Máquina | Resultado |
|---|---|---|
| Análisis y pruebas | Ubuntu | `flutter analyze` + `flutter test`. No frena la compilación de las apps. |
| APK Android | Ubuntu | `lapticon-<n>.apk` (release, instalable directo). |
| IPA iOS (sin firmar) | macOS | `lapticon-<n>-sin-firmar.ipa` y `lapticon-<n>-simulador.zip`. |
| Publicar Release | Ubuntu | Solo con tags `practica-*`: sube los tres archivos a una Release del repo. |

`<n>` es el número de ejecución; también se usa como `versionCode`/`CFBundleVersion`, así que cada
compilación instala **encima** de la anterior.

Los archivos quedan 30 días en la pestaña **Actions → (la ejecución) → Artifacts**. En un repo público,
para descargarlos hay que haber iniciado sesión en GitHub. Las Releases las puede descargar cualquiera.

### Secretos que hay que crear (Settings → Secrets and variables → Actions)

| Secreto | ¿Obligatorio? | Qué poner |
|---|---|---|
| `GOOGLE_SERVICES_JSON` | Sí | El contenido completo de `referencias/google-services.json`. |
| `GOOGLE_SERVICE_INFO_PLIST` | No | El `GoogleService-Info.plist` de una app **iOS** registrada en Firebase (ver §4). |
| `ANDROID_DEBUG_KEYSTORE_BASE64` | No, pero se recomienda | La salida de `base64 -i ~/.android/debug.keystore`. Sin él, cada APK sale con una llave distinta y Android obliga a desinstalar antes de actualizar. |

Desde la terminal, con la CLI de GitHub:

```bash
gh secret set GOOGLE_SERVICES_JSON < referencias/google-services.json
```

```bash
base64 -i ~/.android/debug.keystore | gh secret set ANDROID_DEBUG_KEYSTORE_BASE64
```

### Detalles de iOS dentro del workflow

El repo no tiene carpeta `ios/`, así que el runner la genera en cada ejecución (nada se sube al repo) y:

- pone el bundle id `com.lapticon.app`, el nombre visible "Lapticon" y iOS 15 como versión mínima
  (lo exige el SDK de Firebase);
- escribe un `firebase_options.dart` con un caso para iOS (el generador de `tool/` solo conoce Android);
- compila con `--no-codesign`, porque firmar exige una cuenta de Apple. **El IPA sin firmar no se puede
  instalar tal cual**: hay que firmarlo con un Apple ID en el momento de instalarlo (§2).

Si algún día se versiona la carpeta `ios/`, el workflow la respeta y solo ajusta esos valores.

**Requisito de Xcode:** `firebase_core 5` trae `firebase-ios-sdk 13`, que exige Swift 6.2, o sea
**Xcode 26 o superior**. El workflow lo selecciona solo. Para compilar iOS en un Mac propio con Xcode 16
hay que actualizar Xcode primero (con Xcode 16.4 falla al resolver los paquetes de Swift).

## 2. Cómo instalarla en iPhones sin pagar

Apple no deja instalar apps fuera del App Store sin una firma. Con un **Apple ID gratuito** (el de iCloud
de cada persona) se puede firmar, con estas restricciones:

- la firma **vence a los 7 días**: hay que reinstalar o "refrescar";
- máximo **3 apps instaladas así** por dispositivo al mismo tiempo;
- hay un límite semanal de identificadores de app y de dispositivos por cuenta (Apple no lo publica;
  las guías hablan de unos 10 identificadores y 3 dispositivos por semana);
- en iOS 16 o superior hay que activar el **Modo de desarrollador**.

Truco: **cada compañero usa su propio Apple ID** para su propio iPhone. Así nadie gasta los cupos de otro.

### Opción A — Sideloadly (recomendada para los compañeros, sirve en Windows y Mac)

1. Descargar el `*-sin-firmar.ipa` de la última ejecución o de la Release.
2. Instalar [Sideloadly](https://sideloadly.io) y, en Windows, iTunes e iCloud **de la página de Apple**
   (no los de la Microsoft Store).
3. Conectar el iPhone por cable y aceptar "Confiar en este computador".
4. Arrastrar el IPA a Sideloadly, escribir el Apple ID y pulsar **Start**. Si dice que el bundle id ya
   está en uso, en *Advanced options* activar el cambio de bundle id (por ejemplo, `com.lapticon.app.juan`).
5. En el iPhone: **Ajustes → General → VPN y gestión de dispositivos → (tu Apple ID) → Confiar**.
6. iOS 16+: **Ajustes → Privacidad y seguridad → Modo de desarrollador → activar** y reiniciar.

A los 7 días la app deja de abrir. Se repite el paso 4 (los datos de la app se conservan) o se deja activo
el refresco automático de Sideloadly con el teléfono en la misma red Wi-Fi.

### Opción B — AltStore / SideStore

Hacen lo mismo que Sideloadly, pero la app que instala se queda en el teléfono y refresca las firmas sola.
AltStore necesita un computador encendido en la misma Wi-Fi para refrescar. SideStore lo hace desde el
propio teléfono después de configurarlo. Su configuración inicial es más larga: útil si alguien va a
probar la app durante varias semanas.

### Opción C — Xcode directo (solo Harold o quien tenga Mac)

Es la más estable para desarrollar, porque permite `flutter run` con recarga en caliente:

```bash
cd lapticon_app
flutter create . --platforms ios --org com.lapticon
open ios/Runner.xcworkspace
```

En Xcode: **Runner → Signing & Capabilities → Team = (tu Apple ID, "Personal Team")** y un bundle id
único. Luego, con el iPhone conectado:

```bash
flutter run --release
```

Mismas reglas de 7 días y 3 apps. Antes de hacerlo en local, ten en cuenta tres cosas. Necesitas Xcode 26.
El `lib/firebase_options.dart` que genera `setup.sh` solo trae Android (en iOS lanza `UnsupportedError`),
así que hay que añadirle el caso iOS igual que hace el workflow. Y `flutter create` también reescribe
`analysis_options.yaml`: revisa el diff antes de hacer commit. Ojo: una compilación **debug** lanzada desde el ícono (sin `flutter run`
conectado) se cierra al abrir en iOS 14+. Para usarla sin cable instala `--release` o `--profile`.

### Opción D — Simulador (cualquiera con Mac, sin Apple ID)

Descomprimir `*-simulador.zip`, abrir el simulador (`open -a Simulator`) y arrastrar `Runner.app` a la
ventana. También se puede con la terminal:

```bash
xcrun simctl install booted Runner.app
```

No tiene límites de firma. Sirve para la demo en clase desde el portátil.

## 3. Opciones de pago o institucionales (sin límites de 7 días)

| Opción | Costo | Qué da |
|---|---|---|
| Apple Developer Program (individual) | 99 USD/año | Firma por un año. **TestFlight**: los compañeros instalan la app TestFlight y entran con un enlace, sin cables ni Modo de desarrollador. Hasta 10 000 probadores externos con una revisión beta rápida de Apple. También *Ad Hoc* (hasta 100 iPhones registrados por UDID). |
| Exención de la cuota para la universidad | Gratis | La UMB, como institución educativa acreditada, puede pedir el Developer Program sin pagar (*fee waiver*). La solicitud la hace la institución, no un estudiante. El antiguo "iOS Developer University Program" lo cerró Apple en mayo de 2024. |
| Una cuenta paga compartida del grupo | 99 USD/año entre todos | Un integrante paga, invita a los demás y se publica en TestFlight. |

Si el grupo paga, el workflow se extiende con firma real y subida a TestFlight
(certificado y perfil como secretos, más `xcrun altool`/`fastlane`). Hoy está preparado para la vía gratuita.

## 4. Firebase en iOS

El proyecto Firebase `lapticon-eba31` solo tiene registradas apps **Android**. Hay dos caminos:

1. **Lo correcto:** pedir al profesor (dueño del proyecto) que registre una app iOS con bundle id
   `com.lapticon.app` y comparta el `GoogleService-Info.plist`. Se guarda como secreto
   `GOOGLE_SERVICE_INFO_PLIST` y el workflow lo usa solo.
2. **Sin ese archivo no funciona (comprobado el 23-oct-2026).** El workflow pone en iOS los mismos datos del
   cliente Android y la app **compila**. Pero al abrirla en el simulador se cierra enseguida, con el error
   `Configuration fails. It may be caused by an invalid GOOGLE_APP_ID`: el SDK nativo de Firebase para iOS
   exige un `appId` de tipo `:ios:`. Hasta tener el plist, el IPA y el `.app` del simulador no sirven para probar.

Crear un proyecto Firebase propio tampoco sirve: el backend del curso solo acepta tokens de `lapticon-eba31`.
Con la app iOS registrada, Auth y Firestore deberían funcionar igual que en Android.

Esto ya está en la lista de preguntas al profesor (ver `docs/06`).

## 5. Lista corta para el grupo

1. Harold crea el secreto `GOOGLE_SERVICES_JSON` (y, de paso, `ANDROID_DEBUG_KEYSTORE_BASE64`). ✅ Hecho.
   Para iPhone falta el `GOOGLE_SERVICE_INFO_PLIST` que debe dar el profesor (§4).
2. Push a `main` o *Run workflow* → en unos 15–25 min aparecen los artifacts.
3. Android: descargar el APK en el teléfono y abrirlo (permitir "instalar apps desconocidas").
4. iPhone: cada uno instala el IPA con **Sideloadly y su propio Apple ID** (§2-A) y lo renueva cada 7 días.
5. Para la entrega: `git tag practica-6 && git push --tags` → Release con los tres archivos.
