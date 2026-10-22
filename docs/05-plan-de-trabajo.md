# 5. Plan de trabajo (22-oct → 05-dic-2026)

Basado en el "Plan de desarrollo · 5 semanas" de *session 10.pdf*, ajustado al calendario real del cronograma.
**Supuesto:** las 5 entregas empiezan la semana del 27-oct. Si el profesor ya empezó a contar desde antes, hay que comprimir
las semanas 0–1 (ver doc 06, pregunta P1).

## Vista general

| Semana | Fechas | Sesión | Prácticas | Entrega (revisión en clase sobre el repo) |
|---|---|---|---|---|
| 0 | 22-oct → 26-oct | 13 | Preparación | Planeación + entorno + contrato verificado |
| 1 | 27-oct → 31-oct | 14 | **P1** Autenticación | Repo + login funcionando |
| 2 | 03-nov → 07-nov | 15 | **P2** Roles · **P3** (crear) | Roles + crear encomienda |
| 3 | 10-nov → 14-nov | 16 | **P3** (listas) · **P4** Viajes | Flujo remitente–viajero |
| 4 | 17-nov → 21-nov | 17 | **P5** Chat · **P6** Entrega y calificación | Ciclo completo de la encomienda |
| 5 | 24-nov → 28-nov | 18 | Cierre | App final + documentación |
| 19 | 30-nov → 05-dic | — | Parcial final | Demo y sustentación |

---

## Semana 0 — Preparación (ahora)

- [ ] Leer esta planeación y resolver las decisiones del README.
- [ ] Conseguir la documentación de la API (`claude.ai/artifact/3j2Hm5PgBJQGq25ye2Nuqz`) y guardarla en `referencias/`.
- [ ] Enviar al profesor las preguntas del doc 06 (fechas de entrega, rol en backend, Firestore, endpoints faltantes).
- [ ] Instalar/actualizar Flutter estable y Android Studio; `flutter doctor` sin errores.
- [ ] Importar la colección y el environment de Postman (`referencias/`), crear **cuenta propia** y ejecutar la carpeta 0–7.
- [ ] Guardar las respuestas reales en `referencias/respuestas/` y completar la checklist 3.5 del doc 03.
- [x] Investigación y sistema de diseño UX/UI → `docs/07-diseno-ux-ui.md` (wireframes de texto por pantalla).
- [ ] Crear el repositorio Git (privado) con este README y `docs/`.

## Semana 1 — Práctica 1: Autenticación

- [x] Proyecto `lapticon_app/` + `setup.sh` (genera Android, `applicationId = com.lapticon.app`, dependencias).
- [x] Firebase inicializado con `lib/firebase_options.dart` generado desde el `google-services.json`.
- [x] `AuthService`: registro, login correo/contraseña, logout, `authStateChanges`, recuperar contraseña (Google Sign-In pospuesto).
- [x] `ApiClient` con Bearer idToken, reintento ante 401, timeouts, aviso de servidor dormido y `ApiException`.
- [x] Pantalla completar perfil → `POST /api/users/register`; perfil → `GET /api/users/{uid}` (**primera llamada protegida**).
- [x] Tema Material 3 del sistema de diseño · [ ] ícono y splash nativos.
- [ ] **Ejecutar en el teléfono/emulador** (`bash setup.sh && flutter run`) y probar con una cuenta propia.
- **Entrega:** repo + login funcionando + captura del 200 en perfil propio. Tag `practica-1`.
- Adelantado de la Práctica 2: elegir rol, inicio por rol, editar perfil y cambiar de rol.

> **Avance 22-oct:** el código de las prácticas 2 a 6 ya está escrito (4 agentes en paralelo) y analiza limpio contra Flutter 3.47. Falta: ejecutarlo en el teléfono, verificar el contrato real de la API y ajustar.

## Semana 2 — Práctica 2 (Roles y navegación) + Práctica 3 (crear encomienda)

- [ ] `go_router` con redirecciones: sin sesión → login; sin perfil → completar perfil; sin rol → seleccionar rol.
- [ ] Seleccionar rol; guardarlo en backend (`PUT /api/users/{uid}` con `rol`, si se acepta) y en `SharedPreferences` como caché.
- [ ] Menús por rol (bottom navigation).
- [ ] `CiudadesRepo` con caché local y autocompletar ciudades.
- [ ] Formulario crear encomienda con validaciones → `POST /api/encomiendas`.
- [ ] Editar perfil (`PUT /api/users/{uid}`) y prueba del 403 documentada.
- **Entrega:** roles + crear encomienda. Tags `practica-2`, `practica-3a`.

## Semana 3 — Práctica 3 (listas) + Práctica 4 (Viajes)

- [ ] Mis encomiendas con pestañas por estado + pull-to-refresh + estados vacío/error.
- [ ] Detalle de encomienda (maestro-detalle) y cancelar.
- [ ] Registrar viaje con validación del vuelo (indicador de carga) y manejo del 400 "viaje activo".
- [ ] Mi viaje disponible / historial.
- [ ] Encomiendas disponibles para mi ruta → detalle → **tomar**.
- [ ] Remitente: buscar viajeros por ciudad y ver su calificación.
- **Entrega:** flujo remitente–viajero (A crea, B toma). Tags `practica-3`, `practica-4`.

## Semana 4 — Práctica 5 (Chat) + Práctica 6 (Entrega y calificación)

- [ ] `ChatService` sobre Firestore (`chats/{uid1_uid2}/mensajes`), `StreamBuilder`, envío y orden por fecha.
- [ ] Consultar `/api/chats/estado/{chatId}` y bloquear el envío si está cerrado.
- [ ] Lista de conversaciones.
- [ ] Viajero marca **entregada**; formulario de calificación (estrellas + comentario) → `POST /api/ratings`.
- [ ] Perfil: calificaciones recibidas (total, promedio, lista).
- [ ] Verificar que el chat se cierra cuando ambos califican.
- **Entrega:** ciclo completo de la encomienda. Tags `practica-5`, `practica-6`.

## Semana 5 — Cierre

- [ ] Pruebas: unitarias (modelos `fromJson`, validadores, `ApiClient` con mocks), widget tests de login y crear encomienda.
- [ ] Prueba de extremo a extremo manual con dos dispositivos (criterios 2.4 del doc 02) y grabación de video de respaldo.
- [ ] Extras si hay tiempo: chatbot, aviso sin conexión, GPS para ciudad de origen.
- [ ] Revisión de UI, accesibilidad y mensajes de error.
- [ ] README final: instalación, arquitectura, capturas, decisiones (tecnología, persistencia, manejo de fallos), limitaciones conocidas.
- [ ] APK de release firmado para la demo. Tag `v1.0`.

## Semana 19 — Demo y sustentación

Preparar para argumentar (resultado de aprendizaje del PDF): por qué Flutter, cómo fluye el idToken, persistencia local vs remota
(rol en backend vs `SharedPreferences`, caché de ciudades), cómo se manejan los fallos (401/400/sin red/arranque en frío) y cómo funciona el chat en tiempo real.

## Convenciones de repositorio

- Rama `main` estable; ramas `feat/p1-auth`, `feat/p3-encomiendas`, etc.; merge por pull request.
- Commits en español con prefijo: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`.
- No subir: claves propias, contraseñas, `key.properties`, keystores. Si el repo es público, tampoco `google-services.json`.
