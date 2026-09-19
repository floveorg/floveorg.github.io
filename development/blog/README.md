# blog (flove development/blog)

Fuente **Hugo** del blog de flove. Vive en este repo, en `development/blog`. El
HTML construido se escribe **dentro de este mismo directorio** (sin segmento
`public`) y viaja con el sitio principal vía `publish-web.sh` →
**https://flove.org/development/blog/**.

- **Editas aquí** — `development/blog`, parte de `marc/flove` (Gitea, privado).
  Los **borradores son de verdad privados**: ni se construyen ni se publican;
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
- **Post público:** `draft: false` → entra en la build y sale a
  flove.org/development/blog.

## Publicar

```bash
./build-blog.sh build     # regenera el HTML en development/blog/ (production, sin borradores)
./build-blog.sh publish   # build + commit + push Gitea + publish-web.sh → live
```

`publish` hace lo mismo que `updaty-web` (commit del output, push a Gitea,
`publish-web.sh` a GitHub). El blog ya **no** se publica a un repo separado
`floveorg/blog`: sale junto al sitio principal.

## Estructura

```
.
├── hugo.toml            # config (baseURL https://flove.org/development/blog/)
├── content/posts/       # los artículos (.md)
├── themes/flovelite/    # tema propio, sin JS
├── archetypes/          # plantilla de post nuevo (draft: true por defecto)
├── build-blog.sh        # serve · build · publish
└── index.html, posts/, tags/…  # HTML construido (committed, se sirve en flove.org/development/blog)
```

Licencia del contenido: **CC BY-SA 4.0**.
