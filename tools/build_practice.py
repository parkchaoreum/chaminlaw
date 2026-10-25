#!/usr/bin/env python3
"""분야별 안내 페이지(practice-*.html)를 만든다. 내용은 tools/practice_data.py, 
성공사례는 results.html, 칼럼은 blog/index.html 에서 자동으로 가져온다. build_post.py 가 자동 호출."""
import re, json, html, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from practice_data import AREAS
SITE = 'https://www.chaminlaw.com/'

prac = (ROOT / 'practice.html').read_text(encoding='utf-8')
lines = prac.split('\n')
mi, me = prac.index('<main id="main">'), prac.index('</main>')
head_tpl, foot_tpl = prac[:mi], prac[me:]
head_tpl = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head_tpl, flags=re.S)
cta = re.search(r'  <section class="cta".*?</section>\n', prac, re.S).group(0)

# 성공사례
res = (ROOT / 'results.html').read_text(encoding='utf-8')
res_nc = re.sub(r'<!--.*?-->', '', res, flags=re.S)
cases = re.findall(r'(        <article class="case"[^>]*>.*?</article>)', res_nc, re.S)
def case_area(c):
    h = re.search(r'case__h">([^<]*)', c).group(1)
    if re.search(r'추행|강간|촬영|성희롱', h): return 'practice-sexual'
    if re.search(r'교특법|도주치상|음주|운전', h): return 'practice-dui'
    if '형사' in c: return 'practice-criminal'
    return ''

# 칼럼
idx = (ROOT / 'blog/index.html').read_text(encoding='utf-8')
a, b = idx.index('<!-- POSTS:START -->'), idx.index('<!-- POSTS:END -->')
cards = re.findall(r'(        <a class="post" href="([^"]+)">.*?post__tag">([^<]*)</span>.*?</a>\n)', idx[a:b], re.S)
def col_areas(href, tag):
    t = tag.strip(); out = set()
    if '성범죄' in t or 'seonghuirong' in href: out.add('practice-sexual')
    if '음주운전' in t or '교통' in t or 'unjeonja' in href: out.add('practice-dui')
    if t.startswith('형사') and not out: out.add('practice-criminal')
    if t.startswith('이혼'): out.add('practice-divorce')
    if t.startswith('가사'): out.add('practice-family')
    if t.startswith('민사') or t == '형사 · 민사': out.add('practice-civil')
    if t.startswith('학교폭력'): out.add('practice-school')
    if '징계' in t or t.startswith('노동'): out.add('practice-discipline')
    return out

