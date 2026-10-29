# 7. Diseño UX/UI — investigación y sistema de diseño

> Objetivo: que Lapticon se sienta **confiable, claro y con identidad de viaje**, no como una plantilla de Material.
> Este documento guía todas las pantallas. **Versión 2** (23-oct-2026): sistema rediseñado a partir de la guía de
> UI/UX de *Cuentas Claras* (estilo iOS, tarjetas, barra flotante); la planeación y las decisiones están en
> `docs/08-plan-rediseno-ui.md`. El código vive en `lib/core/theme/` (tokens y tema) y `lib/core/widgets/`
> (componentes).
> Lo aprendido en el rediseño, reutilizable en otras apps o en una PWA: `docs/09-lecciones-ux-rediseno.md`.

## 7.1 Investigación: qué aprendimos de referentes

### Apps de envío entre personas (crowdshipping)

| Referente | Cómo funciona | Qué tomamos para Lapticon |
|---|---|---|
| **Grabr** (viajeros traen compras internacionales) | El solicitante publica foto, precio máximo y recompensa; el viajero acepta; el pago queda en garantía hasta la entrega; se recomienda entrega en persona. | La **recompensa/valor** es visible desde la tarjeta; dejar claro *quién hace qué* en cada estado. |
| **Roadie** (entregas "de camino") | El remitente publica el envío; los conductores **verificados** que van en esa dirección ofrecen llevarlo; se revisan **perfil y reseñas** antes de elegir. | Mostrar **calificación y reseñas del viajero** antes de confiar; insignia de **"vuelo verificado"**. |
| **Dolly** (ayuda de mudanza) | Foto, fecha y número de ayudantes; precio antes de reservar; notificación cuando alguien acepta. | **Precio/valor antes de confirmar** y **aviso de cambio de estado**. |

### Confianza en marketplaces entre pares

- Las **reseñas** son el mecanismo principal: estrellas + texto, visibles desde el primer día, y **reseñas mutuas** (ambas partes califican).
- **Verificar la oferta**: insignias por pasos completados (en nuestro caso: perfil completo; validar el vuelo con AeroDataBox queda para cuando el servidor lo soporte).
- Perfiles fuertes: calificación, número de reseñas, antigüedad y verificaciones.
- Pedir solo lo esencial en el registro (nombre, correo, contraseña) y pedir el resto **cuando se necesita**, explicando por qué.
- Mostrar **una lista corta y relevante** de coincidencias (encomiendas de *mi* ruta) en vez de un catálogo enorme.

### Formularios móviles

- **Validar al salir del campo**, no mientras la persona está escribiendo por primera vez; **quitar el error apenas se corrige** (en cada pulsación).
- **Validación positiva** (check verde) en campos correctos para dar sensación de progreso.
- **Etiquetas fuera del campo** (encima o flotantes que no desaparecen), nunca solo *placeholder*.
- Mantener la validación al enviar como respaldo.

### Accesibilidad (Flutter / WCAG)

- Contraste ≥ **4.5:1** para texto normal y ≥ **3:1** para texto grande.
- Áreas táctiles ≥ **48 × 48 dp**.
- Respetar el tamaño de letra del sistema: probar con la letra más grande en un teléfono pequeño.
- Probar en widget tests con `meetsGuideline(androidTapTargetGuideline)`, `labeledTapTargetGuideline` y `textContrastGuideline`.

## 7.2 Usuarios (proto-personas)

**Laura — remitente.** 34 años, Bogotá. Quiere enviarle un regalo y medicamentos de venta libre a su hermana en Miami
sin pagar un courier caro. *Preocupaciones:* ¿es confiable quien lo lleva?, ¿cuándo llega?, ¿en qué estado va?
*Necesita:* publicar rápido, ver el estado de un vistazo, conocer al viajero (reseñas) y hablar con él.

**Andrés — viajero.** 27 años, viaja Bogotá–Miami cada mes por trabajo. Quiere ganar algo extra sin complicarse.
*Preocupaciones:* qué lleva en la maleta (aduana), coordinar la entrega, no perder tiempo. *Necesita:* registrar el vuelo
una vez, ver solo encomiendas de su ruta con el valor que paga cada una, tomarlas en un toque y coordinar por chat.

## 7.3 Principios de diseño de Lapticon

1. **La ruta es la protagonista.** Cada encomienda es un pase de abordar: *ORIGEN → DESTINO* en grande.
2. **El estado siempre visible**, con color **+ ícono + texto** (nunca solo color) y línea de tiempo en el detalle.
3. **Confianza a la vista.** Calificación ★ y número de reseñas. La interfaz no promete lo que no puede cumplir:
   "Verificar vuelo" se quitó porque `/api/vuelos` responde siempre 500 (docs/11 §2H).
