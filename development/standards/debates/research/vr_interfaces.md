# Flove · Theory — Godot + VR, vía software libre

*Notas de investigación. Criterio: **open source primero, "free as in freedom"**.
Última revisión: 2026-06-03.*

Resumen de una conversación de investigación sobre cómo montar experiencias
VR (motor + locomoción + hardware + arte + datos) priorizando software y
hardware **libres**, y dejando lo propietario solo como último recurso y
marcado como tal. Encaja con el ethos flove: *slow it · flow it · love it*,
low-tech, single-file, gift-economy.

---

## 0. Punto de partida y criterio

- **KatVR** (cintas omnidireccionales C2/C2+, mini S, Loco S) es **propietario**:
  SDK cerrado (`KATNativeSDK.dll`), **solo Windows**, licencia de dev bajo
  petición, soporte oficial únicamente para Unity/Unreal. **No** hay plugin
  oficial de Godot. → No debería ser el punto de partida si valoras la libertad.
- Regla adoptada: ante cualquier tooling, **nombrar primero el equivalente
  FOSS**, distinguir *free as in beer* de *free as in freedom*, y señalar
  explícitamente lo cerrado.

---

## 1. Los tres niveles de locomoción VR (por grado de libertad)

### Tier 0 — Stack 100% software libre (sin hardware especial)
La base más libre y la que mejor encaja con flove:

- **Godot** (MIT) — motor; **OpenXR en el core** (sin plugin) desde Godot 4.
- **Monado** — el **runtime OpenXR libre**, equivalente *free-as-in-freedom*
  de SteamVR (propietario). Stack "fully open source" con Godot, sobre todo en
  **Linux**.
- **godot-xr-tools** (MIT) — locomoción lista: teleport, suave y **arm-swing**
  (caminar moviendo los brazos). Cero hardware extra.
- **OpenVR-WalkInPlace** (open source) — "caminar en el sitio" por podómetro.
- **OpenVR-FBTWalk** (open source) — movimiento de trackers → caminar; pensado
  para una **cinta NO motorizada** (pasiva).
- **libsurvive** — tracking Lighthouse abierto para alimentar dirección de pies.

👉 **Lo más libre y barato:** Godot + Monado + godot-xr-tools con **arm-swing /
walk-in-place**. Funciona hoy, sin una línea de código cerrado.

### Tier 1 — Hardware abierto / DIY (cinta omnidireccional libre)
"Piernas de verdad" como la KatVR pero en abierto. Son proyectos de ingeniería
real (motores, rodillos, **seguridad**):

- **TACOVR** — ODT basada en Infento, código en GitHub.
- **PODFirmware** — ODT del proyecto ESIEA, firmware en GitHub.
- **TolDish** — ODT casera documentada paso a paso (Instructables).
- **Hex-Core-MK1** — ODT con rodillos en espiral (paper académico, ~1.76 m²).
- **VR-Stepper** — interfaz DIY tipo *stepper*, mucho más simple de construir.

Alimentan Godot igual que la KatVR (vector dirección+velocidad → `PacketPeerUDP`
o GDExtension), pero **sin SDK cerrado**.

### Tier 2 — Comercial propietario (solo si lo demás no llega)
- **KatVR C2/C2+** — producto pulido pero cerrado y Windows-only. *Fallback* si
  necesitas algo comercial "enchufar y andar" y aceptas el coste de libertad.
  Si hay que integrarlo: la pieza clave es `KATNativeSDK.dll`, llamable desde
  C# (lo confirma el mod FOSS de FFXIV `xivr-Ex_KatWalkC2`).

---

## 2. Editores / motores de juego libres (con XR)

| Motor | Lenguaje | Licencia | XR | Nota |
|---|---|---|---|---|
| **Godot 4** | GDScript / C# | MIT (libre) | **OpenXR core** + godot-xr-tools | Recomendado: editor visual, ligero |
| **A-Frame** | HTML/JS | MIT | **WebXR nativo** | HTML declarativo sobre Three.js — ideal para perfil frontend vanilla |
| **Three.js** | JS | MIT | WebXR | Más bajo nivel, control total |
| **Babylon.js** | JS | Apache/MIT | WebXR de 1ª clase | Motor JS completo, glTF robusto |
| **Bevy** | Rust | MIT/Apache | `bevy_xr` (experimental) | Potente, sin editor visual maduro |
| **Stride** | C# | MIT | XR limitado | Editor visual, PBR |
| **Fyrox / O3DE** | Rust / C++ | MIT / Apache | Limitado | Nicho |
| **Armory3D** | Haxe (en Blender) | Zlib | Limitado | Vive en Blender; mantenimiento irregular |
| **Flax** | C#/C++ | ⚠️ **source-available, NO libre** | Sí | ❌ Evitar si el criterio es libertad |

