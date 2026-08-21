# Risa Liberada — Presentación y estándar del circuito (v1)

**Fecha:** 2026-08-16
**Versión:** **v1 en polish — release sin cortar todavía** · changelog y política de versiones en el repo (`CHANGELOG.md` · `VERSIONING.md`)
**App:** Risa Liberada (`projects/liberada/risa/`)
**Bot:** @RisaLiberadaBot · **Canal público:** @risaliberada
**Web en vivo:** [risa.liberada.net](https://risa.liberada.net) · **Réplica del sistema:** sección «Replica Nuestro Sistema» de la web (pestaña **Ciencia**), con *Introducción* (flujo paso a paso + **Agentes** plegable + **features ya hechas** plegable) y *Desarrollo* (v2 + v3)
**Estado:** estándar v1 — **estable** (base de recuperación; el polish llega después de flove v2, D20)
**Plan v2:** [`plan-v2.md`](plan-v2.md) — todos los planes para la v2 centralizados (repo de risa + flove central)
**Diagramas:** `mermaid/` (risaliberada-v1-thread · risaliberada-v1-flow · flove-v2-thread · flove-v2-flow) — `.mmd` para Excalidraw, `.png` (3×) y `.svg` (vector, nítidos)

---

## Introducción

Un circuito para que **la gente aporte su risa** y **un grupo de moderadores la publique o la descarte**, sin servidor que mantener. Telegram es la herramienta de tres caras — **subir · moderar · escuchar** — y la web es el escaparate público.

- **Alguien sube** un audio (o vídeo) de su risa **por Telegram** (nota de voz al bot, el gesto nativo del móvil).
- **Un grupo de moderadores** recibe cada clip en un chat privado y decide con botones: **✅ Publicar / 🗑 Borrar / ✏️ Editar**.
- Si se **publica**, el clip entra en la **playlist reproducible de la web** *y* se publica en el **canal público de Telegram**, para escucharlo también ahí.
- Si se **borra**, se descarta.

### Objetivos (desde el diseño original, siguen vigentes)

- Circuito completo subir → aprobar → publicar, funcionando de punta a punta.
- **Cero servidor que vigilar**: todo vive en GitHub (repo + secret + un workflow).
- **Mobile-first**: grabar una nota de voz es el gesto nativo del móvil.
- Todo **FOSS** y con **licencia libre** en cada clip (CC BY-SA 4.0).

### Decisiones de arquitectura que dan forma al sistema

- **El único punto delicado — y cómo se resuelve «escuchar en Telegram»:** un bot por cron solo está «despierto» cada pocos minutos, así que **no puede** responder en tiempo real. Por eso **escuchar en Telegram = un canal público**: cada clip aprobado se publica ahí como audio reproducible; cualquiera hace scroll y toca play cuando quiera. Subir y los toques ✅/🗑 sí pueden ser asíncronos — unos minutos de retardo en una risa no importan.
- **Por qué GitHub Actions (cron) y no un VPS:** todo en GitHub, mismo espíritu serverless, `ffmpeg` ya viene en el runner. Compromisos aceptados: latencia de un ciclo (~5–15 min), cron *best-effort* (se pausa tras 60 días sin actividad; cualquier push lo reactiva) y estado guardado en el repo (`offset.txt`) para no reprocesar ni perder. Un VPS queda como respaldo futuro y el diseño lo deja como *drop-in* (§Modelo de datos: lógica pura).
- **Repo dedicado** `floveorg/risa`, separado del repo fuente de flove (Gitea) y del sitio publicado: aísla binarios, concentra el secret en un solo sitio y **no toca** el pipeline `updaty-web`. La web hace `fetch` de `risa.json` desde ese origen (CORS permisivo); `<audio>`/`<video>` cross-origin no necesita CORS.

### No-objetivos (v1)

- Puerta de subida web con login social/email → **authy + claim son v2** (`plan-v2.md`).
- Clasificar el clip en playlists temáticas al aprobar → resuelto con **etiquetas** (chips/búsqueda/favoritos).
- Bot conversacional en tiempo real → resuelto vía canal (escuchar) + comandos de solo lectura y reproducción.

---

## 1. Superficies y roles

| Rol | Cómo entra | Qué puede hacer |
|-----|-----------|-----------------|
| **Persona que aporta** | DM a @RisaLiberadaBot | Pulsar START, enviar nota de voz/audio/vídeo, elegir identidad, etiquetas y visibilidad |
| **Moderador/a** | Miembro del **grupo privado de moderación** | Ver la cola, tocar **✅ Publicar / 🗑 Borrar / ✏️ Editar** |
| **Público** | Web (`index.html`, risa.liberada.net) · canal @risaliberada | Escuchar las risas |

La subida es **abierta pero identificada**: cualquiera aporta, pero Telegram da una identidad verificada que frena el spam y da a los moderadores un contacto.

---

## 2. Cómo funciona — el circuito en cuatro hilos

### Hilo A · Subir (persona ↔ bot)

1. La persona entra al bot por **deep link** (`t.me/RisaLiberadaBot`, botón «💬 Comparte tu risa» de la web) o **QR** del modal «cómo aportar».
2. **(Primera vez)** pulsa el botón **START / Iniciar**.
3. El bot muestra el **aviso de licencia**: *«Al enviar tu risa la publicas en libre, bajo CC BY-SA 4.0, atribuida al nombre que elijas.»* **Enviar = consentir.**
4. La persona envía su **nota de voz / audio / vídeo** (máx. 1 min · 10 MB · 5 en cola y 5 al día).
5. El bot pregunta **identidad** — 3 opciones:
   - **① ID Telegram** — el id de Telegram. Solo: se muestra directo. Combinado con ②: se oscurece (hash).
   - **② Nombre público** — la persona elige un **nombre** a mostrar (palabra).
   - **③ Anónimo** — sin nombre («Anónima»).
   - **Combinación ①+②:** el Nombre público **oscurece** el ID — se guarda solo un **hash salado** como handle; el id en claro nunca viaja. *No es claim (eso es v2).*
6. El bot pregunta **etiquetas** (opcional, separadas por coma). Default: **`libre`**.
7. **Confirmación.** El bot responde con el mensaje real: *«Gracias, lo revisamos en breve y te avisamos cuando se publique.»*
8. El siguiente **cron** recoge el clip → lo mete en `state/queue.json` (con `file_id`, sin descargar aún) → lo reenvía al **grupo privado de moderación**.

### Hilo B · Moderar (bot ↔ grupo privado)

1. El clip llega con audio/vídeo reproducible + palabra + tags (+ enlace opt-in) y botones inline **✅ Publicar / 🗑 Borrar / ✏️ Editar** (el `callback_data` lleva el id de la cola).
2. Un moderador toca un botón; el siguiente cron recoge el `callback_query`.
   - **✅ Publicar:** descarga el `file_id` → `ffmpeg` → MP3 normalizado (o MP4 H.264 si es vídeo) → sube a **Cloudflare R2** (`risa/b_*.mp3`/`.mp4`) → `src` = URL R2 pública → **prepend** de la entrada a `risa.json` (newest-first) → commit + push → post del audio al **canal público @risaliberada** → edita el mensaje del grupo a «✅ Publicado».
   - **🗑 Borrar:** quita el clip de `state/queue.json`, edita el mensaje a «🗑 Borrada».
   - **✏️ Editar (detalles con visto bueno del autor):** el moderador manda una línea `Título | Tags | Nombre` → el bot la propone al grupo; con «📨 Proponer al autor» envía el DM al autor original con **✅ Aceptar / ❌ Rechazar**; el bot solo publica si el autor acepta (el ✅ del grupo queda bloqueado mientras tanto). Rechazar conserva lo original.
3. Se actualiza `state/offset.txt`.

> El handle del moderador vive **solo** en el grupo privado; nunca llega a la web.

### Hilo C · Escuchar (público)

- **Web:** `fetch` de `risa.json` → **playlist «Risa liberada»** (mismo renderizador que las otras) + feed **«Últimas risas»** = últimos N reales (`slice(0,N)`). Estados **vacío** («aún no hay risas, sé la primera 💛») y **error de red**. **Tags → chips** (filtrables). Nombre = **palabra**; con **①+②** el hash habilita el enlace a `t.me/<usuario>` (opt-in `tg_public`); con **solo-①** se muestra el ID directo. **Cada autor publicado tiene su página de autor** (`#/u/<key>`, tag-url automática) con su propio **feed**: el bot regala la URL en el DM de publicación, incluso con solo nombre público. **Hilos** (v1 adelanto): clips con `parent` forman cadenas infinitas; `threadOrder()` aplica recorrido en profundidad; conectores visuales y etiqueta del autor respondido.
- **Subdominio automático** (v1 adelanto): al aprobar el primer clip, `ensureUsername()` genera `username.liberada.net` sin auth ni claim; se almacena en `usernames.json` y la web lo muestra en la confirmación.
- **Perfil agregador** (`liberada.net/usa/<username>/`): el Worker de Cloudflare redirige `username.liberada.net` → `liberada.net/usa/<username>/`, que agrega risas + amas del usuario. Genérico para cualquier username; sin deploy por usuario.
- **Telegram:** el canal acumula cada clip aprobado como audio reproducible; se escucha con scroll.

### Hilo D · Consultar (persona ↔ bot)

El bot responde a comandos de **solo lectura y reproducción** (no cambian estado; el parseo y las consultas viven en `bot/logic.mjs` y sus tests):
- **Base:** `/me` (tu página de autor y tus números) · `/stats` (totales) · `/profile [palabra]` (tu página, o las de quien lleve ese nombre) · `/status` (estado del circuito) · `/queue` (lo que hay en moderación).
- **Exploración:** `/latest` · `/now` · `/today` · `/since <N días>` · `/random` · `/trending`.
- **Reproducción:** `/play` (manda el último clip publicado).

---

## 3. Funcionalidades — inventario completo (v1)

### Web — el escaparate

- App de archivo único: HTML + CSS + JS, sin build y sin dependencias; servida desde GitHub Pages (estático, HTTPS, coste cero).
- Un solo feed (`risa.json`) como fuente de verdad de la web.
- Playlists con un reproductor factory compartido: play/pausa, anterior/siguiente y lista de pistas.
- El feed puede incluir **vídeo** (mp4/webm) de otros bots sin tocar la web (mark `video: true` por entrada).
- «Últimas risas»: feed de las últimas n piezas (por defecto 6) · paginador del feed.
- Chips de etiquetas filtrables · nube de tags flotante con colisiones evitadas (`floatChips`) · búsqueda por tag · título · nombre.
- Favoritos ❤️/⭐ compartidos por las playlists · **v1.x (D21):** suben a dato de autor vía bot (DM/Mini App → cron → `lol/<key>/favorites.json`), sin claim — aprobado = derechos.
- Página de autor `#/u/<key>` con su propio feed.
- **Hilos** (v1 adelanto): clips con `parent` forman cadenas infinitas; `threadOrder()` aplica DFS; conectores CSS verticales + etiqueta del autor respondido.
- **Subdominio automático** (v1 adelanto): al primer approve, `ensureUsername()` genera `username.liberada.net` (sin auth ni claim) y lo muestra en la confirmación.
- **Perfil agregador** (`liberada.net/usa/<username>/`): Cloudflare Worker redirige `username.liberada.net` → perfil que agrega risas + amas.
- Compartir por WhatsApp, Telegram, e-mail y copiar · QR del deep link `t.me/RisaLiberadaBot`.
- Imágenes y audio servidos desde R2 con URL pública (no desde GitHub) · procedencia y licencia enlazada.
- Carrusel de beneficios de la risa (20 datos) que conecta con la sección ciencia.
- Modal «cómo aportar» con **Ver/Ocultar** de los requisitos (límites, licencia, página de autor, comandos, etiquetas, deep link + QR, repo dedicado) y selector **«Como aquí» / «Pregúntame»** para la réplica.
- Sección «Replica Nuestro Sistema»: *Introducción* (flujo paso a paso + **Agentes** plegable con copiar + **features ya hechas**) y *Desarrollo* (v2 + v3).

### Bot — el circuito serverless

- Ingesta por Telegram: audios **y vídeos** de hasta 1 min.
- Límites duros: 10 MB por pieza (20 MB en la ingesta de vídeo), 5 en cola y 5 al día por remitente.
- Validación de tipo, extensión, tamaño y duración antes de subir.
- Offset persistido e idempotencia en `getUpdates` (ni pérdidas ni duplicados) · long polling de 25 s (sin endpoint público ni webhook).
- Cron de GitHub Actions como motor (cada 5–10 minutos).
- Identidad al subir: nombre público, id de Telegram o anónima · handle estable por palabra + hash salado (nunca `@username`).
- Formulario guiado con botones inline: descripción, etiquetas y visibilidad.
- **Cadenas** (v1 adelanto): forward del canal → bot detecta `forward_from_chat` → usuario responde → clip publicado con `parent`. Ciclo detectado con `hasAncestor()`. Notificación al autor original en reply.
- **Subdominio automático** (v1 adelanto): `ensureUsername()` en approve genera `username.liberada.net`, almacena en `usernames.json`, muestra en la confirmación.
- Normalización a MP3 (audio) o MP4 H.264 (vídeo) con `ffmpeg` · subida a Cloudflare R2 con firma SigV4 propia (cero dependencias).
- La pieza aprobada **antepone** a `risa.json` (git como base de datos) · commit + push automáticos del feed · publicación en el canal público @risaliberada.
- Moderación humana en grupo privado: ✅ publicar, 🗑 borrar, ✏️ proponer detalles · edición con visto bueno del autor (nadie publica contra su voluntad).
- Confirmaciones y avisos en español (subida, aprobación, rechazo, publicación) · reconocimiento de decisiones por palabra («ok», «sí», «no», «borrar»…).
- Mensajes malformados nunca tumban el bucle: `parseUpdates` es una función pura · cliente de Telegram con timeout y manejo de errores de red.
- Bienvenida con las reglas claras (1 min, 10 MB, 5 al día).
- Scripts de mantenimiento: `migrate-r2.mjs` y `sync-media.mjs`.

### Moderación y confianza

- Solo los moderadores del grupo pueden aprobar o rechazar · nada se publica sin revisión humana.
- Gate de aceptación: la edición propuesta se publica solo si el autor acepta.
- Certificación «autenticado en Telegram» en la página de autor (un moderador aceptó tu post).
- Enlace a t.me solo con opt-in explícito (nunca automático) · cuota y cola por remitente como anti-abuso.
- Licencia CC BY-SA 4.0 declarada en cada pieza publicada.

### Página de autor — tag-url

- Cada publicación genera su tag-url `#/u/<key>` automáticamente · el bot envía la URL en el aviso de publicación (funciona aunque solo añadas nombre público).
- Feed propio con todas tus risas · el reproductor reutiliza el global · avatar con inicial y fecha relativa (`timeAgo`).
- Enlace a t.me solo si hay opt-in.

### Privacidad y datos

- Nunca se guardan ids de Telegram en claro en el repo · el handle público es un hash salado de la identidad · anónimo es una opción real.
- Esquema `risa.json` versionado: `id`, `t`, `name`, `tags`, `src`, `when`, `tg`, `key` (+ `video`).
- Retrocompatible: el feed puede ser array (v1) u objeto `{flag, clips}` · addons por flag que se activan sin romper lo publicado · feed agregable (puede sumar risas de otros bots, vídeo incluido) · las claves desconocidas de `flove.json` se ignoran.

### Integración con flove

- `flove.json` enriquece sin interrumpir: timeout de 4 s y fail-silent · regla de oro: `risa.json` es la verdad; `flove.json` solo añade.
- Al claim (v2), el enlace lleva al perfil único de flove donde ves tus risas y activas Lovy ya autenticado.

### Infraestructura y hosting

- Coste cero: R2 (10 GB gratis) + Pages + Actions · sin servidor propio y sin base de datos: git + archivos.
- Secretos de GitHub Actions (BOT_TOKEN, CHANNEL_ID, MOD_GROUP_ID, R2_*).
- Uploader R2 propio (SigV4) que sustituyó a Cloudinary por falta de permiso · migración de prefijos lista en `migrate-r2.mjs` · medios sincronizados a R2 con `sync-media.mjs` (idempotente).
- **Cloudflare Worker** (`risa/worker/`): intercepta `*.liberada.net`, conoce risa/ama, redirige usuarios nuevos a `liberada.net/usa/<username>/` vía `usernames.json` (caché 5 min). Desplegado con `wrangler deploy`.
- Replicable en una tarde: clona, lee este estándar, lanza tu bot, tu bucket y tu canal.
- El sitio se sirve dentro de flove.org, que además precachea offline (service worker).

### Calidad y documentación

- Suite de tests `node --test` sobre la lógica del bot y de la web · ayudantes puros compartidos (`risa.js` corre igual en la web y en Node) · verificación con jsdom sin navegador (harness repetible) · `node --check` en todos los archivos.
- Este estándar documenta flujos, datos, identidad, hosting y licencia · diagramas mermaid (thread + flow) versionados en `mermaid/`.
- Plan de v2 centralizado en [`plan-v2.md`](plan-v2.md) · changelog y política de versiones en el repo.
- Vocabulario consistente: los nombres del código coinciden con el texto de la interfaz.

### Accesibilidad y experiencia

- `prefers-reduced-motion` respetado · teclado: flechas en carruseles, foco visible en chips y botones · `aria-label` y roles en los controles importantes.
- Contraste alto sobre crema/ink · `alt` descriptivo en todas las imágenes · carga perezosa (`loading="lazy"`).
- Audio con `preload="none"` (no descarga hasta reproducir) · micro-interacciones solo con CSS · el botón de la risa reproduce un clip al toque · QR + deep link pensados para el móvil.

---

## 4. Identidad y privacidad

- La **palabra sobrescribe** a cualquier identidad de Telegram en el display. Si el autor no elige palabra → **«Anónima»**; **jamás** se infiere del @username ni del nombre de Telegram.
- **ID Telegram:** en modo **①+②** solo viaja un **hash salado** (handle de autor); en modo **solo-①** viaja el id directo. El `from_user` real y el @username viven **solo** en: DM del autor · grupo privado · cabecera del bot. El id en claro **nunca** en `risa.json` ni en la web.
- **Opt-in ① Telegram:** la única vía de que la identidad tg aparezca en la web; la decide el autor, y solo como **enlace** (o id directo si eligió solo-①).
- **Fuga por tags:** bloqueada — las etiquetas son input del autor o default `libre`; nunca derivadas de la identidad tg.
- **Página de autor automática (v1, sin authy):** todo clip publicado lleva la `key` de su autor — hash salado del id de Telegram, siempre presente, nunca en claro. Con ella se sirve `#/u/<key>` y el bot la regala en el aviso de publicación (vale con solo nombre público). Es un mecanismo general (`bot/pages.mjs`); **no hay archivo authy en v1** (queda en git y se reconstruye en v2): «autenticado en Telegram» solo significa que un moderador aceptó la publicación del autor. Claims, niveles e ids múltiples se construyen en v2 (`plan-v2.md` §A5).
- `state/queue.json` (commit) lleva **solo** el id oscurecido: `idHash` si ①+②, `idDirect` si solo-①, nada si ③/②. Salt del hash: `TG_ID_SECRET` (env). El id en claro para el DM de publicación vive en `state/.uploaders.json` (gitignored, local) y `state/drafts.json` tampoco se commitea.

---

## 5. Modelo de datos (repo `floveorg/risa`)

- **`state/offset.txt`** — último `update_id` de Telegram procesado (idempotencia: no avanza sin commit → reprocesa, nunca pierde).
- **`state/queue.json`** — pendientes (commit; nunca el id en claro):
  ```json
  [{ "id": "q_ab12", "fileId": "<telegram file_id>",
     "idHash": "<hash salado sha256 si ①+②>", "idDirect": "<id si solo-①>",
     "name": "palabra", "tags": "libre", "sel": { "tg": true, "name": true, "anon": false },
     "modMsgId": 678 }]
  ```
- **`state/.uploaders.json`** — gitignored, local: `{ "<clip_id>": <chat_id en claro> }`, para el DM de publicación; se borra al publicar/borrar.
- **`risa.json`** — publicados, **newest-first** (el bot **prepend**):
  ```json
  [{ "id": "b_9f3", "name": "palabra", "t": "Risa de palabra", "src": "https://…r2.dev/risa/b_9f3.mp3",
     "tags": "libre", "when": "2026-08-11", "channel_msg": 42, "tg_public": false, "video": false }]
  ```

**Contrato F0 (`risa.js`):** el bot escribe `name` + `src` + opcionales (`t`, `tags`, `when`, `tg_public`, `video`). **NO** escribe `by` ni `orig`: la web los **compone** desde la licencia constante — `by = "<name> · CC BY-SA 4.0"`, `orig = deed`. Licencia fuera de los datos; un solo sitio. La web filtra los vídeos por el mark `video: true` (`risa.js` `isVideoClip`).

---

## 6. GitHub (topología y despliegue)

- **Repo dedicado `floveorg/risa`** (GitHub), separado del repo fuente de flove (Gitea) y del sitio publicado (`floveorg/floveorg.github.io`). Contiene: el workflow del bot, `state/`, `risa.json` y el script de bot. Se sirve por su **propio GitHub Pages**.
  - Aísla binarios del repo principal · concentra el secret en un solo sitio · **no toca** el pipeline `updaty-web`.
  - La web hace `fetch` de `risa.json` desde ese origen (CORS permisivo); `<audio>`/`<video>` cross-origin no necesita CORS.
- **GitHub Actions (cron ~5–10 min):** `getUpdates` → procesa → commit+push. El runner trae `ffmpeg`.
  - **Secrets:** credenciales de Cloudflare R2 (`R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`, `R2_BUCKET`) + token del bot de Telegram.
  - **Latencia:** un clip aparece/publica dentro de un ciclo (~5–15 min). Aceptable para risas.
  - **Fiabilidad:** cron gratuito *best-effort*; los workflows se pausan tras 60 días sin actividad — cualquier push los reactiva.
  - **Estado:** `state/offset.txt` en el repo; procesamiento **idempotente por `id`**.
  - **Lógica como funciones puras** (parseo → acciones; añadir a `risa.json`; gestión de offset): migrar a VPS/webhook futuro es *drop-in*, no reescritura.

---

## 7. Hosting del audio y vídeo — Cloudflare R2

- Cada clip aprobado se sube a **Cloudflare R2** (bucket `risa`, prefijo `risa/b_*.mp3` para audio y `risa/b_*.mp4` para vídeo), con **URL pública** que se guarda en `src`.
- **Por qué R2 (mejor que Cloudinary):** objeto storage tipo S3 de Cloudflare — **sin coste de egress**, URLs públicas listas para reproducir, sin dependencia de CDN propietario, mismo espíritu FOSS que el resto. Sustituye a la enmienda Cloudinary (2026-07-19).
- `src` es una URL simple → **cambiar de host es una línea** (Backblaze B2 / MinIO autoalojado si hiciera falta).
- **Vídeo:** solo se comprime el vídeo (no el audio, que nunca supera 10 MB en 1 min). La compresión (MP4 H.264, crf 26, fit ≤10 MB con retry crf 33) la hace el runner de Actions con `ffmpeg`, y el mark `video: true` permite a la web filtrarlo.

---

## 8. Licencia y anti-abuso

- **Licencia:** cada clip bajo **CC BY-SA 4.0**. El bot lo declara antes de aceptar; la web compone `by` desde la constante.
- **Anti-abuso:** solo mensajes de **voz/audio/vídeo**; duración máx (1 min) y tamaño máx (10 MB; 20 MB en la ingesta de vídeo); límite de frecuencia por `from_user` (máx 5 risas en cola y 5 al día, contadas por el hash de su id); los moderadores son la puerta final.

---

## 9. Versión y releases (v1 producción · v2/v3 desarrollo)

- **Estado: NO hay release cortada todavía.** v1 (este estándar y el repo `floveorg/risa`) es producción **en polish**; cuando quede afinado se corta la primera release `v1.0.0` (release logics abajo).
- **v1 = producción (base de recuperación).** Congelado salvo **fixes** más los **adelantos v1.x** (D21): Mini App, favoritos por aprobación y edición de lo propio. Cada fix/adelanto corta su propia release: entrada en `CHANGELOG.md` + bump de `version` en `config.json` + tag `v1.x.y` en el repo.
- **v2 = desarrollo (risa + flove central).** Todos los planes para la v2 están **centralizados** en [`plan-v2.md`](plan-v2.md): Railway + libSQL + FastAPI + webhooks, perfiles de autor `lol/<key>/` (filespace propio de risa — `central/users/` queda para flove), claim L2→L3 con nonce server-side, **lovy** en su propio repo (`floveorg/lovy`) como clon extendido (audio + vídeo + cadenas) y **flovebot** agregador minimal por ahora en `floveorg.github.io` (identidad cruzada risa↔lovy). **No** se corta en el repo v1; risa migra a v2 cuando lovy pruebe estabilidad. **v3**: pendiente (sección «Réplica del sistema»).
- **Retrocompatibilidad:** `risa.json` es el contrato hacia la web; la web nunca exige campos nuevos (`key`, `tg`, `authy`, `author`, `tg_public`, `video` son aditivos y opcionales; `clipsOf`/`flagsOf` aceptan array u objeto `{flag, clips}`). Cualquier cambio de **formato** en `risa.json`/`state/` es una migración explícita con su changelog.
- **Release logics (cortar un v1.x.y):** ① entry en `CHANGELOG.md` → ② bump `config.json` → ③ commit + tag en `floveorg/risa` (reactiva el cron si >60 días) → ④ `Versión:` de este estándar = tag → ⑤ push a GitHub (Pages sirve `risa.liberada.net`); el pointer del submodule del repo fuente se sincroniza aparte.
- Detalle completo: `VERSIONING.md` del repo (`projects/liberada/risa/`).

---

## 10. Nota de consolidación (2026-08-16)

Este estándar es la **presentación única y amplia** del circuito v1, y **absorbe** el contenido útil del
diseño original y de los planes de implementación de la v1 (spec de diseño 2026-07-19, phase 0 web y
phase 1 bot): objetivos, decisiones de arquitectura, no-objetivos e inventario de funcionalidades ya
hechas viven en las secciones anteriores. Los artefactos v1 originales y los planes de v2 se han
centralizado/retirado; la historia de diseño queda en el historial de git. Los planes para la v2 viven
en [`plan-v2.md`](plan-v2.md).
