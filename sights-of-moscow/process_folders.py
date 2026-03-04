import os
import re
from pathlib import Path
from transliterate import translit
from docx import Document
from PIL import Image

ROOT = Path(".")
FOLDERS = [
    "arka-vdnh"
]

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif"}

def slugify(name: str) -> str:
    # Транслитерация только при наличии кириллицы
    if re.search(r"[а-яА-ЯёЁ]", name):
        name = translit(name, "ru", reversed=True)
    name = re.sub(r"[^a-zA-Z0-9.\-]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name.lower()

def extract_title_and_text(docx_path: Path) -> tuple[str, list[str]]:
    doc = Document(docx_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    # Ищем заголовок: первый непустой параграф — это title (по логике твоих файлов)
    title = paragraphs[0] if paragraphs else "Без названия"
    text = paragraphs[1:]  # всё остальное — абзацы текста
    return title, text

def ensure_image(folder: Path) -> str | None:
    img_files = [f for f in folder.iterdir() if f.suffix.lower() in IMG_EXTS]
    if not img_files:
        return None
    img = sorted(img_files, key=lambda x: x.stat().st_mtime)[-1]  # самое свежее — на случай дублей

    try:
        with Image.open(img) as im:
            im.load()  # проверка целостности
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                out_path = folder / "image.png"
                im.convert("RGBA").save(out_path, "PNG")
                ext = "png"
            else:
                out_path = folder / "image.jpg"
                im.convert("RGB").save(out_path, "JPEG", quality=90)
                ext = "jpg"

        # Удаляем старые изображения (кроме image.*)
        for f in img_files:
            if f.name not in ("image.jpg", "image.jpeg", "image.png"):
                f.unlink(missing_ok=True)
        return f"image.{ext}"
    except Exception as e:
        print(f"⚠️ Ошибка конвертации изображения в {folder.name}: {e}")
        return None

def process_folder(folder: Path):
    print(f"\n📁 Обрабатываю: {folder.name}")

    # --- 1. Аудио ---
    mp3_files = [f for f in folder.iterdir() if f.suffix.lower() == ".mp3"]
    audio_map = {}
    for f in mp3_files:
        if f.stem == "Чтение текста":
            new_name = "voice.mp3"
            audio_map["voice"] = new_name
        else:
            new_name = slugify(f.stem) + ".mp3"
            audio_map["extra"] = new_name
        if f.name != new_name:
            target = folder / new_name
            if target.exists():
                target.unlink()
            f.rename(target)
            print(f"🔊 {f.name} → {new_name}")

    # --- 2. Изображение ---
    img_filename = ensure_image(folder) or "image.jpg"

    # --- 3. Чтение docx ---
    docx_files = [f for f in folder.iterdir() if f.suffix.lower() == ".docx"]
    if not docx_files:
        print(f"❌ .docx не найден в {folder.name}")
        return
    docx_path = docx_files[0]
    title, paragraphs = extract_title_and_text(docx_path)
    print(f"🔤 Заголовок: {title}")

    # --- 4. Собираем HTML ---
    audio_blocks = []
    if "voice" in audio_map:
        audio_blocks.append(
            f'<div class="audio-block">\n'
            f'    <label for="voice">🎙️ Чтение текста</label>\n'
            f'    <audio id="voice" src="{audio_map["voice"]}" controls></audio>\n'
            f'</div>'
        )
    if "extra" in audio_map:
        label = "🎵 Песня" if "песн" in audio_map["extra"] else "🎧 Доп. аудио"
        audio_blocks.append(
            f'<div class="audio-block">\n'
            f'    <label for="extra">{label}</label>\n'
            f'    <audio id="extra" src="{audio_map["extra"]}" controls></audio>\n'
            f'</div>'
        )

    text_html = "\n".join(f"        <p>{p}</p>" for p in paragraphs if p)

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="stylesheet" href="../styles.css" />
</head>
<body>
    <img src="{img_filename}" alt="{title}" />

{chr(10).join(audio_blocks)}

    <h1>{title}</h1>

    <div class="text">
{text_html}
    </div>

    <div id="qrcode" style="width: 128px; height: 128px;"></div>
    <script src="../qrcode.min.js"></script>
    <script src="../qr.js"></script>
</body>
</html>"""

    html_path = folder / "index.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"✅ index.html обновлён")

# --- Запуск ---
for name in FOLDERS:
    folder = ROOT / name
    if folder.is_dir():
        process_folder(folder)
    else:
        print(f"⚠️ Пропущено (не папка): {name}")

print("\n🎉 Всё готово!")