---

## 3. Plantillas y elementos disponibles

- **godot-xr-tools** (MIT) — la "plantilla" XR de facto (locomoción, manos,
  *grab*, UI 3D, *climbing*). Punto de partida en Godot.
- **A-Frame registry** — componentes sueltos (`aframe-extras`, física…).
- **Assets libres:** **Kenney.nl** y **Quaternius** (modelos **CC0**, libertad
  total); **OpenGameArt** (enorme pero ⚠️ licencias mezcladas); **Godot Asset
  Library** (MIT).
- **Plantillas Godot XR** — proyectos *starter* (incluido material apoyado por
  Meta para Quest).

---

## 4. Incompatibilidades (el eje principal)

**a) Blender ↔ Godot (el dolor clásico):**
- El `.blend` se importa **convirtiéndolo a glTF por debajo** → requiere
  **Blender en el PATH** y hereda las limitaciones de glTF.
- **Roturas por versión:** Blender **4.2** deprecó `vertex_colors` → imports
  `.blend` **fallan en silencio**. Blender **3.5** reescribió el exportador glTF
  → escenas **en blanco** en Godot viejos.
- **Se pierden:** física, config de cámaras/luces, *shader nodes*, *splines*; y
  los *geometry nodes* con instancias → **mallas separadas** (no multimesh,
  ineficiente).
- 🛠️ **Regla:** fija un par de versiones concreto y **prueba el pipeline con un
  cubo antes de modelar en serio**.

**b) Runtime XR:**
- **Monado** (libre) es **Linux-first**; **SteamVR** (propietario) cubre
  Windows/Linux. Cascos como Quest exigen su **runtime propietario** (en PC,
  ALVR/Monado parcial).
- **OpenXR** es el estándar, pero las **extensiones de vendor (Meta…) NO son
  portables**.
- **KatVR SDK** = Windows-only y propietario → **no encaja** en stack
  Monado/Linux.

**c) Web (JS) ↔ nativo (Godot):**
- Three.js/Babylon/A-Frame viven en el **navegador (WebXR)**. Godot exporta a
  web (WASM) pero su **WebXR es más flojo**. **No se mezclan runtimes.**
- **glTF es el puente común**, pero con **extensiones distintas** (Draco, KTX2)
  que no todos importan igual.

**d) Licencias:**
- **Flax** = source-available, **no libre**. **OpenGameArt** = mezcla; combinar
  **GPL** puede "contagiar" tu proyecto; **CC-BY** exige atribución; **CC0** es
  libre total → preferir CC0.

**e) Hardware:**
- **Relativty** = 3DoF, sin mandos → experimentar, no locomoción seria.
- **libsurvive** = tracking libre **pero** necesita *basestations* Valve
  (hardware propietario) → libertad **parcial**.

---

## 5. Hardware recomendado por su libertad

- **Relativty** — HMD **open source** (~200 $, 2K/120fps, SteamVR; 3DoF, sin
  mandos).
- **libsurvive** (Collabora, MIT) — tracking **Lighthouse 6DoF libre**.
- **Lo más purista (free as in freedom):** tracker **DIY** con **KiCad**
  (sensores TS4231 + IMU BNO085) usando el **gateware Lighthouse de Bitcraze
  (LGPL)**, sobre placa **FSF-RYF (Talos II)** — documentado en el blog de la
  FSFE.
- **Project North Star** — HMD **AR de hardware abierto**.
- **Piernas libres** = Tier 1 (ODT DIY) o trackers + cinta pasiva.

---

## 6. Importadores Blender / JavaScript

- **Blender → Web (lo más limpio):** exporta **glTF/.glb** y carga con
  `GLTFLoader` (Three.js), `SceneLoader` (Babylon) o `<a-gltf-model>` (A-Frame).
  glTF es el **formato nativo de la web** → **menos pérdidas** que hacia Godot.
- **Blender → Godot:** glTF 2.0 (mejor exportar `.glb` a mano) o `.blend`
  directo (requiere Blender en PATH; add-on oficial aún en propuesta).
