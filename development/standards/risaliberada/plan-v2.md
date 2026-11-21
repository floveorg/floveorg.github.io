# Risa v2 — Planes centralizados

**Fecha:** 2026-08-16 (consolidación de `risa/PLAN-V2.md` y `2026-08-11-risa-authy-telegram-shared.md`)
**Estado:** diseño — sin implementar
**v1:** producción **estable** con adelantos v1.x (base de recuperación, D20)
**Regla de puerta:** risa NO pasa a v2 hasta que **lovy** (su clon extendido) pruebe estabilidad — v1 y v2 conviven mientras tanto.
**Referencia del estándar v1:** [`risaliberada.md`](risaliberada.md)

> **Adelantos v1.x ya en producción:** hilos (cadenas infinitas con `parent`), subdominio
> automático (`username.liberada.net` al primer approve), perfil agregador
> (`liberada.net/usa/<username>/`), Cloudflare Worker para routing de subdominios.
> El claim L2→L3 de v2 complementa y protege este espacio; no lo reemplaza.

> **División clara de filespaces:** `central/users/` es **para flove**. Risa v2 tiene su
> propio filespace de perfiles: **`lol/<key>/`** (risa = risa, y «lol» es risa). El plan
> de flove central sigue como referencia (Parte B), pero la identidad de risa vive en su
> store, no depende de flove.

---

## 1. Objetivo (ambas partes)

Evolucionar el circuito de risa (serverless: cron de GitHub Actions + archivos en el repo)
a un **sistema con backend propio, siempre activo y con API**, y convertirlo a la vez en un
**patrón compartido y reutilizable** para cualquier app de comunidad (risa ahora, lovy después):

- **Railway** (hosting) + **libSQL** (base de datos) + **FastAPI** (API REST) + **webhooks**
  (respuesta instantánea, adiós al poll de 5–10 min).
- **Authy** como capa de identidad canal-agnóstica (Telegram es un *driver* más; mañana email/phone).
- **Claim flow** (L2 → L3): vincular un clip a un perfil sin exponer nunca el @username real de Telegram en la web.
- Perfiles de autor con navegación estable y agregación cross-app.
- Ser la **base del clon extendido lovy** (repo propio) y del **agregador flovebot**: identidad compartida, publicación cruzada.

---

# Parte A · Plan del repo de risa — Risa v2 (backend propio)

## A2. Arquitectura v2

```
  Autor ──(nota de voz / vídeo + palabra)──▶ 🤖 RisaLiberadaBot (webhook)
         │                                   Railway · FastAPI
         │  (moderador ve el @username real; el público NUNCA)
         ▼
  libSQL ───────────────────▶ store canónico (perfiles · claims · clips · cola · rate-limit)
         │
         ├──▶ Cloudflare R2 (audio/vídeo) ──▶ src pública
         ├──▶ lol/<key>/  (perfiles de autor de risa v2)   ← NO central/users (eso es flove)
         ├──▶ risa.json   (el feed: la web lo lee, contrato v1 intacto)
         └──▶ canal público de Telegram

  hermanas:
  lovy     (floveorg/lovy)        clon extendido de risa v2 · audio + vídeo + cadenas
  flovebot (floveorg.github.io)   agregador minimal · identidad cruzada risa ↔ lovy
```

La **web sigue leyendo `risa.json`** (mismo contrato, campos nuevos aditivos). El backend
escribe y el filespace `lol/` se sirve como read-model estático/API (fallback).

## A3. Stack

| Pieza | Para qué |
|---|---|
| **Railway** | Servidor siempre-activo: bot con webhook + FastAPI. Reemplaza el cron best-effort (que queda como respaldo). |
| **libSQL** (Turso) | Base canónica: `profiles` · `claims` · `clips` (meta) · `reactions` · `moderation` · `rate_limits`. |
| **FastAPI** (Python) | API REST: `/api/upload` · `/api/moderate` · `/api/authy/claim` · `/api/users/<handle>/` · `/api/lol/<key>/`. Webhooks de Telegram. |
| **Telegram Bot API** | Webhook en vez de `getUpdates`; notificaciones DM instantáneas. |
| **Cloudflare R2** | Audio/vídeo (igual que v1); `anonimo/` por app. |
| **GitHub Pages** | Sigue sirviendo la web + `risa.json` (contrato de lectura intacto). |

## A4. `lol/` — perfiles de autor de risa v2

- **v1 ya regala páginas de autor automáticas**: `#/u/<key>` (tag-url por autor,
  key = hash salado del id de Telegram, nunca en claro) que el bot manda en el
  aviso de publicación — funciona con solo nombre público. Son **generales** y
  **no dependen de authy** (viven en `bot/pages.mjs`). `lol/<key>/` es la
  evolución de esas páginas servida por el backend en v2.
- **`lol/<key>/`** es el filespace de perfiles de **risa** (el equivalente de
  `central/users/`, que **queda para flove**).
- Contenido por perfil:
  ```
  lol/<key>/
    clips.json   → [{app: "risa", id, src, when, tags, name}]  (+ lovy si cross-publish)
    index.html   → página de autor generada (risa.liberada.net/lol/<key>/)
    authy.json   → al reclamar: { handle, claimed_at, tg_public }
  ```
- **v2** persiste lo mismo en **libSQL** (canónico) y sirve `lol/` como read-model.
- **Enlace a flove** (opcional): cuando exista perfil en flove central
  (`flove.org/users/<key>/`), risa puede enlazarlo — pero la identidad de risa vive en su
  store, no depende de flove.

## A5. Identidad authy en v2

- **v1 no tiene archivo authy** (se elimina; la historia queda en git y authy se
  reconstruye en v2). Lo que v1 certifica — «autenticado en Telegram»: un
  moderador aceptó la publicación del autor — lo sirve la **página de autor**
  (`bot/pages.mjs`, tag-url automática), general y desacoplada.
- **Niveles L1–L5** (v1 ya trae L1 anónima/palabra + L2 presencia). v2 añade:
  - **Claim L2→L3**: web → `POST /api/authy/claim {clipId}` → FastAPI mintea **nonce** en
    libSQL (one-shot, TTL, rate-limited) → deep link `t.me/<bot>?start=claim_<nonce>` →
    confirmación en DM verificando **id entrante == id que subió** (D7) → libSQL persiste.
  - **API de renombrado**: `/name` en DM (v1) + edición por API (v2) con backfill en `risa.json`.
  - **Portabilidad**: `/passport` (resumen authy portable) · `/vault` (recovery) — v2.
- **Privacidad firme** (regla v1 intacta): el @username real nunca se renderiza en la web;
  solo la palabra/`key`.
- **Alcance M1 (questy 2026-08-16):** el claim se implementa **solo con flujo DM** — web →
  `POST /api/authy/claim` → nonce en libSQL → deep link → confirmación DM (id == id) →
  `lol/<key>/` servido → botón «Claim it» en la web. El **cross-app risa↔lovy sale de M1** y se
  cierra cuando lovy pruebe estabilidad (D20).

## A6. lovy — la hermana, clon extendido (repo propio)

- **Repo:** `floveorg/lovy` (propio), en paralelo desde el esqueleto de risa v2.
- **Componentes:** LovyBot + `index.html` (misma familia visual, `risa.js` generalizado).
- **Contenido:** audio **y vídeo ≤ 1 min** + acciones (L1) · bucket R2 propio (L3) ·
  cadenas colaborativas `/chain` · `/seeds` · `/cameo` · `/lore` · `/reprise` (L7).
- **Identidad compartida:** mismo authy → si ya eres de risa, Lovy te ve claimed
  (L4, `lol/` compartido o enlazado).
- **Puerta de migración (D20):** lovy es el banco de pruebas; risa migra a v2 cuando
  lovy sea estable.
