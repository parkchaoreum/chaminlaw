#!/usr/bin/env python3
"""키워드별 안내 페이지(guide-*.html)와 허브(guide.html)를 만든다.
내용은 tools/guide_data.py. 레이아웃(머리말·바닥글·상담 CTA)은 practice.html 에서 가져온다.
페이지마다 고유한 설명·쟁점·절차·FAQ를 쓰고, 관련 칼럼으로 연결한다(키워드만 바꾼 복제 페이지 금지)."""
import re, json, html, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from guide_data import GUIDES
SITE = 'https://www.chaminlaw.com/'
esc = lambda s: html.escape(s, quote=True)

prac = (ROOT / 'practice.html').read_text(encoding='utf-8')
mi, me = prac.index('<main id="main">'), prac.index('</main>')
head_tpl, foot_tpl = prac[:mi], prac[me:]
head_tpl = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head_tpl, flags=re.S)
cta = re.search(r'  <section class="cta".*?</section>\n', prac, re.S).group(0)

idx = (ROOT / 'blog' / 'index.html').read_text(encoding='utf-8')
a, b = idx.find('POSTS:START'), idx.find('POSTS:END')
cards = {re.search(r'href="([^"]+)\.html"', c).group(1): c for c in re.findall(r'        <a class="post" href="[^"]+">.*?</a>\n', idx[a:b], re.S)}

def head_for(title, desc, url):
    h = head_tpl
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), h)
    h = h.replace('https://www.chaminlaw.com/practice.html', url)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(title), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(desc), h)
    return h

def phero(crumbs, en, h1):
    c = '<span class="crumb__sep" aria-hidden="true">/</span>'.join(
        f'<a href="{u}">{esc(t)}</a>' if u else f'<span aria-current="page">{esc(t)}</span>' for t, u in crumbs)
    return f'''<main id="main">
  <section class="phero">
    <div class="phero__field" aria-hidden="true"></div>
    <div class="wrap">
      <nav class="crumb" aria-label="현재 위치">
        {c}
      </nav>
      <p class="phero__en">{en}</p>
      <h1 class="phero__title">{esc(h1)}</h1>
    </div>
  </section>
'''

groups = {}
for g in GUIDES:
    groups.setdefault(g['group'], []).append(g)

