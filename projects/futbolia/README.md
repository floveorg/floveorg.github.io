# Futbolia — clon y reedición

Recuperación web de **futbolia.org**, el club de fútbol surrealista: un **clon fiel** del sitio original y una **reedición editorial** en HTML que reordena el mismo contenido.

Abre [`index.html`](index.html) para ver la reedición.

```
futbolia/
├── index.html              Reedición autocontenida (HTML + CSS + JS)
├── clone/                  Clon fiel del sitio original (16 HTML + CSS)
│   ├── index.html          Portada: «Entra un revulsivo…»
│   ├── blog.html           Blog con las 7 entradas
│   ├── oficinas.html       Contactos del club
│   ├── entrada-*.html      7 entradas individuales
│   ├── categoria-*.html    6 archivos de categoría
│   └── clone.css
├── assets/
│   ├── img/                27 imágenes y favicons originales
│   ├── audio/              23 MP3 del archivo original (nombres de fichero)
│   ├── fonts/              Manrope + Instrument Serif (woff2)
│   └── previews/           Capturas del clon y de la reedición
└── README.md
```

## Cómo abrirlo

No requiere instalación ni build. Abre `index.html` directamente en el navegador.

Para servir el proyecto en local (recomendado si el navegador restringe archivos locales):

```bash
cd flove/projects/futbolia
python3 -m http.server 8000
# http://localhost:8000
```

- Clon: `http://localhost:8000/clone/`
- Reedición: `http://localhost:8000/`

## El clon fiel

Se reconstruyó a partir del HTML y los estilos publicados por el sitio original, respetando:

- Columna de contenido de **645 px** sobre fondo blanco, con los espaciados verticales medidos (197, 152, 136, 202 px…).
- Tipografía y jerarquía: H1 de 48 px, cuerpo de 18 px, botones negros en píldora.
- Las **7 entradas** (`atleti`, `luis-padrique`, `rafa-y`, `altas-cejas-derechas`, `luka`, `clasico-choque-de-filosofias`, `imanol`) y las **6 categorías** (`fotomontajes`, `historia`, `otros`, `otros-deportes`, `recortes-de-prensa`, `videos`).
- Galerías, retratos de oficinas, escudo, favicons y la cantada del portero en local.
- Los mismos enlaces externos: paquetes de Codeberg, vídeos de YouTube e Internet Archive, narración AAC e Instagram.

Diferencias inevitables: los archivos multimedia y las fuentes se sirven en local (el original dependía de la red), y se añadieron un enlace de salto al contenido y textos alternativos en las imágenes.

## La reedición

Una sola página, sin frameworks ni peticiones externas, con el contenido original reinterpretado:

- **Portada editorial**: el **escudo con glow animado** en verdes cambiantes y translúcidos abre la página, a la izquierda del gran reproductor de audio. Debajo, la playlist y las descargas. En el **pie**, tres **contadores-botón cuadrados** (23 canciones, 24 fotomontajes, 5 descargas) que llevan a sus secciones y el carrusel de palabras con pausa propia; no se detiene al pasar el ratón ni al enfocarlo y cada palabra abre una respuesta distinta.
- **La música del club** primero: reproductor propio con onda dibujada en JS, reproducción, búsqueda por clic o teclado, tiempos y descarga local desde el icono al final del reproductor. Debajo, en dos columnas, una **playlist de 23 temas** con los nombres originales de los ficheros (10 pistas y carga de 10 en 10) y las **descargas** en cajas iconizadas con su formato caricaturizado (ZIP, MP3, MP4, AAC).
- **Entradas salvajes**: filtros por categoría y fichas que se abren en un diálogo con galería, miniaturas y navegación.
- **«Cercanos al Área»** con Mas Poesía y Mas Visual, y sus enlaces originales.
- **Oficinas**: contacto real y formulario de socio de demostración (valida en cliente, no envía datos).
- **Reproductor flotante**: aparece al reproducir audio o vídeo, mantiene el control de pausa y progreso aunque se haga scroll, y se detiene y oculta al cerrarlo o al abandonar la página.
- **Interfaz en español** y **tema claro/oscuro**, con la preferencia de tema guardada cuando el navegador lo permite.
- Accesibilidad: navegación por teclado, `aria` en controles, foco visible, contraste revisado, `prefers-reduced-motion`, enlace de salto y diálogo nativo.
- Responsive de 320 px en adelante.

### Notas de la reedición

- El **texto de presentación** de cada entrada en el diálogo es una adición editorial; el contenido y los enlaces originales se conservan. La página lo indica en cada ficha.
- El **abono de temporada**, la cita de oficinas y los textos de la portada son piezas de diseño de esta edición, no contenido del sitio original.
- El **formulario de socio es una demostración**: no tiene backend ni envía datos.
- Los enlaces a Codeberg, Internet Archive e Instagram apuntan a los destinos originales y pueden cambiar con el tiempo.

## Fuente y créditos

- Contenido original: [futbolia.org](http://futbolia.org/) (el sitio responde por HTTP; HTTPS devuelve error TLS en el momento de la recuperación).
- Fechas de las entradas: mayo–julio de 2025.
- Contacto en la reedición: `marc@futbolia.org` (presidente); el clon fiel conserva los contactos originales del sitio.
- Tipografías: Manrope e Instrument Serif (woff2, servidas en local).
- Este proyecto es un ejercicio de recuperación y diseño; **no es una edición oficial del club**.
