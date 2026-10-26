# Lapticon · App móvil en Flutter — Planeación (2.º corte, Computación Móvil)

## Repositorios

Este repositorio es la **documentación** del proyecto (planeación, contrato de la API, diseño, decisiones, bitácora y
referencias del curso). El código vive en dos repositorios propios:

| Repositorio | Qué tiene |
|---|---|
| [**…-lapicon-flutter**](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter) | App móvil en Flutter (Android e iOS), sus pruebas y el CI que publica el APK |
| [**…-lapicon-pwa**](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-pwa) | La misma app como PWA instalable (React + TypeScript), sus pruebas y su CI |
| **…-lapicon** (este) | `docs/`, `referencias/`, `CLAUDE.md` |

**[⬇️ Descargar Lapticon para Android (lapticon.apk)](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter/releases/latest/download/lapticon.apk)** — siempre la última
versión, compilada con cada cambio en `main` del repo de Flutter. iPhone: ver [docs/08](docs/08-compilacion-y-pruebas-ios.md).

### Organización local

Los repositorios de código se clonan **dentro** de esta carpeta (este repo los ignora), así las rutas relativas
`../referencias` y `../docs` siguen funcionando:

```text
proyecto_2_corte/          ← este repo (documentación)
├── docs/  referencias/  CLAUDE.md
├── lapticon_app/          ← git clone …-lapicon-flutter lapticon_app
└── aplicacion_pwa/        ← git clone …-lapicon-pwa aplicacion_pwa
```

```bash
git clone https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter.git lapticon_app
```

```bash
git clone https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-pwa.git aplicacion_pwa
```

> Planeación elaborada el 22-oct-2026 a partir del material de Canvas
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
| 8 | [docs/08-plan-rediseno-ui.md](docs/08-plan-rediseno-ui.md) · [docs/08-compilacion-y-pruebas-ios.md](docs/08-compilacion-y-pruebas-ios.md) | Rediseño v2 de la interfaz · compilar y probar en iOS |
| 9 | [docs/09-lecciones-ux-rediseno.md](docs/09-lecciones-ux-rediseno.md) | Lecciones de UX reutilizables (Flutter y PWA) |
| 10 | [docs/10-plan-migracion-pwa.md](docs/10-plan-migracion-pwa.md) | Plan y estado de la migración a PWA |
| ★ | [**docs/api/**](docs/api/README.md) | **Contrato de la API en Swagger** (OpenAPI 3.1): bodies, respuestas reales y endpoints que faltan. Abrir `docs/api/index.html` |
| ★ | [**docs/entregables/**](docs/entregables/README.md) | **Entregables del tablero**: semanas 0–4, UX/UI, documento técnico, guion del video, código fuente y sustentación |
| — | [docs/BITACORA.md](docs/BITACORA.md) | Qué se hizo en cada paso, errores y cómo se resolvieron |
| — | [App Flutter](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter) · [PWA](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-pwa) | Código (repositorios propios; ver su README para ejecutarlos) |
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
