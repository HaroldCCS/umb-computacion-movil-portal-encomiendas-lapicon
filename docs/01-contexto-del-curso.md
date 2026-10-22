# 1. Contexto del curso — ¿qué pide el 2.º corte?

> **Línea a seguir (decisión 22-oct-2026):** hubo cambio de profesor. Se sigue **solo el material nuevo, orientado a Flutter**:
> la presentación *"session 10.pdf" – LAPTICON*, la colección/environment de Postman, el `google-services.json` y las
> sesiones de Canvas que ya citan Flutter (13 sensores, 14–15 maestro-detalle). El material heredado (Visual Studio,
> .NET MAUI, Xamarin, Xlabs, TFS, plan de actividades y PDA antiguos) **no se tiene en cuenta**.

## 1.1 ¿Desde qué sesión empieza el 2.º corte?

El 2.º corte empieza en la **sesión 11**, no en la 8. Las sesiones 9 y 10 fueron los parciales del 1.er corte (22-sep → 03-oct).
En la sesión 10 se presentó el proyecto **Lapticon**, que es el eje de este corte.

## 1.2 Calendario de referencia (semanas del cronograma, solo fechas)

| Sem. | Fechas (2026) | Tema nuevo relacionado (Canvas) |
|---|---|---|
| 11–12 | 06-oct → 17-oct | Cross Platform: arquitectura y configuración de una solución multiplataforma |
| **13** | **20-oct → 24-oct** *(semana actual)* | Sensores en Flutter (`sensors_plus`, GPS, acelerómetro) |
| 14–15 | 27-oct → 07-nov | Maestro-Detalle en Flutter (Navigator, ListView, pasar argumentos) |
| 16–18 | 10-nov → 28-nov | Desarrollo y cierre del proyecto |
| 19 | 30-nov → 05-dic | Parcial final / demo y sustentación *(confirmar con el profesor)* |

Bibliografía Flutter citada: *Flutter Apprentice* (Kodeco, 4.ª ed.), docs.flutter.dev (Navigation and routing,
Navigation cookbook), `sensors_plus` en pub.dev.

## 1.3 Enunciado del proyecto (session 10.pdf — "LAPTICON")

- **Objetivo:** "Que cada equipo desarrolle una app móvil funcional que consuma el backend de Lapticon y cubra el ciclo completo de una encomienda."
- **Tecnología:** libre; el curso sigue **Flutter**. **Requisito:** consumir la API REST con el idToken de Firebase.
- **Arquitectura dada:** App ↔ **Firebase** (Auth para identidad, Firestore para el chat) y App ↔ **Backend Node/Express** (REST + Bearer) ↔ **MongoDB Atlas**.
  El backend usa OpenRouter (chatbot), un microservicio de *matching IA* (no incluido) y AeroDataBox (validación de vuelos).
- **Seis prácticas incrementales:**

| # | Práctica | Qué construyen | Qué aprenden |
|---|---|---|---|
| 1 | Autenticación | Login con Firebase y primera llamada protegida *(por ahora solo correo y contraseña)* | idToken, Bearer |
| 2 | Roles y navegación | Selección de rol y menús por rol, con el rol guardado en servidor | Estado, rutas, persistencia local vs remota |
| 3 | Encomiendas | Formulario, listas por estado y POST/GET a `/api/encomiendas` | Consumo REST, validación, manejo de errores |
| 4 | Viajes | Registro de viaje validado contra un vuelo real | Servicios externos, asincronía, carga |
| 5 | Chat | Conversación remitente–viajero sobre Firestore | Tiempo real, streams, reglas de seguridad |
| 6 | Entrega y calificación | Marcar entrega, calificar y cerrar el chat | Flujo de extremo a extremo, pruebas |

- **Retos ("manos a la obra"):** (1) persistir el rol en el backend, (2) conectar el matching IA, (3) vencimientos programados,
  (4) chat completo bloqueando el envío cuando el chat está cerrado. Los retos 2 y 3 son **del lado del backend** → ver doc 06.
- **Plan de 5 semanas** del PDF: S1 Práctica 1 · S2 Prácticas 2–3 · S3 Prácticas 3–4 · S4 Prácticas 5–6 · S5 Cierre.
  Entregas: *Repo + login* → *Roles + crear encomienda* → *Flujo remitente–viajero* → *Ciclo completo* → *App final + demo*.

## 1.4 Evaluación (según session 10.pdf)

| Peso | Qué se evalúa |
|---|---|
| **40 %** | Prácticas 1 a 6, entregadas por etapa (revisión semanal en clase sobre el repositorio) |
| **30 %** | App final funcionando de extremo a extremo |
| **20 %** | Demo y sustentación técnica |
| **10 %** | Repositorio, código y documentación |

Resultados de aprendizaje que se sustentan: arquitectura cliente-servidor con servicios en la nube; autenticación con Firebase
y consumo de API protegida; datos en tiempo real y servicios externos (vuelos, IA); argumentar decisiones (tecnología,
persistencia y manejo de fallos).

## 1.5 Pendientes de documentación

- La documentación de la API ("Lapticon en Apiary") está en `https://claude.ai/artifact/3j2Hm5PgBJQGq25ye2Nuqz` y **no es pública**.
  Si se consigue, guardarla en `referencias/` y actualizar el doc 03.
- Postman y el PDF no coinciden en algunos endpoints (detalle en el doc 03).
