#!/usr/bin/env python3
"""按站点六色 token 生成品牌统一的封面图与 og 图。16:10=1200x750 卡片；og=1200x630。"""
from PIL import Image, ImageDraw, ImageFont
import os, math, random

BG, SURFACE, LINE, INK, MUTED, ACCENT = '#0d1117', '#161b22', '#21262d', '#e6edf3', '#8b949e', '#58a6ff'
W, H = 1200, 750
OUT = 'public/products'
os.makedirs(OUT, exist_ok=True)

def font(size, bold=False):
    for p in (['/mnt/c/Windows/Fonts/msyhbd.ttc'] if bold else []) + ['/mnt/c/Windows/Fonts/msyh.ttc', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def canvas():
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    return im, d

def frame(d, pad=36):
    """内容内框：细边 + 四角短标（工程制图感）"""
    d.rectangle([pad, pad, W - pad, H - pad], outline=LINE, width=2)
    L = 26
    for (x, y, dx, dy) in [(pad, pad, 1, 1), (W - pad, pad, -1, 1), (pad, H - pad, 1, -1), (W - pad, H - pad, -1, -1)]:
        d.line([x, y, x + L * dx, y], fill=MUTED, width=3)
        d.line([x, y, x, y + L * dy], fill=MUTED, width=3)

def center(d, text, y, size, fill, bold=False, ls=0):
    f = font(size, bold)
    tw = d.textlength(text, font=f) + ls * (len(text) - 1)
    x = (W - tw) / 2
    d.text((x, y), text, font=f, fill=fill)
    return f

def tag(d, text, x, y, fill=MUTED, border=LINE):
    f = font(22)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 28, y + 44], radius=22, outline=border, width=2)
    d.text((x + 14, y + 8), text, font=f, fill=fill)
    return tw + 28

# ---------- og.png 1200x630 ----------
im = Image.new('RGB', (1200, 630), BG)
d = ImageDraw.Draw(im)
d.rectangle([30, 30, 1170, 600], outline=LINE, width=2)
f60 = font(84, True); f28 = font(30); f24 = font(26)
d.text((90, 170), 'WangZhi', font=f60, fill=INK)
d.text((90 + d.textlength('WangZhi', font=f60) + 8, 222), '.', font=f60, fill=ACCENT)
d.text((90, 300), '独立开发者 · 做实用的小产品', font=f28, fill=MUTED)
tx = 90
for t in ['火花快讯', '第三战', 'AI 虚拟试衣', '量化选股']:
    w = d.textlength(t, font=f24) + 32
    d.rounded_rectangle([tx, 420, tx + w, 470], radius=24, outline=ACCENT if t == '火花快讯' else LINE, width=2)
    d.text((tx + 16, 432), t, font=f24, fill=ACCENT if t == '火花快讯' else MUTED)
    tx += w + 16
d.text((90, 530), 'https://bailin1125.github.io', font=f24, fill=MUTED)
im.save('public/og.png', optimize=True)

# ---------- sparkfeed.jpg：快讯邮件卡片模拟 ----------
im, d = canvas(); frame(d)
f22, f26, f34 = font(22), font(26), font(34, True)
d.text((80, 86), '火花快讯', font=f34, fill=INK)
d.text((80 + d.textlength('火花快讯', font=f34) + 16, 98), '2026-10-30 · 3 个点子', font=f26, fill=MUTED)
d.line([80, 160, W - 80, 160], fill=LINE, width=2)
cards = [
    ('① 基于 RAG 管线模板的垂直问答 SaaS', '订阅 $9/月', 78),
    ('② 老龄化社区的健康提醒小程序', '流量主 + 增值', 84),
    ('③ 面向独立开发者的合规清单工具', '付费模板', 75),
]
y = 190
for title, rev, score in cards:
    d.rounded_rectangle([80, y, W - 80, y + 128], radius=14, fill=SURFACE, outline=LINE, width=2)
    d.text((108, y + 22), title, font=f26, fill=INK)
    d.text((108, y + 74), f'变现路径: {rev}', font=f22, fill=MUTED)
    sw = d.textlength(f'火花分 {score}', font=f22) + 28
    d.rounded_rectangle([W - 108 - sw, y + 68, W - 108, y + 110], radius=20, outline=ACCENT, width=2)
    d.text((W - 108 - sw + 14, y + 78), f'火花分 {score}', font=f22, fill=ACCENT)
    y += 150
d.text((80, H - 78), '每日 08:30 · 五源情报 · LLM 合成 · 邮件送达', font=f22, fill=MUTED)
im.save(f'{OUT}/sparkfeed.jpg', quality=88, optimize=True)

# ---------- quant.jpg：双基准曲线 ----------
im, d = canvas(); frame(d)
f22, f26 = font(22), font(26)
d.text((80, 80), '策略 vs 中证500 vs 沪深300', font=f26, fill=INK)
d.text((80, 124), '近 12 个月 · 真实成本回测', font=f22, fill=MUTED)
x0, y0, x1, y1 = 90, 200, W - 90, H - 110
d.rectangle([x0, y0, x1, y1], fill=SURFACE, outline=LINE, width=2)
for gy in range(1, 4):
    yy = y0 + (y1 - y0) * gy // 4
    d.line([x0, yy, x1, yy], fill=LINE, width=1)