- **Cross-app (questy Q005/Q006):** el claim de M1 **no** arrastra a lovy; el cross-app
  risa↔lovy se cierra como hito propio cuando lovy pruebe estabilidad.

## A7. flovebot — agregador minimal (por ahora en `floveorg.github.io`)

- Un bot **minimal**, no el paraguas completo del spec: lo justo para **conectar los dos perfiles**:
  `si eres de risa puedes publicar en lovy ya autenticado, y viceversa`.
- **Cómo:** misma identidad authy (claim una vez) + cross-publish (el clip subido a risa
  puede replicarse a lovy y al revés, con el mismo perfil `lol/<key>/`/equivalente).
- **Comandos mínimos:** `/start` · `/app` (risa | lovy) · `/me` · `/search` · `/latest` ·
  `/play` — esqueleto compartido, sin la capa avanzada v2 del spec §10 (ver B10).

## A8. Qué puede hacer el usuario sobre los contenidos en v2

Features del usuario **sobre los clips/contenidos** que habilita v2:

| Feature | Nivel | Detalle |
|---|---|---|
| **Escuchar / ver** | v1 | playlist + canal; v2 añade vídeo (lovy) y reproducción en-chat (`/play`) |
| **Buscar y filtrar** | v1 | tags · título · nombre (chips + buscador); v2: `/search` unificado + similitud |
| **Subir con identidad** | v1 | palabra / hash / anónima; v2: claim + perfil |
| **Reclamar clips (claim)** | v2 | L2→L3: adjuntar a su perfil `lol/<key>/` sin exponer el @username |
| **Renombrar su palabra** | v1 / v2 | `/name` en DM ya activo; edición por API con backfill en v2 |
| **Editar / ocultar / borrar sus publicaciones** | v2 | en la web, desde su perfil; en Telegram se mantienen (el grupo puede retirarlas si van firmadas con su id) |
| **Favoritos** | v1.x · v2 | **Adelantado a v1.x (D21, sin claim):** DM/Mini App → cron → `lol/<key>/favorites.json` (serverless). ❤️ públicos / ⭐ privados según nivel authy en v2 |
| **Reacciones «lol»** | v2 | reír un clip (cuenta en libSQL); señal para moderación y ranking |
| **Cadenas colaborativas** | v2 (lovy) | `/chain` · `/seeds` · `/cameo` (invitar a un autor) · `/lore` · `/reprise` (secuela/remix en hilo) |
| **Confianza** | v2 | notas de confianza en perfiles (`/trust`) |
| **Reportar / reglas** | v1 / v2 | `/report` · `/rules` · control del autor sobre su cola (`/draft` · `/retake`) |
| **Portabilidad** | v2 | `/passport` · `/vault`: la identidad sobrevive entre canales |
| **Cross-app** | v2 | flovebot: publicar en lovy desde risa (y viceversa) ya autenticado |

> Principio: el **autor manda sobre su contenido** en la web (editar/ocultar/borrar);
> Telegram es inmutable por diseño; la moderación humana sigue siendo la puerta final.

## A9. Fases (risa v2)

- **Fase 0 · Adelantos v1.x (antes de v2, D21):** Mini App (página estática embebida en
  Telegram, identidad por initData **sin claim**) + favoritos por aprobación + edición de lo
  propio; cada adelanto corta su release v1.1.0/v1.2.0 (VERSIONING §2). Inline mode necesita
  respuesta rápida (sub-segundo): serverless (cron) no cumple el timeout → se sirve con
  webhook (v2) o solo desde la Mini App.
- **M0 · Cimientos:** Railway + FastAPI + libSQL desplegados; bot con webhook; migración de
  la lógica pura (`bot/logic.mjs`, tests) al backend; `risa.json` intacto. Desde M0 **Railway
  escribe `risa.json`** (un solo escritor del contrato); el cron v1 queda de **respaldo lector**.
- **M1 · Perfiles `lol/` + claim (DM solo):** `lol/<key>/` servido; `POST /api/authy/claim`
  con nonce en libSQL; confirmación DM (id == id); botón «Claim it» en la web. Convive con
  `#/u/<key>` v1 (las URLs viejas no mueren).
- **M2 · Contenido del autor (prioridad a+b):** editar/ocultar/borrar propios clips **y**
  renombrar palabra por API con backfill, **y** favoritos/reacciones (los favoritos ya llegan
  adelantados en v1.x por D21).
- **M3 · lovy (paralelo):** crear `floveorg/lovy` como clon extendido (audio+vídeo, cadenas).
- **M4 · flovebot:** agregador minimal en `floveorg.github.io` — identidad cruzada risa↔lovy.
- **M5 · Estabilización:** risa v2 a producción (cuando lovy sea estable, D20); v1 sigue
  como base de recuperación.

## A10. Retrocompatibilidad y convivencia

- **`risa.json` es el contrato hacia la web** (regla de oro): v2 solo añade campos
  opcionales (`key`, `authy`, `author`, `reactions`…); la web nunca los exige.
- **v1 ∥ v2:** el circuito serverless (cron) sigue de respaldo; webhooks y API se encienden
  encima. Sin ramas forzadas: feeds y filespace por app permiten convivir.
- **Cambios de formato** en `risa.json`/`state/` = migración explícita con entrada en `CHANGELOG.md`.
- Cada **fix** de v1 corta su release (ver `VERSIONING.md`); v2 no se versiona aquí hasta
  que pase a producción.

---

# Parte B · Plan de flove central — Risa → Authy · circuito compartido

**Origen:** plan de referencia de flove central (2026-08-11). Detalla el patrón compartido
y las decisiones de diseño que lo gobiernan. La división con la Parte A: `central/users/`
(filespace de flove) vs `lol/<key>/` (filespace de risa).

## B2. Arquitectura (flove central)

```
  Autor ──(nota de voz / acción + palabra)──▶ 🤖 bot <app> (Telegram)
         │  (moderador ve el @username real; el público NUNCA)
         │  GitHub Actions cron
         ▼
  ✅ aprobado ─▶ ffmpeg/audio a Cloudflare R2  (+/anonimo/ si anónima)
         │
         ├──▶ prepend `risa.json` (app)   { id, name: PALABRA, src, when, tags?, authy?, author?, key? }
         ├──▶ registra/actualiza `central/users/<key>/`  (clips.json + index.html + authy.json)
         └──▶ post al canal público de Telegram

  Web: fetch risa.json → playlist / feed
       nombre = PALABRA (nunca @username)
       no reclamada → rojo + modal «Claim it»
       reclamada   → enlace al perfil
```

**Regla de privacidad (firme):** en la web solo se muestra la **palabra** (`name`). El
`@username` real vive solo en: (a) el DM del propio autor, (b) la superficie privada de
moderación, (c) la cabecera del bot. Nunca se renderiza en la web, ni en clips, ni en el
modal, ni tras el claim.

## B3. Decisiones (asentadas por Marc)

