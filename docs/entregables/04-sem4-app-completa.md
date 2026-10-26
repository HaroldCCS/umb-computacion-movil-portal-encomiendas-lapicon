# Semana 4 · App completa

> Entregable del tablero: **"Sem 4 — Full APP"** (Prácticas 5 y 6: chat, entrega y calificación, más el asistente).
> Estado: ✅ hecha en Flutter (Android e iOS) y como PWA instalable.

## 1. Objetivo

Cerrar el ciclo de vida de la encomienda de punta a punta: publicar → tomar → coordinar por chat → entregar →
calificar, con las dos partes usando la app al mismo tiempo.

## 2. Lo que se agregó esta semana

| Función | Dónde vive | Comportamiento |
|---|---|---|
| **Chat en tiempo real** | Firestore `chats/{uidA_uidB}` + `mensajes/{autoId}` | El id une los dos uid **ordenados**: el mismo par siempre abre el mismo chat. Resumen y mensaje se escriben en **un solo lote** atómico. Muestra "Enviando…" hasta que el servidor confirma; sin conexión queda en cola. |
| Estado del chat | `GET /api/chats/estado/{chatId}` | Se consulta **antes de cada envío** (reto 4); si está cerrado, la barra de escribir se bloquea con la explicación. Hoy el endpoint da 500 → se trata como abierto. |
| Mis chats | Firestore `where participantes array-contains uid` | Nombre, ruta, último mensaje, "Tú:" y hora relativa. |
| **Marcar entregada** | `PUT /api/encomiendas/{id}/estado` → `entregada` | Irreversible: hay que **escribir ENTREGAR**. |
| **Calificar** | `POST /api/ratings` | 1–5 estrellas con etiqueta (Malo… Excelente), sugerencias rápidas y comentario. La app recuerda qué entregas calificó (el backend no lo guarda). |
| Reseñas | `GET /api/ratings/{uid}` | Promedio, barras por estrella y lista de comentarios. |
| **Asistente IA** | `POST /api/chatbot` | Chat con sugerencias según el rol. Hoy el servidor responde 500: el error aparece en la burbuja con "Reintentar". |
| **Avisos que llevan a la acción** | Rutas `?accion=calificar` / `?accion=entregar` | "Tu encomienda a Miami ya fue entregada · Califica al viajero" abre el detalle con el botón resaltado. Contadores en las pestañas (por calificar, por entregar). |

## 3. Flujo completo (criterios de aceptación)

1. A se registra, completa el perfil y elige **Remitente**; publica una encomienda Bogota → Miami.
2. B se registra, elige **Viajero**, registra un vuelo Bogota → Miami y ve la encomienda de A en Explorar.
3. B la toma → A la ve **En camino**, con B como viajero y su calificación.
4. A y B **chatean en tiempo real**.
5. B la marca **entregada** escribiendo ENTREGAR → A recibe el aviso → ambos se califican.
6. Con errores del backend (400, 401, 403, 500, sin red o servidor dormido) la app explica qué pasó y no se cierra.

Este flujo está automatizado en la PWA (E2E con **dos personas a la vez** en iPhone y Android) y se probó en el
emulador Android con las cuentas reales.

## 4. Las dos versiones de la app

| | App Flutter | PWA |
|---|---|---|
| Para qué | App nativa Android/iOS (lo que pide el curso) | La misma app desde el navegador del celular, instalable |
| Dónde | [APK de la última versión](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter/releases/latest/download/lapticon.apk) | https://lapticon.haroldsoftware.com |
| Tecnología | Flutter 3.47, Riverpod 3, go_router, Firebase | React 19, TypeScript, Vite, TanStack Query, Firebase web |
| Pruebas | 184 casos (unidad, widgets, accesibilidad) | 123 unitarias + 26 E2E en iPhone y Android |
| Extra | IPA sin firmar para iPhone | Funciona sin conexión, se instala en la pantalla de inicio |

Ambas comparten backend, proyecto de Firebase, esquema del chat y diseño: un chat abierto en una se ve en la otra.

## 5. Limitaciones conocidas (del servidor, no de la app)

- `/api/vuelos`, `/api/chats/estado` y `/api/chatbot` responden 500 (claves que faltan en el servidor).
- No hay endpoint de "encomiendas que tomé": la app las recuerda en el dispositivo donde se tomaron.
- Las reglas de Firestore permiten a cualquier usuario autenticado listar chats (reportado al profesor).

## 6. Evidencia

- Flutter: `lib/features/chat/`, `calificaciones/`, `asistente/`, `home/`; pruebas en `test/chat/`,
  `test/calificaciones/`, `test/asistente/`, `test/home/inicio_test.dart`.
- PWA: `src/funciones/chat/`, `calificaciones/`, `asistente/`; E2E `pruebas/e2e/flujos.spec.ts`.
- Bitácora de cada paso, con los errores encontrados: [`docs/BITACORA.md`](../BITACORA.md).