- **Blender → Armory:** nativo (Armory vive dentro de Blender).
- **JS:** *loaders* para glTF/OBJ/FBX; y para **datos**, JSON es nativo del
  lenguaje.

---

## 7. Resultados de juego en JSON

- **En web/JS (vía natural para flove):** `JSON.stringify(resultado)` + `Blob`
  + descarga. Single-file, sin backend, sin red.
- **En Godot:** `JSON.stringify()` / `JSON.parse_string()` + `FileAccess` para
  guardar el `.json`.
- **Validación/forma:** define tu **JSON Schema** y valida con **ajv** (JS) o
  inspecciona con **jq**.
- **Ojo:** glTF también es "JSON", pero describe **la escena 3D**, no **los
  resultados de la partida** (eventos, scores, relaciones, ratings) — para eso
  usas **tu propio esquema**.

---

## 8. Síntesis (para el perfil frontend-vanilla, open-source-first, low-tech)

1. **Interfaces 2D/UI** → **A-Frame / Three.js o HTML-JS vanilla** + WebXR;
   resultados en **JSON nativo** (Blob). Lo más cercano a lo que ya se domina.
2. **Juego 3D con cinta** → **Godot + Monado + godot-xr-tools**; arte vía
   **glTF desde Blender fijando versiones**; JSON con `FileAccess`.
3. **Hardware libre** → **Relativty + libsurvive** para trastear; **ODT DIY**
   para piernas.
4. **Evitar por libertad:** **Flax**, y depender de **SteamVR / KatVR**.

Aviso honesto: el camino libre vive mejor en **Linux** (Monado); las ODT DIY
exigen tiempo, taller y seguridad; y walk-in-place no es tan inmersivo como una
cinta — pero es lo más libre y lo más "flove".

---

## Fuentes

- Motores: [Top FOSS engines 2025 (Blacave)](https://blacave.com/en/articles/bestopensourcegameengines) · [FOSS engines (Stride blog)](https://www.stride3d.net/blog/open-worlds-intro-to-foss-game-engines/)
- Godot↔Blender: [Interoperability (Blender devtalk)](https://devtalk.blender.org/t/state-of-interoperability-between-godot-and-blender/38559) · [Blender 4.2 .blend roto (#93997)](https://github.com/godotengine/godot/issues/93997) · [Formatos glTF (Godot docs)](https://github.com/godotengine/godot-docs/blob/master/tutorials/assets_pipeline/importing_3d_scenes/available_formats.rst)
- Runtime libre: [Monado](https://monado.dev/) · [monado_godot_openxr](https://github.com/seconrg/monado_godot_openxr)
- Locomoción libre: [OpenVR-WalkInPlace](https://github.com/pottedmeat7/OpenVR-WalkInPlace) · [OpenVR-FBTWalk](https://github.com/Yuumum/OpenVR-FBTWalk)
- Hardware ODT DIY: [TACOVR](https://github.com/srepmub/tacovr) · [PODFirmware](https://github.com/Ybalrid/PODFirmware) · [TolDish (Instructables)](https://www.instructables.com/TolDish-a-DIY-Omnidirectional-Treadmill/) · [Hex-Core-MK1 (arXiv)](https://arxiv.org/pdf/2204.08437) · [VR-Stepper (arXiv)](https://arxiv.org/pdf/1407.3948)
- Hardware libre HMD/tracking: [Relativty](https://github.com/relativty/Relativty) · [libsurvive (Collabora)](https://github.com/collabora/libsurvive) · [Tracker RYF DIY (FSFE)](https://blogs.fsfe.org/tobias_platen/2025/04/01/building-my-own-libsurvive-compatible-lighthouse-tracker/)
- Web/JS: [Top 5 WebXR frameworks (Wonderland)](https://wonderlandengine.com/news/top-5-webxr-frameworks-comparison/) · [Babylon.js vs Three.js](https://dev.to/devin-rosario/babylonjs-vs-threejs-the-360deg-technical-comparison-for-production-workloads-2fn6)
- KatVR (propietario, referencia): [KAT SDK](https://www.kat-vr.com/pages/sdk) · [xivr-Ex_KatWalkC2 (usa la DLL)](https://github.com/Haurrus/xivr-Ex_KatWalkC2)

---

*Asterism: . Slow it · flow it · love it — incluso la libertad del software.*