| # | Decisión |
|---|---|
| D1 | **Authy abstraído y canal-agnóstico.** `authy.js` = núcleo (niveles, identidad, claim/verify); `authy-telegram.js` = driver; email/phone = stubs futuros. El clip referencia `authy` + `author`, nunca el canal. |
| D2 | **Niveles:** L1 self/authored (anónima o con palabra) · L2 telegram-presencia no reclamada · L3 telegram verificado (claimed) · L4 +phone (futuro) · L5 +biometría (futuro). |
| D3 | **`key` inmutable = URL estable** (`users/sara-2/`); **`name` = palabra, por defecto el key, editable** por el autor (DM `/name` en v1; API en v2). Los moderadores NO renombran. |
| D4 | **Colisión de keys:** slug (`a–z0–9-`, minúsculas), *first-wins*, sufijo `-2`, `-3`… Sólo se sufija el key, nunca la palabra mostrada. El telegram id (claim) es el tie-breaker autoritativo. |
| D5 | **La palabra es el display.** En la subida (input de autor en web; bot DM para notas de voz) la palabra sobrescribe la muestra del id; el id de Telegram se guarda como **link-info oculto** para el claim. |
| D6 | **Revelar Telegram = opt-in.** Por defecto la palabra es display-only. Solo si el autor marca «muestra también mi Telegram» tras grabar, la palabra enlaza a `t.me/…` (o muestra el handle en hover). |
| D7 | **Claim = gate por id.** Permitido ⟺ el id que confirma en el DM == id que subió el clip. Nonce (aleatorio, one-shot, TTL) identifica el intento y evita replay; el id autoriza. |
| D8 | **El nonce (v1)** vive en `state/pending-claims.json` del repo del bot (one-shot, TTL ~10–15 min). **v2:** FastAPI lo mintea server-side en libSQL (`claims`), rate-limited. |
| D9 | **`central/users/` es el store canónico de identidad** (v1 filespace; v2 lee lo mismo desde libSQL). El repo del bot deja de ser dueño de identidad → bot puro. |
| D10 | **El bot escribe claims en `central/users/`** vía PAT dedicado (v1) o `POST /api/authy/claim` (v2). La web NUNCA escribe identidad (sin token en cliente). |
| D11 | **Los clips se actualizan al renombrar:** el bot hace backfill de `name` en `risa.json` para todos los clips con ese `key` (opción 2a). |
| D12 | **Anónima:** sin carpeta de autor; el audio va a prefijo `anonimo/` del bucket R2. Sin claim posible. |
| D13 | **Legacy:** los clips ya publicados sin key se dejan como están y se documentan. |
| D14 | **`risa.json` v2:** `name` = palabra; `key?`, `authy?`, `author?` (handle tras claim). `tg_ref` (hash salado) NUNCA en `risa.json`. |
| D15 | **Namespace:** `users/` es top-level nuevo → alta en el filtro de publish-web y ruta network-first del SW. Palabras reservadas (`index.html`, nombres de app), tope por cuenta anti-squatting. |
| D16 | **Primera-gana id→perfil** (un telegram id → un perfil; un perfil puede tener muchos ids y muchos avatares). |
| D17 | **Sin re-derivación de claves:** vincular authy a browsy NO re-deriva la clave Ed25519; los claims añaden facetas, nunca re-key. |
| D18 | **Backfill `name` = opción (a)** (bot backfill), no preferencia de renderer. |
| D19 | **i18n + a11y** del modal «Claim it» y de la página de autor (en/es; el «rojo» nunca es color-only: icono + aria). |
| D20 | **Versionado paralelo (v1 ∥ v2):** risa v1 queda **estable** (base de recuperación; polish posterior a v2). **flove v2** integra **lovy completo + risa parcial** (authy, helpers generalizados, renderer de autor, claims). **risa NO pasa a v2** hasta que lovy pruebe estabilidad. |
| D21 | **Aprobado = derechos (v1.x, sin claim).** Al publicarse el primer clip, el autor gana automáticamente todos los derechos posibles sin claim: página de autor, favoritos (❤️/⭐) y edición de lo suyo. Los favoritos se adelantan a v1.x vía bot (DM/Mini App → cron → `lol/<key>/favorites.json`), sin esperar a libSQL. |

## B4. Modelo de datos (flove central)

### Clip (`risa.json` v2, denormalizado para la web)
```json
{ "id": "q_…", "name": "sara-2", "key": "sara-2", "src": "https://…r2.dev/<app>/q_….mp3",
  "when": "2026-08-11", "tags": "…", "authy": 2, "author": null, "tg_public": false }
```
- `name` = palabra visible. `key` = clave de carpeta (inmutable). `authy` = 1|2|3. `author` = handle tras claim. `tg_public` = opt-in de mostrar Telegram.

### Filespace por autor (`central/users/<key>/`)
```
central/users/
  sara-2/
    clips.json      → [{app, id, src, when, tags, name}]  (app: risa | lovy | …)
    index.html      → página de autor generada (navegación persistente)
    authy.json      → aparece al reclamar: { handle, claimed_at, tg_public, avatars? }
    profile.json    → (v2) avatares/subperfiles, handles hermanos
```
Servido en `flove.org/users/<key>/` (mismo origen, SW network-first).

### LibSQL (v2, mapping 1:1 desde el filespace)
`profiles` · `avatars` · `authy_refs` · `clips` · `claims` — el backend importa el filespace al arrancar y sirve `/api/authy/…`, `/api/users/<handle>/…`.

## B5. Authy API (contrato del driver)

```js
authy.levels            // { anon:1, presence:2, verified:3, phone:4, bio:5 }
authy.verify(channel, proof) → facet      // prueba de posesión del canal
authy.claim(channel, key, handle, proof)  // liga un authy-ref a un perfil
authy.levelOf(identity) → 1..5
authy.resolveKey(name) → key              // slug, first-wins, sufijos
// driver telegram:
authyTelegram.dmLink(bot, payload)        // t.me/<bot>?start=…
authyTelegram.claimModal(clip, opts)      // modal «Claim it» (i18n, a11y)
```

## B6. Claim flow

**v1 (serverless):**
1. Web: clip no reclamada (L2) muestra la palabra en rojo + affordance.
2. Modal «Claim it»: *«Este clip está atribuido a “sara-2”. Si es tuyo, vincula tu Telegram para adjuntar este y futuros clips a tu perfil. Tu usuario de Telegram no se mostrará.»*
3. Deep link `t.me/<bot>?start=claim_<nonce>`; el bot busca en `state/pending-claims.json`, valida TTL, y confirma en DM: *«¿Reclamas el clip “sara-2”? ✅/✗»* verificando **id entrante == id que subió**.
4. ✅ → bot escribe `central/users/<key>/authy.json` (+ `claimed_by`), y el siguiente fetch de la web re-renderiza (claimed → enlace al perfil). Futuros clips del mismo id auto-registran al mismo key.

**v2 (Railway):** web `POST /api/authy/claim {clipId}` → FastAPI mintea el nonce en libSQL → deep link → bot confirma → FastAPI persiste `authy_refs`+`claims`, browsy firma el claim cuando el bridge está presente. Filespace = read model / fallback estático.

## B7. Fases (flove central)

### P1 — Núcleo compartido + risa
- [ ] `addons/code/js/authy/authy.js` (núcleo + `resolveKey`)
- [ ] `addons/code/js/authy/authy-telegram.js` (deep-link, modal, driver)
- [ ] Helpers generalizados del feed/playlist (contrato, estados de autor: anónima / roja / claimed)
- [ ] Filtro publish-web + SW: `users/` (allowlist + network-first)
- [ ] Bot: captura `tg_username` + `name` (palabra) en subida; backfill de `name`; registro de `central/users/<key>/`; opt-in `tg_public`; anónimas → `anonimo/` R2
- [ ] `risa.json` v2 + fixtures de test (key-assignment, claim, estados)
- [ ] `state/pending-claims.json` + `/name` + confirm DM
- [ ] Web: palabra en vez de nombre; rojo+modal «Claim it»; fetch de `users/<key>/` para re-resolver

### P2 — Perfil de appy + páginas de autor
- [ ] `central/users/<key>/index.html` generado (página de autor, navegación cross-app)
- [ ] Feed de contribuciones en appy (lee su `clips.json` / API)
- [ ] Enlaces autor: clip → `users/<key>/` → perfil appy; perfil → clips

### P3 — lovy (ver B9)
- [ ] Bot **LovyBot** sobre el mismo esqueleto (ingesta: audio **y vídeo ≤ 1 min**)
- [ ] Bucket R2 **nuevo** (`lovy`) + `anonimo/` por app
- [ ] **Crear lovy en `apps/economy/lovy.html`** (`index.html` canónico): mantener diseño y funcionalidades actuales, sustituyendo todo lo posible por las abstracciones de `addons` (helpers, authy-telegram, renderer de autor)
- [ ] Sección «feed de la comunidad» en lovy + integración de autor
- [ ] `risa.json` de lovy + `central/users/` compartido (la página de autor agrega risa + lovy)
- [ ] Grupo de moderación de lovy: lo crea Marc (misma mecánica ✅/🗑)

