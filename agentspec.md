# AgentSpec: YouTube Video Downloader CLI

Especificación técnica para la implementación de una herramienta de línea de comandos (CLI) en Python destinada a descargar vídeos de YouTube según configuraciones de resolución y bitrate de audio predeterminadas, con fallback a la máxima calidad disponible.

---

## 1. Objetivo y Alcance

Desarrollar un script en Python autónomo que permita a un usuario descargar un vídeo de YouTube ingresando su identificador (ID) o la URL completa. La descarga debe realizarse de forma automatizada combinando vídeo y audio en las calidades especificadas, garantizando una degradación suave (*fallback*) en caso de que la resolución o bitrate deseados no existan para el recurso.

---

## 2. Requisitos Técnicos y Dependencias

- **Lenguaje:** Python 3.9+
- **Librería principal:** `yt-dlp` (recomendada frente a librerías obsoletas como `pytube` por mantenimiento y soporte continuo del protocolo).
- **Herramienta del sistema:** `ffmpeg` (imprescindible para mezclar pistas separadas de vídeo y audio en resoluciones de 1080p o superiores).
- **Dependencias Python sugeridas (`requirements.txt`):**
  ```text
  yt-dlp>=2024.0.0

## 3. Configuración y Constantes
El script debe exponer constantes en el encabezado del archivo para facilitar ajustes sin modificar la lógica interna:  
TARGET_VIDEO_HEIGHT = 1080    # Resolución vertical objetivo en píxeles
TARGET_AUDIO_BITRATE = 128    # Bitrate de audio objetivo en kbps
OUTPUT_TEMPLATE = "%(title)s.%(ext)s"  # Plantilla de nombre para el archivo final
MERGE_OUTPUT_FORMAT = "mp4"   # Contenedor final

## 4. Comportamiento y Flujo de Ejecución
Entrada de usuario:

Solicitar por consola mediante input() la URL completa o el código/ID del vídeo (ej. dQw4w9WgXcQ o https://www.youtube.com/watch?v=dQw4w9WgXcQ).

Normalizar la entrada para garantizar que yt-dlp pueda procesarla directamente (si se ingresa un código de 11 caracteres alfanuméricos, construir la URL canónica o pasar el identificador directamente).

Cálculo de Formatos y Fallback (Estrategia de descarga):

Vídeo: Intentar obtener pista de vídeo de altura igual a TARGET_VIDEO_HEIGHT. Si no está disponible, seleccionar la pista de mayor resolución inferior o superior más cercana/máxima posible (bestvideo).

Audio: Intentar obtener pista de audio con bitrate aproximado a TARGET_AUDIO_BITRATE kbps. Si no está disponible, seleccionar la mejor calidad de audio disponible (bestaudio).

Cadena de formato yt-dlp sugerida:
bestvideo[height<=1080]+bestaudio[abr<=128]/bestvideo+bestaudio/best

(Parametrizada dinámicamente con las constantes TARGET_VIDEO_HEIGHT y TARGET_AUDIO_BITRATE).

Postprocesado y Mezcla:

Fusión automática de las pistas de vídeo y audio seleccionadas en un contenedor .mp4 usando ffmpeg.

Manejo de Errores y Validaciones:

Validar que la entrada no esté vacía.

Capturar excepciones de extracción (DownloadError, URLs inválidas o vídeos privados/inexistentes).

Verificar la disponibilidad de ffmpeg en el sistema y advertir al usuario con un mensaje claro si no está instalado.

Mostrar progreso visual durante la descarga (usando hooks de progreso nativos de yt-dlp).

## 5. Criterios de Aceptación
Entrada flexible: El programa acepta tanto https://youtu.be/..., URLs estándar youtube.com/watch?v=..., como IDs aislados de 11 caracteres.

Priorización de calidad:

Si el vídeo dispone de versión 1080p, descarga la pista a 1080p.

Si el vídeo solo llega a 720p o 480p, descarga la versión 720p o 480p sin arrojar error.

Si el vídeo está en 4K y no existe 1080p exacto, descarga la calidad disponible según la regla de fallback.

Consistencia de audio: El audio se descarga y comprime/selecciona al bitrate más cercano a 128 kbps (o el mejor disponible).

Archivo resultante: Un único archivo .mp4 con vídeo y audio sincronizados en el directorio de ejecución.
