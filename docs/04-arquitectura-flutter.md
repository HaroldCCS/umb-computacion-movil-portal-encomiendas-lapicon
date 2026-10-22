# 4. Arquitectura de la app Flutter

## 4.1 Vista general

```text
┌──────────────────────── APP FLUTTER (Android) ────────────────────────┐
│  Presentación   pantallas · widgets · controladores (Riverpod)        │
│        │                                                              │
│  Dominio        modelos (Encomienda, Viaje, Usuario…) · reglas de UI  │
│        │                                                              │
│  Datos          repositorios ─┬─ ApiClient (http + Bearer idToken) ───┼──► Backend Lapticon (Render)
│                               ├─ AuthService (firebase_auth) ─────────┼──► Firebase Auth
│                               ├─ ChatService (cloud_firestore) ───────┼──► Firestore  chats/{uid1_uid2}
│                               └─ SharedPreferences ───────────────────│   (caché local: rol, ciudades)
└───────────────────────────────────────────────────────────────────────┘
```

Principios:
- Las pantallas **nunca** llaman a `http` ni a Firebase directamente: pasan por repositorios (separación en capas).
- `ApiClient` centraliza la URL base, los headers (`_getHeaders()` con el idToken), los timeouts, el manejo de errores y el reintento por 401.
- Los repositorios devuelven modelos tipados y lanzan excepciones propias (`ApiException(statusCode, mensaje)`).

## 4.2 Paquetes propuestos

| Paquete | Para qué |
|---|---|
| `firebase_core`, `firebase_auth` | Inicializar Firebase y autenticación correo/contraseña |
| `cloud_firestore` | Chat en tiempo real |
| `http` (o `dio`) | Llamadas REST. `http` es suficiente y más didáctico; `dio` facilita interceptores |
| `flutter_riverpod` | Gestión de estado e inyección de dependencias (alternativa simple: `provider`) |
| `go_router` | Rutas declarativas y redirecciones (login → perfil → rol → menú) |
| `shared_preferences` | Caché del rol, de la lista de ciudades/países y preferencias |
| `intl` | Formato de fechas y moneda |
| `connectivity_plus` | Aviso sin conexión |
| `flutter_rating_bar` (o widget propio) | Estrellas de calificación |
| `geolocator` + `geocoding` *(opcional)* | Sugerir ciudad de origen con GPS (tema de sensores) |
| `flutter_launcher_icons`, `flutter_native_splash` | Ícono y splash |
| Dev: `flutter_lints`, `mocktail` | Análisis estático y pruebas |

Las versiones exactas se fijan al crear el proyecto (`flutter pub add …`) con la versión de Flutter estable instalada.

## 4.3 Estructura de carpetas

```text
lapticon_app/
├── android/app/google-services.json        ← del curso (applicationId = com.lapticon.app)
├── lib/
│   ├── main.dart                           ← Firebase.initializeApp + ProviderScope
│   ├── app.dart                            ← MaterialApp.router, tema Material 3
│   ├── core/
│   │   ├── config/env.dart                 ← baseUrl, timeouts
│   │   ├── network/api_client.dart         ← headers con Bearer, errores, retry 401
│   │   ├── network/api_exception.dart
│   │   ├── router/app_router.dart          ← go_router + redirecciones por sesión/rol
│   │   ├── theme/app_theme.dart
│   │   └── utils/validators.dart, formatters.dart
│   ├── data/
│   │   ├── models/ usuario.dart, viaje.dart, encomienda.dart, rating.dart, mensaje_chat.dart
│   │   ├── local/ prefs.dart
│   │   ├── services/ auth_service.dart, chat_service.dart
│   │   └── repositories/ usuario_repo.dart, viaje_repo.dart, encomienda_repo.dart,
│   │                     rating_repo.dart, ciudades_repo.dart, chatbot_repo.dart
│   └── features/
│       ├── auth/        login_screen, registro_screen, recuperar_screen
│       ├── perfil/      completar_perfil_screen, perfil_screen
│       ├── rol/         role_redirector_screen, seleccionar_rol_screen
│       ├── remitente/   home_remitente, crear_encomienda_screen, mis_encomiendas_screen,
│       │                encomienda_detalle_screen, buscar_viajeros_screen
│       ├── viajero/     home_viajero, registrar_viaje_screen, mi_viaje_screen,
│       │                encomiendas_disponibles_screen, mis_entregas_screen
│       ├── chat/        conversaciones_screen, chat_screen
│       ├── rating/      rating_form_screen, mis_calificaciones_screen
│       └── chatbot/     chatbot_screen
├── test/                                   ← pruebas de modelos, repositorios y widgets
└── README.md
```