### P4 — Railway + libSQL + browsy
- [ ] FastAPI: `/api/authy/claim`, `/api/users/<handle>/…`; import del filespace
- [ ] Tablas libSQL (mapping B4); filespace como fallback
- [ ] Browsy firma claims; sin re-derivación de claves (D17)

## B8. Trabajo pendiente / aplazado

- **`flovebot` paraguas (L2)**: ofrece interactuar con **lovy y/o risa** desde un mismo bot (misma mecánica, más avanzado) — plan futuro, spec en B10.
- Feed cross-app vía endpoint central (v2) en vez de fetch por app.
- Email/phone drivers de authy.
- Avatares/subperfiles en la página de autor (v2).
- Editar la palabra por API (v2); v1 solo `/name` del bot.

## B9. Decisiones de lovy (respuestas de Marc a los issues)

| # | Decisión |
|---|---|
| L1 | **Contenido:** lovy = **audio y vídeo ≤ 1 min** + acciones (relaja la regla «solo voz/audio» del spec risa §8). |
| L2 | **Bot LovyBot** dedicado, sobre el mismo esqueleto. **flovebot** = paraguas futuro que ofrece interactuar con **lovy y/o risa** desde un mismo bot (misma mecánica, pero más avanzado). |
| L3 | **Bucket R2 nuevo** (`lovy`); `anonimo/` por app. |
| L4 | `central/users/<key>/` **compartido**: `risa.json` per-app, usuarios no (la página de autor agrega risa + lovy). |
| L5 | Integración web propia del layout de lovy; **compartido** = renderer de autor, modal «Claim it», fetch (helpers / authy-telegram). |
| L6 | Strings parametrizables (títulos, tags, empty states, licencia) vía helpers generalizados (D19). |
| L7 | **lovy se crea en `apps/economy/lovy.html`** manteniendo diseño y funcionalidades actuales, sustituyendo lo posible por las abstracciones de `addons`. |
| L8 | Grupo de moderación de lovy: lo crea **Marc**, misma mecánica ✅/🗑. |

## B10. Spec de flovebot (paraguas lovy + risa)

**Idea (L2):** un solo bot (`flovebot`) que ofrece interactuar con **lovy y/o risa** desde el mismo chat — misma mecánica que los bots dedicados (subida → moderación → `risa.json`), pero más avanzado: routing por app, búsqueda cross-app, perfil e historial del autor, y reproducción en-chat.

**Identidad compartida:** flovebot usa el **mismo** registro authy / `central/users` — claim una vez en risa y flovebot/LovyBot ya te ven claimed. Eso es lo que hace el paraguas «más avanzado» sin duplicar identidad.

### Mapa de comandos (v1 = serverless en cron, v2 = Railway)

| Comando | Qué hace | Fase | Enriquecería a los bots dedicados |
|---|---|---|---|
| `/start` | Menú: *«Elige app — 😹 risa · 💗 lovy»* (inline). Elección recordada por usuario; `/app` para cambiar | v1 | sí (LovyBot / RisaLiberada) |
| `/app <risa\|lovy>` | Cambio rápido de app activa | v1 | sí |
| `/me` | Tu identidad authy: key, palabra, nivel L1–L3, estado del claim, enlace a tu página de autor | v1 | sí |
| `/name <word>` | Set/editar palabra de display | v1 (D3/D11) | sí |
| `/claim` | Flow de claim desde el bot (nonce + id-confirm; sin web) | v1 | sí |
| `/link <handle>` | Vincular telegram a un perfil appy vía API | v2 (D9) | sí |
| `/history` | Tus subidas + estado: pending / approved / denied (lee `state/queue.json` + `risa.json` por tg id) | v1 | sí |
| `/stats` | Tus números: clips publicados | v1 conteos (las reales, en la web) | sí |
| `/profile` | Tus enlaces: `flove.org/users/<key>/` + perfil appy | v1 | sí |
| `/search <q>` | **Búsqueda unificada** (uno para encontrarlo todo): palabra/tag/nombre o **similitud a un clip** (`/search <id>`); reemplaza `/browse` y `/more` (fetch de ambos `risa.json`, filtro local — mismo fetch que ya hace la web) | v1 texto/tag; v2 similitud | sí |
| `/latest` | Los N más nuevos de ambas apps | v1 | sí |
| `/random` | Clip sorpresa | v1 | sí |
| `/trending` | Top tags/chips por app | v1 (conteos de tags de risa.json) | sí |
| `/play <id\|word>` | Reproduce el clip en-chat (bot manda la URL R2 pública como `sendAudio`/`sendVideo`; sin almacenar `file_id`) | v1 | sí |
| `/today` | «risa del día» / «acción del día» rotatoria | v1 | sí |
| `/status` | Salud: offset, pendientes, último run | v1 | sí |
| `/queue [app]` | Cola de pendientes (admin); en flovebot, `[app]` elige risa\|lovy (merge tabla base + avanzada) | v1 | sí |

### Capa v2 «avanzada»

**2 · Identidad & perfil (authy)**
- **`/fave <id>`**: favoritos personales → «mis favoritos» en `users/<key>/` (v1).
- **`/alias <palabra>`**: palabra adicional = **subperfil del perfil principal, misma key** (muchos handles → un perfil) (v2).
- **`/swap <id> <avatar>`**: mover un clip entre tus avatares/subperfiles (v2).
- **`/echo <id>`**: tarjeta bonita de metadatos del clip (palabra, tags, app, fecha, nivel) — base compartida de `/fave`, `/play`, `/report` (v1).
- **`/totem`**: marca animal/emoji determinista derivada de tu `key`, mostrada en tu página (v1).

**4 · Privacidad, recuperación & portabilidad (authy)**
- **`/vault`**: tu «recovery sheet» — frase/palabra + QR para restaurar tu identidad authy entre canales (v2).
- **`/passport`**: resumen portátil de authy (key, nivel, enlaces públicos) para ser reconocido fuera (v2).

**5 · Confianza & herencia**
- **`/trust <word>`**: nota de confianza en el perfil de otro autor; aparece en su página (v1).
- **`/heritage`** *(absorbe `/invite`)*: para **transferir/recuperar la cuenta**. El bot formatea la **cadena completa** y dibuja el **grafo de herencia fuera de Telegram** (web: página de la cadena / perfiles); la red de avales sirve de prueba para **transferir/recuperar** la cuenta authy (v2).

**7 · Lovy — Cadenas (solo lovy)**
- **`/chain`**: cadenas colaborativas — un prompt de palabra, cada contribución continúa la anterior (v1).
- **`/seeds`**: lista de cadenas/prompts abiertos a los que puedes unirte (v1).
- **`/cameo <palabra>`**: invitar a un autor concreto a hacer un dúo/continuar tu clip o cadena (v2).
- **`/lore <cadena>`**: storyline de la cadena para la web (narrativa + grafo de herencia juntos) (v2).

**8 · Búsqueda & exploración** (uno para encontrarlo todo)
- **`/search` unificado**: palabra, tag, nombre o **similitud a un clip** (`/search <q>`, `/search <id>`). Reemplaza `/browse` y `/more` (v1 texto/tag; v2 similitud).
- **`/latest`** · **`/random`** · **`/trending`** · **`/now`** · **`/since <fecha>`** ("qué hay de nuevo desde…", por app) (v1).

