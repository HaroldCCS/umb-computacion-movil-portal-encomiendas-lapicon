# Lapticon — contexto para Claude Code

Proyecto del 2.º corte de Computación Móvil (UMB, Ingeniería de Software). Estudiante: Harold Camargo.
Idioma de trabajo: **español** (código con nombres en español, UI en español de "tú").

## Qué es
App Flutter (solo frontend) que une a un **remitente** (envía un paquete) con un **viajero** (ya viaja a ese destino).
Backend ya existe y es compartido por todo el curso: `https://lapticon-backend.onrender.com` (Node/Express + MongoDB, Render
gratuito → primera petición puede tardar ~60 s). Identidad con Firebase Auth (proyecto `lapticon-eba31`); toda ruta protegida
exige `Authorization: Bearer <idToken>`. El chat va directo a Firestore.

## Dónde está todo
- `docs/01..07` — contexto del curso, requerimientos, **contrato de la API** (03), arquitectura (04), plan (05),
  riesgos y preguntas al profesor (06), **sistema de diseño UX/UI** (07). Léelos antes de cambiar comportamiento o UI.
- `referencias/` — colección y environment de Postman, `google-services.json`, PDF del enunciado ("session 10").
- `lapticon_app/` — la app Flutter. **Es otro repositorio** (`…-lapicon-flutter`) clonado aquí e ignorado por este;
  sus commits y push se hacen DENTRO de esa carpeta. Su `README.md` explica puesta en marcha y problemas comunes.
- `aplicacion_pwa/` — la PWA. **Otro repositorio** (`…-lapicon-pwa`) clonado aquí, igual que el de Flutter.
- Este repositorio (`…-lapicon`) es solo documentación: `docs/`, `referencias/`, `CLAUDE.md`, `README.md`.

## Estado (22-oct-2026)
- Prácticas 1–6 **escritas** (auth, perfil, roles, remitente, viajero, chat Firestore, calificaciones, asistente IA).
- Analizado limpio contra el código fuente de Flutter 3.47 / Dart 3.13, pero **nunca se ha compilado ni ejecutado en un
  dispositivo** (se escribió sin SDK de Flutter disponible). Espera ajustes de Gradle/Android y del contrato real de la API.
- `lib/firebase_options.dart` y `android/` NO están en el repo: los genera `lapticon_app/setup.sh`.

## PWA (`aplicacion_pwa/`, repo …-lapicon-pwa, 24-oct-2026)
Migración completa de la app a PWA (React 19 + TS + Vite + TanStack Query + React Router + Tailwind con los tokens v2).
Plan y estado en `docs/10`; uso en `aplicacion_pwa/README.md`. Comandos: `npm run typecheck && npm run lint && npm test
&& npm run e2e`; `npm run humo` prueba el servidor real en solo lectura. La clave de Firebase va en
`aplicacion_pwa/.env.local` (no se sube). Mismos nombres de componentes, mismas claves locales y mismo esquema de chat
que Flutter: si cambia uno, revisar el otro. Despliegue en Cloudflare Pages pendiente (lo hace Harold).

## Trabajo pendiente (28-oct-2026) — empezar por aquí
**`docs/11-plan-swagger-oficial.md`** es el plan vigente y basta para desarrollar sin más contexto. Contiene:
- el Swagger oficial del profesor (`referencias/swagger-oficial.json`), con lo que corrige de nuestro contrato;
- sus dos observaciones de UX: que quede claro cuándo un viajero tomó la encomienda, y quitar "Verificar vuelo";
- cancelar viaje, que ya existe: `PATCH /api/viajes/{id}/estado`;
- el orden de los pasos y el criterio de aceptación de cada uno.

Cancelar encomienda sigue bloqueado, esperando al profesor.

## Decisiones tomadas
- Flutter, Android primero. Riverpod 3 (no usar `StateProvider`/`StateNotifierProvider`, están en legacy), go_router,
  `http`, `shared_preferences`, `google_fonts`, Firebase Auth + Cloud Firestore.
