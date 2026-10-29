# UX / UI

> Entregable del tablero: **"UX / UI"**. Estado: ✅ hecho (investigación 22-oct, rediseño v2 23-oct, llevado a la PWA
> 24-oct). Este es el resumen para entregar; el detalle completo está en
> [`docs/07-diseno-ux-ui.md`](../07-diseno-ux-ui.md) (sistema de diseño),
> [`docs/08-plan-rediseno-ui.md`](../08-plan-rediseno-ui.md) (por qué y cómo se rediseñó) y
> [`docs/09-lecciones-ux-rediseno.md`](../09-lecciones-ux-rediseno.md) (lecciones reutilizables).

## 1. El problema de diseño

Lapticon le pide a una persona que entregue un paquete a un desconocido que viaja. La interfaz tiene que resolver
tres cosas: **confianza** (¿quién lo lleva?), **claridad del estado** (¿en qué va mi encomienda?) y **cero
ambigüedad en las acciones** (tomar, entregar y retirar tienen consecuencias reales).

## 2. Investigación

| Fuente | Qué se tomó |
|---|---|
| Apps de envío entre personas: **Grabr, Roadie, Dolly** | Valor visible desde la tarjeta, perfil y reseñas antes de confiar, aviso de cambio de estado |
| Confianza en marketplaces | Reseñas mutuas, lista corta y relevante (solo *mi* ruta) |
| Formularios móviles (Baymard) | Validar al salir del campo, quitar el error apenas se corrige, check verde, etiqueta siempre visible |
| Accesibilidad (WCAG / Flutter) | Contraste ≥ 4.5:1, toques ≥ 48 dp, letra del sistema al doble sin desbordes |

**Personas:** *Laura*, remitente (quiere enviar un regalo a Miami y saber en quién confía) y *Andrés*, viajero (viaja
cada mes y quiere ganar algo extra sin complicarse).

## 3. Principios aplicados

1. **La ruta es la protagonista:** cada encomienda es un **pase de abordar** (ORIGEN → DESTINO con muescas).
2. **Estado siempre visible**, con color **+ ícono + texto**, y línea de tiempo en el detalle.
3. **Confianza a la vista:** ★ promedio y reseñas. No se muestra lo que no se puede cumplir: "Verificar vuelo" se quitó porque el servidor no lo soporta.
4. **La acción importante no se esconde:** una principal por pantalla, fija abajo en los detalles; los avisos llevan
   directo a ella y las pestañas cuentan lo pendiente.
5. **Ningún error en silencio:** cargando con texto ("Publicando…"), error **junto al botón**, éxito en aviso flotante.
6. **Fricción proporcional al riesgo:** reversible = un toque · con consecuencias = hoja que explica · irreversible =
   **escribir una palabra** (RETIRAR, ENTREGAR).
7. **No mostrar lo que no aplica** y **pedir datos en el momento justo** (registro → perfil → rol).
8. **Identidad por rol:** remitente en ámbar sobre Medianoche, viajero en Cielo.
9. **Se siente nativa:** título grande que se compacta, barra de vidrio, jalar para actualizar, escala al tocar.

## 4. Sistema de diseño v2

- **Tokens** de color en claro y oscuro (fondo, superficies, texto, marca, acentos por rol y estados), radios,
  medidas y curvas de movimiento. Ningún componente usa colores sueltos.
- **Tipografía:** la del sistema y **Space Grotesk** solo en las ciudades del pase y las cifras grandes; montos con
  cifras tabulares.
- **Componentes** con el mismo nombre en Flutter y en la PWA: `Pantalla`, `BarraPestanas`, `TarjetaHero`,
  `RouteTicket`, `Grupo`/`Fila`, `Boton`, `Campo`, `Chips`, `Insignia`, `Aviso`, `Hoja`, `ConfirmacionEscrita`,
  `AccionResaltada`…

## 5. Arquitectura de información

```text
Login ─► Completar perfil ─► Elegir rol
   REMITENTE  ( Inicio · Envíos · Chats · Perfil )   (+) Nueva encomienda
   VIAJERO    ( Mi viaje · Explorar · Chats · Perfil ) (+) Registrar viaje (solo sin viaje activo)
```

## 6. Cómo se verificó

| Verificación | Flutter | PWA |
|---|---|---|
| Contraste AA de cada par de tokens, claro y oscuro | `test/theme/tema_test.dart` | `src/core/tema/tema.test.ts` |
| Pantallas principales: contraste, toques ≥ 48, letra al doble en 360 dp | `test/accesibilidad_test.dart` | E2E de diseño (320 px efectivos al 200 %, oscuro, toques ≥ 48 px, campos ≥ 16 px) |
| Ningún color fuera de los tokens | revisión de código | prueba automática |
| Lector de pantalla (etiquetas, un nodo por acción) | widget tests | `axe-core` en componentes |
| Revisión visual | emulador Android en claro y oscuro | capturas en iPhone y Android |

## 7. Capturas para el documento

Tomar de la app (claro y oscuro): Login · Inicio del remitente · Envíos · Detalle con la línea de tiempo · Nueva
encomienda · Mi viaje · Explorar · Hoja "¿Tomar esta encomienda?" · Chat · Calificar · Perfil.
