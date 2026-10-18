#!/usr/bin/env python3
"""blog/*.html 본문을 모아 칼럼 검색용 blog/search-index.json 을 만든다. build_post.py 가 자동 호출."""
import json, re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = []
for f in sorted((ROOT / 'blog').glob('*.html')):
    if f.name in ('index.html',) or f.name.startswith('_'):
        continue
    s = f.read_text(encoding='utf-8')
    m = re.search(r'<article class="article[^"]*">(.*?)<aside class="office-box"', s, re.S)
    if not m:
        continue
    body = re.sub(r'<(script|style)\b.*?</\1>', ' ', m.group(1), flags=re.S)
    body = re.sub(r'<span class="faq__q-mark"[^>]*>.*?</span>', ' ', body, flags=re.S)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    text = re.sub(r'\s+', ' ', text).strip()
    title = html.unescape(re.search(r'<h1 class="phero__title">(.*?)</h1>', s, re.S).group(1)).strip()
    out.append({'u': f.name, 't': title, 'x': text})
(ROOT / 'blog/search-index.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print('search index:', len(out), 'posts')
