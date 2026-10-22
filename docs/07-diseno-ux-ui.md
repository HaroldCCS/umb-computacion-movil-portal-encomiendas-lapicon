# 7. Diseño UX/UI — investigación y sistema de diseño

> Objetivo: que Lapticon se sienta **confiable, claro y con identidad de viaje**, no como una plantilla de Material.
> Este documento guía todas las pantallas; el código implementa estos tokens en `lib/core/theme/`.

## 7.1 Investigación: qué aprendimos de referentes

### Apps de envío entre personas (crowdshipping)

| Referente | Cómo funciona | Qué tomamos para Lapticon |
|---|---|---|
| **Grabr** (viajeros traen compras internacionales) | El solicitante publica foto, precio máximo y recompensa; el viajero acepta; el pago queda en garantía hasta la entrega; se recomienda entrega en persona. | La **recompensa/valor** es visible desde la tarjeta; dejar claro *quién hace qué* en cada estado. |
| **Roadie** (entregas "de camino") | El remitente publica el envío; los conductores **verificados** que van en esa dirección ofrecen llevarlo; se revisan **perfil y reseñas** antes de elegir. | Mostrar **calificación y reseñas del viajero** antes de confiar; insignia de **"vuelo verificado"**. |
| **Dolly** (ayuda de mudanza) | Foto, fecha y número de ayudantes; precio antes de reservar; notificación cuando alguien acepta. | **Precio/valor antes de confirmar** y **aviso de cambio de estado**. |

### Confianza en marketplaces entre pares

- Las **reseñas** son el mecanismo principal: estrellas + texto, visibles desde el primer día, y **reseñas mutuas** (ambas partes califican).
- **Verificar la oferta**: insignias por pasos completados (en nuestro caso: perfil completo, vuelo validado con AeroDataBox).
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

1. **La ruta es la protagonista.** Cada tarjeta muestra *ORIGEN → DESTINO* en grande, como un pase de abordar.
2. **El estado siempre visible.** Chip de estado con color **+ ícono + texto** (nunca solo color) y línea de tiempo en el detalle.
3. **Confianza a la vista.** Calificación ★, número de reseñas, "vuelo verificado" y perfil completo junto al nombre de cada persona.
4. **Una acción principal por pantalla.** Un botón lleno (FilledButton); el resto, secundarias.
5. **Pedir datos en el momento justo.** Registro solo con correo y contraseña → completar perfil → elegir rol.
6. **Nunca dejar a la persona adivinando.** Skeletons al cargar, mensaje especial cuando el servidor está "despertando",
   estados vacíos con una acción y errores en lenguaje humano con "Reintentar".
7. **Identidad por rol.** Remitente usa acento **ámbar (paquete)**; viajero usa acento **cielo (avión)**: siempre se sabe en qué modo se está.

## 7.4 Arquitectura de información

```text
Inicio de sesión ─► Completar perfil (1.ª vez) ─► Elegir rol
                                                   │
         ┌─────────────── REMITENTE ───────────────┴──────────────── VIAJERO ───────────────┐
         │ [Envíos]  [Viajeros]  [Chats]  [Perfil]  │  [Mi viaje]  [Explorar]  [Chats]  [Perfil] │
         │  FAB "Nueva encomienda"                   │   FAB "Registrar viaje" (si no hay viaje)   │
         └───────────────────────────────────────────┴─────────────────────────────────────────────┘
Perfil: datos · calificaciones · cambiar de rol · cerrar sesión
```

- **Envíos** (remitente): pestañas *Activas* (disponible + tomada) · *Entregadas* · *Historial* (vencidas + canceladas). Toca → detalle.
- **Viajeros** (remitente): buscar viajeros por ciudad de origen, con su calificación.
- **Mi viaje** (viajero): tarjeta-pase del viaje activo + encomiendas que tomé.
- **Explorar** (viajero): encomiendas disponibles para la ruta de mi viaje.
- Máximo 4 destinos en la barra inferior (NavigationBar de Material 3).

