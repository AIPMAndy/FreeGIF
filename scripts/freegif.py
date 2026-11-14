#!/usr/bin/env python3
"""FreeGIF command-line animator. MIT; optional Pillow runtime for Codex workflows."""
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

DEFAULT_BG = '#edeef8'
FONTS = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/System/Library/Fonts/PingFang.ttc',
    'C:/Windows/Fonts/msyhbd.ttc',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]

def parse_args():
    parser = argparse.ArgumentParser(description='FreeGIF · 免费制作循环动图（Pillow 本地渲染）')
    parser.add_argument('--input', type=Path, required=True, help='原图 PNG/JPG/WebP')
    parser.add_argument('--input-b', type=Path, help='双图切换的第二张图（flip 模式必填）')
    parser.add_argument('--output', type=Path, default=Path('freegif.gif'))
    parser.add_argument('--mode', choices=['float','bounce','sway','zoom','flip','type'], default='float')
    parser.add_argument('--text', default='', help='中文标题或表情包文字')
    parser.add_argument('--watermark', default='', help='可选署名，默认无水印')
    parser.add_argument('--size', type=int, choices=[240,320,480], default=320)
    parser.add_argument('--ratio', choices=['1:1','9:16','16:9'], default='1:1')
    parser.add_argument('--fps', type=int, choices=[8,10,15], default=10)
    parser.add_argument('--seconds', type=float, default=2.0)
    parser.add_argument('--background', default=DEFAULT_BG)
    parser.add_argument('--font', type=Path, help='自定义字体文件，中文需中文字体')
    return parser.parse_args()

def font_for(size, chosen=None):
    for path in ([str(chosen)] if chosen else []) + FONTS:
        if not path:
            continue
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)

def contain_rounded(src, side):
    padded = ImageOps.fit(src.convert('RGBA'), (side, side), method=Image.Resampling.LANCZOS)
    mask = Image.new('L', (side, side), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, side - 1, side - 1), radius=int(side * .15), fill=255)
    padded.putalpha(mask)
    return padded

def make_frames(args):
    if not args.input.is_file():
        raise SystemExit(f'找不到图片：{args.input}')
    if args.mode == 'flip' and (not args.input_b or not args.input_b.is_file()):
        raise SystemExit('flip 模式需要 --input-b 第二张图')
    if not (0.5 <= args.seconds <= 6):
        raise SystemExit('seconds 必须在 0.5–6 秒范围内')
    width = args.size
    height = round(width * {'1:1':1, '9:16':16/9, '16:9':9/16}[args.ratio])
    count = round(args.fps * args.seconds)
    if width * height * count > 12_000_000:
        raise SystemExit('素材太大，降低时长、画幅、尺寸或帧率')
    first = Image.open(args.input).convert('RGBA')
    second = Image.open(args.input_b).convert('RGBA') if args.input_b else None
    side = round(min(width, height) * .54)
    sticker_a = contain_rounded(first, side)
    sticker_b = contain_rounded(second, side) if second else None
    frames = []
    large_font = font_for(max(17, round(min(width, height) * .09)), args.font)
    small_font = font_for(max(10, round(min(width, height) * .031)), args.font)
    for i in range(count):
        t = i / count
        phase = 2 * math.pi * t
        frame = Image.new('RGBA', (width, height), args.background)
        draw = ImageDraw.Draw(frame, 'RGBA')
        for band in range(1, 4):
            radius = min(width, height) * (.27 + band * .13)
            draw.ellipse(
                (width / 2 - radius, height * .42 - radius, width / 2 + radius, height * .42 + radius),
                outline=(113, 112, 153, 35), width=2,
            )
        sticker = sticker_a
        offset = 0
        angle = 0
        scale = 1
        if args.mode == 'float':
            offset = -min(width, height) * .043 * math.sin(phase)
            angle = 1.6 * math.sin(phase)
        elif args.mode == 'bounce':
            offset = -min(width, height) * .16 * abs(math.sin(math.pi * t))
            scale = 1 + .05 * math.sin(phase)
        elif args.mode == 'sway':
            angle = 7 * math.sin(phase)
            offset = min(width, height) * .018 * math.cos(phase)
        elif args.mode == 'zoom':
            scale = 1 + .14 * (.5 - .5 * math.cos(phase))
        elif args.mode == 'flip' and sticker_b is not None:
            sticker = Image.blend(sticker_a, sticker_b, abs(math.sin(math.pi * t)))
        newside = max(8, round(side * scale))
        rotated = sticker.resize((newside, newside), Image.Resampling.LANCZOS).rotate(
            angle, resample=Image.Resampling.BICUBIC, expand=True
        )
        x = round((width - rotated.width) / 2)
        y = round(height * .40 + offset - rotated.height / 2)
        frame.alpha_composite(rotated, (x, y))
        title = args.text
        if args.mode == 'type':
            title = ''.join(list(title)[:int(len(title) * min(1, t * 1.45) ** .6)])
        if title:
            lines = []
            row = ''
            for char in title:
                if char == '\n':
                    lines.append(row)
                    row = ''
                    continue
                if draw.textlength(row + char, font=large_font) > width * .86 and row:
                    lines.append(row)
                    row = char
                else:
                    row += char
            if row:
                lines.append(row)
            lines = lines[:3]
            lineh = large_font.size * 1.3
            start = height * (.74 if height > width * 1.2 else .77) - (len(lines) - 1) * lineh / 2
            for n, line in enumerate(lines):
                draw.text((width / 2, start + n * lineh), line, font=large_font, anchor='mm', fill='#24243a')
        if args.watermark:
            draw.text(
                (width - min(width, height) * .05, height - min(width, height) * .04),
                args.watermark[:32], font=small_font, anchor='rd', fill='#767589'
            )
        frames.append(frame.convert('RGB'))
    return frames

def main():
    args = parse_args()
    frames = make_frames(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    converted = [frame.quantize(colors=192, method=Image.Quantize.MEDIANCUT) for frame in frames]
    converted[0].save(
        args.output,
        save_all=True,
        append_images=converted[1:],
        duration=round(1000 / args.fps),
        loop=0,
        disposal=2,
        optimize=False,
    )
    print(f'✓ {args.output} · {len(frames)} 帧 · {frames[0].size[0]}×{frames[0].size[1]} · {args.fps} FPS')

if __name__ == '__main__':
    main()