- Auth: **solo correo y contraseña** (Google Sign-In pospuesto).
- `applicationId = com.lapticon.app` (debe coincidir con `google-services.json`), `minSdk ≥ 23`.
- Material desde `package:flutter/material.dart`. Ojo: google_fonts ≥ 9 usa tipos de `material_ui`; por eso el tema usa
  solo `GoogleFonts.xxx(textStyle: ...)` y nunca los helpers `xxxTextTheme`.
- Solo se sigue el material nuevo del profesor (Flutter). Ignorar material heredado de .NET MAUI/Xamarin/TFS en Canvas.

## Arquitectura (resumen)
`lib/core` (red, router, tema, widgets del sistema de diseño) · `lib/data` (modelos con `fromJson` tolerante,
repositorios = contrato de la API) · `lib/features/<funcionalidad>` (pantallas, providers y rutas propias con prefijo).
Las pantallas nunca llaman a `http`/Firebase directo. Rutas compartidas y sus argumentos en `lib/core/router/routes.dart`.
La navegación de onboarding la decide `redirectFor()` según `SessionStatus`.

## Contrato del backend (verificado el 22-oct y el 28-oct-2026 con dos cuentas propias; detalle en docs/03 y docs/api/)
- Fuente oficial: Swagger del profesor (`referencias/swagger-oficial.json`). Su `servers` apunta a un host que no existe;
  la URL buena sigue siendo `lapticon-backend.onrender.com`.
- Respuestas: `/api/users` → `{ message?, user }`; errores siempre `{ error }`. Respuestas guardadas en `referencias/respuestas/`.
- El backend **no guarda `rol`** (vive en la app), **ignora `fechaVencimiento`** (vence al mes) y **`encomiendaId`** (rating).
- Estados de encomienda: `disponible, tomada, vencida, entregada, recibida` (no hay `cancelada`; retirar = `vencida`).
- Viajes: `PATCH /api/viajes/{id}/estado` con `cancelado` o `completado` (no `contactado`); un viaje cancelado se puede
  reactivar, pero la app no lo ofrece. `GET /api/viajes/disponibles` (pública) da el `nombreUsuario` de los viajeros de una ruta.
- Viajero: `GET /api/encomiendas/buscar?origen&destino` → `{ disponibles, tomadas }`, con `uid` y `remitenteNombre`.
  Incluye las propias, y `tomadas` solo trae las que están en `tomada` (lo entregado sigue en el celular).
- Chat: `GET /api/chats/estado/{uids ordenados con _}` → `{ estado: activo|cerrado, fechaCierre }`. Se abre al tomar y
  se cierra al marcar `entregada` (es por par de usuarios).
- `POST /api/encomiendas/emparejar-viajes` responde. `GET /api/vuelos/...` (pública) y `POST /api/chatbot` dan 500, por
  configuración del servidor. "Verificar vuelo" se quitó de la interfaz.
- Falta confirmar: las reglas de Firestore para el chat (propuesta en `features/chat/chat_service.dart`).
- Cuentas de prueba propias: el remitente y el viajero de Harold. Tokens con `lapticon_app/tool/obtener_token.sh` (fuera del repo).

## Comandos
```bash
cd lapticon_app
bash setup.sh          # una vez: genera android/, ajusta Gradle, pub add, firebase_options, analyze, test
flutter analyze
flutter test
flutter run            # con un emulador Android abierto o un teléfono conectado
```

## Reglas de trabajo
- Mantener `flutter analyze` sin errores ni warnings y `flutter test` en verde.
- Respetar el sistema de diseño de `docs/07` (tokens en `lib/core/theme/`, componentes en `lib/core/widgets/`),
  accesibilidad (≥48 dp, contraste, nada solo por color) y textos en español.
- Git: commits pequeños en español (`feat:`, `fix:`, `docs:`…), tags por práctica (`practica-1` … `practica-6`).
  No subir `lib/firebase_options.dart`, `google-services.json` ni credenciales (ya están en `.gitignore`).
