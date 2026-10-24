# 9. Lecciones de UX del rediseño v2 — para reutilizar en otras apps (Flutter o PWA)

> Qué aprendimos al rediseñar Lapticon (oct-2026) a partir de la guía de *Cuentas Claras*
> (`GUIA-UI-UX-FLUTTER.md`). Esa guía da el **punto de partida** (tokens, componentes, código); este documento
> recoge lo que **la práctica corrigió o agregó**: qué funcionó, qué se rompió y cómo evitarlo la próxima vez.
> Está escrito para servir en cualquier app; cada lección trae el caso real de Lapticon y, al final, cómo se
> traduce a una **PWA**.
>
> Contexto del proyecto: plan en `docs/08-plan-rediseno-ui.md`, sistema final en `docs/07-diseno-ux-ui.md`,
> errores en `docs/BITACORA.md` (paso 6). 18 commits entre los tags `pre-rediseno-v2` y `rediseno-v2`;
> las pruebas pasaron de 105 a 220.

---

## 1. Cómo rediseñar sin romper la app

1. **Planear completo antes de tocar código**, y escribir el plan en un archivo (`docs/08`): qué se toma de la
   guía, qué se adapta y por qué, los tokens con sus valores, cada componente nuevo con el que reemplaza, la
   pantalla por pantalla y las fases. Las 4 decisiones que eran del dueño (paleta, tipografía, navegación,
   estilo de plataforma) se preguntaron **una sola vez, al final del plan**, con una recomendación.
2. **Adoptar la estructura de la guía, no su marca.** De *Cuentas Claras* se copió el sistema (tokens con
   nombre, tarjeta principal, barra flotante, hojas, toasts); los **valores** salieron de la identidad propia
   (Medianoche/Ámbar/Cielo). Una guía de otra app es un método, no un color.
3. **Alias temporales.** En la fase 1 los nombres viejos (`AppTheme`, `AppColors`, `StatusChip`…) pasaron a
   apuntar a los valores nuevos: toda la app se vio "v2" el primer día sin romper ninguna pantalla, y cada
   pantalla migró en su fase. Los alias se borraron al final, cuando `grep` confirmó cero usos.
4. **Fases pequeñas, cada una cerrada** con análisis limpio, pruebas en verde, revisión en el dispositivo y
   commit. Orden que funcionó: tokens → componentes base → estructura (barra, pantalla, hero) → inicio por rol →
   pantallas por grupo → limpieza y accesibilidad.
5. **Tag antes de empezar** (`pre-rediseno-v2`) y al terminar (`rediseno-v2`): siempre hay a dónde volver.
6. **Galería temporal** para ver componentes o pantallas que la app real todavía no usa o que necesitan otra
   cuenta: un `main` aparte con datos y servicios falsos, fuera de `lib/`, que se borra antes del commit.
7. **Mover trabajo de fase cuando el flujo lo exige** (Envíos con chips se adelantó porque Inicio necesitaba
   abrir un chip concreto) y dejarlo anotado en el plan.

## 2. Principios de experiencia que quedaron confirmados

### 2.1 La acción importante nunca queda escondida

- **Pie fijo en los detalles.** La acción principal (Tomar, Marcar entregada, Calificar, Retirar) vive fija
  abajo: siempre visible sin importar el largo del contenido.
- **Avisos que llevan directo a la acción.** "Tu encomienda a Lima ya fue entregada · Califica a Andrés" abre el
  detalle con `?accion=calificar`; el detalle **explica la acción encima del botón** (aviso ámbar). El enlace va
  al lugar de la acción, no a la portada de la pantalla.
- **Contadores en las pestañas** con lo que falta por hacer (por calificar, por entregar), con rebote al
  cambiar. Nunca se muestra "0".
- **Lección técnica:** "desplazar hasta la acción" falla si la lista se construye perezosamente (el botón aún no
  existe). Por eso la acción va en el pie fijo, o la pantalla se construye completa.

### 2.2 Ningún error en silencio, y cada cosa en su lugar

| Qué pasó | Dónde se muestra |
|---|---|
| Error de una acción | **Junto al botón que la lanzó** (aviso rojo), no en un mensaje genérico |
| Éxito | Aviso flotante **arriba**, que se va solo (no tapa la barra de pestañas) |
| Regla del negocio ("Ya tienes un viaje activo") | Hoja que explica **y ofrece el camino** ("Ver mi viaje") |
| Error al cargar una pantalla | Tarjeta con motivo humano + "Reintentar" |
| Cargando | Esqueleto con la forma del contenido; el botón dice qué hace ("Publicando…") |

- El botón cargando **no se atenúa** (sigue viéndose activo) pero ignora toques: evita el doble envío sin
  parecer roto.