random.seed(42)
def series(base, drift, noise):
    pts, v = [], 0.0
    for i in range(60):
        v += drift + random.uniform(-noise, noise)
        pts.append(v)
    return pts
def draw_series(pts, color, width=4):
    lo, hi = min(pts), max(pts)
    span = max(hi - lo, 1e-6)
    xy = []
    for i, v in enumerate(pts):
        x = x0 + 24 + (x1 - x0 - 48) * i / (len(pts) - 1)
        y = y1 - 20 - (y1 - y0 - 40) * (v - lo) / span
        xy.append((x, y))
    d.line(xy, fill=color, width=width, joint='curve')
draw_series(series(0, 0.55, 0.9), MUTED, 3)
draw_series(series(0, 0.35, 0.8), '#8b949e', 3)
draw_series(series(0, 1.35, 1.0), ACCENT, 5)
lx = x0 + 40
for label, color in [('策略', ACCENT), ('中证500', MUTED), ('沪深300', '#8b949e')]:
    d.line([lx, y0 + 34, lx + 34, y0 + 34], fill=color, width=4)
    d.text((lx + 44, y0 + 22), label, font=f22, fill=MUTED)
    lx += 44 + d.textlength(label, font=f22) + 36
d.text((x0, y1 + 22), '月度调仓 · 买0.13%/卖0.18% · 涨跌停不成交', font=f22, fill=MUTED)
im.save(f'{OUT}/quant.jpg', quality=88, optimize=True)

# ---------- tryon.jpg：抽象流程示意 ----------
im, d = canvas(); frame(d)
f22, f26, f40 = font(22), font(26), font(44, True)
d.text((80, 80), '照片 + 服装 → AI 换装', font=f40, fill=INK)
cy, ch = 210, 300
for i, label in enumerate(['人像照', '服装图']):
    x = 90 + i * 380
    d.rounded_rectangle([x, cy, x + 300, cy + ch], radius=16, fill=SURFACE, outline=LINE, width=2)
    d.ellipse([x + 105, cy + 70, x + 195, cy + 160], outline=MUTED, width=3)
    d.line([x + 150, cy + 160, x + 150, cy + 230], fill=MUTED, width=3)
    d.text((x + (300 - d.textlength(label, font=f26)) / 2, cy + ch + 18), label, font=f26, fill=MUTED)
ax = 90 + 2 * 380 + 30
d.text((ax, cy + 120), '→', font=f40, fill=ACCENT)
d.text((ax - 16, cy + 172), 'IDM-VTON', font=f22, fill=ACCENT)
rx = ax + 110
d.rounded_rectangle([rx, cy, rx + 300, cy + ch], radius=16, outline=ACCENT, width=3)
d.ellipse([rx + 105, cy + 70, rx + 195, cy + 160], outline=ACCENT, width=3)
d.line([rx + 150, cy + 160, rx + 150, cy + 230], fill=ACCENT, width=3)
d.text((rx + (300 - d.textlength('换装效果', font=f26)) / 2, cy + ch + 18), '换装效果', font=f26, fill=ACCENT)
d.text((90, cy + ch + 90), 'Flutter App · Fastify BFF · Replicate · 历史记录存档', font=f22, fill=MUTED)
im.save(f'{OUT}/tryon.jpg', quality=88, optimize=True)

# ---------- personal-page.jpg：终端/代码卡片 ----------
im, d = canvas(); frame(d)
f22, f26, f30 = font(22), font(26), font(30, True)
d.text((80, 80), '这个站本身的源码', font=f30, fill=INK)
x0, y0, x1, y1 = 90, 170, W - 90, H - 120
d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=SURFACE, outline=LINE, width=2)
for i in range(3):
    d.ellipse([x0 + 28 + i * 34, y0 + 22, x0 + 44 + i * 34, y0 + 38], outline=MUTED, width=2)
code = [
    ('$ git push origin main', MUTED),
    ('✔ deploy: astro check → build → pages', INK),
    ('→ https://bailin1125.github.io  live', ACCENT),
    ('', INK),
    ('# 内容即文件：产品与文章都是 Markdown', MUTED),
]
y = y0 + 76
for line, color in code:
    if line: d.text((x0 + 32, y), line, font=f26, fill=color)
    y += 52
d.text((x0, y1 + 24), 'Astro 5 · Tailwind 4 · 零客户端 JS · push 即部署', font=f22, fill=MUTED)
im.save(f'{OUT}/personal-page.jpg', quality=88, optimize=True)

# ---------- unnamed-a/b.jpg：极简字标 ----------
for name, ch in [('unnamed-a', 'A'), ('unnamed-b', 'B')]:
    im, d = canvas(); frame(d)
    f200 = font(220, True)
    tw = d.textlength(ch, font=f200)
    d.text(((W - tw) / 2, H / 2 - 150), ch, font=f200, fill=MUTED)
    f26 = font(26)
    t = '开发中 · 敬请期待'
    d.text(((W - d.textlength(t, font=f26)) / 2, H / 2 + 120), t, font=f26, fill=LINE)
    im.save(f'{OUT}/{name}.jpg', quality=88, optimize=True)

for f_ in ['public/og.png'] + [f'{OUT}/{n}.jpg' for n in ['sparkfeed', 'quant', 'tryon', 'personal-page', 'unnamed-a', 'unnamed-b']]:
    print(f_, os.path.getsize(f_) // 1024, 'KB')
