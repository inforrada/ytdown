# 🎬 ytdown

Descargador de vídeos de YouTube por línea de comandos, sencillo y ligero, basado en [yt-dlp](https://github.com/yt-dlp/yt-dlp).

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)

## ✨ Características

- Acepta **URL completa** o solo el **ID del vídeo** (11 caracteres).
- Selecciona por defecto vídeo hasta **1080p** y audio hasta **128 kbps**, con *fallback* automático a la mejor calidad disponible.
- Fusiona vídeo y audio en un único archivo **MP4**.
- **Barra de progreso** con velocidad y tiempo restante (ETA).
- Detecta `ffmpeg` en el `PATH` o usa el binario incluido en `imageio-ffmpeg`.
- Si no hay `ffmpeg`, descarga un formato progresivo (vídeo+audio en un solo archivo).
- Mensajes de error claros (URL inválida, vídeo privado o inexistente).

## 📦 Requisitos

- Python 3.8 o superior
- Dependencias: `yt-dlp` e `imageio-ffmpeg`

## 🚀 Instalación

```bash
git clone https://github.com/inforrada/ytdown.git
cd ytdown
pip install -r requirements.txt
```

## ▶️ Uso

```bash
python ytdown.py
```

El programa te pedirá la URL o el ID del vídeo:

```text
=== YouTube Downloader ===
URL o ID del vídeo: dQw4w9WgXcQ

🎬 Título del vídeo
  Vídeo: 1080p (avc1.640028)
  Audio: 128 kbps (mp4a.40.2)

  [██████████████████████████████] 100.0%  5.20MiB/s  ETA 00:00
  ✔ Pista descargada.

✅ Descarga completada en formato .mp4
```

Formatos de entrada admitidos:

| Entrada | Ejemplo |
|---|---|
| ID del vídeo | `dQw4w9WgXcQ` |
| URL completa | `https://www.youtube.com/watch?v=dQw4w9WgXcQ` |
| URL corta | `https://youtu.be/dQw4w9WgXcQ` |
| Sin protocolo | `youtube.com/watch?v=dQw4w9WgXcQ` |

## ⚙️ Configuración

Puedes ajustar las constantes al principio de [`ytdown.py`](ytdown.py):

| Constante | Valor por defecto | Descripción |
|---|---|---|
| `TARGET_VIDEO_HEIGHT` | `1080` | Resolución vertical máxima (px) |
| `TARGET_AUDIO_BITRATE` | `128` | Bitrate de audio máximo (kbps) |
| `OUTPUT_TEMPLATE` | `%(title)s.%(ext)s` | Plantilla del nombre de archivo |
| `MERGE_OUTPUT_FORMAT` | `mp4` | Contenedor final |

## ⚠️ Aviso legal

Esta herramienta es solo para uso personal y educativo. Respeta los [Términos de servicio de YouTube](https://www.youtube.com/t/terms) y los derechos de autor del contenido que descargues.
