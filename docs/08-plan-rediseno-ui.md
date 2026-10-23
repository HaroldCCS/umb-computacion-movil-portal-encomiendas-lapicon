# 8. Plan de rediseño UI/UX — Lapticon v2

> Fuente: `GUIA-UI-UX-FLUTTER.md` (lecciones de *Cuentas Claras*, estilo inspirado en *Lukas*).
> **Estado (23-oct-2026): implementado** en las fases 1–6 (commits `be59daf` … y tag `rediseno-v2`). El sistema
> final está descrito en `docs/07`; este archivo queda como registro del plan y de las decisiones.

## 8.1 Qué se toma de la guía y qué se adapta

| De la guía | En Lapticon | Por qué |
|---|---|---|
| Tokens con nombre en `ThemeExtension` (`context.c.xxx`), claro y oscuro | **Se adopta tal cual** la estructura (`fondo`, `superficie`, `superficie2`, `separador`, `texto/2/3`, `marca…`, `exito/atencion/peligro` + `Suave`) | Hoy hay colores sueltos (`AppColors.estado*`, `Colors.amber`, `Colors.white`) en 6 pantallas |
| Paleta verde azulada | **Se adapta**: los *valores* salen de la identidad Lapticon (Medianoche, Ámbar, Cielo) | El verde es la marca de Cuentas Claras; docs/07 §7.3-7 pide identidad por rol |
| Tarjeta principal con degradado + sub-tarjetas vidrio | **Se adopta**: degradado *Medianoche* (remitente) y *Cielo* (viajero) | Es el "hero" de Inicio y de Mi viaje |
| Barra de pestañas flotante en píldora + botón "+" | **Se adopta** | Reemplaza `NavigationBar` + `FloatingActionButton.extended` |
| Chips con el activo en negro | **Se adopta** | Reemplaza el `TabBar` de Envíos y el `SegmentedButton` de moneda |
| Hojas inferiores, toasts arriba, esqueletos, escala al presionar, entrada escalonada | **Se adopta** | Reemplaza `AlertDialog`, `SnackBar`, `CircularProgressIndicator` en listas, `InkWell` |
| Fricción proporcional (1 toque · hoja · escribir palabra) | **Se adopta** | Retirar encomienda y marcar entregada son irreversibles |
| `Vocabulario` por contexto | **Se adopta por rol** (remitente / viajero) | Mismas pantallas (chat, calificar, detalle) hablan distinto según el rol |
| `Monto` con cifras tabulares | **Se adopta** con moneda (`USD 25`, `COP 50.000`) usando `Fmt.dinero` | El valor de la encomienda es la cifra principal del viajero |
| Botón del ojo (ocultar montos) | **Se omite** (opcional, fase final) | Principio 1.4: no aplica mucho; los valores no son saldos personales |
| Modos de confianza explícitos | **Se adapta**: "Vuelo verificado" vs. "Vuelo **sin** verificar" siempre visible | `GET /api/vuelos` responde 500; la interfaz debe decir siempre qué garantiza |
| Título grande iOS (`CupertinoSliverNavigationBar`) | **Se adopta tal cual** (decisión §8.8-4): título grande que se compacta en vidrio, `BouncingScrollPhysics`, `CupertinoSliverRefreshControl` y transición Cupertino en Android e iOS | Sensación de app nativa de la guía |
| Fuente del sistema | **Se adapta** (decisión §8.8-2): sistema para todo + Space Grotesk solo en ciudades del pase y cifras grandes; Manrope sale | Mantiene la firma del "pase de abordar" |
| Carpeta `lib/ui/` | **Se adapta**: se mantiene `lib/core/theme/` y `lib/core/widgets/` | Lo exige `CLAUDE.md` y docs/04 |

Lo que **se conserva** de Lapticon porque ya cumple la guía o es su firma: `RouteTicket` (tarjeta-pase,
re-estilizado), `StatusTimeline`, `TrustRow`, validación al salir del campo de `AppTextField`, banner de
"servidor despertando", estados con **color + ícono + texto**.

