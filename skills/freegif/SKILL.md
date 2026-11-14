---
name: freegif
description: Use FreeGIF to create looping GIF stickers and lightweight animated posters from local images. No API key or account.
---

# FreeGIF Skill for Codex

The project contains a dependency-free mobile-friendly web editor (`index.html`) and a Pillow-based Python CLI (`scripts/freegif.py`).

## Use it when

A user requests GIF, animated sticker, animated text, comparison of two pictures or lightweight motion poster. Use local images they own or have permission to use.

## Workflow

1. Check the input and output requirements; default to square 320px, 10fps and 2 seconds.
2. Install Python dependency: `python -m pip install -r requirements.txt`.
3. Run `python scripts/freegif.py --help` and choose one mode: `float`, `bounce`, `sway`, `zoom`, `flip`, `type`.
4. Example: `python scripts/freegif.py --input photo.png --mode bounce --text "你好" --output output.gif`.
5. For two images: `python scripts/freegif.py --input before.png --input-b after.png --mode flip --output comparison.gif`.
6. Decode and inspect the produced GIF; verify loop, size, visible change between frames, and target-platform requirements. Provide the actual output artifact.

Do not claim AI-generated full-body movements, automatically verified social-platform compliance, or GitHub deployment unless it was truly performed. Never upload private images without permission. Watermarks are optional and off by default.
