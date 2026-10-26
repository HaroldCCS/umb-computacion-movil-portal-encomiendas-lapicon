# Contrato de la API en Swagger (OpenAPI 3.1)

La colección de Postman del profesor convertida en un contrato OpenAPI, **corregido con lo que responde el servidor de
verdad** (22-oct-2026) y con los endpoints que **faltan** en el backend.

| Archivo | Qué es |
|---|---|
| [`openapi.yaml`](openapi.yaml) | El contrato (fuente única): rutas, bodies, esquemas y ejemplos reales |
| [`index.html`](index.html) | Visor Swagger UI con el contrato incrustado. **Abre con doble clic**, sin servidor |
| [`generar_visor.py`](generar_visor.py) | Regenera `index.html` después de editar `openapi.yaml` |

## Cómo verlo

- **Local:** abrir `docs/api/index.html` en el navegador.
- **En línea, sin instalar nada:** pegar el contenido de `openapi.yaml` en https://editor.swagger.io.
- **En Postman:** *Import* → `openapi.yaml` crea una colección nueva con los bodies de ejemplo.

## Qué contiene

28 operaciones en 9 grupos, cada una marcada en el título:

| Marca | Significado | Cuántas |
|---|---|---|
| ✅ | Existe y responde como se documenta | 11 |
| ⚠️ | Existe, pero falla en el servidor (500) o se comporta distinto (no valida, descarta campos) | 9 |
| 🆕 | **No existe**: la app lo necesita y hoy lo resuelve en el dispositivo | 8 |

Cada operación trae el body de entrada con su esquema, las respuestas reales por código (200/201, 400, 401, 403, 404,
500) y, cuando aplica, la explicación de lo que hace distinto el servidor.

### Endpoints que faltan (sección 🆕)

| Propuesta | Por qué hace falta |
|---|---|
| `PUT /api/users/{uid}/rol` | El backend descarta `rol`; la app lo guarda en el celular y se pierde al cambiar de dispositivo |
| `GET /api/users/{uid}/publico` | Ver el perfil de otro usuario da 403: el remitente no puede ver el nombre del viajero que tomó su encomienda |
| `GET /api/encomiendas/viajero` | No hay forma de listar las encomiendas que tomé; la app las recuerda por dispositivo |
| `GET /api/encomiendas/{id}` | No hay detalle de una sola encomienda; la app recarga listas enteras |
| `DELETE /api/encomiendas/{id}` | No existe `cancelada`: retirar deja la encomienda `vencida`, igual que una caducada |
| `PUT /api/viajes/{id}/estado` | El error de "ya tienes un viaje" dice "debes cerrarlo", pero no hay cómo cerrarlo |
| `GET /api/ratings/pendientes` | `encomiendaId` se ignora; la app recuerda en el celular qué entregas ya calificó |
| `PUT /api/users/{uid}/token-push` | Sin notificaciones push, nadie se entera de un cambio si no abre la app |

## Por qué el visor es de solo lectura

El backend responde sin `Access-Control-Allow-Origin`, así que el navegador bloquea las peticiones de "Try it out"
desde otro dominio (la PWA lo evita con su propio proxy). Para probar: Postman (con la colección importada) o `curl`
con `Authorization: Bearer <idToken>`.

## Mantenerlo

1. Editar `openapi.yaml`. Los ejemplos que se repiten están al inicio en `x-ejemplos` como anclas YAML (`&viaje`,
   `*viaje`), porque `$ref` no funciona dentro de `example`.
2. Validar:

   ```bash
   npx @redocly/cli@1.34.3 lint docs/api/openapi.yaml
   ```

   Hoy da 0 errores y 5 avisos esperados: falta `license`, `tomar/{id}` y `{id}/estado` son rutas ambiguas (así son
   en el backend) y tres rutas públicas no tienen respuesta 4xx.
3. Regenerar el visor:

   ```bash
   python3 docs/api/generar_visor.py
   ```