> Diferencia importante con la guía: su `Insignia` no lleva ícono. En Lapticon **sí lleva ícono**
> (docs/07: "nada solo por color").

## 8.2 Tokens propuestos

Valores iniciales; cada par texto/fondo se valida con `textContrastGuideline` en pruebas (fase 6).

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `fondo` | `#F5F6F8` | `#000000` | Fondo de pantalla |
| `superficie` | `#FFFFFF` | `#171A20` | Tarjetas, hojas, barra |
| `superficie2` | `#EFF1F5` | `#252A33` | Campos, chips inactivos |
| `separador` | `#E2E6EC` | `#323844` | Bordes y divisores |
| `texto` | `#111A2C` | `#F3F5F8` | Texto principal |
| `texto2` | `#5C6678` | `#A6AEBB` | Secundario (AA) |
| `texto3` | `#8E97A6` | `#717A88` | Solo info no esencial |
| `marca` (Cielo) | `#0B63C4` | `#8CC4FF` | Enlaces, ícono activo |
| `marcaSolido` (Medianoche) | `#1B2A4A` | `#AFC6FF` | Botón primario, "+" |
| `sobreMarca` | `#FFFFFF` | `#0E1A33` | Texto sobre botón primario |
| `marcaSuave` | `#E4EDFA` | `#14284A` | Botón tonal |
| `remitente` / `sobreRemitente` | `#F2A93B` / `#1B2A4A` | `#FFC56E` / `#11141B` | Acento del rol remitente |
| `viajero` / `sobreViajero` | `#0B63C4` / `#FFFFFF` | `#8CC4FF` / `#00213F` | Acento del rol viajero |
| `exito` / `exitoSuave` | `#17663F` / `#DEF5E9` | `#5CD696` / `#0E3624` | Entregada, recibida, verificado |
| `atencion` / `atencionSuave` | `#8A4B00` / `#FEF2DC` | `#FABE46` / `#3E2A08` | Tomada (en camino), por calificar |
| `peligro` / `peligroSuave` | `#C62828` / `#FDE6E6` | `#F87878` / `#461616` | Errores, retirar |
| `info` / `infoSuave` | `#0D47A1` / `#E3ECFA` | `#8CC4FF` / `#14284A` | Disponible |

- **Degradado remitente (Medianoche):** `#3A5A8C → #1B2A4A → #0F1A30` a 155° + brillo radial blanco 10 %.
- **Degradado viajero (Cielo):** `#1A5FB0 → #0B4F9E → #083A75` (oscurecido en la fase 3 para AA con texto blanco pequeño) + el mismo brillo.
- Íconos en recuadro pastel (fondo al 14 %): azul `#3B82F6`, violeta `#8B5CF6`, ámbar `#E8930C`,
  rojo `#E5484D`, verde `#1E8458`, celeste `#0EA5E9`.
- En oscuro **sin sombras** (`conSombra: false`).

**Estados → insignia:** disponible = `info` + `schedule` · tomada = `atencion` + `luggage` ·
entregada / recibida = `exito` + `check_circle` / `done_all` · vencida = neutra + `event_busy` ·
viaje completado = neutra + `flight_land`.

**Medidas** (de la guía): margen 16 · bloque 20 · radios campo/botón 16, tarjeta 24, hero y hojas 28,
chips y barra píldora · botón 48 (se sube a **52** para mantener el ≥48 dp con letra grande), ícono 44→**48**
(docs/07 exige 48), fila 52 · barra de pestañas 62.

**Tipografía** (escala de la guía): `tituloGrande` 32/700 · `cifraHero` 40/700 · `titulo` 20/700 ·
`cuerpo` 17 · `secundario` 15 · `etiqueta` 13/500 · `micro` 11/600 MAYÚSCULAS · `insignia` 12/600.
Ciudades del pase y cifras con cifras tabulares.

