#!/usr/bin/env python3
"""YouTube Video Downloader CLI (ver agentspec.md)."""
import re
import shutil
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

try:
    import yt_dlp
    from yt_dlp.utils import DownloadError
except ImportError:
    print("Error: falta 'yt-dlp'. Instálalo con: pip install -r requirements.txt")
    sys.exit(1)

# ---------------- Configuración ----------------
TARGET_VIDEO_HEIGHT = 1080    # Resolución vertical objetivo en píxeles
TARGET_AUDIO_BITRATE = 128    # Bitrate de audio objetivo en kbps
OUTPUT_TEMPLATE = "%(title)s.%(ext)s"  # Plantilla de nombre para el archivo final
MERGE_OUTPUT_FORMAT = "mp4"   # Contenedor final
# ------------------------------------------------

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def build_format_string(height: int = TARGET_VIDEO_HEIGHT, abr: int = TARGET_AUDIO_BITRATE) -> str:
    """Cadena de formato con fallback progresivo."""
    return (
        f"bestvideo[height<={height}]+bestaudio[abr<={abr}]"
        f"/bestvideo[height<={height}]+bestaudio"
        f"/bestvideo+bestaudio"
        f"/best"
    )


def normalize_input(raw: str) -> str:
    """Convierte un ID de 11 caracteres en URL canónica; deja las URLs tal cual."""
    value = raw.strip()
    if VIDEO_ID_RE.match(value):
        return f"https://www.youtube.com/watch?v={value}"
    if not re.match(r"^https?://", value) and ("youtube.com" in value or "youtu.be" in value):
        return "https://" + value
    return value


def progress_hook(d: dict) -> None:
    status = d.get("status")
    if status == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        done = d.get("downloaded_bytes", 0)
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        if total:
            pct = done / total
            bar = "█" * int(pct * 30) + "░" * (30 - int(pct * 30))
            sys.stdout.write(f"\r  [{bar}] {pct*100:5.1f}%  {speed}  ETA {eta}   ")
        else:
            sys.stdout.write(f"\r  {done/1048576:.1f} MiB  {speed}   ")
        sys.stdout.flush()
    elif status == "finished":
        sys.stdout.write("\n  ✔ Pista descargada.\n")
        sys.stdout.flush()


FFMPEG_LOCATION = None  # ruta al binario de ffmpeg si no está en el PATH


def check_ffmpeg() -> bool:
    global FFMPEG_LOCATION
    if shutil.which("ffmpeg") is not None:
        return True
    try:  # ffmpeg empaquetado vía pip (imageio-ffmpeg)
        import imageio_ffmpeg
        FFMPEG_LOCATION = imageio_ffmpeg.get_ffmpeg_exe()
        return True
    except Exception:  # noqa: BLE001
        pass
    print("⚠ ADVERTENCIA: no se encontró 'ffmpeg'.")
    print("  Instálalo con: pip install imageio-ffmpeg  (o añade ffmpeg al PATH).")
    return False


def download(url: str, has_ffmpeg: bool) -> None:
    opts = {
        "format": build_format_string() if has_ffmpeg else "best[vcodec!=none][acodec!=none]/best",
        "outtmpl": OUTPUT_TEMPLATE,
        "merge_output_format": MERGE_OUTPUT_FORMAT,
        "progress_hooks": [progress_hook],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    if FFMPEG_LOCATION:
        opts["ffmpeg_location"] = FFMPEG_LOCATION
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        sel = info.get("requested_formats") or [info]
        print(f"\n🎬 {info.get('title')}")
        for f in sel:
            if f.get("vcodec") not in (None, "none"):
                print(f"  Vídeo: {f.get('height')}p ({f.get('vcodec')})")
            if f.get("acodec") not in (None, "none"):
                abr = f.get("abr")
                print(f"  Audio: {round(abr) if abr else '?'} kbps ({f.get('acodec')})")
        print()
        ydl.process_ie_result(info, download=True)
    print(f"\n✅ Descarga completada en formato .{MERGE_OUTPUT_FORMAT}")


def main() -> int:
    print("=== YouTube Downloader ===")
    has_ffmpeg = check_ffmpeg()
    try:
        raw = input("URL o ID del vídeo: ")
    except (KeyboardInterrupt, EOFError):
        print("\nCancelado.")
        return 1
    if not raw.strip():
        print("Error: la entrada no puede estar vacía.")
        return 1
    url = normalize_input(raw)
    try:
        download(url, has_ffmpeg)
    except DownloadError as e:
        print(f"\n❌ Error de descarga (URL inválida, vídeo privado o inexistente): {e}")
        return 1
    except KeyboardInterrupt:
        print("\nDescarga cancelada por el usuario.")
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"\n❌ Error inesperado: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