**9 · Reproducción & momentos**
- **`/play <id|word>`** · **`/radio`** (sesión seguida: `/next`, `/stop`; shuffle o por tag) · **`/today`** (v1).
- **`/reprise <id>`** (v2, creación): secuela/remix — clip nuevo que referencia a uno viejo; en la web se renderizan como hilo.
- **Reacciones en el canal**: siempre activas (Marc las habilita; no es opt-in); con webhook (v2) el bot las lee como señal para la «selección» HTML.

**10 · Moderación & administración**
- **`/status`** · **`/queue [app]`** · **`/mute` + strikes** (v1) · **`/pin <id>`** · **`/mirror`** (v1, admin).
- **`/report`** · **`/rules`** (v1).
- **Control del autor sobre su cola**: **`/draft`** (borrador antes de entrar a la cola) · **`/retake`** (retirar/re-grabar mientras está pendiente) (v1).
- **Rate-limit + anti-spam server-side** (refuerza D8, v2).

**11 · Sistema (v2)**
- **Webhooks** (respuesta instantánea, no poll de 10 min).
- **Notificaciones al autor**: DM al aprobar/denegar.
- **Telegram Mini App** *(adelantado a v1.x, D21)*: risa.liberada.net embebida en Telegram; identidad por initData **sin claim** → editar favoritos (❤️/⭐) y lo propio.
- **Inline mode** `@RisaLiberadaBot <palabra>` *(Q015: adelantado antes de v2)*: buscar y compartir risas en cualquier chat. Nota: requiere respuesta rápida — serverless (cron) no cumple el timeout; se sirve con webhook (v2) o vía Mini App.
- **`/edit <id>` y `/del <id>` del autor**: cambiar tags/palabra/anónima o retirar el propio clip (confirmación en DM).
- **Programación de publicación** (colas en libSQL).

**Descartado** (mantenido como referencia, comentado):
<!--
- ~~Relay entre canales~~ — Marc: no.
- ~~/dispute~~ (conflictos de palabra) — Marc: no.
- ~~/sessions~~ (canales vinculados) — Marc: no.
- ~~/digest~~ (lote curado periódico) — Marc: no.
- ~~Auto-deny presets~~ (botones con razón predefinida) — Marc: no.
- ~~/word~~ (mini-perfil público de otro autor) — Marc: no.
- ~~/muse~~ (prompt aleatorio «inspírame») — Marc: no.
- ~~/antenna~~ (señal «estoy hoy aquí») — Marc: no.
- ~~/gate~~ (opt-out de aparecer en /now · /latest · /random) — Marc: no.
- ~~/incognito~~ (anónima por defecto) — Marc: no.
- ~~/north~~ (prompt-tema del periodo) — Marc: no.
- ~~/beacon~~ (vía de recuperación secundaria) — Marc: no.
- ~~/witness~~ (testigos para recuperación social) — Marc: no.
- ~~/seal~~ (firma personal en clips) — Marc: no.
-->
En HTML, no en el bot: transcripción/flagging IA para moderadores, dailies + rachas, i18n del copy, y top/trending con stats reales de Central.

### Notas de diseño (flovebot)

- **Privacidad firme (§B2):** `/search` y `/me` renderizan solo palabra/`key`, nunca el @username — misma regla que la web.
- **Playback barato:** las URLs de R2 son públicas → `sendAudio(url)` funciona en v1 serverless, sin bookkeeping de `file_id`.
- **Bots dedicados reutilizan todo:** LovyBot y RisaLiberada ganan `/me`, `/name`, `/claim`, `/history`, `/search`, `/latest`, `/random`, `/play`, `/profile`, `/status` sin coste extra (misma esqueleto).

---

## 2. Versionado y escalabilidad (D20)

**Estrategia (Marc, 2026-08-11):**

| Pieza | Estado | Plan |
|---|---|---|
| risa v1 | **estable v1** (marcado) | base de recuperación; **polish posterior a v2** |
| lovy | → flove v2 | integración **completa** |
| risa v1 | → flove v2 **parcial** | risa **NO** pasa a v2 hasta que lovy pruebe estabilidad |
| LovyBot · flovebot | v2 directo | esqueleto compartido abstracto (`bot-core`) |

- **flove v2** integra **lovy completo + risa parcial** (authy, helpers generalizados, renderer de autor, claims). risa conserva su v1 en paralelo, marcada **estable** y congelada salvo polish.
- **v2 abstrae aún más los códigos v1**: `bot-core` (ingesta, cola, moderación ✅/🗑, claims, `/name`) compartido por lovy y risa; lovy actúa como banco de pruebas antes de migrar risa.
- **Convivencia sin ramas**: `risa.json` y filespace por app (D15, L4) permiten v1 y v2 viviendo a la vez.
- **Escalabilidad**: risa v1 sigue en serverless (Actions cron); flove v2 (Railway + libSQL) sirve lovy y flovebot; risa migra al v2 cuando lovy sea estable.

## 3. Self-review

- Cobertura del circuito original (subir→moderar→publicar) se mantiene intacto; el plan añade identidad (authy) + persistencia por autor (users/ · lol/) + privacidad (palabra, nunca nickname).
- Alineación con planes existentes: browsy (keys/trust, D17), central-backend (P01, D9/D10, B4), proposals P13 (claim via authy).
- No rompe el pipeline `updaty` si se hace D15 (allowlist + SW).
- Pruebas: fixtures compartidos (key-assignment, claim, estados de autor) con `node --test`.

---

## 4. Decisiones questy (2026-08-16) — release v1 + refining v2

Sesión sobre el corte de v1.0.0 y el refining del plan v2. Las respuestas ya están
aplicadas en las secciones de arriba; aquí queda el resumen trazable:

| # | Decisión |
|---|---|
| Q003 | **CI solo en el workflow de release (tag):** `node --test` + `html-validate` ahí (VERSIONING §5). |
| Q004 | **«Lovy estable» = criterios concretos pero abiertos** (revisables): N días en producción sin fix de datos, tests verdes, moderación real funcionando. |
| Q005/Q006 | **M1 = claim con flujo DM solo.** El cross-app risa↔lovy sale de M1; lovy vuelve a M3 con su gate D20 intacto (desacoplado). |
| Q011 | Entrega M1: nonce en libSQL (one-shot/TTL) → deep link → confirmación DM (id==id) → `lol/<key>/` servido → botón «Claim it» en la web. |
| Q012 | **Railway escribe `risa.json` solo desde M0**; el cron v1 queda de respaldo lector (un solo escritor del contrato). |
| Q013 | `#/u/<key>` (v1) y `lol/<key>/` (v2) **conviven**; las URLs viejas no mueren. |
| Q014 | M2 prioriza editar/ocultar/borrar propios + renombrar palabra **y** favoritos/reacciones (a+b). |
| Q015 | **Inline mode + Mini App antes de v2 (v1.x), sin claim**; la Mini App es el acceso autenticado para favoritos y lo propio. |
| D21 | **Aprobado = derechos:** al publicarse el primer clip, el autor gana sin claim todos los derechos posibles (página, favoritos, edición de lo suyo). Favoritos adelantados vía bot (DM/Mini App → cron → `lol/<key>/favorites.json`). |

**Pendientes (corte v1.0.0):**
- Q001 — alinear CHANGELOG (authy v1 → sección v2) y commitear el borrado de `authy.js` como parte de la release.
- Q002 — añadir campo `version` a `config.json` (VERSIONING §4.2).
- Q007 — checklist pre-corte (commits limpios, VERSIONING §5) antes de cortar.

---

# Parte C · Risa v2-d1 — Cloudflare D1 + Workers

> Merged 2026-11-21 from `projects/liberada/risa/plans/PLAN-V2-D1.md` (N11merge).
> **Owner of the v2-D1 follow-ups:** the risa project (`projects/liberada/risa/`);
> Work pointers stay with that project even though the plan now lives here.
> This part is additive to v1: `risa.json` remains the web read-model and the
> Actions cron keeps serving audio; D1 + Workers add accounts, search, activity
> and editing. If D1/Workers are switched off, v1 keeps serving.