4. **La acción importante nunca queda escondida.** Una acción principal por pantalla; en los detalles va **fija
   abajo**. Los avisos ("Tu encomienda ya fue entregada · Califica al viajero") llevan **directo** a la acción
   (`?accion=calificar|entregar`) y la explican encima del botón. Las pestañas cuentan lo pendiente.
5. **Ningún error en silencio.** Toda acción muestra *cargando* con texto ("Publicando…"), el **error junto a
   lo que lo causó** (no un mensaje genérico) y el **éxito en un aviso flotante** arriba.
6. **Fricción proporcional al riesgo.** Reversible → un toque (cambiar de rol). Con consecuencias → hoja inferior
   que explica (tomar una encomienda, cerrar sesión). Irreversible → **escribir una palabra** (RETIRAR, ENTREGAR).
7. **No mostrar lo que no aplica.** Sin envíos no hay tarjeta en cero; con viaje activo no aparece "Registrar
   viaje"; las monedas no se mezclan (no se ordena por valor entre USD y COP).
8. **Pedir datos en el momento justo.** Registro solo con correo y contraseña → completar perfil → elegir rol.
9. **Nunca dejar a la persona adivinando.** Esqueletos al cargar, aviso de "servidor despertando", estados
   vacíos con una acción y errores en lenguaje humano con "Reintentar".
10. **Identidad por rol.** Remitente: acento **ámbar** y tarjeta **Medianoche**. Viajero: acento y tarjeta **Cielo**.
11. **Se siente nativa.** Título grande que se compacta, barra de vidrio, rebote, jalar para actualizar, escala al
    tocar (sin onda de Material), entrada escalonada; todo respeta "reducir movimiento".

## 7.4 Arquitectura de información

```text
Inicio de sesión ─► Completar perfil (1.ª vez) ─► Elegir rol
                                                   │
       ┌──────────── REMITENTE ────────────────────┴──────────── VIAJERO ─────────────────────┐
       │ ( Inicio · Envíos · Chats · Perfil )  (+)  │ ( Mi viaje · Explorar · Chats · Perfil )  (+)  │
       │  "+" = Nueva encomienda                    │  "+" = Registrar viaje (solo sin viaje activo)  │
       └────────────────────────────────────────────┴──────────────────────────────────────────────┘
Perfil: calificaciones · datos de contacto · cambiar de rol · cerrar sesión
```

- **Barra flotante** en píldora de vidrio con el botón circular de la acción principal aparte.
- **Contadores:** Envíos = entregas por calificar; Mi viaje = encomiendas por entregar.
- **Inicio (remitente):** encabezado (saludo, fecha, avatar → Perfil), tarjeta principal Medianoche con los envíos
  activos, avisos por calificar y *Vista rápida* (por calificar, entregadas, buscar viajeros, asistente).
- **Envíos:** chips *Activas · Entregadas · Historial*; toca → detalle.
- **Mi viaje:** tarjeta Cielo (ruta, vuelo, por entregar, te pagan), avisos, mis entregas, historial.
- **Explorar:** encomiendas de la ruta del viaje, ordenables por *Más recientes* o *Vencen pronto*.
- Lo que se calificó se recuerda en el teléfono (`Prefs.calificadas`): el backend ignora `encomiendaId`.

## 7.5 Sistema de diseño v2

### Color (`Colores`, una `ThemeExtension`; se lee con `context.c.xxx`)

Ningún widget usa colores directos (salvo blanco sobre los degradados y el velo de las hojas).

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `fondo` | `#F5F6F8` | `#000000` | Fondo de pantalla |
| `superficie` / `superficie2` | `#FFFFFF` / `#EFF1F5` | `#171A20` / `#252A33` | Tarjetas, hojas / campos y chips |
| `separador` | `#E2E6EC` | `#323844` | Bordes y divisores (en oscuro reemplazan la sombra) |
| `texto` / `texto2` / `texto3` | `#111A2C` / `#5C6678` / `#8E97A6` | `#F3F5F8` / `#A6AEBB` / `#717A88` | Principal / secundario (AA) / no esencial |
| `marca` (Cielo) | `#0B63C4` | `#8CC4FF` | Enlaces, íconos activos |
| `marcaSolido` / `sobreMarca` | `#1B2A4A` / blanco | `#AFC6FF` / `#0E1A33` | Botón primario y su texto |
| `remitente` / `viajero` | `#F2A93B` / `#0B63C4` | `#FFC56E` / `#8CC4FF` | Acento por rol (con su `sobre…`) |
| `exito` / `atencion` / `peligro` / `info` (+ `…Suave`) | `#17663F` / `#8A4B00` / `#C62828` / `#0D47A1` | `#5CD696` / `#FABE46` / `#F87878` / `#8CC4FF` | Estados y avisos |