## 7.5 Sistema de diseño (tokens)

### Color

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `primary` (Medianoche) | `#1B2A4A` | `#AFC6FF` | Barra superior, botones principales, ruta |
| `secondary` / acento remitente (Ámbar) | `#F2A93B` (siempre con texto Medianoche encima, 7.1:1) | `#FFC56E` | Rol remitente, FAB, destacados |
| `tertiary` / acento viajero (Cielo) | `#0B63C4` (texto/relleno) · `#2D8CFF` (solo decorativo) | `#8CC4FF` | Rol viajero, avión, enlaces |
| `surface` | `#F7F5F0` (papel) | `#11141B` | Fondo |
| `surfaceContainer` | `#FFFFFF` | `#1A1F2A` | Tarjetas |
| `error` | `#C62828` | `#FFB4AB` | Errores |

Se genera el `ColorScheme` con `ColorScheme.fromSeed(seedColor: #1B2A4A)` y se sobrescriben `secondary`/`tertiary`/`surface`.

**Estados de la encomienda / viaje** (color + ícono + texto):

| Estado | Color | Ícono (Material Symbols) | Texto |
|---|---|---|---|
| disponible | Azul `#0D47A1` | `schedule` | Disponible |
| tomada | Ámbar oscuro `#8A4B00` | `luggage` | En camino |
| entregada | Verde `#1B5E20` | `check_circle` | Entregada |
| vencida | Gris `#5F5F5F` | `event_busy` | Vencida |
| cancelada | Rojo `#B71C1C` | `cancel` | Cancelada |
| viaje completado | Gris azulado `#455A64` | `flight_land` | Completado |

Los chips usan el color al 12 % de opacidad como fondo y el color pleno en texto/ícono (contraste calculado: entre 4.9:1 y 7.1:1 sobre blanco y sobre el fondo papel). Nunca se pone texto blanco sobre ámbar (2:1) ni sobre `#2D8CFF` (3.3:1).

### Tipografía (Google Fonts)

| Estilo | Fuente | Tamaño / peso | Uso |
|---|---|---|---|
| `displaySmall` | **Space Grotesk** | 32 / 700 | Ciudades en la tarjeta-pase |
| `headlineSmall` | Space Grotesk | 24 / 600 | Títulos de pantalla |
| `titleMedium` | **Manrope** | 16 / 700 | Títulos de tarjeta |
| `bodyLarge` | Manrope | 16 / 400 | Texto principal (mínimo 16 para lectura) |
| `bodyMedium` | Manrope | 14 / 400 | Texto secundario |
| `labelLarge` | Manrope | 14 / 700 | Botones |
| `labelSmall` | Space Grotesk | 11 / 600, tracking 1.2, MAYÚSCULAS | Etiquetas tipo pase ("ORIGEN", "VUELO") |

### Espaciado, forma y elevación

- Retícula de **4 dp**: 4 · 8 · 12 · 16 · 24 · 32 · 48. Margen lateral de pantalla 16 (20 en tabletas).
- Radios: campos y chips 12 · tarjetas 20 · hojas inferiores 28 · botones con forma de píldora.
- Elevación casi nula: tarjetas planas con borde `outlineVariant` de 1 dp; sombra suave solo en la tarjeta-pase.
- Botones principales de **alto 56 dp** y ancho completo en formularios.

### Componentes propios

