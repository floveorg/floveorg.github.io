# flove

Sitio del proyecto **flove** — _slow it · flow it · love it._

Una página por app, HTML/CSS/JS sin frameworks. `index.html` en la raíz **es el
home**; las apps viven en `apps/` y la maquinaria del distro en `tools/`.

**Solo** ya no es una carpeta: es la *cualidad* de las apps (una app = un fichero
autocontenido, sin CSS/JS compartido, que funciona desde `file://`). El modo de
ejecución local se llama **LocalHost** (`flove-localhost.zip`, `localhost:8642`).
La especificación canónica sigue siendo **Central** (`central/apps/`) — ver
`development/standards/apps/README.md`.

## Estructura del repo

```
.
├── index.html          # home (flove.org/)
├── 404.html            # "cartel-recepcionista" de motes — GENERADO por tools/build-aliases.mjs
├── sw.js               # service worker (scope /) — GENERADO por tools/build-sw.mjs
├── .well-known/        # assetlinks.json (verificación Android TWA; ruta obligatoria)
├── apps/               # todas las apps + lanzador
│   ├── index.html      # lanzador (grafo / entrada / cuadrícula)
│   ├── apps-full.html  # catálogo completo
│   ├── appy · bio · blogy · economy · metas · psicosocial · puzzy · trusty
│   └── bubbles.html · apps-graph.html
├── tools/              # maquinaria del distro
│   ├── start.html      # selector de idioma + tour (?tour=1)
│   ├── manifest.webmanifest · apple-touch-icon.png
│   ├── routing.json    # metadatos de apps
│   ├── build-sw.mjs · build-aliases.mjs · build-flove-zip.sh
│   ├── check-distro.sh · serve-dev.sh
│   ├── flove-apk/      # Android TWA (keystore gitignored) — skill updaty-apk
│   └── flove-localhost.zip  # paquete de descarga ("Download / Go local")
├── docs/               # teoría / "Whole" (flove.org/docs/)
│   ├── index.html · paradigms.html · theory/
│   ├── README.md       # este archivo
│   └── LICENSE         # CC BY-SA 4.0
├── central/            # hub central (flove.org/central/): apps + shared (incl. media/images) + backend
├── decentral/          # área p2p (flove.org/decentral/): browsy y nety
├── development/        # workspace dev (binarios/addons gitignored)
│   ├── blog/           # blog Hugo → flove.org/development/blog (build in-place)
│   └── standards/      # context book dev: estándares + debates + herramientas
│       ├── apps/       # índice del distro (apps/README.md)
│       └── skills/     # skill library, trackeada en el repo
├── CNAME · .nojekyll   # config de GitHub Pages (dominio + sin Jekyll)
└── .gitignore
```

## Cómo se publica

**Gitea es la fuente de verdad; GitHub Pages sirve el sitio.**

1. Trabajas y commiteas contra Gitea: `localhost:3000/marc/flove` (rama `main`).
2. Para publicar, la skill `updaty-web` commitea el trabajo pendiente (tras
   listarlo y pedir confirmación), lo empuja a Gitea y refleja `main` a
   GitHub `floveorg/floveorg.github.io` (sólo el sitio principal: no recompila
   `sw.js`, ni el zip, ni los subdominios). Esas tareas pesadas van con
   `upgrady` cuando toca un release.
3. GitHub Pages sirve esa rama tal cual (estático, `.nojekyll`) en
   **https://flove.org** (dominio vía `CNAME`).

No hay build en CI: lo que está commiteado _es_ lo que se sirve.

### Rutas en producción

| Ruta | Qué es |
|---|---|
| `/` | home |
| `/apps/` | lanzador de apps (grafo / entrada / cuadrícula) |
| `/apps/apps-full.html` | catálogo completo |
| `/tools/start.html` | selector de idioma + tour (`?tour=1`) |
| `/central/shared/media/images/` | arte compartido (única carpeta canónica) |
| `/central/` | hub central (canonical: apps + shared + backend) |
| `/docs/` | teoría / Whole |
| `/decentral/` | área p2p (browsy, nety) |
| `/development/` | workspace dev; `/development/blog/` es el blog |
| `/development#localhost` | LocalHost (v0): el distro local explicado |
| `/nety`, `/willy`, … | motes → redirigen (404.html generada) |

## Descarga / uso local ("Go local")

El botón **Download / Go local** del home reparte
`tools/flove-localhost.zip`. Es un **subconjunto con las mismas rutas** que el
sitio: `index.html` + `apps/` + `central/shared/media/images/` + `tools/` + `docs/` + `sw.js`, todo
en `flove-localhost/`. No se aplana ni se reescribe ningún enlace:

1. Descomprime el zip.
2. Ejecuta el lanzador de tu sistema: **START-FLOVE-LINUX.sh** ·
   **START-FLOVE-MAC.command** · **START-FLOVE-WINDOWS.bat**.
3. Sirve `flove-localhost/` en `localhost:8642` y abre `/index.html` — el mismo
   home que flove.org. El selector de idioma y el tour están en
   `/tools/start.html`.
4. El lanzador escribe `tools/devices.json` con las direcciones LAN/Tailscale
   para abrir la misma instancia desde el móvil (Ajustes ▸ Devices).

Los lanzadores se **generan al construir el zip** — no se versionan, para
mantener limpia la raíz servida y que ninguna ruta de máquina acabe en git.

### Reconstruir el paquete

El zip y `sw.js` son artefactos de **release pesada**: los refresca la skill
`upgrady`, nunca el desarrollo normal ni `updaty-web`. `updaty-web` solo
commitea el trabajo pendiente (tras listarlo y pedir confirmación), lo empuja a
Gitea y lo publica en GitHub.

El zip excluye lo que solo tiene sentido en la web: `central/`, `decentral/`,
`development/`, el APK, `docs/docs-files` y los propios scripts de build.

## Trabajo local (dev)

```bash
tools/serve-dev.sh                 # sirve la raíz del repo en localhost:8642
# → http://localhost:8642/index.html
```

Sirve **la raíz del repo**, así que las rutas locales son idénticas a las de
flove.org (`/apps/…`, `/tools/…`, `/docs/…`).

## Blog (`flove.org/development/blog`)

El blog vive **dentro de este repo**, en `development/blog` (Hugo, tema
`flovelite`). `development/blog/build-blog.sh build` regenera el HTML **dentro
del propio directorio** (sin segmento `public`) y viaja con el sitio principal
vía `publish-web.sh` → sirve en `flove.org/development/blog/`.

- Escribir/publicar posts, borradores privados → en `development/blog` (ver su README).
- Los borradores (`draft:true`) viven solo en local y **nunca** se sirven.
- El blog **no** va en `flove-localhost.zip` (la descarga es apps + docs).

## Licencia

Todo el contenido de este repositorio (texto, código, diseños) está bajo
**[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
Ver [`LICENSE`](./LICENSE) para los términos completos.

Atribución sugerida: `flove · Marc (marcflove) · flove.org · CC BY-SA 4.0`.