- **Trampa encontrada:** si una acción abre una hoja (regla del negocio) mientras sigue "cargando", el botón
  queda girando debajo. Termina la carga **antes** de abrir la hoja.
- Los mensajes que antes eran SnackBar inferiores quedaban **debajo de la barra flotante**: al cambiar de
  navegación revisa todo lo que aparece abajo.

### 2.3 Fricción proporcional al riesgo

| Tipo de acción | Fricción | En Lapticon |
|---|---|---|
| Reversible | Un toque | Cambiar de rol |
| Con consecuencias | Hoja que explica qué va a pasar | Tomar una encomienda, cerrar sesión |
| Irreversible | **Escribir una palabra** | RETIRAR (encomienda), ENTREGAR (cierra el chat) |

El botón de confirmar se habilita solo cuando la palabra coincide (sin importar mayúsculas).

### 2.4 Decir siempre qué está garantizado y qué no

- Si algo no se pudo verificar, **la interfaz lo dice en todas partes**: "Vuelo verificado" o "**Sin
  verificar**" en la tarjeta del viaje, y al registrar: "puedes registrarlo igual y aparecerá como
  *sin verificar*". Nunca ocultar la falta de garantía (el servicio de vuelos del backend respondía 500).
- Lo que el usuario acepta se muestra **completo, en una caja visible**, no como un enlace: al tomar una
  encomienda, "Revisa el contenido antes de aceptarlo. Eres responsable de lo que llevas en tu equipaje."
- **No inventar textos con promesas.** Se cambió "Lo acuerdas con el viajero al entregar" por "Lo que ofreciste
  por llevarla": la app no define cómo se paga, así que no puede afirmarlo.
- Recuperar contraseña **no revela si el correo existe** (el "no existe" se muestra igual que el éxito).

### 2.5 No mostrar lo que no aplica

- Sin envíos no aparece una tarjeta llena de ceros: solo la invitación "Publica tu primera encomienda".
- Con un viaje activo desaparece el "+" de "Registrar viaje" (solo se puede tener uno) y la barra ocupa el ancho.
- **No mezclar unidades:** no se ordena por valor entre USD y COP; las ganancias se suman **por moneda**.
- Los chips de orden solo aparecen si hay más de un elemento.

### 2.6 Una sola fuente para los textos que cambian por contexto

Los textos que dependen del rol (crear, contraparte, título de la tarjeta) salen de un `Vocabulario.de(rol)`.
Así "¿Cómo te fue con **el viajero**?" o "con **el remitente**" no se condiciona pantalla por pantalla.

### 2.7 Si el backend no guarda algo que la experiencia necesita, guárdalo en el dispositivo y dilo

El backend ignoraba qué encomienda se calificaba, así que no había forma de saber "qué falta por calificar". Se
guarda en el teléfono por usuario y encomienda. **Consecuencia aceptada y documentada:** lo calificado antes del
cambio aparece una vez como pendiente. Cuando migres algo así, anota qué datos viejos no quedan cubiertos.

## 3. Sistema visual: lo que la práctica corrigió

- **Tokens con nombre semántico y modo claro/oscuro en un solo lugar** (`fondo`, `superficie`, `texto2`,
  `marcaSolido`, `exito`…). Ninguna pantalla usa un color directo; se comprueba con `grep "Color(0x"`. Al final
  solo quedaron transparente, blanco sobre degradados y el negro del velo de las hojas.
- **Probar el contraste de cada par de colores en código**, no a ojo. Dos colores de la guía/plan no pasaban AA
  y se corrigieron: el verde de éxito sobre su fondo tintado (4,2:1 → más oscuro) y el **degradado azul con
  texto blanco pequeño** (3,2:1 → degradado más oscuro y brillo al 10 %). Mide el contraste **en la zona más
  clara** del degradado, incluido el brillo.
- **En oscuro no hay sombras**: la separación la dan las superficies y un borde fino.
- **Identidad por rol** con el acento y el degradado de la tarjeta principal: siempre se sabe en qué modo se está.
- **Fuente del sistema para leer + una fuente de marca solo para cifras y títulos de la tarjeta-firma** (aquí
  Space Grotesk en las ciudades del pase). Cifras con números tabulares.
- **Estados con color + ícono + texto**, nunca solo color (la insignia de la guía no tenía ícono; se agregó).

## 4. Accesibilidad: lo que solo apareció al probarla

### 4.1 El lector de pantalla

- **Etiqueta y acción de toque en el mismo nodo.** Si un contenedor pone la etiqueta y otro hijo pone el toque,
  el lector anuncia un botón sin nombre. Pasó en la tarjeta principal de Inicio.
- Ocultar la semántica de los hijos (`excludeSemantics`) **también oculta su acción de toque**: hay que darla en
  el mismo nodo que la etiqueta.
