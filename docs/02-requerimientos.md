# 2. Requerimientos de la app Lapticon (frontend Flutter)

Prioridad: **M** = obligatorio (lo exige el PDF/práctica) · **D** = deseable (suma nota o calidad) · **O** = opcional/extra.
La columna *Práctica* indica en qué entrega se demuestra (ver doc 05).

## 2.1 Actores

| Actor | Descripción |
|---|---|
| **Remitente** | Publica encomiendas (ruta, valor, observaciones, fecha límite), sigue su estado, chatea con el viajero y lo califica al recibir la entrega. |
| **Viajero** | Registra un viaje (vuelo real), busca encomiendas de su ruta, las toma, las entrega, chatea con el remitente y lo califica. |
| Backend Lapticon | API REST en `https://lapticon-backend.onrender.com` (no lo modificamos). |
| Firebase (`lapticon-eba31`) | Auth (identidad) y Firestore (mensajes del chat). |

Un mismo usuario puede ser remitente o viajero; el rol se elige después del login (y debe poder cambiarse).

## 2.2 Requerimientos funcionales

### RF-A · Autenticación y perfil (Práctica 1)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-A1 | Registro de cuenta con correo y contraseña usando `firebase_auth` (validar formato de correo y contraseña ≥ 6 caracteres). | M |
| RF-A2 | Inicio de sesión con correo y contraseña. | M |
| RF-A3 | Inicio de sesión con Google (`google_sign_in`). **Pospuesto (decisión 22-oct): por ahora solo correo y contraseña.** Requeriría registrar el SHA-1 en Firebase. | O (después) |
| RF-A4 | Recuperar contraseña (`sendPasswordResetEmail`). | D |
| RF-A5 | Mantener la sesión abierta al reabrir la app (`authStateChanges`) y cerrar sesión. | M |
| RF-A6 | Tras el primer login, completar perfil: nombre, apellido, teléfono, nacionalidad (lista de países de `/api/ciudades/paises`) → `POST /api/users/register`. | M |
| RF-A7 | Ver y editar mi perfil (`GET`/`PUT /api/users/{uid}`). | M |
| RF-A8 | Toda llamada protegida envía `Authorization: Bearer <idToken>` obtenido con `user.getIdToken()` (refrescado automáticamente). | M |
| RF-A9 | Si el backend responde 401, refrescar el token una vez y reintentar; si vuelve a fallar, cerrar sesión. | D |

### RF-B · Roles y navegación (Práctica 2)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-B1 | Pantalla de selección de rol (Remitente / Viajero) tras el login (`RoleRedirectorScreen`). | M |
| RF-B2 | Menú/inicio distinto por rol (barra de navegación inferior con las secciones del rol). | M |
| RF-B3 | Guardar el rol **en el perfil del backend** y usar `SharedPreferences` solo como caché (reto 1). *Si el backend no acepta el campo `rol`, se deja en caché local y se documenta.* | M |
| RF-B4 | Cambiar de rol desde el perfil. | D |

### RF-C · Encomiendas — rol Remitente (Práctica 3)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-C1 | Formulario para crear encomienda: ciudad origen, ciudad destino (autocompletar con `/api/ciudades/ciudades`), observaciones, moneda, valor y fecha límite (si el backend la acepta). Validación de todos los campos. → `POST /api/encomiendas`. | M |
| RF-C2 | Listar mis encomiendas (`GET /api/encomiendas`) **agrupadas por estado**: disponibles, tomadas, entregadas, vencidas, canceladas (pestañas o filtros). | M |
| RF-C3 | Detalle de la encomienda (patrón **maestro-detalle**): datos, estado, viajero asignado, acciones. | M |
| RF-C4 | Cancelar mi encomienda (`PUT /api/encomiendas/{id}/estado` con `cancelada`) mientras esté disponible. | M |
| RF-C5 | Buscar viajeros que salen de una ciudad (`GET /api/viajes/buscar?ciudad=`) para ver quién podría llevar el paquete. | D |
| RF-C6 | Ver la calificación promedio de un viajero (`GET /api/ratings/{uid}`). | D |
| RF-C7 | Ver viajes sugeridos con puntaje del matching IA (reto 2). *Solo si el profesor habilita el endpoint.* | O |

### RF-D · Viajes — rol Viajero (Práctica 4)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-D1 | Registrar viaje: número de vuelo, ciudad origen, ciudad destino, fecha → `POST /api/viajes`. | M |
| RF-D2 | Validar el vuelo contra AeroDataBox (`/api/vuelos/{numero}/{fecha}`) antes o durante el registro, con indicador de carga. | M |
| RF-D3 | Respetar la regla "un viaje activo a la vez": si el backend responde 400, mostrar el mensaje y llevar al viaje activo. | M |
| RF-D4 | Ver mi viaje disponible (`GET /api/viajes/disponible`) y el historial (`GET /api/viajes`). | M |
| RF-D5 | Buscar encomiendas disponibles para la ruta de mi viaje (`GET /api/encomiendas/disponibles?origen=&destino=`). | M |
| RF-D6 | Tomar una encomienda (`PUT /api/encomiendas/tomar/{id}`) con confirmación. | M |
| RF-D7 | Ver las encomiendas que tomé y su estado. | M |