- **Degradados de la tarjeta principal:** Medianoche `#3A5A8C → #1B2A4A → #0F1A30` (remitente) y Cielo
  `#1A5FB0 → #0B4F9E → #083A75` (viajero), con brillo radial blanco al 10 %. Texto blanco con AA.
- **Estados → insignia:** disponible = info + reloj · tomada = atención, según quién mira: **"Tomada"** + persona
  para el remitente y **"La llevas tú"** + maleta para el viajero que la lleva (docs/11 §2G) · entregada / recibida
  = éxito + check · vencida y viaje completado = neutra · viaje cancelado = peligro + círculo con X.
- **"Te la tomaron":** el remitente ve arriba en Inicio y Envíos "¡{nombre} tomó tu encomienda…!" (Escribirle ·
  Ver envío · Entendido) y "1 nueva" en la pestaña. El viajero ve un aviso fijo "Tú llevas esta encomienda" con los
  pasos que siguen.
- **En oscuro no hay sombras**: la separación la dan las superficies y el borde.
- Todos los pares texto/fondo se validan en `test/theme/tema_test.dart`.

### Tipografía

Fuente del sistema para todo; **Space Grotesk** solo en los estilos `display*` (ciudades del pase y cifras grandes).
Montos con **cifras tabulares** (`Monto`).

| Estilo | Tamaño / peso | Uso |
|---|---|---|
| `displayLarge` | 40 / 700 | Cifra de la tarjeta principal |
| `displaySmall` | 32 / 700 | Ciudades del pase (24 en el compacto) |
| Título grande (barra iOS) | 32 / 700 | Título de pantalla |
| `titleLarge` | 20 / 700 | Secciones ("Vista rápida") |
| `bodyLarge` / `bodyMedium` | 17 / 15 | Texto y campos / secundario |
| etiqueta | 13 / 500, `texto2` | Encima de cada campo |
| micro | 11 / 600, MAYÚSCULAS | ORIGEN, DESTINO, TE PAGAN |

### Medidas y movimiento (`Medidas`, `Movimiento`)

- Margen 16 · bloque 20 · radios: campo y botón 16, tarjeta 24, tarjeta principal y hojas 28, chips en píldora.
- Botón 52 (≥ 48 con letra grande) · botón de ícono 48 · fila 52 · barra de pestañas 62.
- Entrada 380 ms `Cubic(0.22, 1, 0.36, 1)` · hoja 420 ms `Cubic(0.32, 0.72, 0, 1)` · tocar 150 ms a 0.97 ·
  escalonado de 40 ms por ítem. Con "reducir movimiento" todo va a cero.

### Componentes (`lib/core/widgets/`)

| Componente | Para qué |
|---|---|
| `Pantalla` | Barra iOS con título grande, jalar para actualizar, pie fijo y relleno bajo la barra flotante |
| `BarraPestanas` | Píldora flotante + botón "+"; contadores con rebote |
| `EncabezadoApp`, `TarjetaHero`, `SubTarjetaVidrio`, `EtiquetaVidrio`, `Mosaico` | Inicio y Mi viaje |
| `RouteTicket` | La tarjeta-pase (firma visual) |
| `Tarjeta`, `Grupo`, `Fila`, `FilaAccion`, `TarjetaAccion` | Tarjetas y listas agrupadas estilo ajustes; avisos que llevan a la acción |
| `Boton` (primario · tonal · secundario · peligro), `BotonIcono`, `Enlace` | Acciones con estado de carga |
| `Campo`, `CampoContrasena`, `CampoMonto`, `Chips`, `ChipsMultiples` | Formularios (validan al salir; check verde) |
| `Insignia`, `Avatar`, `IconoEnCaja`, `Progreso`, `Monto` | Estados, personas, cifras |
| `Aviso`, `Vacio`, `ErrorCarga`, `Esqueleto`, `AvisoServidor` | Información, vacío, error y carga |
| `mostrarToast`, `mostrarHoja`, `confirmarConHoja`, `ConfirmacionEscrita` | Éxitos, hojas y confirmaciones |
| `AccionResaltada`, `Presionable`, `Entrada` | Acción a la que lleva un aviso; respuesta al tocar; aparición |

## 7.6 Pantallas