Rama de desarrollo **`v2-d1`** (no sigue plan-v2.md). Enciende una capa
**aditiva** sobre el circuito v1: la web sigue leyendo `risa.json`, el bot
sigue corriendo en el cron de Actions y R2 sigue sirviendo los audios. Lo que
añade v2-d1 es un **SQL local gestionado (D1) + endpoints (Workers)** para lo
que un feed estático no puede: cuentas, búsqueda, actividad y edición.

> **Estado de la infra (native settings):** `worker/wrangler.toml` con binding
> D1 (`DB`), `worker/migrations/0001_initial.sql` (esquema + seed marcflove
> simple · maria avanzada), `worker/api.mjs` (API D1 + fallback al Worker de
> subdominios) y `worker/README.md` (pasos nativos: d1 create, execute, secrets,
> deploy). La web (`index.html`) mantiene su navegación y suma, en v2-d1,
> búsqueda fina vía `/api/search` y favoritos a un feed real vía `/api/fav`
> (fail-silent cuando la API no está).

Regla de oro heredada de v1: **`risa.json` es la verdad de lectura de la web;**
D1 es el nuevo canónico de escritura y `risa.json` queda como read-model que el
Workers regenera. Si D1/Workers se apaga, v1 sigue sirviendo (base de
recuperación).

> **Pendiente de plan:** alineación de reacciones/respuestas en clips sin
> hilo (§6d) — necesita exponer el grafo de hilos desde D1 antes de unificar
> el render de clips.

---

### 1. Arquitectura

```
Telegram bot (cron Actions, v1) ──▶ R2 (audios) ──▶ risa.json (read-model)
        │                                                │
        ▼                                                ▼
  Workers API (v2-d1) ◀───────────────▶ D1 (canónico)  GitHub Pages (web)
        │                                                      │
        └──── addons: búsqueda · actividad · perfiles ────────▶ fetch risa.json
```

- **Workers** publican `/api/*` en `risa.liberada.net` (mismo dominio que la
  web → sin CORS).
- **D1** guarda lo que `risa.json` no puede: claims de identidad, favoritos
  por clave, actividad por app, búsqueda FTS, borradores de edición.
- El bot (v1) sigue escribiendo `risa.json` como hoy; un Workers opcional lo
  **replica a D1** (idempotente) para que los addons no dependan del feed.

### 2. Esquema D1 (mínimo, por tablas)

```sql
-- Identidad: la key (hash salado) es el id de autor, nunca en claro.
CREATE TABLE identities (
  key        TEXT PRIMARY KEY,      -- hash salado (v1) o id futuro
  username   TEXT UNIQUE,           -- subdominio <user>.liberada.net
  name       TEXT,                  -- nombre público
  bio        TEXT DEFAULT '',
  email      TEXT,                  -- vía de recuperación (opt-in)
  socials    TEXT DEFAULT '[]',     -- JSON [{net,url}]
  recover    TEXT DEFAULT '[]',     -- vías: bot · email
  claimed_at TEXT,
  updated_at TEXT
);

-- Actividad: una fila por pieza publicada en cualquier app de liberada.
CREATE TABLE activity (
  key     TEXT,                     -- autor (hash)
  app     TEXT,                     -- risa | ama | lovy | ...
  item_id TEXT,                     -- id en el feed de la app
  at      TEXT,
  PRIMARY KEY (app, item_id)
);
CREATE INDEX idx_act_key ON activity(key, at DESC);

-- Favoritos (multi-app) y actividad local sincronizada.
CREATE TABLE favs (
  key     TEXT,
  app     TEXT,
  item_id TEXT,
  at      TEXT,
  PRIMARY KEY (key, app, item_id)
);

-- Búsqueda full-text (addon f1SS).
CREATE VIRTUAL TABLE search_fts USING fts5(
  item_id, app, title, tags, name, content='activity'
);
```

### 3. Endpoints Workers (`/api/*`)

| Método y ruta | Qué hace | Quién |
|---|---|---|
| `GET  /api/users/<username>` | perfil agregado (identity + actividad + socials) | web / agregador |
| `POST /api/profile` | editar nombre, bio, socials (requiere claim válido) | miniapp / bot |
| `POST /api/recover` | añadir email / vías de recuperación | miniapp |
| `POST /api/fav` · `GET /api/favs/<key>` | favoritos en la nube (sincronizan las playlists) | web |
| `GET  /api/search?q=` | f1SS: búsqueda full-text sobre `search_fts` | web / bot |
| `GET  /api/activity/<key>` | actividad cruzada de apps (juega y filtra) | perfiles |
| `POST /api/ingest` | replica `risa.json` → D1 (idempotente, llama el cron) | bot |

### 4. Addons propuestos

- **f1SS search** — búsqueda full-text (FTS5) sobre títulos, tags y nombres;
  la web mantiene su buscador actual como fallback sin red.
- **Favoritos en la nube** — la estrella ⭐ deja de ser solo local: con claim,
  se sincroniza entre dispositivos y se comparte por URL.
- **Actividad cruzada** — «juega y filtra»: el perfil agrega risas + amas + lo
  que juegues en otras apps liberada (powered by `activity`).
- **Perfiles editables** — nombre, bio extendida y redes desde la miniapp con
  token de reclamo (enlace privado del bot), no solo con comandos.
- **Cadenas enriquecidas** — hilos con contexto en D1 (el `parent` de v1 queda
  intacto; D1 añade conteo y vista).
- **Webhooks reales** — Workers con webhook de Telegram en vez de solo cron:
  avisos al autor al instante, rate-limit y cola gestionada.

### 5. Tunings para el HTML y el flujo actuales

La v1 es **un solo HTML sin build + git como base de datos**. v2-d1 debe
respetar eso, no romperlo:

1. **La web sigue siendo estática y sin build.** Los addons se activan por
   fetch condicional a `/api/*` con timeout y fail-silent (mismo patrón que
   `flove.json`): si el Workers calla, la página queda idéntica.
2. **`risa.json` = read-model garantizado.** El Workers regenera `risa.json`
   desde D1 tras cada escritura (o el cron lo hace); nunca al revés.
3. **Claim token-in-item (local).** El bot emite un enlace privado; el feed
   publica solo `sha256(token)` y la web lo verifica sin servidor.
4. **Una tabla `activity` por app.** Cada app (risa, ama, lovy) replica su feed
   a D1 con `POST /api/ingest`; el perfil agregador las mezcla sin tocar sus
   HTML.
5. **Favoritos: primero local, luego nube.** Sin claim la estrella sigue
   funcionando local (como hoy); con claim se sincroniza. No exige nada nuevo
   en el HTML hasta que el usuario se autentique.
6. **Búsqueda con dos niveles.** `GET /api/search` cuando hay red; el filtro
   local actual cuando no la hay. La UI no cambia: un solo input.
7. **R2 sigue siendo el almacén de medios**; D1 nunca guarda blobs, solo
   metadatos e índices. Misma política de coste cero (D1 gratis hasta
   ~5 M lecturas/mes; Workers gratis 100k peticiones/día).
8. **Moderación intacta en v1.** El grupo de moderadores y el bot no cambian;
   D1 solo añade auditoría opcional (quién aprobó, cuándo).
9. **Ban de usuarios (pendiente v2-D1).** El admin del grupo de moderación
   podría banear usuarios via `/ban @username` — nueva tabla `banned_users`
   en D1 + check en el bot antes de aceptar uploads. No en v1.

### 6b. Hilos y navegación profunda (v2-d1)

v1 ya tiene hilos reales: `parent` en `risa.json`, orden depth-first
(`threadOrder`), conectores visuales y el flujo «reenvía el clip → responde»
en el bot (`clipByChannelMsg` + `hasAncestor` contra ciclos). v2-d1 lo lleva a
una **navegación más interactiva y profunda visualmente** sin tocar el esquema:

