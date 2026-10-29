# Sustentación

> Entregable del tablero: **"Sustentación"** (en el tablero, la flecha va del documento técnico a la sustentación:
> se sustenta con él). Estado: 📝 guía lista · ⏳ **falta presentarla** (Harold).
> Pesa el **20 %** según *session 10.pdf* ("Demo y sustentación técnica").

## 1. Qué hay que demostrar (resultados de aprendizaje del PDF)

1. Arquitectura cliente-servidor con servicios en la nube.
2. Autenticación con Firebase y consumo de una API protegida.
3. Datos en tiempo real y servicios externos (vuelos, IA).
4. **Argumentar decisiones:** tecnología, persistencia y manejo de fallos.

## 2. Estructura sugerida (≈ 10 minutos)

| Min. | Tema | Apoyo |
|---|---|---|
| 0–1 | **Problema y propuesta**: enviar paquetes con viajeros que ya van al destino | [Documento técnico §1](06-documento-tecnico.md) |
| 1–2 | **Alcance**: qué se construyó (6 prácticas + extras) y qué no (y por qué) | §2 |
| 2–4 | **Arquitectura**: app ↔ Firebase (Auth, Firestore) ↔ backend ↔ MongoDB; capas de la app | §4.1 y §4.2 (diagrama) |
| 4–8 | **Demo en vivo** del ciclo completo con dos dispositivos | Guion del [video](07-video-2-minutos.md) |
| 8–9 | **Decisiones y manejo de fallos** (lo que encontramos en el backend y cómo lo resolvimos) | §5 y §4.7 |
| 9–10 | **Calidad y repositorio**: pruebas, CI, tres repos, PWA desplegada | §6 y [código fuente](08-codigo-fuente-github.md) |

## 3. La demo

**Preparación:** igual que la del video (servidor despierto, dos sesiones listas, viajero con viaje activo).

**Plan B** si algo falla en vivo:
- Si el backend tarda: mostrar el aviso "Despertando el servidor…" y explicarlo; es parte del diseño.
- Si el wifi del salón falla: el **video de 2 minutos** como respaldo.
- Si un celular falla: la PWA en el computador (https://lapticon.haroldsoftware.com) con el otro rol.

## 4. Preguntas probables y cómo responderlas

| Pregunta | Respuesta corta |
|---|---|
| ¿Cómo fluye la autenticación? | Firebase Auth inicia la sesión y da un **idToken**; la app lo manda en `Authorization: Bearer` en cada llamada. El backend lo verifica con Firebase. Si responde 401, la app pide un token nuevo y reintenta una vez. |
| ¿Dónde se guarda cada dato? | Negocio (perfil, viajes, encomiendas, calificaciones) en el **backend/MongoDB**; mensajes en **Firestore**; rol, entregas calificadas y caché de ciudades en el **dispositivo**, porque el backend no los guarda o no hace falta pedirlos cada vez. |
| ¿Por qué el rol no está en el servidor? | Lo probamos: `PUT /api/users/{uid}` con `rol` responde 200 pero no lo guarda. La app lo intenta y, si no queda, lo recuerda localmente y lo avisa en el Perfil. |
| ¿Cómo funciona el chat en tiempo real? | Va directo a Firestore. El id del chat une los dos uid **ordenados**, así el mismo par abre siempre el mismo chat. Cada envío escribe el resumen y el mensaje en un solo lote atómico; la app escucha los cambios en vivo. |
| ¿Cómo se bloquea un chat cerrado? | Antes de cada envío consulta `GET /api/chats/estado/{chatId}`; si dice cerrado, deshabilita la barra de escribir. Hoy ese endpoint da 500 y la app lo trata como abierto para no bloquear a nadie. |
| ¿Qué pasa si el servidor falla? | Cada error tiene un mensaje humano junto a la acción: sin red, servidor dormido (aviso a los 5 s, espera hasta 75 s), 400 explicado en una hoja, 403, 404 como "vacío", 500 con "Reintentar". |
| ¿Qué servicios externos usan? | AeroDataBox (vuelos) y OpenRouter (asistente), **a través del backend**. Los dos dan 500 hoy por claves que faltan en el servidor. La verificación del vuelo la **quitamos de la interfaz** porque el servidor no tiene la clave (no queremos prometer algo que no se cumple); la dejamos lista en el repositorio. El asistente muestra el error con "Reintentar" y la app sigue funcionando. |
| ¿Cómo validan si el backend no valida? | Todo se valida en la app antes de enviar: ciudades de la lista oficial, origen ≠ destino, valor entero > 0, descripción de 3 a 200 caracteres, calificación de 1 a 5. |
| ¿Por qué Flutter? ¿Y por qué una PWA también? | Flutter es el material del curso y da Android e iOS con un solo código. La PWA permite usar la app desde cualquier celular sin instalar un APK, con el mismo diseño y los mismos datos. |
| ¿Cómo se aseguran de que funciona? | Pruebas automáticas en las dos apps (unidad, contrato con respuestas reales, interfaz, accesibilidad y E2E en iPhone y Android), CI en cada push y una comprobación contra el servidor real. |
| ¿Qué harían con más tiempo? | Notificaciones push, guardar en el backend el rol y "mis entregas" (hoy por dispositivo), inicio con Google y reglas de Firestore más estrictas. |

## 5. Hallazgos del backend para mencionar (muestran análisis, no excusas)

- No existe el estado `cancelada` → retirar deja la encomienda `vencida`.
- `fechaVencimiento` se ignora → vence siempre al mes.
- `POST /api/encomiendas` acepta cuerpos vacíos y las calificaciones inválidas dan 500 en vez de 400.
- `/disponibles` no trae el uid del remitente → la app cruza datos para no ofrecerle a alguien su propia encomienda.
- Las fechas de viaje llegan en medianoche UTC → leídas como instante, en Colombia se verían un día antes.
- Tres endpoints dan 500 por configuración del servidor.

## 6. Lista para el día

- [ ] Celulares cargados, con las dos sesiones abiertas y el servidor despierto.
- [ ] Video descargado en el computador (plan B).
- [ ] Documento técnico abierto en la sección de arquitectura.
- [ ] Repositorios abiertos en el navegador, con el CI en verde.
