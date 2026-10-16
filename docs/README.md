# flove

Sitio del proyecto **flove** — _slow it · flow it · love it._

Página única por app, HTML/CSS/JS sin frameworks. `index.html` en la raíz
redirige al home **`solo/`** (flove.org/solo/). El distro **Solo** está en
**bajo mantenimiento / poco desarrollo**: la especificación canónica son las apps
**Central** (`central/apps/`) — ver `development/standards/solo/README.md`.

## Estructura del repo

```
.
├── index.html          # redirige a /solo/
├── 404.html            # "cartel-recepcionista" de motes (nety, willy, …) — GENERADO por solo/build-aliases.mjs
├── central/            # hub central (flove.org/central/): apps + shared + backend
├── solo/               # área PWA (flove.org/solo/) — EL home real; distro bajo mantenimiento/legacy
│   ├── index.html      # home del solo
│   ├── launch.html     # selector de idioma EN/ES (→ START.html dentro del zip)
│   ├── manifest.webmanifest  # metadatos PWA (instalar como app)
│   ├── sw.js           # service worker (offline) — GENERADO por build-sw.mjs
│   ├── apps/           # índice de demos (flove.org/solo/apps/) + las apps
│   ├── appy · blogy · economy · metas · …   # las apps (appy/nety.html incluye nety)
│   ├── flove-apk/      # Android TWA (keystore gitignored) — ver skill updaty-apk
│   ├── build-sw.mjs    # regenera sw.js (precache + versión)
│   ├── build-flove-zip.sh  # construye flove-solo.zip desde solo+aplanada + docs + images
│   ├── build-aliases.mjs   # genera la 404.html de motes desde solo/apps/index.html
│   └── flove-solo.zip  # paquete de descarga ("Download / Go local")
├── docs/               # teoría / "Whole" (flove.org/docs/)
│   ├── index.html · paradigms.html · theory/
│   ├── README.md       # este archivo
│   └── LICENSE         # CC BY-SA 4.0
├── decentral/          # área p2p (flove.org/decentral/): browsy y nety
│   ├── browsy/         # extensión
│   └── nety/           # repo APARTE (floveorg/nety) anidado + gitignored — solo su página va aquí
├── development/        # workspace dev (binarios/addons gitignored)
│   ├── blog/           # blog Hugo → flove.org/development/blog (build in-place)
│   └── standards/      # context book dev: estándares de producción + debates + herramientas
│       ├── solo/       # SOLO (legacy) — estado/distro bajo mantenimiento + índice (solo/README.md)
│       └── skills/     # skill library de Claude Code, trackeada en el repo (flove.org sirve la copia)
├── CNAME · .nojekyll   # config de GitHub Pages (dominio + sin Jekyll)
└── .gitignore · .htmlvalidate.json
```

Nota: `solo/flove.zip` (antiguo) sigue versionado pero ya no se reconstruye; el
paquete actual es `flove-solo.zip`.

## Cómo se publica

**Gitea es la fuente de verdad; GitHub Pages sirve el sitio.**

1. Trabajas y commiteas contra Gitea: `localhost:3000/marc/flove` (rama `main`).
2. Para publicar, la skill `updaty-web` regenera `sw.js`, empuja a Gitea y
   refleja `main` a GitHub `floveorg/floveorg.github.io`.
3. GitHub Pages sirve esa rama tal cual (estático, `.nojekyll`) en
   **https://flove.org** (dominio vía `CNAME`).

No hay build en CI: lo que está commiteado _es_ lo que se sirve.

### Rutas en producción

| Ruta | Qué es |
|---|---|
| `/` | redirige a `/solo/` |
| `/central/` | hub central (canonical: apps + shared + backend) |
| `/solo/` · `/solo/apps/` | home real · índice de demos (distro bajo mantenimiento) |
| `/docs/` | teoría / Whole |
| `/decentral/` | área p2p (browsy, nety) |
| `/development/blog/` | blog (viaja con el sitio principal) |
| `/nety`, `/willy`, … | motes → redirigen (404.html generada) |

## Descarga / uso local ("Go local")

El botón **Download / Go local** del home reparte `solo/flove-solo.zip` —
empaqueta exactamente dos cosas: `solo/` (la app, renombrada a `flove-solo/` y
aplanada: su contenido —incluidos `audio/` e `images/`— queda en la raíz del
paquete) y un `docs/` mínimo (solo `index.html` y `paradigms.html`, las dos
páginas que enlaza el sitio). Nada se extrae de `central/`:

1. Descomprímelo.
2. Ejecuta el lanzador de tu sistema: **START-FLOVE-LINUX.sh** ·
   **START-FLOVE-MAC.command** · **START-FLOVE-WINDOWS.bat**.
3. Sirve la carpeta en `localhost:8642` y abre `flove-solo/START.html` (el
   selector de idioma, renombrado desde `launch.html` en la descarga). Elige
   idioma y listo.

Los lanzadores se **generan al construir el zip** — no se versionan, para
mantener limpia la raíz servida y que ninguna ruta de máquina acabe en git.

### Reconstruir el paquete (tras commitear tus cambios)

```bash
node solo/build-sw.mjs              # sw.js al día (commitéalo si cambia)
bash solo/build-flove-zip.sh        # → solo/flove-solo.zip (solo+aplanada + docs + images)
git add solo/flove-solo.zip && git commit
```

El zip excluye lo que solo tiene sentido en la web: lowai (se publica aparte),
fuga, los generadores, el APK y la infraestructura del repo.

## Trabajo local (dev)

```bash
cd flove && python3 -m http.server 8000
# → http://localhost:8000/
```

## Blog (`flove.org/development/blog`)

El blog vive **dentro de este repo**, en `development/blog` (Hugo, tema
`flovelite`). `development/blog/build-blog.sh build` regenera el HTML **dentro
del propio directorio** (sin segmento `public`) y viaja con el sitio principal
vía `publish-web.sh` → sirve en `flove.org/development/blog/`.

- Escribir/publicar posts, borradores privados → en `development/blog` (ver su README).
- Los borradores (`draft:true`) viven solo en local y **nunca** se sirven.
- El blog **no** va en `flove-solo.zip` (la descarga es solo las apps + docs).

## Licencia

Todo el contenido de este repositorio (texto, código, diseños) está bajo
**[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**.
Ver [`LICENSE`](./LICENSE) para los términos completos.

Atribución sugerida: `flove · Marc (marcflove) · flove.org · CC BY-SA 4.0`.