- **Vista árbol de ramas.** En la página de autor y en la playlist, un clip con
  respuestas despliega un árbol colapsable: ramas por autor, profundidad visual
  (indentación + conector), y botón «seguir la rama» que filtra a esa línea.
- **Modo foco.** Clic en un clip → vista centrada con el contexto del padre
  (preview), sus respuestas y las de los siguientes: navegación por flechas
  entre nodos (arriba/abajo), sin salir de la página.
- **Previews de padre.** En el feed plano, las respuestas muestran un chip
  «↳ responde a <título>» que abre un mini-preview del padre en el propio
  reproductor (sin recargar la lista).
- **Contadores y reacciones en el árbol.** D1 (`activity` + tabla nueva
  `threads`) agrega cuántas respuestas tiene cada nodo, quién las dio y desde
  qué app — el árbol pasa a ser «actividad viva», no solo estructura.
- **Búsqueda dentro de hilos (f1SS).** `search_fts` indexa cada nodo; buscar
  un título devuelve también la **posición en su hilo** (subir/bajar).
- **Story / modo lector.** Un hilo completo como tarjeta continua (nodos
  encadenados con su audio), ideal para «leer» una conversación de risas de
  principio a fin y compartirla por URL (`#/t/<id-del-hilo>`).

Todo vive **encima** de v1: el feed sigue siendo `risa.json` y el esquema
`parent` no cambia; D1 solo añade la vista y los contadores.

### 6c. Webhook real (avisos al instante)

El v1 corre solo con cron (getUpdates cada 5–10 min). v2-d1 añade un **webhook**
de Telegram en el Workers para los avisos en tiempo real, con el cron como
**respaldo** (si el webhook falla, el cron sigue vaciando la cola):

- `POST /api/tg` (Webhook handler) — verifica `X-Telegram-Bot-Api-Secret-Token`
  (mismo secreto en `setWebhook`), procesa updates con la misma
  `parseUpdates` pura y devuelve acciones al bot que corresponda.
- `setWebhook` se configura una vez (script `bot/set-webhook.mjs`):
  `https://risa.liberada.net/api/tg?secret=<token>`; `drop_pending_updates`
  solo en el primer despliegue.
- **Avisos al instante**: al aprobarse una risa, el autor recibe el mensaje en
  segundos (no en el próximo tick); el canal y el grupo de moderación se
  actualizan igual de rápido.
- **Rate-limit y cola en D1**: tabla `updates` (update_id, status, at) para
  idempotencia compartida entre webhook y cron; `update_id` único evita
  duplicados si ambos procesan a la vez.
- **Fallback**: si `/api/tg` devuelve error, el cron sigue corriendo; el
  `offset` del cron y el del webhook comparten la misma cola (nunca procesan
  el mismo update dos veces).
- El bot v1 **no cambia**: solo se añade el handler Workers + el script de
  `setWebhook`. El webhook puede encenderse app a app (risa primero).

### 6d. Dificultad-bug: alineación de `.react-chip` / `.reply-btn` en clips SIN respuestas

> **Estado:** documentado para planificar — NO arreglado. Antes de tocar el
> frontend, hay que actualizar las tablas D1 (ver §6d.5) para que la reparación
> sea limpia y no parche a trozos.
> **Fecha:** 2026-08-20 · **Afecta:** risa (y maria vía `flove-media.css`).

#### 6d.1 Síntoma (lo que ve el usuario)

En los clips de la lista que **tienen respuestas** (cadena), el chip de
reacciones (emoji) y el botón `+` (responder) quedan **pegados a la derecha**
de la tarjeta. En los clips **sin respuestas**, esos dos botones **no quedan
alineados a la derecha**: se quedan colgando a la izquierda de donde deberían,
como si el espacio flexible no se repartiera.

```
✓ con respuestas:     [▶]  Título ……………        [🤣] [+]
✗ sin respuestas:     [▶]  Título ……………  [🤣] [+]        ← hueco a la derecha
```

#### 6d.2 Por qué es una "dificultad" (y no un bug de una línea)

El renderizador **no produce la misma estructura** según si el clip tiene o no
respuestas, y el CSS depende de esa diferencia estructural. Los dos caminos
viven en `central/shared/code/js/flove-player.js` → `buildLi()`:

#### Camino A — clip CON respuestas (`toggleLine` presente)

```
<li class="tgl">
  <div class="clip-card">            ← caja flexible con padding
    <div class="thread-item">        ← flex fila; .ti{flex:1} empuja a la derecha
      <span class="tag dl">▶</span>
      <span class="ti">Título …</span>
      … react-chip + reply-btn        ← pegados a la derecha ✓
    </div>
  </div>
  <div class="thread-toggle-line">…</div>
</li>
```

#### Camino B — clip SIN respuestas (sin `toggleLine`)

```
<li>                                 ← el propio <li> es la caja (sin .clip-card)
  <div class="thread-item">          ← flex fila; .ti{flex:1} empuja a la derecha
    <span class="tag dl">▶</span>
    <span class="ti">Título …</span>
    … react-chip + reply-btn          ← NO empujan: .ti no ocupa todo el ancho ✗
  </div>
</li>
```

El **`li` base** de risa tiene su propio `display:flex; align-items:center;
gap:10px; padding:5px 12px` (línea 200 de `index.html`), y `.thread-item`
tiene `width:100%` (línea 600). Pero en el camino B el `li` es a la vez
contenedor flex **y** borde/padding de la tarjeta: el `.thread-item` (único
hijo) con `width:100%` debería llenarlo, y sin embargo el `flex:1` del `.ti`
no estira hasta el borde derecho porque el contexto flex de risa deja el
`thread-item` con `gap` interno que no se compensa con el `padding` del `li`.

En el camino A, el `.clip-card` **sí** tiene `display:flex; align-items:center;
gap:10px; padding:5px 12px; width:100%` (línea 374), y el `thread-item` con
`width:100%` queda dentro de ese flex con `padding` resuelto — por eso ahí
funciona.

**Conclusión del diagnóstico:** el alineado correcto en B depende de que
`li` no sea el contenedor estético + el flex del `thread-item` a la vez. Son
dos roles que chocan. La solución "parche" sería añadir `margin-left:auto` al
`.react-chip`/`.reply-btn` en el camino B o forzar `.ti{flex:1}` con un fix
de especificidad — todo eso es exactamente el tipo de parche que luego rompe
otra vista (maria, el feed, las páginas de autor).

#### 6d.3 Evidencia de medición (headless, 2026-08-20)

Render local de `risa/index.html` con Chrome headless (`--dump-dom`) y feed
inyectado. Medidas de `getBoundingClientRect()` sobre los clips del camino B:

```
tiRight:       100px   (distancia del borde derecho del <li> al borde del .ti)
reactRight:     51px   (el chip de emoji NO llega al borde: 51px de hueco)
replyRight:     14px   (el botón + sí llega: 14px = padding 12 + borde 2)
```

Es decir: **el `+` sí se pega a la derecha, el emoji chip no.** Ese hueco de
~37px entre `.react-chip` y `.reply-btn` es el `gap` + el ancho mal
repartido del `flex:1` del `.ti` en el contexto B. En el camino A ese hueco
no existe porque `.clip-card` media el layout.

#### 6d.4 Por qué arreglarlo bien exige tocar la base de datos primero

El frontend decide **qué camino** usa según `tree.children.get(cid)` →
`kids.length` (`flove-player.js:201-223`), y `cid` viene de `t.clip.id`. Esa
información de "¿tiene respuestas?" se deriva hoy de:

- `risa.json` (feed estático): **no** lleva `parent`/`depth` de forma fiable
  para todas las piezas (solo algunas filas de demo tienen `threads`).