**Movimiento:** entrada 380 ms `Cubic(0.22,1,0.36,1)` · hoja 420 ms `Cubic(0.32,0.72,0,1)` · toast 360 ms ·
presionar 150 ms a 0.97 · progreso 900 ms · rebote del contador 500 ms. Todo a cero con
`MediaQuery.disableAnimationsOf`.

## 8.3 Componentes (archivos en `lib/core/`)

| Archivo nuevo | Reemplaza | Notas |
|---|---|---|
| `theme/tema.dart` (`Colores`, `Medidas`, `Movimiento`, `construirTema`) | `app_theme.dart`, `app_tokens.dart` | `ColorScheme` también se alinea para widgets Material que quedan (date picker, `TextField` del chat). Solo `GoogleFonts.xxx(textStyle:)` |
| `theme/vocabulario.dart` | textos condicionados por rol | `Vocabulario.de(Rol)` |
| `widgets/presionable.dart` | `InkWell` | `splashFactory: NoSplash` global |
| `widgets/tarjeta.dart`, `grupo.dart` (`Grupo`, `Fila`) | `Card`, `ListTile` (perfil, mi viaje) | |
| `widgets/boton.dart` (primario · tonal · secundario · peligro, con `textoCargando`) | `PrimaryButton`, `FilledButton`, `OutlinedButton` | |
| `widgets/campo.dart` (`Campo`, `CampoContrasena`, `CampoMonto`) | `AppTextField` | **Se conserva** la lógica de validar al salir + check verde, envuelta en el estilo nuevo. `CampoMonto` con prefijo de moneda |
| `widgets/insignia.dart` (con ícono) | `StatusChip` | `Insignia.encomienda(estado)`, `Insignia.viaje(estado)` |
| `widgets/icono_en_caja.dart`, `avatar.dart`, `progreso.dart` | `CircleAvatar`, `LinearProgressIndicator` | Avatar con color estable por nombre |
| `widgets/chips.dart` (con contador) | `TabBar`, `SegmentedButton`, `FilterChip` | |
| `widgets/aviso.dart` (`Aviso`, `Vacio`) | `EmptyState`, `ErrorView` | Error con "Reintentar" como `accion` |
| `widgets/esqueleto.dart` | spinners de listas | Esqueleto con forma de tarjeta-pase |
| `widgets/entrada.dart` | — | Escalonado 40 ms, máx. 8 |
| `widgets/toast.dart` (`Toasts` en `MaterialApp.builder`) | `showAppSnackBar` | API equivalente: `mostrarToast(context, texto, tipo:)` |
| `widgets/hoja.dart` (`mostrarHoja`) | `showModalBottomSheet` / `confirmar()` con `AlertDialog` | `confirmarConHoja(...)` reemplaza a `confirmar()` |
| `widgets/confirmacion_escrita.dart` | — | Retirar encomienda, marcar entregada |
| `widgets/barra_pestanas.dart` | `NavigationBar`, FAB | Contador con rebote |
| `widgets/pantalla.dart` | `Scaffold + AppBar + RefreshIndicator` | `CupertinoSliverNavigationBar` (con `previousPageTitle` en pantallas internas) + `CupertinoSliverRefreshControl`; relleno inferior para la barra flotante. Las pantallas internas (detalle, formularios) también lo usan |
| `widgets/encabezado_app.dart` | — | Marca + saludo + fecha + avatar (sin ojo) |
| `widgets/tarjeta_hero.dart` (`TarjetaHero`, `SubTarjetaVidrio`) | — | Nombre `TarjetaHero` para no chocar con `Hero` (que ya se usa en el pase) |
| `widgets/mosaico.dart` (`Mosaico`, `GrillaMosaicos`) | — | "Vista rápida" |
| `widgets/monto.dart` | `Text(Fmt.dinero(...))` | Cifras tabulares |
| `widgets/route_ticket.dart` | (se queda) | Re-estilo: radio 24, `sombraTarjeta`, `separador`, `Presionable` |
| `features/remitente/widgets/trust_row.dart`, `status_timeline.dart` | (se quedan) | Pasan a tokens y `Avatar` |