## 4.4 Pantallas y navegación

```text
Splash ─► ¿sesión? ──no──► Login ─┬─► Registro
                │                 └─► Recuperar contraseña
               sí
                ▼
        ¿perfil completo? ──no──► Completar perfil (POST /api/users/register)
                │ sí
                ▼
        ¿rol guardado? ──no──► Seleccionar rol
                │ sí
     ┌──────────┴───────────┐
     ▼                      ▼
 REMITENTE (bottom nav)          VIAJERO (bottom nav)
 • Mis encomiendas [tabs x estado]  • Mi viaje / Registrar viaje
     └► Detalle encomienda          • Encomiendas disponibles (mi ruta)
         ├► Chat con viajero            └► Detalle → Tomar
         ├► Cancelar                 • Mis entregas
         └► Calificar viajero            └► Detalle → Chat / Marcar entregada / Calificar
 • Nueva encomienda (FAB)          • Chats
 • Buscar viajeros                 • Perfil (cambiar rol, calificaciones, cerrar sesión)
 • Chats · Perfil · Asistente IA
```

El patrón **maestro-detalle** (sesiones 14–15) aparece en: lista de encomiendas → detalle, disponibles → detalle,
conversaciones → chat. Se pasa el objeto (o el `_id`) como argumento de la ruta.

## 4.5 Configuración de Firebase (punto crítico)

- El `google-services.json` del curso registra **dos apps Android**: `com.lapticon.app` y `com.example.lapticon_clean`.
  El `applicationId` en `android/app/build.gradle(.kts)` **debe ser uno de esos** (propuesta: `com.lapticon.app`) o Firebase no inicializa.
- Agregar el plugin `com.google.gms.google-services` en Gradle (o usar `flutterfire configure` si el profesor nos da acceso al proyecto).
- **Autenticación: solo correo y contraseña por ahora** (decisión 22-oct). Si más adelante se agrega Google Sign-In, hará falta
  que el profesor registre el SHA-1 del equipo (`cd android && ./gradlew signingReport`) en el proyecto `lapticon-eba31`.
- Verificar que el proveedor *Email/Password* esté habilitado en Firebase (el usuario de prueba de Postman lo usa, así que debería estarlo).
- iOS: solo hay un cliente OAuth iOS para `com.example.lapticonClean` y no hay `GoogleService-Info.plist` → fuera de alcance.

## 4.6 Manejo de errores y estados (contrato interno)

| Código | Qué muestra la app |
|---|---|
| sin red / timeout | "Sin conexión" o "El servidor está despertando, intenta de nuevo" (Render en frío) + botón reintentar |
| 400 | El mensaje del backend (p. ej. "Ya tienes un viaje activo") |
| 401 | Refresca token y reintenta 1 vez; si persiste → cerrar sesión e ir a Login |
| 403 | "No tienes permiso para esta acción" |
| 404 | Estado vacío ("Aún no tienes viajes") |
| 5xx | "Error del servidor" + reintentar |

Cada lista usa un `AsyncValue` (loading / data / error) con vistas de carga, vacío y error, y pull-to-refresh.

## 4.7 Entorno de desarrollo necesario

- Flutter SDK estable + Android Studio (SDK y emulador) o dispositivo físico en modo depuración.
- VS Code o Android Studio con extensiones Flutter/Dart.
- Postman con la colección del curso importada (para verificar el contrato).
- Git + cuenta GitHub (repositorio **privado** si se suben `google-services.json` o credenciales de prueba).
- Dos cuentas de prueba propias (una remitente, una viajera) y, para la demo, dos dispositivos/emuladores.