- `threads` (tabla D1, `0001_initial.sql:48-54`): guarda `item_id, parent,
  app, depth`, pero **no** se sirve a la web en el render (la web lee
  `risa.json`; el Workers la replica, no la expone).
- `reactions` / `replies` (D1 `0007_community.sql:16-22, 50-59`): existen en
  la API (`/api/reactions`, `/api/replies`) pero **no** hay un endpoint que
  devuelva, para cada clip, "tiene respuestas / es respuesta de / depth".

Sin ese dato consistente por clip, el render no puede elegir el camino A/B de
forma fiable y se queda en el parche estético.

#### 6d.5 Trabajo previo en D1 (tablas) para desbloquear la reparación

1. **Exponer el grafo de hilos a la web** — nuevo endpoint `GET /api/threads?app=risa`
   (o ampliar `/api/search`) que devuelva `[{item_id, parent, depth}]` a partir de
   `threads` (+ `replies` como hojas `kind='quick'`), para que el frontend
   construya `tree.children` con datos reales y no con el feed estático.
2. **Normalizar `threads`** — añadir `kind` (`audio|video|quick|text`) y
   `src` opcional, para que un hilo mezcle respuestas de audio y quick-replies
   sin duplicar lógica. Añadir `parent_id` nullable en `replies` para
   anidamiento > 1 nivel.
3. **Relleno** — backfill de `threads` desde `replies` existentes
   (una `replies` sin `threads` = hoja de hilo huérfana hoy).
4. **Seed de demo** — ampliar `0001_initial.sql` (y/o `0007`) con un par de
   cadenas completas (padre + 1-2 respuestas) en `risa` para que el render
   A/B sea comprobable sin producción.

Una vez D1 da `parent/depth` por clip, `buildLi` puede renderizar **una sola
estructura** (camino A con `.clip-card` siempre, o el nuevo contrato único) y
eliminar el camino B divergente — ahí la alineación se arregla de una vez,
para risa y para maria, sin selectores de rescate.

#### 6d.6 Archivos y líneas implicadas

| Archivo | Línea | Qué es |
|---|---|---|
| `central/shared/code/js/flove-player.js` | 201-224 | Elección camino A/B en `buildLi` (`toggleLine`/`clip-card`) |
| `central/shared/code/js/flove-feed.js` | 69-119 | `threadOrder` / `buildTree` (derivan hijos por `clip.parent`) |
| `risa/index.html` | 200 | `li` base: flex + padding (contexto del camino B) |
| `risa/index.html` | 217 | `.ti{flex:1}` (el estiramiento que no llega en B) |
| `risa/index.html` | 298-308 | `.reply-btn` y `.react-chip` |
| `risa/index.html` | 374-375 | `.clip-card` (el contexto que funciona en A) |
| `risa/index.html` | 600 | `.thread-item{width:100%}` |
| `central/shared/code/css/flove-media.css` | 68-69, 107 | `.thread-item` compartido + `.thread-item.clip-remix` |
| `risa/worker/migrations/0001_initial.sql` | 48-54 | tabla `threads` |
| `risa/worker/migrations/0007_community.sql` | 16-22, 50-59 | `reactions`, `replies` |
| `risa/worker/api.mjs` | 212-257 | `POST /api/reactions`, `POST /api/replies` (no hay GET de hilos) |
| `maria/index.html` | 13, 38, 159-162 | importa `flove-media.css` + aliases de tokens (blasst radius) |

#### 6d.7 Notas para el arreglo final (post-D1)

- **Unificar el render**: siempre `.clip-card` como caja (camino A), con el
  `li` solo como contenedor de grid. Borrar el `li`-como-tarjeta del camino B.
- **`.ti` con `min-width:0`** ya está; asegurar `flex:1 1 0` no `1` a secas
  cuando el contenedor sea el `li` pelado.
- **Verificar en maria** después de tocar `flove-media.css`/`flove-player.js`:
  comparte el render de clips y sus tokens (`--paper-card`, `--app-accent`)
  ya mapeados (maria `index.html:38`).
- **No** añadir `margin-left:auto` suelto: es el parche que este doc quiere
  evitar. El dato de hilos en D1 es el que permite la unificación limpia.

### 6. Hoja de ruta sugerida

1. `worker/` + `wrangler.toml` con rutas `/api/*` y D1 binding (worker ya
   existe para subdominios; se extiende).
2. Migración D1: crear tablas + seed (identities con marcflove y maria).
3. Claim token-in-item + registro de subdominio (bot `/usuario` o endpoint).
4. `POST /api/profile` → el editor del perfil pasa a escribir en D1 (nombre,
   bio, socials) en vez de solo generar comandos.
5. f1SS: `search_fts` + `GET /api/search`; conectar el input de búsqueda.
6. `POST /api/ingest` llamado por el cron del bot tras cada publicación.
7. Favoritos en la nube y actividad cruzada en los perfiles agregadores.

### 7. Comunidad en D1 (0007) — seguir · reacciones · escuchas · avisos · respuestas

Migración `0007_community.sql` + endpoints `/api/*` (nativos en D1):

| Tabla | Uso | Endpoint |
|---|---|---|
| `follows(follower,target,at)` | seguir/dejar de seguir | `GET /api/follows/:key` · `POST /api/follows` |
| `reactions(app,item_id,reaction,at)` | reacción rápida con emoji (pública) | `POST /api/reactions` |
| `plays(app,item_id,at)` | 1 fila por reproducción → trending | `POST /api/plays` (fire-and-forget) |
| `notifications` + `notify_prefs` | avisos de respuestas/seguidores + preferencia | `GET /api/notifications/:key` · `POST /api/notify-pref` |
| `replies(parent,item_id,content)` | respuesta rápida de la web (quick) | `POST /api/replies` |

Principios:
- **Reacciones/escuchas son públicas y best-effort**: la web las manda con
  timeout corto y fail-silent; nunca bloquean la navegación. Sin identidad
  obligatoria (bajo riesgo de spam, mitigable con rate-limit de Cloudflare).
- **El feed sigue siendo estático** (`risa.json`): D1 nunca reemplaza la
  lectura del feed, solo añade la capa de comunidad.

### 8. Principios de bajo consumo (cuota crítica de Cloudflare)

La cuota gratuita de Workers es **100k peticiones/día** (y 10 ms de CPU por
request). Normas para no agotarla:

1. **El app nunca pasa por el Worker.** `risa.liberada.net` (HTML, `risa.js`,
   `risa.json`, media) se sirve en **grey (DNS-only)** desde GitHub Pages. El
   Worker solo ve `api.liberada.net/*` y los subdominios de usuario.
2. **API en subdominio propio**: `api.liberada.net` (proxied). Separar el API
   del sitio hace que navegar por la web = 0 peticiones de Worker.
3. **Perfiles baratos**: el Worker **302-redirige** `<user>.liberada.net` →
   `liberada.net/usa/<user>/` (µs de CPU) en vez de buscar+y servir el HTML.
   Solo hace fetch-and-serve para usuarios sin carpeta estática.
4. **Cache en el borde**: `Cache-Control` + Cache API en GETs de lectura
   (`/api/search`, `/api/users`, `/api/aliases`) y en los perfiles servidos.
   Reintentos idénticos se resuelven desde el edge.
5. **Menos round-trips del cliente**: un solo `GET /api/profile/:user`
   (identidad+actividad+aliases); leer `usernames.json`/`risa.json` estáticos
   primero y solo llamar al API para lo dinámico.
6. **D1 con cabeza**: cachear lecturas, agrupar escrituras; no duplicar el
   feed en `activity` (el feed vive en `risa.json`). D1 gratuito: 5M filas
   leídas/día, 100k escritas/día.
7. **Monitor**: revisar el gráfico de requests/día y poner una alerta de uso
   al ~80% de las 100k.