Al final se borran `primary_button.dart`, `placeholder_tab.dart`, `feedback_views.dart` (salvo el banner,
que pasa a `aviso.dart`) y `app_tokens.dart`.

## 8.4 Navegación nueva

```text
REMITENTE   ( Inicio · Envíos · Chats · Perfil )   ( + ) Nueva encomienda
VIAJERO     ( Mi viaje · Explorar · Chats · Perfil ) ( + ) Registrar viaje   ← solo si no hay viaje activo
```

- **Inicio del remitente (pantalla nueva):** `EncabezadoApp` → `TarjetaHero` Medianoche
  ("Tus envíos activos": número grande; sub-tarjetas *En camino* / *Disponibles*) → avisos que empujan a la
  acción → "Vista rápida" (mosaicos: *Por calificar*, *Entregadas*, *Buscar viajeros*, *Asistente*).
  La búsqueda de viajeros deja de ser pestaña y se abre desde su mosaico (decisión §8.8-3).
  Se agregan las rutas `/remitente/inicio` (contenido de la pestaña) y `/remitente/viajeros` (pantalla empujada).
- **Mi viaje (viajero):** `TarjetaHero` Cielo con la ruta y la fecha; sub-tarjetas *Llevas N* /
  *Ganas USD X* (suma de `valor` de las tomadas) + insignia de vuelo verificado / sin verificar.
- Si el viajero ya tiene viaje, el "+" **no se muestra** y la píldora ocupa todo el ancho (principio 1.4).
- **Contadores en la barra:** Envíos = entregadas sin calificar · Mi viaje = tomadas sin entregar.
  Chats no lleva contador (no hay "no leídos" en Firestore todavía).
- **Qué falta por calificar** se guarda en el teléfono (`Prefs.calificadas`): el backend ignora
  `encomiendaId` al calificar, así que no hay otra forma de saberlo. Lo calificado antes de la fase 4 no
  quedó registrado y puede aparecer una vez como pendiente.
- **Avisos que llevan directo a la acción** (principio 1.1), con `?accion=` en la ruta del detalle para
  desplazar hasta el botón:
  - Remitente: "Tu encomienda a Miami ya fue entregada · Califica al viajero" → calificar.
  - Viajero: "Tienes 2 encomiendas por entregar" → detalle con el botón *Marcar entregada* visible.
- El banner de "servidor despertando" se reubica por encima de la barra flotante
  (`Medidas.alturaTabbar + padding inferior + 12`).

## 8.5 Pantalla por pantalla