- Las tarjetas tocables fusionan su contenido en un solo botón (el texto es la etiqueta); por eso **no se
  anidan botones dentro de una tarjeta tocable**.
- Lo que debe leerse aparte (el rol actual en el perfil) se marca como nodo propio.
- Elementos decorativos (íconos en caja, avatar junto al nombre) se excluyen; el texto de al lado ya lo dice.

### 4.2 Toque

- Área mínima de **48 dp** aunque el elemento visible sea menor: chips y botones chicos miden 40 y llevan 4 de
  relleno arriba y abajo; el botón de cerrar de una hoja mide 32 dentro de un área de 48.

### 4.3 Letra grande — la que más errores dio

Un barrido con la **letra del sistema al doble en un teléfono de 360 dp** encontró desbordes en 5 de 9 pantallas.
Patrones de arreglo:

| Problema | Arreglo |
|---|---|
| Fila con detalles + insignia que no cabe | Envolver (`Wrap`): la insignia baja a otra línea |
| Etiqueta + valor en una fila | Ambos flexibles y repartidos a los extremos |
| Título + etiqueta de vidrio | La etiqueta también envuelve su texto |
| Logo con nombre | Se **ajusta al ancho** (escala hacia abajo), no desborda |
| Estrellas al lado de una cifra grande | Se encogen si no caben |
| Barra de pestañas de alto fijo | Limitar el crecimiento de letra **solo ahí** (×1,3) |

**Ojo: los arreglos de letra grande causan regresiones visuales.** Un `Wrap` se encoge a su contenido y la
columna lo centra; dos hijos flexibles dejan el espacio sobrante al final. Las dos cosas se vieron en el
dispositivo, no en las pruebas de accesibilidad (que no miden alineación). Después de arreglar desbordes, revisa
la alineación y fíjala con una prueba.

### 4.4 Movimiento

Todo respeta "reducir movimiento": entrada escalonada, hojas, toasts, esqueletos (quietos) y la escala al tocar.

## 5. Patrones nativos que hicieron la diferencia

| Patrón | Para qué |
|---|---|
| Título grande que se compacta en barra de vidrio | Jerarquía clara sin gastar espacio |
| Barra de pestañas flotante en píldora + "+" aparte | La acción de crear siempre a un toque; el "+" desaparece si no aplica |
| Tarjeta principal con degradado y sub-tarjetas de vidrio | Resumen de un vistazo ("Por entregar 0 · Te pagan USD 20") |
| Listas agrupadas estilo ajustes (Perfil, detalles) | Datos y acciones ordenados sin "tarjetas sueltas" |
| Hojas inferiores para confirmar y elegir (país, ciudad, fecha) | No se pierde el contexto |
| Escala al presionar en vez de la onda de Material | Respuesta táctil sobria y consistente |
| Esqueletos, jalar para actualizar, entrada escalonada | Se percibe rápida y viva |

**Cuidado al quitar la onda de Material para toda la app:** primero reemplaza todo lo que dependía de ella
(botones de texto, botones de ícono); si no, esos elementos quedan sin ninguna respuesta al tocar.

## 6. Trampas técnicas (Flutter) y su equivalente en web

| Lo que pasó | Por qué | En web/PWA vigila |
|---|---|---|
| **Pantalla en blanco en Android sin ningún error** | El primer cuadro mide 0 y una grilla calculó un ancho negativo | Cálculos con `calc()` o JS que restan márgenes sin piso |
| El detalle mostraba solo los botones | Un componente en el pie fijo ocupaba **todo el alto** | Pies `position: fixed`/flex que crecen sin límite |
| Validar un formulario no veía todos los campos | La lista perezosa no había construido los de abajo | Virtualización: los campos fuera de pantalla no existen |
| "Desplazar hasta la acción" no hacía nada | El destino aún no existía (lista perezosa) | `scrollIntoView` sobre algo virtualizado |
| Flecha de volver como un cuadro | Faltaba la fuente de íconos de iOS | Fuentes de íconos sin cargar; prefiere SVG embebido |
| Fuentes de marca fallaban en una galería | Se pidieron antes de iniciar la app | Cargar fuentes antes del primer render (FOUT/FOIT) |
| Toasts que no se veían sobre las hojas | Deben vivir **por encima** del navegador de pantallas | Capa de toasts fuera del contenedor de modales, con `z-index` propio |

## 7. Pruebas que valieron la pena

- **Contraste de cada par de tokens** en claro y oscuro (incluido texto blanco sobre los degradados).
- **Barrido de accesibilidad** de las pantallas principales: contraste, 48 dp y etiquetas en claro y oscuro, y
  letra ×2 en 360 dp. Encontró desbordes en 5 de 9 pantallas y un botón sin nombre para el lector.
- **Pruebas de comportamiento** con servicios falsos (sin red): errores junto al botón, palabra para confirmar,
  deep links, contadores, privacidad de "recuperar contraseña".
