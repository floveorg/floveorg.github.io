# blog (marc/blog)

Fuente **Hugo** del blog de flove. Vive anidado en `flove/blog` (repo Gitea
`marc/blog`, privado). El HTML construido se publica a **GitHub `floveorg/blog`**,
que sirve **https://flove.org/blog/**.

- **Editas aquí** — Gitea `marc/blog` (privado, no se sirve en la web). Por eso
  los **borradores son de verdad privados**: ni se construyen ni se publican;
  viven solo en este repo.
- Tema propio **`flovelite`** (0-JS, una hoja de estilo, claro/oscuro).
- Requiere [Hugo extended](https://gohugo.io/installation/)
  (`snap install hugo --channel=extended`).

## Escribir

```bash
hugo new posts/mi-articulo.md   # nace con draft: true (privado)
./build-blog.sh serve           # preview CON borradores → http://localhost:1313/
```

- **Borrador privado:** `draft: true` → no entra en la build ni en la web; vive
  solo en este repo. Para publicarlo, pon `draft: false`.
- **Post público:** `draft: false` → entra en la build y sale a flove.org/blog.

## Publicar

```bash
./build-blog.sh publish   # build (sin borradores) + push a floveorg/blog → live en flove.org/blog
```

Usa el token de `~/Claude/token-github-flove.md` (ampliado a `floveorg/blog`). El
`push` reescribe el output como un único commit en `floveorg/blog` (repo de
deploy). No hace falta `update-web` para el blog: publica directo.

## Estructura

```
.
├── hugo.toml            # config (baseURL https://flove.org/blog/)
├── content/posts/       # los artículos (.md)
├── themes/flovelite/    # tema propio, sin JS
├── archetypes/          # plantilla de post nuevo (draft: true por defecto)
└── build-blog.sh        # serve · build · publish
```

Licencia del contenido: **CC BY-SA 4.0**.
