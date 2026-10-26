# Semana 0 · Descubrimiento de la API

> Entregable del tablero: **"Sem 0 — Descubrimiento API"**. Estado: ✅ hecho (22-oct-2026).
> Detalle completo del contrato: [`docs/03-contrato-api.md`](../03-contrato-api.md).
> **Versión visual (Swagger):** [`docs/api/`](../api/README.md) — abrir `docs/api/index.html`.

## 1. Objetivo

Conocer el backend compartido del curso antes de programar: qué endpoints existen, cómo se autentican, qué responden
de verdad (no solo lo que dice la documentación) y qué falla, para diseñar la app sobre el contrato real.

## 2. Cómo se hizo

1. Se importaron la colección y el environment de **Postman** del profesor (`referencias/`) y se cruzaron con el
   "Mapa de endpoints" de la presentación *session 10.pdf*.
2. Se crearon **dos cuentas propias** (un remitente y un viajero), nunca la cuenta de prueba compartida del curso.
3. Se obtuvo el **idToken de Firebase** de cada cuenta con un script propio (`tool/obtener_token.sh`, guarda el token
   fuera del repositorio) y se llamó **cada endpoint con `curl`** enviando `Authorization: Bearer <idToken>`.
4. Las respuestas reales se guardaron en `referencias/respuestas/` (48 archivos, con teléfono y correo enmascarados).
   Esas mismas respuestas alimentan las pruebas de contrato de las dos apps.
5. Con todo eso se escribió el contrato en **OpenAPI 3.1** ([`docs/api/openapi.yaml`](../api/openapi.yaml)) y un visor
   **Swagger UI** ([`docs/api/index.html`](../api/index.html)): 28 operaciones con sus bodies, esquemas y respuestas
   reales, marcadas ✅ funciona · ⚠️ falla o difiere · 🆕 **falta en el backend** (8 propuestas, cada una con el
   motivo). Es más práctico que la colección de Postman para revisar los bodies y ver qué hace falta.

## 3. Datos de conexión

| Elemento | Valor |
|---|---|
| Backend | `https://lapticon-backend.onrender.com` (Node/Express + MongoDB, Render gratuito) |
| Identidad | Firebase Auth, proyecto `lapticon-eba31` |
| Autenticación de la API | `Authorization: Bearer <idToken>` en todo, salvo `GET /api/ratings/{uid}` y `/api/ciudades/*` |
| Formato de error | Siempre `{ "error": "…" }` |
| Chat | No pasa por el backend: va directo a **Firestore** |

## 4. Mapa de endpoints verificado

| Recurso | Endpoint | Resultado real |
|---|---|---|
| Usuarios | `POST /api/users/register` | ✅ 201 `{ message, user }` (crea o actualiza) |
| | `GET /api/users/{uid}` | ✅ 200 `{ user }` · 403 si es otro usuario |
| | `PUT /api/users/{uid}` | ✅ 200 · **ignora el campo `rol`** |
| Viajes | `POST /api/viajes` | ✅ 201 · **400 si ya hay un viaje activo** |
| | `GET /api/viajes` · `/disponible` · `/buscar?ciudad=` | ✅ (`/disponible` sin viaje → 404) |
| Vuelos | `GET /api/vuelos/{numero}/{fecha}` | ⚠️ **500**: falta `RAPIDAPI_KEY` en el servidor |
| Encomiendas | `POST /api/encomiendas` | ✅ 201 · **no valida el body** |
| | `GET /api/encomiendas` · `/disponibles?origen=&destino=` | ✅ (`/disponibles` trae `remitenteNombre`, no el uid) |
| | `PUT /api/encomiendas/tomar/{id}` | ✅ 200 `{ mensaje }` (sin la encomienda) |
| | `PUT /api/encomiendas/{id}/estado` | ✅ estados: `disponible, tomada, vencida, entregada, recibida` |
| Calificaciones | `POST /api/ratings` · `GET /api/ratings/{uid}` | ✅ · fuera de 1–5 da **500** (no 400) |
| Chat | `GET /api/chats/estado/{chatId}` | ⚠️ **500** siempre (o 404 con ids inexistentes) |
| Catálogo | `GET /api/ciudades/paises` · `/ciudades` | ✅ listas de texto (~2.000 ciudades, sin tildes) |
| Asistente | `POST /api/chatbot` | ⚠️ **500**: la clave de OpenRouter del servidor no es válida |

## 5. Hallazgos que cambiaron el diseño de la app

| Hallazgo | Decisión en la app |
|---|---|
| No existe el estado `cancelada` | "Retirar" una encomienda la deja `vencida` |
| `fechaVencimiento` se ignora (vence al mes) | No se pide la fecha; se muestra la automática |
| El backend no guarda el `rol` | El rol vive en el dispositivo (`SharedPreferences` / `localStorage`) |
| `POST /api/encomiendas` acepta cualquier cosa | La app valida todos los campos antes de enviar |
| `/disponibles` no trae el uid del remitente | La app cruza con mis encomiendas para no ofrecer las propias |
| Calificar no guarda la encomienda | La app recuerda localmente qué entregas ya calificó |
| Render gratuito "se duerme" (~60 s) | Tiempo de espera de 75 s y aviso "Despertando el servidor…" |
| Las fechas de viaje llegan como medianoche UTC | Se leen como día del calendario (si no, en Colombia se ven un día antes) |
| Tres endpoints responden 500 | La app los llama y muestra un mensaje claro sin bloquear el flujo |

## 6. Evidencia

- Contrato OpenAPI y visor Swagger: [`docs/api/`](../api/README.md).
- Respuestas reales: `referencias/respuestas/*.json`.
- Pruebas de contrato: `test/contrato_test.dart` (Flutter) y `src/datos/contrato.test.ts` (PWA).
- Comprobación automática contra el servidor real: `npm run humo` en la PWA (13/13 endpoints responden como espera la
  app, 26-oct-2026).
- Preguntas enviadas al profesor: [`docs/06-riesgos-y-preguntas.md`](../06-riesgos-y-preguntas.md).
