#!/usr/bin/env python3
"""각 칼럼에 대표 썸네일을 붙인다: 본문 첫 문단 아래 이미지 + og:image·twitter:image·구조화 데이터 image. build_post.py 가 자동 호출."""
import re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://www.chaminlaw.com/'
n = 0
for f in sorted((ROOT / 'blog').glob('*.html')):
    if f.name == 'index.html' or f.name.startswith('_'):
        continue
    slug = f.stem
    rel = 'images/blog/' + ('20261016-damages-cover.jpg' if slug == '20261016-gunsan-sonhaebaesang' else f'{slug}-cover.jpg')
    if not (ROOT / rel).exists():
        continue
    s = f.read_text(encoding='utf-8'); o = s
    url = SITE + rel
    s = s.replace(SITE + 'images/og-cover.jpg', url)
    s = re.sub(r'(<meta property="og:image:width" content=")\d+', r'\g<1>1000', s)
    s = re.sub(r'(<meta property="og:image:height" content=")\d+', r'\g<1>1000', s)
    title = html.unescape(re.search(r'<h1 class="phero__title">(.*?)</h1>', s, re.S).group(1)).strip()
    if 'article__cover' not in s:
        fig = f'\n\n        <figure class="article__cover"><img src="../{rel}" alt="{html.escape(title)}" width="1000" height="1000"></figure>'
        s = re.sub(r'(<p class="article__lead">.*?</p>)', lambda m: m.group(1) + fig, s, count=1, flags=re.S)
    if s != o:
        f.write_text(s, encoding='utf-8'); n += 1
print('covers applied:', n)