### RF-E · Chat (Práctica 5)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-E1 | Abrir chat entre remitente y viajero de una encomienda tomada. ID del chat: `uid1_uid2` con los uid **ordenados**. | M |
| RF-E2 | Mensajes en tiempo real leyendo/escribiendo en Firestore (`chats/{chatId}/...`) con `StreamBuilder`. | M |
| RF-E3 | Consultar `GET /api/chats/estado/{chatId}` y **bloquear el envío** si el chat está cerrado (reto 4). | M |
| RF-E4 | Lista de mis conversaciones. | D |
| RF-E5 | Indicador de no leídos / hora del mensaje. | O |

### RF-F · Entrega y calificación (Práctica 6)

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-F1 | El viajero marca la encomienda como **entregada** (`PUT /api/encomiendas/{id}/estado`). | M |
| RF-F2 | Al quedar entregada, ambas partes pueden calificar (1–5 estrellas + comentario) → `POST /api/ratings` con `rolDestino` correcto. | M |
| RF-F3 | Ver calificaciones recibidas (total, promedio y lista) en el perfil. | M |
| RF-F4 | Tras calificar ambos, el chat aparece cerrado (lo cierra el backend) y la UI lo refleja. | M |

### RF-G · Extras

| ID | Requerimiento | Prioridad | Relación |
|---|---|---|---|
| RF-G1 | Asistente/chatbot (`POST /api/chatbot`) en una pantalla tipo chat. | D | Servicios externos / IA (PDF) |
| RF-G2 | Caché local de la lista de ciudades/países (evita descargar ~2.000 ciudades cada vez). `shared_preferences` o archivo local. | D | Persistencia local vs remota (PDF) |
| RF-G3 | Detección de conectividad y aviso "sin conexión". | D | Manejo de fallos (PDF) |
| RF-G4 | Sugerir la ciudad de origen usando el **GPS** (`geolocator` + geocoding). | O | Sesión 13 (sensores en Flutter) |
| RF-G5 | Ícono de app y splash propios. | D | Presentación de la demo |

## 2.3 Requerimientos no funcionales

| ID | Requerimiento |
|---|---|
| RNF-1 | **Seguridad:** nunca guardar contraseñas; el token solo en memoria (lo maneja Firebase). No subir claves/credenciales de prueba a un repo público. |
| RNF-2 | **Arquitectura por capas** (presentación / dominio / datos) y separación de modelos, repositorios y servicios (ver doc 04). |
| RNF-3 | **Manejo de errores**: mensajes claros para 400 (regla de negocio), 401 (sesión), 403 (sin permiso), 404, 5xx y timeouts. |
| RNF-4 | **Arranque en frío del backend** (Render free puede tardar ~30–60 s): timeout amplio en la primera llamada + mensaje "despertando el servidor…". |
| RNF-5 | **Estados de carga, vacío y error** en todas las listas. Pull-to-refresh. |
| RNF-6 | **Usabilidad:** Material 3, textos en español, formularios con validación en línea, accesible (contraste, tamaños táctiles ≥ 48 dp). |
| RNF-7 | **Plataforma:** Android (minSdk 23+). iOS fuera de alcance salvo que el profesor entregue `GoogleService-Info.plist`. |
| RNF-8 | **Calidad:** `flutter analyze` sin errores; pruebas unitarias de modelos/repositorios y al menos un widget test por flujo crítico. |
| RNF-9 | **Control de versiones:** repositorio Git con commits por práctica, ramas por funcionalidad y tags `practica-1` … `practica-6`, `v1.0`. |
| RNF-10 | **Documentación:** README con instalación, arquitectura, capturas y decisiones (cubre el 10 % de "repositorio y documentación"). |

## 2.4 Criterios de aceptación del flujo completo (demo final)

1. Usuario A se registra, completa perfil y elige **Remitente**; crea una encomienda Bogota → Miami.
2. Usuario B se registra, elige **Viajero**, registra un vuelo válido Bogota → Miami (validado) y ve la encomienda de A en "disponibles".
3. B toma la encomienda → en el teléfono de A aparece como **tomada** con B como viajero.
4. A y B chatean en tiempo real.
5. B marca **entregada** → ambos se califican → el chat queda **cerrado** y no permite enviar.
6. Con el backend devolviendo 401/400/403 la app muestra mensajes adecuados y no se cierra.

## 2.5 Fuera de alcance (lo hace el backend, no el frontend)

- Implementar el microservicio de matching IA y configurar `MATCHING_API_URL` (reto 2, parte backend).
- Reemplazar la actualización *lazy* de vencidas/completados por un cron (reto 3).
- Cambios en el modelo de usuario del backend para guardar el rol (reto 1, parte backend).

Si el profesor espera que también hagamos estos retos, hay que pedir acceso al repositorio del backend (ver doc 06).
