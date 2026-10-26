"""Genera docs/api/index.html (Swagger UI con el contrato incrustado) a partir de openapi.yaml.

Se incrusta el contrato para que index.html abra con doble clic, sin servidor.
Uso: python3 docs/api/generar_visor.py
"""
import json
from pathlib import Path

import yaml

AQUI = Path(__file__).parent
SWAGGER_UI = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14"

contrato = yaml.safe_load((AQUI / "openapi.yaml").read_text(encoding="utf-8"))
contrato.pop("x-ejemplos", None)  # solo servían de anclas
spec = json.dumps(contrato, ensure_ascii=False).replace("</", "<\\/")

html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lapticon API</title>
  <link rel="stylesheet" href="{SWAGGER_UI}/swagger-ui.css">
  <style>
    body {{ margin: 0; background: #fff; }}
    .aviso {{ font: 14px/1.5 system-ui, sans-serif; background: #FFF7E6; color: #5C3B00;
             border-bottom: 1px solid #F0D9A8; padding: 10px 16px; }}
    .aviso code {{ background: #F7E7C4; padding: 0 4px; border-radius: 4px; }}
    /* Resalta la sección de endpoints que faltan en el backend. */
    .opblock-tag[data-tag^="🆕"] {{ background: #FFF4F0; border-left: 4px solid #D9480F; }}
  </style>
</head>
<body>
  <div class="aviso">
    Contrato verificado contra el servidor el 22-oct-2026. ✅ funciona · ⚠️ falla o se comporta distinto ·
    🆕 <strong>no existe</strong> (propuesta). Solo lectura: el backend no permite CORS desde el navegador, así que
    las pruebas se hacen con Postman o <code>curl</code>. Generado desde <code>openapi.yaml</code>.
  </div>
  <div id="swagger-ui"></div>
  <script src="{SWAGGER_UI}/swagger-ui-bundle.js" crossorigin></script>
  <script>
    window.ui = SwaggerUIBundle({{
      spec: {spec},
      dom_id: "#swagger-ui",
      deepLinking: true,
      docExpansion: "list",
      defaultModelsExpandDepth: 0,
      defaultModelExpandDepth: 2,
      displayOperationId: false,
      supportedSubmitMethods: [],
    }});
  </script>
</body>
</html>
"""
(AQUI / "index.html").write_text(html, encoding="utf-8")
print("docs/api/index.html generado")