| Componente | Descripción |
|---|---|
| **RouteTicketCard** (tarjeta-pase) | Firma visual de la app. Arriba "ORIGEN" / "DESTINO" en `labelSmall`, ciudades en `displaySmall`, ícono de avión entre ambas con línea punteada; muesca semicircular a los lados (como un boleto perforado); abajo, fecha · vuelo/valor · chip de estado. |
| **StatusChip** | Color + ícono + texto según la tabla de estados. |
| **TrustRow** | Avatar con iniciales · nombre · ★ 4,8 (12 reseñas) · insignia "Vuelo verificado". |
| **StatusTimeline** | Línea de tiempo vertical: Publicada → Tomada → Entregada → Calificada, con el paso actual resaltado. |
| **AppTextField** | Etiqueta arriba, ayuda debajo, error al salir del campo, check verde al ser válido. |
| **EmptyState** | Ilustración simple (ícono grande en círculo de color) + título + texto + botón. |
| **ErrorState / ColdStartBanner** | "El servidor está despertando, puede tardar hasta un minuto…" con indicador de progreso y "Reintentar". |
| **RoleCard** | Tarjeta grande seleccionable para elegir rol (ícono, título, 2 líneas de beneficio). |

### Movimiento

- Transiciones de página estándar de Material 3 (fade-through) y `Hero` de la tarjeta-pase al detalle.
- Duraciones 200–300 ms; respetar "reducir movimiento" (`MediaQuery.disableAnimations`).

## 7.6 Especificación de pantallas

### Práctica 1

**Bienvenida / Inicio de sesión**
```text
┌──────────────────────────────┐
│  ✈ LAPTICON                  │  logotipo (Space Grotesk)
│  Tu paquete viaja con alguien│  propuesta de valor en 1 línea
│  que ya va para allá.        │
│  ┌ BOG ─ ─ ✈ ─ ─ MIA ┐       │  mini tarjeta-pase decorativa
│  Correo  [______________]    │
│  Contraseña [__________ 👁]  │
│            ¿Olvidaste tu contraseña?
│  [      Iniciar sesión      ]│  FilledButton 56 dp
│  ¿No tienes cuenta? Crear cuenta │
└──────────────────────────────┘
```
- Teclado de correo, `autofillHints`, acción "siguiente/enviar" en el teclado, mostrar/ocultar contraseña.
- Errores de Firebase traducidos ("Correo o contraseña incorrectos", "Demasiados intentos, espera un momento").

**Crear cuenta**: correo, contraseña (≥ 6, indicador de fortaleza), confirmar contraseña (se valida en cada pulsación).
Texto: *"Solo te pedimos lo necesario. Tus datos de contacto los completas después."*

**Recuperar contraseña**: un campo + botón; confirmación: *"Si el correo está registrado, te enviamos un enlace."* (no revela si existe).

**Completar perfil** (1.ª vez, paso 1 de 2 con indicador de progreso): nombre, apellido, teléfono (teclado numérico), nacionalidad
(buscador sobre `/api/ciudades/paises`). Texto: *"Así te reconocerán remitentes y viajeros."*

**Elegir rol** (paso 2 de 2): dos `RoleCard`:
- 📦 **Quiero enviar** — "Publica tu encomienda y encuentra quién la lleve."
- ✈️ **Voy a viajar** — "Registra tu vuelo y gana llevando encomiendas de tu ruta."
Nota: *"Puedes cambiar de rol cuando quieras desde tu perfil."*

**Perfil**: cabecera con iniciales, nombre, chip de rol; tarjeta de calificaciones (promedio ★, total); datos editables;
acciones: editar perfil, cambiar rol, cerrar sesión (con confirmación).

### Prácticas 2–6 (resumen)

