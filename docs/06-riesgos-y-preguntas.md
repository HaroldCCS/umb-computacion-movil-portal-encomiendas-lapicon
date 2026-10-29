# 6. Riesgos y preguntas abiertas

## 6.1 Preguntas para el profesor (antes de programar)

| # | Pregunta | Por qué importa |
|---|---|---|
| P1 | ¿Desde qué semana cuentan las **5 entregas** del plan de Lapticon y en qué fecha es la primera revisión? | El PDF se presentó en la sesión 10 (inicios de octubre); si ya empezó a contar, la entrega 1 (repo + login) podría estar vencida. |
| P2 | ¿Se mantiene la evaluación del PDF (40 % prácticas, 30 % app final, 20 % sustentación, 10 % repo) y la demo es en la semana 19 (30-nov → 05-dic)? | Define en qué invertir tiempo y la fecha final. |
| P3 | ¿Es individual o en parejas? | Reparto de tareas. |
| P4 | ¿El backend acepta guardar el **rol** en el perfil (campo `rol` en `register`/`PUT users`)? Si no, ¿basta con `SharedPreferences`? | Reto 1 y Práctica 2. |
| P5 | ¿Es aceptable entregar la Práctica 1 solo con correo y contraseña (sin Google Sign-In)? | Decisión tomada por el equipo el 22-oct; conviene confirmarla. |
| P6 | ¿Cuál es la estructura exacta del chat en Firestore (subcolección, campos del mensaje) y qué reglas de seguridad tiene? | Práctica 5; si las reglas no coinciden, Firestore rechaza las escrituras. |
| P7 | ¿Existen en el servidor desplegado `PUT /api/encomiendas/tomar/:id` y `GET /api/vuelos/:numero/:fecha`? No están en Postman. | Prácticas 3–4. |
| P8 | ¿La encomienda lleva `fechaVencimiento`? El PDF lo menciona y Postman no. | Formulario de creación. |
| P9 | ¿Nos comparte la documentación "Lapticon en Apiary" (`claude.ai/artifact/3j2Hm5PgBJQGq25ye2Nuqz`) y, si existe, el repositorio de la app Flutter de referencia (`crear_encomienda_screen.dart`, etc.)? | Contrato exacto de respuestas. |
| P10 | ¿Los retos 2 (matching IA) y 3 (vencimientos programados) se esperan de nosotros? Son cambios de backend y no tenemos su repositorio. | Alcance. |
| P11 | ¿Se requiere iOS o basta Android? | Configuración de Firebase iOS. |
| P12 | ¿Puede agregar **`https://lapticon-pwa.pages.dev`** a la lista de orígenes permitidos (CORS) del backend? Hoy solo acepta `http://localhost:5500` y `http://127.0.0.1:5500` (comprobado el 24-oct-2026). | Versión PWA de la app (`docs/10`): desde ese dominio el navegador bloquea todas las llamadas a la API. Mientras tanto se usa un proxy propio como plan B. |

### Respondidas por la verificación y el Swagger oficial (22-oct y 28-oct-2026)

| # | Respuesta |
|---|---|
| P4 | **No**: `PUT /api/users` responde 200, pero descarta `rol`. Sigue guardado en el dispositivo. |
| P6 | En parte. El estado del chat ya responde (`GET /api/chats/estado/{uidsOrdenados}` → `{ estado: activo \| cerrado, fechaCierre }`): se abre al tomar y se cierra al marcar `entregada`. Faltan las reglas de Firestore. |
| P7 | **Sí existen las dos.** `tomar` funciona; `vuelos` da 500 (`RAPIDAPI_KEY`) y se quitó de la interfaz (docs/11 §2H). |
| P8 | Se acepta, pero **se ignora**: siempre vence un mes después de creada. |
| P10 | El backend ya tiene `POST /api/encomiendas/emparejar-viajes` (responde 200) y `POST /api/encomiendas/actualizar-vencidas`. No hay que construirlos; la app puede usar el primero (docs/11 §2F). |

### Preguntas nuevas (Swagger oficial, 28-oct-2026)