| Pantalla | Claves |
|---|---|
| Login | Marca, propuesta de valor, pase decorativo; error de Firebase junto al botón ("Entrando…") |
| Registro / Recuperar | Barra de fuerza y mínimo en verde; Recuperar no revela si el correo existe |
| Completar perfil / Elegir rol | Paso 1 y 2 de 2; tarjetas de rol con marca de selección; país en hoja con buscador |
| Inicio (remitente) | Tarjeta Medianoche, avisos por calificar, Vista rápida |
| Envíos | Chips con contador; pases; vacío con "Publicar encomienda" |
| Nueva encomienda | Ruta (⇅) · pago con `CampoMonto` y moneda en chips · detalles; vista previa del pase |
| Detalle (remitente) | Pase, línea de tiempo, detalles, quién la lleva; pie: retirar (RETIRAR), chat o calificar |
| Buscar viajeros | Ciudad arriba; cada viajero con su calificación y el pase de su vuelo |
| Mi viaje / Explorar | Tarjeta Cielo y avisos / ruta del viaje, orden y valor a la vista |
| Registrar viaje | Fecha con rueda iOS; sin verificación del vuelo (el servidor no la soporta) |
| Encomienda (viajero) | Tomar = hoja con la responsabilidad completa; entregar = escribir ENTREGAR |
| Chats / chat | Lista agrupada; burbujas propias en Medianoche; chat cerrado con candado y explicación |
| Calificar / Reseñas | Estrellas de 48 dp, sugerencias en chips, comentario; resumen con barras por estrella |
| Perfil | Estilo ajustes; cambiar de rol en un toque, cerrar sesión en hoja |
| Asistente | Sugerencias por rol; el error se ve en la burbuja con "Reintentar" |

## 7.7 Estados y microcopy

| Situación | Qué ve la persona |
|---|---|
| Cargando | Esqueletos con la forma del contenido (no spinner a pantalla completa) |
| Servidor en frío | "Despertando el servidor… la primera carga puede tardar hasta un minuto." encima de la barra |
| Error al cargar | `ErrorCarga`: "No pudimos cargar la información" + motivo + "Reintentar" |
| Error de una acción | `Aviso` rojo **junto al botón** que la lanzó (o en el pie del detalle) |
| Regla del backend | Hoja que explica y ofrece el camino ("Ya tienes un viaje activo" → "Ver mi viaje") |
| Éxito | Aviso flotante arriba: "Encomienda publicada", "Perfil actualizado" |
| Acción irreversible | Hoja con el verbo explícito y la palabra a escribir |

Tono: cercano y directo, de *tú*, frases cortas, sin tecnicismos (no "error 500", sí "Algo falló en el servidor").

## 7.8 Lista de verificación (automatizada)

`test/accesibilidad_test.dart` recorre las pantallas principales (login, registro, elegir rol, inicio, envíos,
nueva encomienda, mi viaje, explorar y perfil) y comprueba en cada una:

- [x] Contraste de texto (WCAG AA) en tema **claro y oscuro**.
- [x] Áreas táctiles ≥ 48 dp y botones con etiqueta para el lector de pantalla.
- [x] **Letra del sistema al doble** en un teléfono de **360 dp** sin desbordes.

Además: ningún `Color(0x…)` fuera de `tema.dart` (en las pantallas solo quedan `Colors.transparent`, blanco sobre
los degradados y el negro del velo de las hojas), toda cifra de dinero con cifras tabulares, y las animaciones
respetan "reducir movimiento" (`componentes_test.dart`).

## Fuentes

- [Paste Magazine — Dolly, Roadie and Grabr: peer-to-peer shipping apps](https://pastemagazine.com/tech/apps/dolly-roadie-and-grabr-are-the-peer-to-peer-shippi)
- [Lenny's Newsletter — How to build trust in a marketplace](https://www.lennysnewsletter.com/p/how-to-build-trust-in-a-marketplace)
- [Sharetribe — 5 principles of great marketplace UX](https://sharetribe.com/academy/online-marketplace-design-principles)
- [Baymard Institute — Inline form validation](https://baymard.com/blog/inline-form-validation)
- [Baymard Institute — Mobile forms: avoid inline labels](https://baymard.com/blog/mobile-forms-avoid-inline-labels)
- [Flutter docs — Accessibility: UI design & styling](https://docs.flutter.dev/ui/accessibility/ui-design-and-styling)
- [Flutter docs — Migrate to Material 3](https://docs.flutter.dev/release/breaking-changes/material-3-migration)
- Guía de UI/UX de *Cuentas Claras* (proyecto propio de Harold, base del rediseño v2; ver `docs/08-plan-rediseno-ui.md`)
