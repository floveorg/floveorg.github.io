# Apps · colores y categorías

> Fuente: `apps/apps-full.html` — idéntico a `apps/apps-full.html`. Dos superficies: **43 fichas** (41 apps + 2 lanzadores) y la **rejilla de 37 tiles**.
> Actualizado el 2026-11-15.

**La categoría es lo canónico.** El color del tile es libertad de coloreado del lanzador: enseña que una misma categoría se puede pintar de varias formas desde la raíz. Las fichas ya llevan la categoría de la rejilla y su color se queda como está.

Tres decisiones aplicadas: **Economy** se queda con una sola clase (`economy`), **Social** pasa a azul y **Economy** a índigo —el color de sus propios tiles—; y las píldoras llevan ya su par inglés/español.

| Eje | Qué pinta | Canónico |
|---|---|---|
| **Categoría** (`cat-*`) | el título y la píldora de la ficha | **sí** — es la clasificación |
| **Color** (`rb-*`) | el degradado del tile y del cubo | no — es libertad del lanzador |

## 1 · Tokens de color

Siete tokens fijos (`r o y g b i v`), cada uno con degradado de dos paradas y su tinta.

| Token | Color | Español | Claro (`--grad-1`) | Saturado (`--grad-2`) | Tinta |
|---|---|---|---|---|---|
| `r` | 🔴 Red | rojo | `#ffd6d6` | `#ff8a8a` | `#3a0e0e` |
| `o` | 🟠 Orange | naranja | `#ffe1cc` | `#ff9b5e` | `#3a1a0a` |
| `y` | 🟡 Yellow | amarillo | `#fff5cc` | `#ffd84d` | `#3d2a0a` |
| `g` | 🟢 Green | verde | `#d4f0db` | `#6ed089` | `#0a3a1f` |
| `b` | 🔵 Blue | azul | `#cfe1f4` | `#5ea4e6` | `#0a2438` |
| `i` | 🟦 Indigo | índigo | `#d6d6f4` | `#6b6bd9` | `#0e0e3a` |
| `v` | 🟣 Violet | violeta | `#e7d4ff` | `#b27aff` | `#28104a` |

## 2 · Categorías

Seis categorías, seis reglas, un nombre por categoría. Los alias en español (`metafisica`, `ciencia`, `biologia`, `lenguajes`) y la regla duplicada de `social` se han retirado: el vocabulario de clases queda cerrado y el de interfaz va en pares `.en`/`.es`.

| Etiqueta | Clase CSS | Degradado del título | Fichas |
|---|---|---|---|
| **Inside** | `cube-cat-inside` | `#ff7a2e` → `#ff9b5e` → `#ffcf9a` | 13 |
| **Mating** | `cube-cat-mating` | `#e8a200` → `#ffce3a` → `#fff0a0` | 8 |
| **Social** | `cube-cat-social` | `#2e74c8` → `#5ea4e6` → `#bcd9f5` | 5 |
| **Economy** | `cube-cat-economy` | `#4b4bc0` → `#6b6bd9` → `#b8b8f0` | 9 |
| **Words** | `cube-cat-ling` | `#ff8aae` → `#c133ff` → `#ffd9d9` | 8 |

### Las seis reglas del CSS

| Clase | Parada 1 | Parada 2 | Parada 3 |
|---|---|---|---|
| `cube-cat-ling` | `#ff8aae` | `#c133ff` | `#ffd9d9` |
| `cube-cat-inside` | `#ff7a2e` | `#ff9b5e` | `#ffcf9a` |
| `cube-cat-mating` | `#e8a200` | `#ffce3a` | `#fff0a0` |
| `cube-cat-social` | `#2e74c8` | `#5ea4e6` | `#bcd9f5` |
| `cube-cat-economy` | `#4b4bc0` | `#6b6bd9` | `#b8b8f0` |

## 3 · Inventario

Las 35 fichas, agrupadas por su categoría ya alineada con la rejilla. **(L)** = lanzador.

### Inside · 13

| App | id | Color | Categoría |
|---|---|---|---|
| **Goddy** | `app-goddy` | 🟠 orange | `cube-cat-inside` |
| **Astry** | `app-astry` | 🟠 orange | `cube-cat-inside` |
| **Willy** | `app-willy` | 🟠 orange | `cube-cat-inside` |
| **Moraly** | `app-moraly` | 🟠 orange | `cube-cat-inside` |
| **Hacky** | `app-hacky` | 🟠 orange | `cube-cat-inside` |
| **DieSafe** | `app-diesafe` | 🟠 orange | `cube-cat-inside` |
| **Profily** | `app-profily` | 🟠 orange | `cube-cat-inside` |
| **Sensy** | `app-sensy` | 🟠 orange | `cube-cat-inside` |
| **Souls** | `app-souls` | 🟠 orange | `cube-cat-inside` |
| **Lovy** | `app-lovy` | 🟡 yellow | `cube-cat-inside` |
| **Pracsys** | `app-pracsys` | 🟠 orange | `cube-cat-inside` |
| **Fity** | `app-fity` | 🟠 orange | `cube-cat-inside` |
| **Questy** | `app-questy` | 🟠 orange | `cube-cat-inside` |