| # | Pregunta | Por qué importa |
|---|---|---|
| P13 | El Swagger dice `lapticon-backend-ed.onrender.com`, pero ese servidor no existe y las rutas están en `lapticon-backend.onrender.com`. ¿Cuál debemos usar para la entrega? | URL base de las dos apps. |
| P14 | **¿Cuándo estará cancelar encomienda?** ¿Será el estado `cancelada` o un `DELETE`? | Hoy "retirar" la deja `vencida`, igual que una que caducó (docs/11 Fase 4, bloqueada). |
| P15 | El enum oficial de encomienda no tiene `entregada`, pero el servidor la acepta. ¿El flujo correcto es `tomada → entregada → recibida` o `tomada → recibida`? | Las dos apps usan `entregada`, y es la que cierra el chat. |
| P16 | El chat se cierra al marcar `entregada`, antes de que el remitente confirme o califique. ¿Es intencional? Y el chat es por par de usuarios: si tienen otra encomienda tomada, ¿debería seguir abierto? | Puede bloquear la coordinación de la entrega. |
| P17 | Viaje `contactado`: ¿quién lo pone y cuándo? El `PATCH` lo rechaza con 400. | Estados que la app debe mostrar. |
| P18 | `GET /api/encomiendas/vencidas` devuelve las de todos los usuarios. ¿Es intencional? | Privacidad; no sirve para "mis vencidas". |
| P19 | ¿Hay endpoint para subir la foto (`fotoUrl`)? | Hoy siempre es `null`. |
| P20 | Un viaje `cancelado` se puede volver a `disponible` con el mismo `PATCH`. ¿Debería impedirse? | Regla de negocio; la app no lo ofrece. |

## 6.2 Riesgos técnicos

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Backend en Render gratuito se "duerme" → primera petición tarda 30–60 s o da timeout | Alta | Medio | Timeout de 60–90 s en la primera llamada, mensaje "despertando el servidor", botón reintentar; hacer un ping a `/api/ciudades/paises` al abrir la app y antes de la demo. |
| Backend **compartido** por todo el curso: datos de otros, regla de "un viaje activo", el usuario de prueba compartido cambia | Alta | Medio | Usar cuentas propias; filtrar lo que se muestra por uid; para la demo crear cuentas limpias el día anterior. |
| El contrato real difiere de Postman (nombres de campos, formato de errores) | Media | Alto | Verificar en la semana 0 y modelos con `fromJson` tolerante. |
| Reglas de Firestore bloquean el chat | Media | Alto | P6; probar con dos cuentas en la semana 3. |
| Validación de vuelo depende de AeroDataBox (cuota/límite) | Alta | Bajo | El servidor responde 500 siempre (`RAPIDAPI_KEY`): se **quitó de la interfaz** (docs/11 §2H). La llamada queda en el repositorio. |
| Estados "lazy" (vencida/completado) desactualizados | Alta | Bajo | Refrescar al entrar a cada lista; explicarlo en la sustentación. |
| Nombres de ciudad con tildes/mayúsculas distintos rompen filtros | Media | Medio | Usar siempre los valores de `/api/ciudades/ciudades` (selección, no texto libre). |
| Chatbot sin `OPENROUTER_API_KEY` en el servidor | Media | Bajo | Es un extra; ocultarlo si responde error. |
| Credenciales del curso en un repo público | Media | Medio | Repo privado o `.gitignore` para `google-services.json` y archivos de entorno. |
| Poco tiempo (5–6 semanas con otras materias) | Alta | Alto | Priorizar los requerimientos **M**; extras (G1–G5) solo en la semana 5. |

## 6.3 Supuestos tomados en esta planeación

- Se sigue solo el material nuevo del profesor actual (Flutter); el material heredado (MAUI, Xamarin, TFS, plan de actividades/PDA antiguos) se descarta.
- Frontend en **Flutter**, Android primero; no modificamos el backend.
- Autenticación solo con correo y contraseña por ahora.
- `applicationId = com.lapticon.app` para que coincida con el `google-services.json`.
- Gestión de estado con **Riverpod** y rutas con **go_router** (se puede cambiar a Provider/Navigator si el profesor prefiere lo visto en clase).
- Las entregas empiezan la semana del 27-oct.