esc = lambda s: html.escape(s, quote=True)
built = []
for ar in AREAS:
    slug = ar['slug']; url = f'{SITE}{slug}.html'
    h = head_tpl
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(ar["title"])}</title>', h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + esc(ar['desc']).replace('\\', r'\\'), h)
    h = h.replace('https://www.chaminlaw.com/practice.html', url)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + esc(ar['title']), h)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + esc(ar['desc']), h)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "업무분야", "item": SITE + "practice.html"},
            {"@type": "ListItem", "position": 3, "name": ar['name'], "item": url}]},
        {"@type": "Service", "name": f"{ar['name']} 법률 상담", "serviceType": ar['name'], "url": url,
         "description": ar['desc'], "areaServed": [{"@type": "City", "name": "군산시"}, {"@type": "AdministrativeArea", "name": "전북특별자치도"}],
         "provider": {"@id": SITE + "#organization", "@type": "LegalService", "name": "법률사무소 차민", "telephone": "+82-63-452-9075", "url": SITE}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": an}} for q, an in ar['faq']]}]}
    h = h.replace('</head>', '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>\n</head>', 1)

    my_cases = sorted([c for c in cases if case_area(c) == slug], key=lambda c: '구속영장 기각' not in c)[:3]  # 구속영장 기각 사례를 앞에
    my_cols = [c.replace('href="', 'href="blog/', 1) for c, hr, tg in cards if slug in col_areas(hr, tg)][:4]
    situ = '\n'.join(f'        <div class="pitem"><p class="pitem__h">{esc(t)}</p><p class="pitem__d">{esc(d)}</p></div>' for t, d in ar['situ'])
    steps = '\n'.join(f'        <li class="step"><p class="step__no">{i+1:02d}</p><h3 class="step__h">{esc(t)}</h3><p class="step__d">{esc(d)}</p></li>' for i, (t, d) in enumerate(ar['steps']))
    faq = '\n'.join(f'''        <div class="faq__item" data-faq>
          <button class="faq__q" type="button" aria-expanded="false" aria-controls="pf-{i}"><span class="faq__q-mark" aria-hidden="true">Q</span><span>{esc(q)}</span><span class="faq__sign" aria-hidden="true"></span></button>
          <div class="faq__a" id="pf-{i}"><div class="faq__a-inner">{esc(an)}</div></div>
        </div>''' for i, (q, an) in enumerate(ar['faq'], 1))
    case_sec = ''
    if my_cases:
        case_sec = f'''
  <section class="sec sec--paper">
    <div class="wrap">
      <p class="eyebrow">Results</p>
      <h2 class="sec-title">{esc(ar['name'])} 성공사례</h2>
      <div class="cases parea__cases">
{chr(10).join(my_cases)}
      </div>
      <p class="parea__more"><a class="ilink" href="results.html">성공사례 전체 보기 →</a></p>
    </div>
  </section>
'''
    col_sec = ''
    if my_cols:
        col_sec = f'''
  <section class="sec sec--paper2">
    <div class="wrap">
      <p class="eyebrow">Columns</p>
      <h2 class="sec-title">{esc(ar['name'])} 관련 법률 칼럼</h2>
      <div class="posts parea__posts">
{''.join(my_cols)}      </div>
      <p class="parea__more"><a class="ilink" href="blog/{ar['blogq']}">관련 칼럼 더 보기 →</a></p>
    </div>
  </section>
'''
    topic_sec = ''
    if ar.get('topics'):
        items = []
        for t, d, links in ar['topics']:
            lk = ' '.join(f'<a class="ilink" href="{h}">{esc(l)} →</a>' for h, l in links)
            items.append(f'        <div class="pitem"><h3 class="pitem__h">{esc(t)}</h3><p class="pitem__d">{esc(d)}</p>' + (f'<p class="pitem__d">{lk}</p>' if lk else '') + '</div>')
        topic_sec = f'''
  <section class="sec sec--paper sec--divided">
    <div class="wrap">
      <p class="eyebrow">By Offense</p>
      <h2 class="sec-title">죄명별 안내</h2>
      <div class="pitems parea__situ">
{chr(10).join(items)}
      </div>
    </div>
  </section>
'''
    others = ' '.join(f'<a class="parea__chip" href="{o["slug"]}.html">{esc(o["name"])}</a>' for o in AREAS if o is not ar)
    main = f'''<main id="main">
  <section class="phero">
    <div class="phero__field" aria-hidden="true"></div>
    <div class="wrap">
      <nav class="crumb" aria-label="현재 위치">
        <a href="index.html">홈</a><span class="crumb__sep" aria-hidden="true">/</span>
        <a href="practice.html">업무분야</a><span class="crumb__sep" aria-hidden="true">/</span>
        <span aria-current="page">{esc(ar['name'])}</span>
      </nav>
      <p class="phero__en">{ar['en']}</p>
      <h1 class="phero__title">{esc(ar.get('h1kw', ar['h1']))}</h1>
      <p class="phero__sub">{esc(ar['h1'])}</p>
    </div>
  </section>

  <section class="sec sec--paper sec--list">
    <div class="wrap">
      <p class="eyebrow">Overview</p>
      <h2 class="sec-title">이런 상황이라면 상담이 필요합니다</h2>
      <p class="sec-lead">{esc(ar['lead'])}</p>
      <div class="pitems parea__situ">
{situ}
      </div>
    </div>
  </section>

{topic_sec}  <section class="sec sec--paper2">
    <div class="wrap">
      <p class="eyebrow">Process</p>
      <h2 class="sec-title">사건은 이렇게 진행됩니다</h2>
      <ol class="steps">
{steps}
      </ol>
    </div>
  </section>
{case_sec}{col_sec}
  <section class="sec sec--paper">
    <div class="wrap parea__narrow">
      <p class="eyebrow">FAQ</p>
      <h2 class="sec-title">자주 묻는 질문</h2>
      <div class="faq parea__faq">
{faq}
      </div>
      <div class="parea__others">
        <p class="parea__others-h">다른 분야 보기</p>
        <div class="parea__chips">{others}</div>
      </div>
    </div>
  </section>

{cta}'''
    (ROOT / f'{slug}.html').write_text(h + main + foot_tpl, encoding='utf-8')
    built.append((slug, ar['name'], ar['kw'], len(my_cases), len(my_cols)))

# 업무분야 허브: 분야별 안내 타일
tile_list = [(f'{ar["slug"]}.html', ar['name']) for ar in AREAS] + [('#corporate', '기업 자문')]
tiles = '\n'.join(f'          <a class="parea-tile" href="{h}"><span class="parea-tile__n">{i+1:02d}</span><span class="parea-tile__h">{esc(n)}</span><span class="parea-tile__go" aria-hidden="true">→</span></a>' for i, (h, n) in enumerate(tile_list))
hub = f'''      <!-- PAREA:START -->
      <nav class="parea-tiles" aria-label="분야별 안내">
{tiles}
      </nav>
      <!-- PAREA:END -->
'''
if '<!-- PAREA:START -->' in prac:
    prac = re.sub(r'      <!-- PAREA:START -->.*?<!-- PAREA:END -->\n', hub, prac, flags=re.S)
else:
    prac = prac.replace('      <div class="pdetail">', hub + '\n      <div class="pdetail">', 1)
# 각 업무 블록에 '자세히' 링크
link_map = {'criminal': [('practice-criminal', '일반형사·군형사'), ('practice-sexual', '성범죄'), ('practice-dui', '음주운전·교통')],
            'divorce': [('practice-divorce', '이혼·상간')], 'school': [('practice-school', '학교폭력')]}
for bid in re.findall(r'<article class="pblock reveal" id="([a-z]+)">', prac):
    pass
def add_links(m):
    bid, body = m.group(1), m.group(2)
    blk = re.search(r'<h2 class="pblock__h">([^<]*)</h2>', body).group(1)
    names = {a['name']: a['slug'] for a in AREAS}
    targets = [(names[blk.strip()], blk.strip().replace(' · ', '·') + ' 자세히')] if blk.strip() in names else []
    body = re.sub(r'\n            <p class="pblock__links">.*?</p>', '', body, flags=re.S)
    if targets:
        links = ' '.join(f'<a class="ilink" href="{s}.html">{t} →</a>' for s, t in targets)
        body = re.sub(r'(</p>\n          </div>\n          <div class="pitems">)', '</p>\n            <p class="pblock__links">' + links + r'</p>\n          </div>\n          <div class="pitems">', body, count=1) if False else body.replace(
            '\n          </div>\n          <div class="pitems">', f'\n            <p class="pblock__links">{links}</p>\n          </div>\n          <div class="pitems">', 1)
    return f'<article class="pblock reveal" id="{bid}">{body}</article>'
prac = re.sub(r'<article class="pblock reveal" id="([a-z]+)">(.*?)</article>', add_links, prac, flags=re.S)
(ROOT / 'practice.html').write_text(prac, encoding='utf-8')

# 사이트맵
sm_p = ROOT / 'sitemap.xml'; sm = sm_p.read_text(encoding='utf-8')
for slug, *_ in built:
    loc = f'{SITE}{slug}.html'
    if loc not in sm:
        sm = sm.replace('</urlset>', f'  <url>\n    <loc>{loc}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n</urlset>')
sm_p.write_text(sm, encoding='utf-8')
for x in built: print(x)
