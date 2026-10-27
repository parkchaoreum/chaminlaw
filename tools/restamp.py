#!/usr/bin/env python3
"""성공사례 이미지는 반드시 이 스크립트로 도장을 찍는다(README '성공사례 이미지 규칙').
성공사례 썸네일: 기존 빨간 도장 제거 → 통일된 도장 합성.
- 서체: 휴먼둥근헤드라인 (HMKMRHD.TTF)
- 도장 크기 고정(이미지 폭의 74%), 윗줄·아랫줄 같은 글자 크기, 기울기 없음, 겹테두리
usage: restamp.py <in.jpg> <out.jpg> "<윗줄(사건명)>" "<아랫줄(결과)>"
"""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/home/claude/fonts/HMKMRHD.TTF"
FONT2 = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"   # 괄호·기호용(휴먼둥근헤드라인은 기호가 전각)
RED = (214, 32, 32)
SYM = set("()·,./-")

def segments(text, size):
    """글자를 (문자열, 폰트) 조각으로 나눔. 공백은 글자 크기의 28% 간격으로 처리."""
    fk = ImageFont.truetype(FONT, size)
    fs = ImageFont.truetype(FONT2, size=int(size * 0.92), index=2)
    out, cur, curf = [], "", None
    for ch in text:
        if ch == " ":
            if cur: out.append((cur, curf)); cur, curf = "", None
            out.append((None, int(size * 0.28)))
            continue
        f = fs if ch in SYM else fk
        if curf is None or f is curf: cur += ch; curf = f
        else: out.append((cur, curf)); cur, curf = ch, f
    if cur: out.append((cur, curf))
    return out

def seg_width(segs):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    w = 0
    for t, f in segs:
        w += f if t is None else d.textbbox((0, 0), t, font=f)[2] - d.textbbox((0, 0), t, font=f)[0]
    return w

def draw_line(d, cx, cy, text, size, fill):
    segs = segments(text, size)
    x = cx - seg_width(segs) / 2
    for t, f in segs:
        if t is None: x += f; continue
        bb = d.textbbox((0, 0), t, font=f)
        d.text((x - bb[0], cy), t, font=f, fill=fill, anchor="lm")
        x += bb[2] - bb[0]

def clean(im):
    a = np.array(im.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    sat = r - np.minimum(g, b)
    red = ((sat > 10) & (r > 80)) | ((sat > 2) & (r > 190))
    m = Image.fromarray((red * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5))
    a[np.array(m) > 0] = [255, 255, 255]
    return Image.fromarray(a.astype("uint8"))

def size_fit(text, size, limit):
    while seg_width(segments(text, size)) > limit and size > 30:
        size -= 2
    return size

def stamp(im, top, bottom, cy=None):
    W, H = im.size
    base = W / 900
    # 고정 치수
    box_w = int(W * 0.70)
    outer, space, inner = int(13 * base), int(9 * base), int(5 * base)
    frame = outer + space + inner
    pad_y, gap = int(22 * base), int(6 * base)
    size = int(110 * base)
    text_limit = box_w - int(30 * base) * 2
    st = size_fit(top, size, text_limit)
    sb = size_fit(bottom, size, text_limit)
    line_h = int(size * 1.08)                       # 두 줄 높이는 글자 크기와 무관하게 고정
    box_h = line_h * 2 + gap + pad_y * 2

    L = Image.new("RGBA", (box_w + frame * 2 + 20, box_h + frame * 2 + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    ox = oy = 10
    d.rectangle([ox, oy, ox + box_w + frame * 2, oy + box_h + frame * 2], outline=RED + (255,), width=outer)
    d.rectangle([ox + outer + space, oy + outer + space,
                 ox + outer + space + box_w + inner * 2, oy + outer + space + box_h + inner * 2],
                outline=RED + (255,), width=inner)
    cx = ox + frame + box_w / 2
    y1 = oy + frame + pad_y + line_h / 2
    y2 = y1 + line_h + gap
    draw_line(d, cx, y1, top, st, RED + (255,))
    draw_line(d, cx, y2, bottom, sb, RED + (255,))

    # 고무도장 질감
    rng = np.random.default_rng(13)
    n1 = Image.fromarray((rng.random((L.height // 3 + 1, L.width // 3 + 1)) * 255).astype("uint8")).resize(L.size, Image.BILINEAR)
    n2 = Image.fromarray((rng.random((L.height, L.width)) * 255).astype("uint8"))
    tex = np.array(n1).astype(float) / 255 * 0.55 + np.array(n2).astype(float) / 255 * 0.45
    arr = np.array(L); al = arr[..., 3].astype(float)
    al = al * np.clip(0.55 + 0.75 * tex, 0, 1)
    al[tex < 0.14] *= 0.35
    arr[..., 3] = al.astype("uint8")
    L = Image.fromarray(arr)

    x = (W - L.width) // 2
    y = int((H * 0.40 if cy is None else cy) - L.height / 2)
    out = im.convert("RGBA")
    out.alpha_composite(L, (max(0, x), max(0, y)))
    return out.convert("RGB")

def thumb(im_clean, top, bottom, W=1200, H=900):
    """카드용 4:3 썸네일: 문서 상단부를 잘라 깔고, 도장을 정중앙에 같은 크기로 찍는다."""
    im = im_clean.convert("RGB")
    s = W / im.width
    im = im.resize((W, int(im.height * s)), Image.LANCZOS)
    if im.height >= H:
        y0 = int(min(max(im.height * 0.30 - H / 2, 0), im.height - H))
        im = im.crop((0, y0, W, y0 + H))
    else:
        canvas = Image.new("RGB", (W, H), "white"); canvas.paste(im, (0, 0)); im = canvas
    return stamp_at(im, top, bottom, cy=H / 2)

def stamp_at(im, top, bottom, cy):
    return stamp(im, top, bottom, cy=cy)


if __name__ == "__main__":
    src, dst, top, bottom = sys.argv[1:5]
    cl = clean(Image.open(src))
    stamp(cl, top, bottom).save(dst, quality=88, optimize=True)
    if len(sys.argv) > 5:
        thumb(cl, top, bottom).save(sys.argv[5], quality=85, optimize=True)