built = []
for g in GUIDES:
    url = f'{SITE}{g["slug"]}.html'
    h = head_for(g['title'], g['desc'], url)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "키워드별 안내", "item": SITE + "guide.html"},
            {"@type": "ListItem", "position": 3, "name": g['kw'], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": an}} for q, an in g['faq']]}]}
    h = h.replace('</head>', '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>\n</head>', 1)

    info = '\n'.join(f'          <tr><th scope="row">{esc(k)}</th><td>{v if "<a " in v else esc(v)}</td></tr>' for k, v in g['info'])
    intro = '\n'.join(f'      <p class="ginfo__p">{esc(p)}</p>' for p in g['intro'])
    points = '\n'.join(f'        <div class="pitem"><h3 class="pitem__h">{esc(t)}</h3><p class="pitem__d">{esc(d)}</p></div>' for t, d in g['points'])
    steps = '\n'.join(f'        <li class="step"><p class="step__no">{i+1:02d}</p><h3 class="step__h">{esc(t)}</h3><p class="step__d">{esc(d)}</p></li>' for i, (t, d) in enumerate(g['steps']))
    cols = ''.join(cards[c].replace('href="', 'href="blog/', 1) for c in g['cols'] if c in cards)
    faq = '\n'.join(f'''        <div class="faq__item" data-faq>
          <button class="faq__q" type="button" aria-expanded="false" aria-controls="gf-{i}"><span class="faq__q-mark" aria-hidden="true">Q</span><span>{esc(q)}</span><span class="faq__sign" aria-hidden="true"></span></button>
          <div class="faq__a" id="gf-{i}"><div class="faq__a-inner">{esc(an)}</div></div>
        </div>''' for i, (q, an) in enumerate(g['faq'], 1))
    sib = ' '.join(f'<a class="parea__chip" href="{o["slug"]}.html">{esc(o["kw"])}</a>' for o in groups[g['group']] if o is not g)
    col_sec = f'''
  <section class="sec sec--paper2">
    <div class="wrap">
      <p class="eyebrow">Columns</p>
      <h2 class="sec-title">{esc(g['kw'])} 관련 법률 칼럼</h2>
      <div class="posts parea__posts">
{cols}      </div>
    </div>
  </section>
''' if cols else ''
    main = phero([('홈', 'index.html'), ('키워드별 안내', 'guide.html'), (g['kw'], None)], 'Guide', g['h1']) + f'''
  <section class="sec sec--paper sec--list">
    <div class="wrap parea__narrow">
      <table class="ginfo">
        <tbody>
{info}
        </tbody>
      </table>
{intro}
    </div>
  </section>

  <section class="sec sec--paper2">
    <div class="wrap">
      <p class="eyebrow">Issues</p>
      <h2 class="sec-title">이 사건에서 쟁점이 되는 것</h2>
      <div class="pitems parea__situ">
{points}
      </div>
    </div>
  </section>

  <section class="sec sec--paper">
    <div class="wrap">
      <p class="eyebrow">Process</p>
      <h2 class="sec-title">사건은 이렇게 진행됩니다</h2>
      <ol class="steps">
{steps}
      </ol>
    </div>
  </section>
{col_sec}
  <section class="sec sec--paper">
    <div class="wrap parea__narrow">
      <p class="eyebrow">FAQ</p>
      <h2 class="sec-title">자주 묻는 질문</h2>
      <div class="faq parea__faq">
{faq}
      </div>
      <div class="parea__others">
        <p class="parea__others-h">{esc(g['group'])} 다른 안내</p>
        <div class="parea__chips">{sib} <a class="parea__chip" href="guide.html">키워드별 안내 전체</a></div>
      </div>
    </div>
  </section>

{cta}'''
    (ROOT / f'{g["slug"]}.html').write_text(h + main + foot_tpl, encoding='utf-8')
    built.append(g['slug'])

# 허브
hub_title = '키워드별 안내 — 군산 형사·성범죄·이혼·상속·민사 | 법률사무소 차민'
hub_desc = '군산에서 많이 찾는 법률 문제를 키워드별로 모았습니다. 각 안내에서 쟁점, 진행 순서, 관할, 관련 칼럼과 자주 묻는 질문을 확인하실 수 있습니다.'
h = head_for(hub_title, hub_desc, SITE + 'guide.html')
secs = []
for grp, items in groups.items():
    chips = '\n'.join(f'          <a class="gchip" href="{o["slug"]}.html"><span>{esc(o["kw"])}</span><span aria-hidden="true">→</span></a>' for o in items)
    secs.append(f'''      <h2 class="ghub__h">{esc(grp)}</h2>
      <div class="ghub__chips">
{chips}
      </div>''')
main = phero([('홈', 'index.html'), ('키워드별 안내', None)], 'Guide', '키워드별 안내') + f'''
  <section class="sec sec--paper sec--list">
    <div class="wrap">
      <p class="sec-lead">군산에서 많이 찾는 법률 문제를 키워드별로 모았습니다. 각 안내에서 쟁점과 진행 순서, 관할, 관련 칼럼을 확인하실 수 있습니다.</p>
{chr(10).join(secs)}
    </div>
  </section>

{cta}'''
(ROOT / 'guide.html').write_text(h + main + foot_tpl, encoding='utf-8')

# sitemap
sm_p = ROOT / 'sitemap.xml'
sm = sm_p.read_text(encoding='utf-8')
import datetime
today = datetime.date.today().isoformat()
for slug in ['guide'] + built:
    loc = f'{SITE}{slug}.html'
    if f'<loc>{loc}</loc>' not in sm:
        sm = sm.replace('</urlset>', f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n</urlset>')
sm_p.write_text(sm, encoding='utf-8')
print('guides:', len(built))