| Pantalla | Cambios |
|---|---|
| **Splash** | Marca centrada + `Progreso` indeterminado con tokens; error como `Aviso` |
| **Login** | Marca + propuesta de valor + mini pase decorativo; `Campo` / `CampoContrasena`; `Boton` con "Entrando…"; error de Firebase como `Aviso` debajo del botón (no snackbar) |
| **Registro** | `CampoContrasena(minimo: 6, nueva: true)` con aviso que se pone verde; confirmar contraseña |
| **Recuperar** | Un `Campo` + `Boton`; confirmación con `Vacio` de éxito |
| **Completar perfil** | Indicador de paso con `Progreso`; campos nuevos; `pais_picker` en `mostrarHoja` |
| **Elegir rol** | Dos `Tarjeta` grandes seleccionables con `IconoEnCaja` (ámbar / cielo) y borde del acento al elegir |
| **Inicio remitente** *(nuevo)* | Ver §8.4 |
| **Envíos** | `Pantalla` con título grande; `Chips` *Activas · Entregadas · Historial* con contador; lista de `RouteTicket` con `Entrada`; esqueletos; `Vacio` con "Publicar encomienda" |
| **Nueva encomienda** | Secciones con `Grupo`: Ruta (⇅) · Pago (`CampoMonto` + `Chips` de moneda) · Detalles; resumen en pase; `Boton` "Publicando…" |
| **Detalle encomienda (remitente)** | Pase arriba (`Hero`), `Insignia`, `StatusTimeline`, `TrustRow`; una acción principal según estado; *Retirar* → `ConfirmacionEscrita("RETIRAR")` en hoja; error dentro de la tarjeta de acción |
| **Buscar viajeros** | Campo de ciudad arriba, lista de `Tarjeta` con `TrustRow` y pase compacto; esqueletos |
| **Mi viaje** | Ver §8.4; encomiendas tomadas en `Grupo`; `Vacio` con "Registrar viaje" |
| **Registrar viaje** | Vuelo en mayúsculas; fecha en hoja; estado "Verificando vuelo…" → `Aviso` éxito o atención ("No pudimos verificar el vuelo; se mostrará como *sin verificar*") |
| **Explorar** | Cabecera con la ruta del viaje; `Chips` de orden (valor / fecha); valor con `Monto` destacado; *Tomar* → hoja con el texto de responsabilidad completo en caja visible (principio 1.6) |
| **Encomienda (viajero)** | Igual que el detalle del remitente; *Marcar entregada* → hoja explicando que cierra el chat + `ConfirmacionEscrita("ENTREGAR")` |
| **Conversaciones** | `Pantalla` + `Grupo` de filas con `Avatar`, ruta compacta y hora; esqueletos |
| **Chat** | Encabezado con ruta e `Insignia`; burbujas propias en `marcaSolido`, ajenas en `superficie`; compositor en `superficie2` radio 16; chat cerrado = `Aviso` fijo abajo |
| **Calificar / Reseñas** | Estrellas 48 dp; `Chips` de etiquetas; resumen de reseñas como `TarjetaHero` pequeña + barras `Progreso` por estrella |
| **Perfil** | Estilo ajustes: cabecera con `Avatar` grande + `Insignia` de rol; `Grupo` *Mis datos* (`Fila`), *Calificaciones*, *Cuenta* (cambiar de rol = 1 toque; cerrar sesión = hoja) |
| **Editar perfil** | `Campo`s en `Grupo`; toast "Perfil actualizado" |
| **Asistente** | Burbujas como el chat; sugerencias en `Chips`; como el backend responde 500, error visible junto al mensaje con "Reintentar" |

## 8.6 Reglas transversales (de la guía §5, aplicadas)

1. Ningún `Color(0x…)` ni `Colors.xxx` fuera de `tema.dart` (salvo blanco sobre degradados del hero).
2. Toda acción: botón con estado cargando + texto ("Publicando…", "Tomando…"), **error junto a la acción**
   (`Aviso` dentro de la tarjeta/hoja) y **toast de éxito**.
3. Toda cifra de dinero pasa por `Monto`.
4. Textos que cambian por rol salen de `Vocabulario`.
5. Irreversible = escribir palabra; con consecuencias = hoja; reversible = 1 toque.
6. Toda lista: esqueleto al cargar, `Vacio` con acción, error con "Reintentar", jalar para actualizar.
7. Relleno inferior en cada pestaña para que la barra flotante no tape contenido.
8. Barra de estado transparente con íconos según el brillo (`SystemUiOverlayStyle`).
9. Botones de ícono con `Semantics`/`tooltip` y 48 dp.

## 8.7 Fases de implementación (commits pequeños)

