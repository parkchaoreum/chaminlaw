#!/usr/bin/env python3
"""칼럼 대표 썸네일(정사각형 JPG)을 만든다. 문구는 tools/cover_text.json (slug: [분야, 주제, 요약]).
usage: make_cover.py [slug ...]   (생략하면 이미지가 없는 칼럼 전부)"""
import json, sys, pathlib, html
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT = json.loads((ROOT / 'tools/cover_text.json').read_text(encoding='utf-8'))
import base64
LOGO = 'data:image/png;base64,' + base64.b64encode((ROOT / 'images/blog/cover-logo.png').read_bytes()).decode()
def out_path(slug):
    return ROOT / 'images/blog' / ('20261016-damages-cover.jpg' if slug == '20261016-gunsan-sonhaebaesang' else f'{slug}-cover.jpg')
TPL = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
html,body{margin:0;width:1254px;height:1254px;overflow:hidden}
body{position:relative;font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif;background:radial-gradient(ellipse at 40% 30%,#fff 0%,#f4f6fb 60%,#e9edf6 100%)}
svg.bg{position:absolute;left:0;top:0}
.t{position:absolute;left:0;width:1254px;text-align:center;white-space:nowrap}
.field{top:285px;font-size:262px;font-weight:900;color:#0c1b5a;letter-spacing:-8px;line-height:1.1}
.rule{position:absolute;left:157px;width:960px;top:625px;border-top:2px solid #0c1b5a}
.dot{position:absolute;left:615px;top:617px;width:18px;height:18px;border-radius:50%;background:#0c1b3a;box-shadow:0 0 0 8px #f4f6fb}
.topic{top:672px;font-size:112px;font-weight:800;color:#0a3fa5;letter-spacing:-3px;line-height:1.15}
.sum{top:790px;font-size:112px;font-weight:800;color:#222;letter-spacing:-3px;line-height:1.15}
.logo{position:absolute;left:477px;top:935px;width:300px;height:255px}
.frame{position:absolute;inset:0;border:20px solid #0c1b4f;box-sizing:border-box}
</style></head><body>
<svg class="bg" width="1254" height="1254" viewBox="0 0 1254 1254" xmlns="http://www.w3.org/2000/svg"><defs>
<filter id="b"><feGaussianBlur stdDeviation="3"/></filter>
<linearGradient id="bl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a5be0"/><stop offset="1" stop-color="#062a86"/></linearGradient>
<linearGradient id="bl2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0646b8"/><stop offset="1" stop-color="#031b5c"/></linearGradient></defs>
<g filter="url(#b)" opacity="0.22" fill="none" stroke="#6f8fcf" stroke-width="10" stroke-linecap="round">
<path d="M1050 130 L1050 190 M1030 190 L1070 190 L1060 240 L1040 240 Z" fill="#9db4e0"/>
<path d="M1020 250 L1080 250 L1070 880 L1030 880 Z" fill="#b9c9ea" stroke="none"/>
<ellipse cx="1050" cy="880" rx="150" ry="40" fill="#b9c9ea" stroke="none"/><ellipse cx="1050" cy="905" rx="190" ry="35" fill="#a9bde6" stroke="none"/>
<path d="M790 250 Q900 190 1050 240 Q1180 195 1254 190" stroke-width="22"/>
<path d="M815 270 L720 640 M815 270 L900 640" stroke-width="5"/><path d="M670 650 Q800 760 940 650 Z" fill="#b9c9ea"/>
<path d="M1254 470 L1180 690 M1254 470 L1254 690" stroke-width="5"/><path d="M1130 690 Q1230 770 1254 700 Z" fill="#b9c9ea"/></g>
<path d="M0 705 C140 940 360 1120 560 1254 L0 1254 Z" fill="url(#bl)"/><path d="M0 980 C140 1060 330 1180 450 1254 L0 1254 Z" fill="url(#bl2)"/>
<path d="M0 705 C140 940 360 1120 560 1254" fill="none" stroke="#fff" stroke-width="3" opacity="0.7"/></svg>
<div class="t field">{F}</div><div class="rule"></div><div class="dot"></div>
<div class="t topic">{T}</div><div class="t sum">{S}</div>
<img class="logo" src="{LOGO}"><div class="frame"></div>
<script>
function fit(sel,max){var e=document.querySelector(sel),s=parseFloat(getComputedStyle(e).fontSize),r=document.createRange();
 while(true){r.selectNodeContents(e);var w=r.getBoundingClientRect().width;if(w<=max||s<40)break;s-=4;e.style.fontSize=s+'px';}
 return s}
var fs=fit('.field',1000); var d=262-fs; if(d>0){document.querySelector('.field').style.top=(285+d*0.55)+'px'}
fit('.topic',1060); fit('.sum',1060);
</script></body></html>'''
def main(slugs):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = b.new_page(viewport={'width': 1254, 'height': 1254})
        tmp = ROOT / 'tools/.cover_tmp.png'
        for s in slugs:
            f, t, su = TEXT[s]
            doc = TPL.replace('{F}', html.escape(f)).replace('{T}', html.escape(t)).replace('{S}', html.escape(su)).replace('{LOGO}', LOGO)
            pg.set_content(doc); pg.wait_for_timeout(150)
            pg.screenshot(path=str(tmp))
            from PIL import Image
            Image.open(tmp).convert('RGB').resize((1000, 1000), Image.LANCZOS).save(out_path(s), quality=84, optimize=True, progressive=True)
            print('cover', s)
        tmp.unlink(missing_ok=True); b.close()
if __name__ == '__main__':
    args = sys.argv[1:] or [s for s in TEXT if not out_path(s).exists()]
    main(args)
