#!/usr/bin/env python3
"""칼럼 1편을 blog/_template.html 로 생성하고, 목록(날짜 내림차순)과 사이트맵을 갱신한다.
usage: build_post.py <spec.json>
spec 키: slug, date(YYYY-MM-DD), title, seo_title, desc, card_desc, category, author,
        city(예: 익산시), lead, body(HTML), faq[[q,a]x3], cover(선택: images/... 경로)
"""
import json, re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
tpl  = (ROOT / 'blog/_template.html').read_text(encoding='utf-8')

y, m, d = spec['date'].split('-')
date_k = f'{int(y)}. {int(m)}. {int(d)}.'
J = lambda s: json.dumps(s, ensure_ascii=False)[1:-1]          # JSON 문자열 안전 처리

out = tpl
out = re.sub(r'<!-- 이 파일은 새 글의 원본 틀입니다.*?-->\n', '', out, flags=re.S)
out = out.replace('<meta name="robots" content="noindex, nofollow">\n', '')
out = re.sub(r'"spatialCoverage": \[.*?\]',
             f'"spatialCoverage": {{ "@type": "City", "name": "{spec["city"]}" }}', out, flags=re.S)
out = out.replace('<title>{{제목}} | 법률사무소 차민</title>', f'<title>{html.escape(spec["seo_title"])}</title>')

# JSON-LD 블록 안의 자리표시는 JSON 이스케이프로, 나머지는 HTML 그대로
ld_start = out.index('<script type="application/ld+json">'); ld_end = out.index('</script>', ld_start)
ld = out[ld_start:ld_end]
rep_ld = {'{{제목}}': J(spec['title']), '{{150자 요약}}': J(spec['desc']), '{{파일명}}': spec['slug'],
          '{{YYYY-MM-DD}}': spec['date'], '{{변호사 성함}}': J(spec['author']), '{{분야}}': J(spec['category'])}
for i, (q, a) in enumerate(spec['faq'], 1):
    rep_ld[f'{{{{질문{i}}}}}'] = J(q); rep_ld[f'{{{{답{i}}}}}'] = J(a)
for k, v in rep_ld.items(): ld = ld.replace(k, v)
out = out[:ld_start] + ld + out[ld_end:]

rep = {"{{150자 요약 — 반드시 '군산' 포함}}": html.escape(spec['desc']), '{{150자 요약}}': html.escape(spec['desc']),
       '{{제목}}': spec['title'], '{{파일명}}': spec['slug'], '{{YYYY-MM-DD}}': spec['date'],
       '{{YYYY. MM. DD.}}': date_k, '{{변호사 성함}}': spec['author'], '{{분야}}': spec['category'],
       '{{첫 문단 — 군산 + 분야 + 이 글이 답하는 질문 한 줄}}': spec['lead'], '{{본문}}': spec['body'].strip()}
for i, (q, a) in enumerate(spec['faq'], 1):
    rep[f'{{{{질문{i}}}}}'] = q; rep[f'{{{{답{i}}}}}'] = a
for k, v in rep.items(): out = out.replace(k, v)

if spec.get('cover'):
    url = 'https://www.chaminlaw.com/' + spec['cover']
    out = out.replace('https://www.chaminlaw.com/images/og-cover.jpg', url)

left = re.findall(r'\{\{[^}]+\}\}', out)
assert not left, left
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S): json.loads(b)
(ROOT / f'blog/{spec["slug"]}.html').write_text(out, encoding='utf-8')

# ---- 목록: 기존 카드 + 새 카드, 날짜 내림차순 ----
idx_p = ROOT / 'blog/index.html'; idx = idx_p.read_text(encoding='utf-8')
a, b = idx.index('<!-- POSTS:START -->') + len('<!-- POSTS:START -->'), idx.index('        <!-- POSTS:END -->')
cards = re.findall(r'        <a class="post" href="[^"]+">.*?</a>\n', idx[a:b], re.S)
cards = [c for c in cards if f'href="{spec["slug"]}.html"' not in c]
cards.append(f'''        <a class="post" href="{spec["slug"]}.html">
          <div class="post__meta"><span class="post__tag">{spec["category"]}</span><time datetime="{spec["date"]}">{date_k}</time></div>
          <h2 class="post__h">{spec["title"]}</h2>
          <p class="post__d">{spec["card_desc"]}</p>
        </a>
''')
cards.sort(key=lambda c: re.search(r'datetime="([\d-]+)"', c).group(1), reverse=True)
idx = idx[:a] + '\n' + ''.join(cards) + idx[b:]
idx_p.write_text(idx, encoding='utf-8')

# ---- 사이트맵 ----
sm_p = ROOT / 'sitemap.xml'; sm = sm_p.read_text(encoding='utf-8')
loc = f'https://www.chaminlaw.com/blog/{spec["slug"]}.html'
if loc in sm:
    sm = re.sub(rf'(<loc>{re.escape(loc)}</loc>\s*<lastmod>)[\d-]+', rf'\g<1>{spec["date"]}', sm)
else:
    sm = sm.replace('</urlset>', f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{spec["date"]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>''')
sm_p.write_text(sm, encoding='utf-8')
print('built', spec['slug'], date_k, '| cards:', len(cards))

# ---- 검색 색인 ----
import subprocess
subprocess.run([sys.executable, str(ROOT / 'tools/build_search_index.py')], check=True)
subprocess.run([sys.executable, str(ROOT / 'tools/build_rss.py')], check=True)
subprocess.run([sys.executable, str(ROOT / "tools/build_llms.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "tools/make_cover.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "tools/apply_covers.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "tools/build_crosslinks.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "tools/build_practice.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "tools/build_guide.py")], check=True)