| Fase | Contenido | Commit(s) | Criterio de listo |
|---|---|---|---|
| **0** | Aprobar este plan y las decisiones §8.8 | `docs: plan de rediseño UI v2` | Decisiones anotadas aquí |
| **1** | Tokens y tema: `tema.dart`, `vocabulario.dart`, `monto.dart`; `app.dart` usa `construirTema`; `AppTheme`/`AppColors` quedan como alias temporales para no romper pantallas | `feat: tokens y tema v2` | `analyze` y `test` en verde, la app abre con colores nuevos |
| **2** | Componentes base: presionable, tarjeta, grupo, botón, campo, insignia, ícono en caja, avatar, progreso, chips, aviso/vacío, esqueleto, entrada, toast, hoja, confirmación escrita + **pruebas de widget** de cada uno (claro/oscuro, contraste, 48 dp, reducir movimiento) | 2–3 commits `feat:` | Pruebas nuevas pasan |
| **3** | Estructura: barra de pestañas, pantalla, encabezado, tarjeta hero, mosaico; re-estilo de `RouteTicket`, `TrustRow`, `StatusTimeline` | `feat: barra flotante y hero` | |
| **4** | `HomeShell` nuevo + Inicio del remitente + Mi viaje con hero; contadores y avisos con deep link. Se adelantó *Envíos* con chips (de 5b), porque Inicio abre un chip concreto, y `showAppSnackBar` pasó a usar toasts (la barra flotante tapaba el SnackBar) | `feat: inicio por rol` | Navegación completa en emulador |
| **5a** | Auth y onboarding (splash, login, registro, recuperar, completar perfil, elegir rol) | `feat(ui): auth y onboarding v2` | |
| **5b** | Remitente (envíos, nueva, detalle, buscar viajeros) | `feat(ui): remitente v2` | |
| **5c** | Viajero (explorar, registrar viaje, encomienda) | `feat(ui): viajero v2` | |
| **5d** | Chat, calificaciones, perfil, asistente | `feat(ui): chat, perfil y calificaciones v2` | |
| **6** | Limpieza (borrar widgets viejos y alias), lista de verificación §8.6 en claro y oscuro, letra al máximo en 360 dp, reescribir `docs/07`, README y bitácora | `refactor:` + `docs:` | Cero `Color(0x` fuera del tema; tag `rediseno-v2` |

Cada fase termina con `flutter analyze` limpio, `flutter test` en verde y prueba en el emulador.
Las pruebas existentes que buscan `FilledButton`, `CircularProgressIndicator`, `TextFormField` o
`Icons.check_circle` (`test/widget_test.dart`) se actualizan en la fase en que cambia el componente;
los textos que buscan las pruebas (p. ej. "Sí, tomarla", "Eres responsable de lo que llevas") se mantienen.

## 8.8 Decisiones (tomadas el 22-oct-2026)

1. **Paleta:** identidad Lapticon (Medianoche/Ámbar/Cielo) dentro de la estructura de tokens de la guía.
2. **Tipografía:** fuente del sistema para todo + Space Grotesk solo en ciudades del pase y cifras grandes.
   Manrope se elimina; `google_fonts` se queda solo para Space Grotesk.
3. **Inicio del remitente:** nueva pestaña Inicio (Inicio · Envíos · Chats · Perfil); Buscar viajeros pasa a
   un mosaico de "Vista rápida".
4. **Plataforma:** estilo iOS completo en ambas plataformas: `CupertinoSliverNavigationBar`,
   `BouncingScrollPhysics`, `CupertinoSliverRefreshControl`, transición `CupertinoPageTransitionsBuilder`.
   Selectores de fecha en hoja con `CupertinoDatePicker` (en vez del `showDatePicker` de Material).
5. *(menor)* Botón del ojo: se omite. Nombres de componentes en español como la guía.

## 8.9 Riesgos

- **Volumen:** ~25 pantallas/widgets tocados. Mitigación: fases con la app funcionando al final de cada una
  (alias temporales en la fase 1).
- **Contraste del degradado Cielo** con texto blanco pequeño (≈4.4:1): etiquetas `micro` con alfa ≥ 0.85
  o degradado más oscuro si la prueba falla.
- **`NoSplash` global** quita la onda de Material en widgets que no migren: por eso todos pasan a `Presionable`.
- **Toasts arriba** pueden tapar el título grande: duran 3,2 s y respetan `SafeArea`.
- **Estilo iOS en Android:** el botón *atrás* del sistema y el gesto predictivo siguen funcionando con
  go_router, pero hay que probar que `CupertinoSliverNavigationBar` muestre el botón de volver en rutas
  empujadas por go_router (si no, se pasa `leading` explícito). La letra grande del sistema puede cortar el
  título grande: se prueba con escala 2.0 en 360 dp.
- **Contadores** dependen de datos que ya se cargan (envíos, tomadas); si un provider no está cargado, el
  contador no aparece (no se muestra "0").
