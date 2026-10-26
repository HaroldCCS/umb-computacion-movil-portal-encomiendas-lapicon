# Semana 1 · Login y registro

> Entregable del tablero: **"Sem 1 — Login / Registro"** (Práctica 1 del proyecto, más el perfil y el rol de la
> Práctica 2). Estado: ✅ hecho en la app Flutter y en la PWA.

## 1. Objetivo

Que una persona cree su cuenta, inicie sesión con Firebase y la app haga su **primera llamada protegida** al backend
enviando el idToken.

## 2. Qué hace la app

```text
Login ──► (sin cuenta) Registro ──► Completar perfil (paso 1 de 2) ──► Elegir rol (paso 2 de 2) ──► Inicio del rol
   └──► ¿Olvidaste tu contraseña? ──► Recuperar (correo de Firebase)
```

| Función | Cómo funciona |
|---|---|
| **Registro** | Correo y contraseña con Firebase Auth. Validación al salir del campo, barra de seguridad de la contraseña y confirmación. |
| **Login** | Correo y contraseña. Los errores de Firebase se traducen ("Correo o contraseña incorrectos.") y se muestran junto al botón. |
| **Recuperar** | `sendPasswordResetEmail`. Por privacidad nunca dice si el correo existe. |
| **Sesión persistente** | `authStateChanges`: al reabrir la app entra directo. |
| **Completar perfil** | Nombre, apellido, teléfono y nacionalidad (buscador de países de `/api/ciudades/paises`) → `POST /api/users/register`. |
| **Primera llamada protegida** | `GET /api/users/{uid}` con `Authorization: Bearer <idToken>` al iniciar la sesión. |
| **Elegir rol** | Remitente ("Quiero enviar") o Viajero ("Voy a viajar"); se puede cambiar desde el Perfil. |
| **Cerrar sesión** | Con confirmación en una hoja inferior. |

## 3. Cómo se decide a qué pantalla ir

La navegación del onboarding la decide una sola regla pura, `redirectFor(estado, ruta)` (Flutter) /
`redirigirPara` (PWA), según el estado de la sesión:

| Estado | Pantalla |
|---|---|
| `cargando` / `error` | Splash (con "Reintentar" si falla) |
| `sinSesion` | Login, Registro o Recuperar |
| `sinPerfil` | Completar perfil |
| `sinRol` | Elegir rol |
| `listo` | Inicio del rol (no se puede volver al login) |

## 4. Cliente HTTP (la base de todas las semanas)

- Agrega `Authorization: Bearer <idToken>` a cada ruta protegida.
- Si el backend responde **401**, pide un token nuevo a Firebase y **reintenta una vez**.
- Tiempo de espera de **75 s**; a los 5 s muestra **"Despertando el servidor…"** (Render gratuito).
- Convierte los errores `{ error }` en mensajes humanos (400, 401, 403, 404, 5xx, sin conexión).

## 5. Decisiones

- **Solo correo y contraseña** (Google Sign-In pospuesto): exige registrar el SHA-1 del equipo en Firebase.
- **El rol se guarda en el dispositivo**: el backend ignora el campo `rol` (verificado en la semana 0). La app intenta
  guardarlo en el servidor y, si no lo acepta, lo recuerda localmente y lo dice en el Perfil.

## 6. Evidencia

| | Flutter | PWA |
|---|---|---|
| Pantallas | `lib/features/auth/`, `onboarding/`, `splash/` | `src/funciones/auth/`, `onboarding/` |
| Sesión | `lib/features/session/session_controller.dart` | `src/funciones/sesion/sesion.ts` |
| Cliente HTTP | `lib/core/network/api_client.dart` | `src/core/red/cliente.ts` |
| Pruebas | `test/auth/auth_onboarding_test.dart`, `router_redirect_test.dart`, `api_client_test.dart`, `validators_test.dart` | `sesion.test.ts`, `core/logica.test.ts`, E2E "cuenta nueva" en iPhone y Android |

**Cómo demostrarlo:** crear una cuenta nueva, completar el perfil eligiendo un país, elegir rol y mostrar el Perfil
cargado desde `GET /api/users/{uid}`.