### Mating · 8

| App | id | Color | Categoría |
|---|---|---|---|
| **Crumbly** | `app-crumbly` | 🟡 yellow | `cube-cat-mating` |
| **MyFamily** | `app-myfamily` | 🟡 yellow | `cube-cat-mating` |
| **Parenty** | `app-parenty` | 🟡 yellow | `cube-cat-mating` |
| **Daty** | `app-daty` | 🟡 yellow | `cube-cat-mating` |
| **Maty** | `app-maty` | 🟡 yellow | `cube-cat-mating` |
| **Varyy** | `app-varyy` | 🟡 yellow | `cube-cat-mating` |
| **Evily** | `app-evily` | 🟡 yellow | `cube-cat-mating` |
| **Trusty** | `app-trusty` | 🟡 yellow | `cube-cat-mating` |

### Social · 5

| App | id | Color | Categoría |
|---|---|---|---|
| **Realy** | `app-realy` | 🟢 green | `cube-cat-social` |
| **Socy** | `app-socy` | 🟢 green | `cube-cat-social` |
| **Nety** | `app-nety` | 🟢 green | `cube-cat-social` |
| **Wizy** | `app-wizy` | 🔵 blue | `cube-cat-social` |
| **Browsy** | `app-browsy` | 🔵 blue | `cube-cat-social` |

### Economy · 9

| App | id | Color | Categoría |
|---|---|---|---|
| **Economy · Launcher (L)** | `launch-offer` | 🟦 indigo | `cube-cat-economy` |
| **Wanty** | `app-wanty` | 🔵 blue | `cube-cat-economy` |
| **Inventary** | `app-inventary` | 🟣 violet | `cube-cat-economy` |
| **Crafty** | `app-crafty` | 🔵 blue | `cube-cat-economy` |
| **Worthing** | `app-worthing` | 🔵 blue | `cube-cat-economy` |
| **Lowy** | `app-lowy` | 🔵 blue | `cube-cat-economy` |
| **Rewardy** | `app-rewardy` | 🟣 violet | `cube-cat-economy` |
| **Freed** | `app-freed` | 🟣 violet | `cube-cat-economy` |
| **Shary** | `app-shary` | 🟣 violet | `cube-cat-economy` |

### Words · 8

| App | id | Color | Categoría |
|---|---|---|---|
| **Puzzy · Launcher (L)** | `launch-puzzy` | 🟢 green | `cube-cat-ling` |
| **Keys** | `app-keys` | 🟣 violet | `cube-cat-ling` |
| **Fivy** | `app-fivy` | 🟠 orange | `cube-cat-ling` |
| **Loly** | `app-loly` | 🟢 green | `cube-cat-ling` |
| **Wisy** | `app-wisy` | 🟢 green | `cube-cat-ling` |
| **Frotis** | `app-frotis` | 🟡 yellow | `cube-cat-ling` |
| **Chacrikun** | `app-chacrikun` | 🔴 red | `cube-cat-ling` |
| **ElectrOrchestra** | `app-electrorchestra` | 🟦 indigo | `cube-cat-ling` |

## 4 · Recuentos

| Categoría | Apps | Lanzadores | Total |
|---|---|---|---|
| Inside | 13 | 0 | 13 |
| Mating | 8 | 0 | 8 |
| Social | 5 | 0 | 5 |
| Economy | 8 | 1 | 9 |
| Words | 7 | 1 | 8 |

| Color | Fichas |
|---|---|
| 🔴 red | 1 |
| 🟠 orange | 13 |
| 🟡 yellow | 10 |
| 🟢 green | 6 |
| 🔵 blue | 6 |
| 🟦 indigo | 2 |
| 🟣 violet | 5 |

## 5 · Rejilla frente a ficha

### 5.1 · Categorías y colores alineados

| Qué | Antes | Ahora |
|---|---|---|
| **Keys** y **Fivy** | categoría `inside` | `ling` · píldora Words / Palabras |
| **Economy** | dos clases: `economy` (4) y `economia` (4) | una sola: `economy` (8) |
| **Social** | verde (y una definición rojo→amarillo muerta) | azul `#2e74c8` → `#5ea4e6` |
| **Economy** | azul | índigo `#4b4bc0` → `#6b6bd9`, como sus tiles |
| **Píldoras** | 5 sin traducción (Social ×4, Psico) | todas con `.en` + `.es` |