- **Comprobar que la prueba falla sin el arreglo.** Una prueba de "ocupa todo el ancho" pasaba igual con el
  error porque comparaba contra el propio contenedor; se reescribió contra el ancho disponible.
- **Revisar en el dispositivo cada fase**: el blanco en Android, la flecha rota, los grupos encogidos y las
  regresiones de alineación solo se vieron ahí.
- Un dispositivo/emulador **por sesión de trabajo**: dos sesiones sobre el mismo emulador lo congelaron.

## 8. Llevarlo a una PWA

| En Flutter (Lapticon) | En una PWA |
|---|---|
| `ThemeExtension` `Colores` claro/oscuro | Variables CSS en `:root` + `@media (prefers-color-scheme: dark)`; respetar también un interruptor manual |
| `Medidas`, `Movimiento` | Variables CSS de espacios, radios, duraciones y curvas (`cubic-bezier(.22,1,.36,1)`) |
| `MediaQuery.disableAnimations` | `@media (prefers-reduced-motion: reduce)` → duraciones a 0 |
| Letra del sistema ×2 | Tamaños en `rem`, probar con zoom de texto al 200 % y ancho de 360 px |
| `Presionable` (escala 0,97) | `:active { transform: scale(.97) }` + `-webkit-tap-highlight-color: transparent` |
| `BarraPestanas` flotante | `position: fixed` + `backdrop-filter: blur()` + `padding-bottom: env(safe-area-inset-bottom)`; reservar ese alto al final del contenido |
| Título grande que se compacta | Encabezado `sticky` + `IntersectionObserver` para cambiar a la barra compacta |
| Jalar para actualizar | Gesto propio con `overscroll-behavior-y: contain` (o botón en escritorio) |
| `mostrarHoja` | `<dialog>` anclado abajo, cierre con gesto y con Esc, foco atrapado y devuelto |
| `mostrarToast` | Región `aria-live="polite"` arriba, fuera del contenedor de modales |
| `Esqueleto` | Gradiente animado en CSS, quieto con `prefers-reduced-motion` |
| `Monto` con cifras tabulares | `font-variant-numeric: tabular-nums` y `Intl.NumberFormat` por moneda |
| `Semantics(label, button, onTap)` | Elemento nativo (`<button>`, `<a>`) o `role` + `aria-label`; nunca `<div onclick>` |
| Área táctil 48 dp | `min-height: 48px` en botones, enlaces y chips (con relleno si el visual es menor) |
| Deep link `?accion=calificar` | Parámetro en la URL → `scrollIntoView({block: 'center'})` + enfocar el botón + aviso encima |
| Calificadas guardadas en el teléfono | `localStorage` (o IndexedDB) por usuario, con la misma advertencia sobre datos viejos |
| `CupertinoPageTransitionsBuilder` | View Transitions API, con alternativa sin animación |
| Contraste en pruebas | axe-core / Lighthouse en CI, más una prueba de cada par de tokens |

Además, de la guía original (siguen aplicando en web): campos de **≥ 16 px** para que Safari no haga zoom, la barra
de estado con el color del fondo, y la API en el mismo dominio (cookies de terceros bloqueadas en iPhone).

## 9. Lista de verificación para la próxima app

**Antes de empezar**
- [ ] Plan escrito: qué se toma, qué se adapta, tokens, componentes y fases; decisiones del dueño preguntadas juntas.
- [ ] Tag del estado anterior; alias temporales para migrar por partes.

**Diseño**
- [ ] Toda acción importante visible (pie fijo) y alcanzable desde los avisos con enlace directo.
- [ ] Contadores solo de lo que pide acción; nada en cero.
- [ ] Error junto a la acción, éxito en toast arriba, regla de negocio en hoja con camino.
- [ ] Fricción proporcional: un toque / hoja / escribir palabra.
- [ ] Lo no verificado o no garantizado se dice siempre; lo que se acepta se muestra completo.
- [ ] No se mezclan monedas ni unidades.

**Sistema**
- [ ] Cero colores directos fuera del tema; contraste AA probado por par, incluido texto sobre degradados.
- [ ] Oscuro sin sombras; estados con color + ícono + texto.

**Accesibilidad**
- [ ] Etiqueta y acción en el mismo nodo; nada de botones dentro de tarjetas tocables.
- [ ] 48 dp en todo lo tocable.
- [ ] Letra ×2 en 360 dp sin desbordes, y la alineación revisada después de arreglarlos.
- [ ] "Reducir movimiento" respetado.

**Cierre**
- [ ] Cada fase revisada en el dispositivo real o emulador.
- [ ] Cada prueba nueva comprobada fallando sin el arreglo.
- [ ] Componentes y alias viejos borrados; documentación del sistema actualizada; tag final.
