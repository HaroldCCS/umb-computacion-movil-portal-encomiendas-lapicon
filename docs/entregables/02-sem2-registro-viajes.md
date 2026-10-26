# Semana 2 · Registro de viajes

> Entregable del tablero: **"Sem 2 — Registro viajes"** (Práctica 4 del proyecto, rol **Viajero**).
> Estado: ✅ hecho en Flutter y en la PWA.

## 1. Objetivo

Que el viajero registre su vuelo real, intente verificarlo contra un servicio externo y, con el viaje activo, vea las
encomiendas que van por su misma ruta.

## 2. Qué hace la app

| Función | Endpoint | Comportamiento |
|---|---|---|
| Registrar viaje | `POST /api/viajes` | Número de vuelo (`AV24`, `AA123`…), fecha, ciudad de origen y destino elegidas de la lista oficial. |
| Verificar el vuelo | `GET /api/vuelos/{numero}/{fecha}` | Botón "Verificar vuelo" con indicador de carga. Hoy el servidor responde **500**: la app lo dice ("Verificación no disponible… aparecerá como *sin verificar*") y deja registrar igual. |
| Un viaje a la vez | `POST /api/viajes` → **400** | El mensaje del backend se explica en una hoja con el camino: "Ver mi viaje". |
| Mi viaje | `GET /api/viajes/disponible` | Tarjeta principal: ruta, vuelo, fecha, **"Vuelo verificado" o "Sin verificar"**, cuántas lleva por entregar y cuánto le pagan. 404 = "sin viaje activo" (no es error). |
| Historial | `GET /api/viajes` | Últimos 5 viajes con su estado (Activo / Completado). |
| Explorar | `GET /api/encomiendas/disponibles?origen=&destino=` | Encomiendas de su ruta, con lo que pagan a la vista y orden por "Más recientes" o "Vencen pronto". |

## 3. Validaciones del formulario

- **Número de vuelo:** código de aerolínea (2 caracteres) + 1 a 4 dígitos + letra opcional; se normaliza a mayúsculas
  sin espacios (`av 24` → `AV24`).
- **Fecha:** entre hoy y dentro de un año, en un selector del sistema dentro de una hoja inferior.
- **Ciudades:** se eligen de `/api/ciudades/ciudades` (buscador sin tildes: "bogotá" encuentra "Bogota"), porque los
  filtros del backend comparan el texto exacto. Origen y destino deben ser distintos.

## 4. Reglas que la app respeta

- Con viaje activo **no se muestra el botón "+"** de registrar otro.
- El viajero **no ve sus propias encomiendas** (publicadas como remitente) en Explorar, aunque el backend las incluya.
- Si un vuelo no se pudo verificar, la tarjeta lo dice **siempre** ("Sin verificar"): no se oculta.

## 5. Evidencia

| | Flutter | PWA |
|---|---|---|
| Pantallas | `lib/features/viajero/registrar_viaje_screen.dart`, `mi_viaje_screen.dart`, `explorar_screen.dart` | `src/funciones/viajero/RegistrarViaje.tsx`, `MiViaje.tsx`, `Explorar.tsx` |
| Lógica pura | `viajero_logic.dart` | `funciones/viajero/logica.ts` |
| Pruebas | `test/viajero/viajero_logic_test.dart`, `viajero_v2_test.dart` | `funciones/logica.test.ts`, E2E "registrar viaje sin verificación y la regla de un solo viaje" |

**Cómo demostrarlo:** registrar un vuelo Bogota → Miami, pulsar "Verificar vuelo" (se ve el aviso de verificación no
disponible), registrar, intentar registrar un segundo viaje (hoja con la regla del backend) y abrir Explorar.