| Pantalla | Claves de UX |
|---|---|
| Envíos (remitente) | Pestañas por estado; lista de `RouteTicketCard`; *pull-to-refresh*; vacío: "Aún no has enviado nada · Publicar encomienda". |
| Nueva encomienda | Una sola pantalla en secciones: **Ruta** (origen/destino con buscador; botón ⇅ para intercambiar) · **Pago** (valor + moneda en el mismo renglón) · **Detalles** (observaciones con contador). Resumen en tarjeta-pase antes de publicar. |
| Detalle de encomienda | `Hero` de la tarjeta; `StatusTimeline`; `TrustRow` del viajero; acción principal según estado: *Cancelar* (disponible) · *Abrir chat* (tomada) · *Calificar* (entregada). |
| Registrar viaje | Número de vuelo en mayúsculas automáticas (`AA123`), fecha con selector, ruta; al validar, estado "Verificando vuelo…" y resultado con insignia **Vuelo verificado**. |
| Explorar (viajero) | Cabecera con la ruta de mi viaje; lista de encomiendas con **valor destacado**; tomar = hoja inferior de confirmación con recordatorio: *"Revisa el contenido antes de aceptarlo. Eres responsable de lo que llevas en tu equipaje."* |
| Chat | Burbujas (propias en `primary`, ajenas en `surfaceContainer`), hora, encabezado con la ruta de la encomienda; si está cerrado: barra inferior deshabilitada con *"Este chat se cerró porque la entrega terminó."* |
| Calificar | 5 estrellas grandes (48 dp), etiquetas por puntaje ("Excelente"), comentario opcional, botón deshabilitado hasta elegir estrellas. |

## 7.7 Estados y microcopy

| Situación | Qué ve la persona |
|---|---|
| Cargando lista | Skeleton de 3 tarjetas (no spinner a pantalla completa) |
| Servidor en frío (>5 s) | Banner: "Despertando el servidor… la primera carga puede tardar hasta un minuto." |
| Sin conexión | Banner superior persistente: "Sin conexión. Revisa tu internet." |
| 400 de negocio | Mensaje del backend en un diálogo o snackbar, p. ej. "Ya tienes un viaje activo." + acción "Ver mi viaje" |
| 401 | Silencioso (se refresca el token); si falla: "Tu sesión expiró, vuelve a iniciar sesión." |
| 403 | "No tienes permiso para hacer esto." |
| Éxito | Snackbar breve: "Encomienda publicada", "Perfil actualizado" |
| Acción destructiva | Diálogo de confirmación con verbo explícito: "¿Cancelar la encomienda? · No · Sí, cancelar" |

Tono: cercano y directo, de *tú*, frases cortas, sin tecnicismos (no "error 500", sí "Algo falló en el servidor").

## 7.8 Checklist de calidad UI por pantalla

- [ ] Funciona en tema claro y oscuro.
- [ ] Probada con letra del sistema al máximo y en pantalla de 360 dp de ancho.
- [ ] Áreas táctiles ≥ 48 dp y todos los íconos-botón con `tooltip`/`semanticLabel`.
- [ ] Estados de carga, vacío y error implementados.
- [ ] Teclado correcto por campo y la acción del teclado avanza al siguiente.
- [ ] Ningún estado comunicado solo con color.

## 7.9 Siguiente paso de diseño

Antes de las prácticas 3–6 conviene validar con 2–3 compañeros el flujo "publicar encomienda" y "tomar encomienda"
(prueba de pasillo de 5 minutos: ¿entienden qué hacer y en qué estado está su envío?) y ajustar.

## Fuentes

- [Paste Magazine — Dolly, Roadie and Grabr: peer-to-peer shipping apps](https://pastemagazine.com/tech/apps/dolly-roadie-and-grabr-are-the-peer-to-peer-shippi)
- [Lenny's Newsletter — How to build trust in a marketplace](https://www.lennysnewsletter.com/p/how-to-build-trust-in-a-marketplace)
- [Sharetribe — 5 principles of great marketplace UX](https://sharetribe.com/academy/online-marketplace-design-principles)
- [Baymard Institute — Inline form validation](https://baymard.com/blog/inline-form-validation)
- [Baymard Institute — Mobile forms: avoid inline labels](https://baymard.com/blog/mobile-forms-avoid-inline-labels)
- [Flutter docs — Accessibility: UI design & styling](https://docs.flutter.dev/ui/accessibility/ui-design-and-styling)
- [Flutter docs — Migrate to Material 3](https://docs.flutter.dev/release/breaking-changes/material-3-migration)
