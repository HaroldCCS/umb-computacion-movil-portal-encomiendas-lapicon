# Semana 3 · Registro de encomiendas

> Entregable del tablero: **"Sem 3 — Registro encomiendas"** (Práctica 3 del proyecto, rol **Remitente**, y la toma
> por parte del viajero). Estado: ✅ hecho en Flutter y en la PWA.

## 1. Objetivo

Que el remitente publique una encomienda validada, siga su estado agrupado y que un viajero de la misma ruta pueda
tomarla: el flujo remitente → viajero.

## 2. Qué hace la app

| Función | Endpoint | Comportamiento |
|---|---|---|
| Nueva encomienda | `POST /api/encomiendas` | Secciones **Ruta · Pago · Detalles** y vista previa del pase tal como la verán los viajeros. |
| Mis envíos | `GET /api/encomiendas` | Chips **Activas · Entregadas · Historial**; el contador de "Entregadas" son las que faltan por calificar. |
| Detalle (maestro-detalle) | — | Pase de la ruta, línea de tiempo **Publicada → Tomada → Entregada → Calificada**, pago, fechas y quién la lleva con su calificación. |
| Retirar | `PUT /api/encomiendas/{id}/estado` → `vencida` | Irreversible: hay que **escribir RETIRAR** para habilitar el botón. |
| Buscar viajeros | `GET /api/viajes/buscar?ciudad=` + `GET /api/ratings/{uid}` | Quién sale de una ciudad y cómo lo califican. |
| Tomar (viajero) | `PUT /api/encomiendas/tomar/{id}` | Hoja con el recordatorio de responsabilidad ("Revisa el contenido antes de aceptarlo…"). |

## 3. Validaciones (el backend no valida el cuerpo)

| Campo | Regla |
|---|---|
| Origen y destino | Elegidos de la lista oficial; deben ser distintos. Botón para intercambiarlos. |
| Valor | Entero mayor que 0 y hasta 100.000.000; se escribe con separador de miles (`1.500.000`). |
| Moneda | USD, COP o EUR (chips). |
| Qué envías | Entre 3 y 200 caracteres. |
| Vencimiento | No se pide: el backend lo fija a un mes; la app lo muestra ("Estará publicada hasta el …"). |

## 4. Estados de la encomienda

```text
DISPONIBLE ──tomar──► TOMADA ──entregar──► ENTREGADA ──(recibir)──► RECIBIDA
    └── retirar o un mes después ──► VENCIDA
```

Cada estado se muestra con **color + ícono + texto** (nunca solo color): Disponible, En camino, Entregada, Recibida,
Vencida. Los estados del backend se actualizan "perezosamente", por eso cada lista se refresca al abrirla y con el
gesto de jalar hacia abajo.

## 5. Evidencia

| | Flutter | PWA |
|---|---|---|
| Pantallas | `lib/features/remitente/` (`nueva_encomienda_screen`, `envios_screen`, `encomienda_detalle_screen`, `buscar_viajeros_screen`) y `viajero/encomienda_viajero_screen` | `src/funciones/remitente/` (`NuevaEncomienda`, `Envios`, `DetalleEnvio`, `BuscarViajeros`) y `viajero/EncomiendaViajero` |
| Lógica pura | `envios_logic.dart` | `funciones/remitente/logica.ts` |
| Pruebas | `test/remitente/envios_logic_test.dart`, `remitente_v2_test.dart`, `status_timeline_test.dart` | `logica.test.ts`, E2E "retirar exige escribir RETIRAR" y el flujo de punta a punta |

**Cómo demostrarlo:** como remitente, publicar Bogota → Miami (mostrar el error si origen y destino son iguales);
como viajero con un viaje en esa ruta, verla en Explorar y tomarla; de vuelta como remitente, verla "En camino".