### 5.2 · Colores distintos (por diseño)

Ocho fichas se pintan con otro color que su tile. **No es un error**: el lanzador elige color y el cubo elige otro, y esa libertad es justo lo que enseña la paleta. Queda aquí como referencia, no como pendiente.

| App | Rejilla | Ficha |
|---|---|---|
| **Realy** | 🔵 blue `b` `#5ea4e6` | 🟢 green `g` `#6ed089` |
| **Keys** | 🟢 green `g` `#6ed089` | 🟣 violet `v` `#b27aff` |
| **Socy** | 🔵 blue `b` `#5ea4e6` | 🟢 green `g` `#6ed089` |
| **Nety** | 🔵 blue `b` `#5ea4e6` | 🟢 green `g` `#6ed089` |
| **Crafty** | 🟦 indigo `i` `#6b6bd9` | 🔵 blue `b` `#5ea4e6` |
| **Worthing** | 🟦 indigo `i` `#6b6bd9` | 🔵 blue `b` `#5ea4e6` |
| **Lowy** | 🟦 indigo `i` `#6b6bd9` | 🔵 blue `b` `#5ea4e6` |
| **Fivy** | 🟢 green `g` `#6ed089` | 🟠 orange `o` `#ff9b5e` |

### 5.3 · Categorías extra solo en la rejilla

La ficha admite una categoría; la rejilla puede llevar varias. Estas la etiquetan además:

| App | Color (igual) | Rejilla | Ficha |
|---|---|---|---|
| **Willy** | 🟠 orange | `cat-inside` · `cat-social` | `cube-cat-inside` |
| **Moraly** | 🟠 orange | `cat-inside` · `cat-social` | `cube-cat-inside` |
| **Profily** | 🟠 orange | `cat-inside` · `cat-social` | `cube-cat-inside` |
| **Lovy** | 🟡 yellow | `cat-inside` · `cat-mating` · `cat-social` · `cat-economy` | `cube-cat-inside` |
| **Questy** | 🟠 orange | `cat-inside` · `cat-social` | `cube-cat-inside` |
| **Loly** | 🟢 green | `cat-ling` · `cat-inside` | `cube-cat-ling` |

## 6 · Las seis fichas nuevas

Las seis apps que solo vivían en la rejilla ya tienen ficha: marca, nombre, lema, categoría, una línea y su enlace. Es la primera versión — **solo marca y destino**, sin capturas ni valores— y la base para el resto.

| App | Color | Categoría | Enlace | Identidad |
|---|---|---|---|---|
| **Fity** | 🟠 orange `o` | `cube-cat-inside` | `bio/fity.html` | estudio hecho |
| **Questy** | 🟠 orange `o` | `cube-cat-inside` | `https://flove.org/development/standards/skills/questy/index.html` | estudio hecho |
| **Loly** | 🟢 green `g` | `cube-cat-ling` | `https://flove.org/projects/liberada/risa/index.html` | estudio hecho |
| **Wisy** | 🟢 green `g` | `cube-cat-ling` | `puzzy/wisy.html` | estudio hecho (04) |
| **Wizy** | 🔵 blue `b` | `cube-cat-social` | `https://flove.org/apps/sys/wizy/index.html` | estudio hecho (01) |
| **Browsy** | 🔵 blue `b` | `cube-cat-social` | `https://flove.org/apps/sys/browsy/index.html` | estudio hecho (06) |

Fity y Questy ya tenían estudio. **Loly** (caras de risa), **Wisy** (la lámpara, 04) y **Wizy** (la chispa, 01) tienen ya el suyo: gama, gama en movimiento y seis animaciones. **Browsy** (las dos ventanas, 06) cierra el set: las cuatro tienen ya su estudio, un archivo cada una.

## 7 · Lo que sigue abierto

1. **Mating** conserva el nombre en inglés; su etiqueta española es «Vínculos». Si el vocabulario debe ser bilingüe también en la clase, el siguiente paso es `cube-cat-links`.
2. **Cuatro apps llevan categorías extra solo en la rejilla** (Willy, Moraly, Profily, Lovy): la ficha admite una, el tile varias.
3. **El catálogo no es idéntico**: 8 entradas con ficha no salen en la rejilla (3 lanzadores + Wanty, Inventary, Rewardy, Freed, Shary).
4. **El color no clasifica** (11 de 32 apps comparten naranja). Es decoración: la clasificación va en el degradado del título y en la píldora.
5. **Cuatro fichas nuevas esperan `brandy`**: Loly, Wisy, Wizy y Browsy.
