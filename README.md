# Lapticon · App móvil en Flutter — Planeación (2.º corte, Computación Móvil)

## 📲 Descargar la app

**[⬇️ Descargar Lapticon para Android (lapticon.apk)](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon/releases/latest/download/lapticon.apk)**

Siempre es la última versión: se compila sola con cada cambio en `main`. Ábrela en el teléfono y permite
"instalar apps desconocidas". Las versiones anteriores están en [Releases](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon/releases).
iPhone: ver [docs/08](docs/08-compilacion-y-pruebas-ios.md).

**Versión web instalable (PWA):** [`aplicacion_pwa/`](aplicacion_pwa/README.md) — la misma app, con el mismo backend,
Firebase y diseño, para abrir desde el navegador del celular e instalar en la pantalla de inicio (plan en
[docs/10](docs/10-plan-migracion-pwa.md); despliegue en Cloudflare Pages pendiente).

> Estado: **planeación** (sin código todavía). Elaborada el 22-oct-2026 a partir del material de Canvas
> (`canvas/04-datos/computacion-movil`): páginas de sesiones, cronograma, PDA, presentación *"session 10.pdf"*
> (Lapticon – cómo funciona la app) y los archivos Postman/Firebase que adjuntó el profesor.

## Resumen en 30 segundos

- **Qué es Lapticon:** una app que une a un **remitente** (quiere enviar un paquete) con un **viajero** (ya viaja a ese destino).
  El remitente publica una *encomienda*, el viajero registra su *viaje* (vuelo real), la toma, se coordinan por *chat*
  y al final se *califican* mutuamente.
- **Qué nos toca:** solo el **frontend móvil**. El backend (Node/Express + MongoDB, en Render) y el proyecto Firebase
  ya existen y son los mismos para todos los equipos. Tecnología del cliente libre → elegimos **Flutter**.
- **Requisito duro del profesor:** consumir la API REST enviando el **idToken de Firebase** (`Authorization: Bearer <idToken>`).
- **Entregables:** 6 prácticas incrementales (login → roles → encomiendas → viajes → chat → entrega y calificación)
  en 5 entregas semanales + app final + demo/sustentación + repositorio documentado.
- **Fecha límite práctica:** semana 19 del cronograma (30-nov → 05-dic-2026) es el parcial final.

## Documentos

| # | Documento | Contenido |
|---|-----------|-----------|
| 1 | [docs/01-contexto-del-curso.md](docs/01-contexto-del-curso.md) | Qué cubre el 2.º corte (sesiones 11–18), cronograma, evaluación e inconsistencias del material |
| 2 | [docs/02-requerimientos.md](docs/02-requerimientos.md) | Requerimientos funcionales y no funcionales, historias de usuario por rol, criterios de aceptación, alcance |
| 3 | [docs/03-contrato-api.md](docs/03-contrato-api.md) | Todos los endpoints (Postman + PDF), modelos de datos, estados, reglas de negocio y lo que falta verificar |
| 4 | [docs/04-arquitectura-flutter.md](docs/04-arquitectura-flutter.md) | Arquitectura por capas, estructura de carpetas, paquetes, pantallas y navegación, configuración de Firebase |
| 5 | [docs/05-plan-de-trabajo.md](docs/05-plan-de-trabajo.md) | Cronograma semana a semana con tareas, entregables y checklist de cada práctica |
| 6 | [docs/06-riesgos-y-preguntas.md](docs/06-riesgos-y-preguntas.md) | Riesgos técnicos, mitigación y **preguntas para hacerle al profesor** antes de programar |
| 7 | [docs/07-diseno-ux-ui.md](docs/07-diseno-ux-ui.md) | Investigación UX (referentes, confianza, formularios, accesibilidad), personas, principios, sistema de diseño y especificación de pantallas |
| — | [lapticon_app/](lapticon_app/) | Código de la app Flutter (ver su README para ejecutarla) |
| — | [referencias/](referencias/) | Copia de la colección y el environment de Postman, del `google-services.json` y del PDF del proyecto (*session 10*) |

## Decisiones tomadas (22-oct-2026)

- Se sigue **solo el material nuevo** del profesor actual (Flutter). El material heredado (MAUI, Xamarin, TFS, plan de actividades antiguo) se ignora.
- **Autenticación:** solo **correo y contraseña** por ahora; Google Sign-In queda pospuesto.
- **Plataforma:** Android primero.

## Pendientes antes de escribir código

1. **Documentación de la API** ("Lapticon en Apiary"): `https://claude.ai/artifact/3j2Hm5PgBJQGq25ye2Nuqz` (no es pública).
   Si se consigue, guardarla en `referencias/`.
2. **Confirmar con el profesor** las preguntas de [06-riesgos-y-preguntas.md](docs/06-riesgos-y-preguntas.md) (fechas reales de las
   5 entregas, rol en el backend, endpoints faltantes y la colección de chat en Firestore).
3. **Equipo**: ¿individual o en pareja?
4. **Gestión de estado**: propuesta **Riverpod** (alternativa más simple: Provider). Ver doc 04.
