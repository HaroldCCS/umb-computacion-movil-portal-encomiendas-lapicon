# Código fuente en GitHub

> Entregable del tablero: **"Cód. fuente GitHub"**. Estado: ✅ publicado (24-oct-2026).

## 1. Repositorios

| Repositorio | Contenido | Para entregar |
|---|---|---|
| [umb-computacion-movil-portal-encomiendas-lapicon-flutter](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter) | App Flutter (Android e iOS), pruebas y CI | Enlace del repo + [APK de la última versión](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter/releases/latest/download/lapticon.apk) |
| [umb-computacion-movil-portal-encomiendas-lapicon-pwa](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-pwa) | PWA (React + TypeScript), pruebas y CI | Enlace del repo + https://lapticon.haroldsoftware.com |
| [umb-computacion-movil-portal-encomiendas-lapicon](https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon) | Documentación: `docs/`, entregables, referencias | Este repositorio |

Los tres son públicos. Las apps se separaron del repositorio original **conservando su historial** de commits.

## 2. Cómo ejecutar cada app

**Flutter** (necesita el `google-services.json` del curso, que no se sube):

```bash
git clone https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-flutter.git lapticon_app
```

```bash
cd lapticon_app && bash setup.sh && flutter run
```

**PWA** (necesita `VITE_FIREBASE_API_KEY` en `.env.local`):

```bash
git clone https://github.com/HaroldCCS/umb-computacion-movil-portal-encomiendas-lapicon-pwa.git aplicacion_pwa
```

```bash
cd aplicacion_pwa && npm install && npm run dev
```

Los README de cada repositorio explican la configuración, la arquitectura y los problemas comunes.

## 3. Lo que un revisor encuentra en el código

| Criterio (10 % "repositorio, código y documentación") | Dónde verlo |
|---|---|
| Arquitectura por capas | `lib/core`, `lib/data`, `lib/features` (Flutter) · `src/core`, `src/datos`, `src/funciones` (PWA) |
| Consumo de la API con Bearer idToken | `lib/core/network/api_client.dart` · `src/core/red/cliente.ts` |
| Contrato de la API en un solo lugar | `lib/data/repositories/` · `src/datos/repositorios/index.ts` |
| Chat en tiempo real | `lib/features/chat/chat_service.dart` · `src/funciones/chat/servicio-firestore.ts` |
| Pruebas | `test/` (184 casos) · `src/**/*.test.ts` (123) y `pruebas/e2e/` (26 en iPhone y Android) |
| Integración continua | `.github/workflows/` de cada repo (verde en cada push) |
| Seguridad de credenciales | `.gitignore`; claves solo en secretos de GitHub y variables de Cloudflare |
| Historial legible | Commits pequeños en español (`feat:`, `fix:`, `docs:`, `test:`, `ci:`) |
| Documentación | README de cada repo, `docs/01`–`docs/10`, bitácora y esta carpeta |

## 4. Antes de entregar

- [ ] Confirmar que el último CI de cada repo está en verde (pestaña *Actions*).
- [ ] Descargar el APK del enlace y probar que instala.
- [ ] Abrir la PWA en el celular e iniciar sesión.
- [ ] Agregar al README de documentación el enlace del video.
