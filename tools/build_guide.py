#!/usr/bin/env python3
"""키워드별 안내 페이지(guide-*.html)와 허브(guide.html)를 만든다.
내용은 tools/guide_data.py. 레이아웃(머리말·바닥글·상담 CTA)은 practice.html 에서 가져온다.
페이지마다 고유한 설명·쟁점·절차·FAQ를 쓰고, 관련 칼럼으로 연결한다(키워드만 바꾼 복제 페이지 금지)."""
import re, json, html, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from guide_data import GUIDES, CITIES, LABELS, tag_group, GROUP_ORDER, KEYMAP
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
    h = h.replace('<a class="hdr__link" href="practice.html" aria-current="page">업무분야</a>', '<a class="hdr__link" href="practice.html">업무분야</a>')
    h = h.replace('<li><a class="hdr__link" href="blog/">법률 칼럼</a></li>', '<li><a class="hdr__link" href="blog/">법률 칼럼</a></li>\n        <li><a class="hdr__link" href="guide.html" aria-current="page">지역별 안내</a></li>', 1)
    return h

def phero(crumbs, en, h1, sub=None):
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
      <h1 class="phero__title">{esc(h1)}</h1>{f'''
      <p class="phero__sub">{esc(sub)}</p>''' if sub else ''}
    </div>
  </section>
'''

groups = {}
for g in GUIDES:
    groups.setdefault((g.get('city', 'gunsan'), g['group']), []).append(g)

# 검색 결과 제목: 이 페이지를 가리키는 군산 키워드를 '군산○○변호사'로 붙여 앞에 둔다.
FIELD = {'형사': 'CRIM', '성범죄': '성범죄전문', '음주운전·교통': '교통사고전문', '이혼·상간': '이혼전문',
         '상속·가사': '상속전문', '민사·부동산': '민사전문', '학교폭력': '학교폭력전문', '노동·징계': '노동전문'}
kw_for = {}
for grp, items in KEYMAP.items():
    for kw, tgt in items:
        if tgt and tgt.startswith('guide-'):
            kw_for.setdefault(tgt[:-5], []).append(kw)
# '○○전문변호사'가 어색한 절차·제도 키워드는 전문 표기를 붙이지 않는다.
AWKWARD = {'경찰조사', '피의자', '공소청조사', '검찰조사', '구속적부심', '보석', '압수수색', '무혐의', '기소유예',
           '집행유예', '약식명령', '정식재판청구', '항소심', '형사항소심', '형사합의', '형사공탁', '고소대리', '범죄피해자', '피해자',
           '불송치이의신청', '거짓말탐지기', '성범죄피의자', '성범죄피해자', '성범죄고소', '성범죄무혐의', '성범죄뒤늦은고소',
           '성범죄구속', '성범죄집행유예', '성범죄항소심', '성범죄무고', '신상정보등록', '음주운전경찰조사', '면허취소행정심판',
           '이혼조정', '이혼후재산분할', '과거양육비', '양육비청구', '유언효력', '강제집행정지', '민사조정', '학폭위',
           '학폭행정심판', '학폭가해학생', '학폭피해학생', '공무원감사', 'SNS계정정지', '대포통장', '내용증명', '원상회복',
           '임대차갱신', '영장실질심사', '구속영장', '면허취소', '유언장', '친권', '면접교섭'}
def key_words(g):
    """(도시명, 대표 키워드 목록[공백 없는 기본형]) — 군산은 KEYMAP, 다른 지역은 kw 에서."""
    city = g.get('city', 'gunsan')
    if city == 'gunsan':
        kws = [re.sub(r'\s+', '', k)[:-3] if k.endswith('변호사') else re.sub(r'\s+', '', k) for k in kw_for.get(g['slug'], [])]
        if not kws: kws = [re.sub(r'[\s·]+|\(.*?\)', '', g['kw'].split(' ', 1)[1])]
        return '군산', kws
    name, rest = g['kw'].split(' ', 1)
    kws = [re.sub(r'[\s·]+', '', re.sub(r'\(.*?\)', '', rest))]
    m = re.search(r'\((.*?)\)', rest)
    if m: kws.append(m.group(1))
    return name, kws
def pro_word(city, base):
    return None if base in AWKWARD else city + base + '전문변호사'
def h1_for(g):
    city, kws = key_words(g)
    pw = pro_word(city, kws[0])
    if pw: return f'{city}{kws[0]}변호사 · {pw}'
    if len(kws) > 1: return f'{city}{kws[0]}변호사 · {city}{kws[1]}변호사'
    return f'{city}{kws[0]}변호사'

crim_n = 0
def seo_title(g):
    global crim_n
    city = g.get('city', 'gunsan')
    if city != 'gunsan':
        cname = g['kw'].split(' ', 1)[0]
        base = re.sub(r'\(.*?\)', '', g['kw'].split(' ', 1)[1])
        words = [cname + re.sub(r'[\s·]+', '', base) + '변호사']
        m = re.search(r'\((.*?)\)', g['kw'])
        if m: words.append(cname + m.group(1) + '변호사')
        f = FIELD[g['group']]
        if f == 'CRIM':
            f = '형사전문' if crim_n % 2 == 0 else '경찰출신'; crim_n += 1
        if '음주' in g['kw']: f = '음주운전전문'
        pw = pro_word(cname, key_words(g)[1][0])
        if pw: words.insert(1, pw)
        words.append(cname + f + '변호사')
        return '·'.join(words) + ' | ' + g['title'].split(' — ', 1)[-1]
    kws = kw_for.get(g['slug'])
    if not kws: return g['title']
    words = ['군산' + re.sub(r'\s+', '', k) + ('' if k.endswith('변호사') else '변호사') for k in kws][:3]
    f = FIELD[g['group']]
    if f == 'CRIM':
        f = '형사전문' if crim_n % 2 == 0 else '경찰출신'; crim_n += 1
    if g['group'] == '음주운전·교통' and any('음주' in k or '면허' in k for k in kws): f = '음주운전전문'
    pw = pro_word('군산', key_words(g)[1][0])
    if pw: words.insert(1, pw)
    fw = '군산' + f + '변호사'
    if fw not in words: words.append(fw)
    tail = g['title'].split(' — ', 1)[-1]
    return '·'.join(words) + ' | ' + tail

built = []
for g in GUIDES:
    url = f'{SITE}{g["slug"]}.html'
    h = head_for(seo_title(g), g['desc'], url)
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
    sib = ' '.join(f'<a class="parea__chip" href="{o["slug"]}.html">{esc(o["kw"])}</a>' for o in groups[(g.get('city', 'gunsan'), g['group'])] if o is not g)
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
    main = phero([('홈', 'index.html'), ('지역별 안내', 'guide.html'), (g['kw'], None)], 'Guide', h1_for(g), g['h1']) + f'''
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
        <div class="parea__chips">{sib} <a class="parea__chip" href="guide.html">지역별 안내 전체</a></div>
      </div>
    </div>
  </section>

{cta}'''
    (ROOT / f'{g["slug"]}.html').write_text(h + main + foot_tpl, encoding='utf-8')
    built.append(g['slug'])

# 허브: 지역별 안내 (도시별 아코디언)
def chip_label(city, kw):
    k = re.sub(r'\s+', '', kw)
    if k.startswith(city): k = k[len(city):]
    return city + k + ('' if k.endswith('변호사') else '변호사')

import json as _j
cover = _j.loads((ROOT / 'tools' / 'cover_text.json').read_text(encoding='utf-8'))
tags = dict(re.findall(r'<a class="post" href="([^"]+)\.html">.*?post__tag">([^<]*)</span>', idx[a:b] if False else idx[idx.find('POSTS:START'):idx.find('POSTS:END')], re.S))
def city_of(slug):
    s2 = re.sub(r'^\d{8}-', '', slug)
    for code, name, *_ in CITIES:
        if s2.startswith(code + '-'): return code
    return None
hub_title = '지역별 안내 — 군산·익산·전주·김제·부안·서천·논산·보령·남원·정읍 | 법률사무소 차민'
hub_desc = '군산, 익산, 전주, 부안, 김제, 서천, 논산, 보령, 남원, 정읍 지역의 형사·성범죄·음주운전·이혼·상속·민사·학교폭력·노동 사건 안내와 관할 법원·공소청·경찰서, 관련 칼럼을 모았습니다.'
h = head_for(hub_title, hub_desc, SITE + 'guide.html')
blocks = []
for code, name, court, police, pros in CITIES:
    groups2 = {}
    used = set()
    if code == 'gunsan':
        for grp, items in KEYMAP.items():
            for kw, tgt in items:
                if not tgt: continue
                groups2.setdefault(grp, []).append((tgt, chip_label(name, kw), not tgt.startswith('blog/')))
                if tgt.startswith('blog/'): used.add(tgt[5:-5])
        for g in GUIDES:   # 군산 안내 페이지에 연결된 칼럼은 칩으로 따로 띄우지 않는다
            if g.get('city', 'gunsan') == 'gunsan': used |= set(g['cols'])
    else:
        for g in GUIDES:
            if g.get('city', 'gunsan') == code:
                used |= set(g['cols'])
                groups2.setdefault(g['group'], []).append((g['slug'] + '.html', chip_label(name, re.sub(r'\(.*?\)', '', g['kw'])), True))
    for slug, tag in tags.items():
        if city_of(slug) != code or slug in used: continue
        label = LABELS.get(slug) or ' '.join(cover.get(slug, ['', slug])[1:2])
        groups2.setdefault(tag_group(tag), []).append((f'blog/{slug}.html', chip_label(name, label), False))
    n = sum(len(v) for v in groups2.values())
    inner = []
    for grp in (list(KEYMAP) + [x for x in GROUP_ORDER if x not in KEYMAP]):
        if grp not in groups2: continue
        chips = '\n'.join(f'          <a class="gchip{" gchip--key" if key else ""}" href="{u}"><span>{esc(t)}</span><span aria-hidden="true">→</span></a>' for u, t, key in (groups2[grp] if code == 'gunsan' else sorted(groups2[grp], key=lambda x: (not x[2], x[1]))))
        glabel = f'{name}형사·군형사' if grp == '형사' else f'{name} {grp}'
        inner.append(f'        <details class="ghub__grp">\n        <summary><h3 class="ghub__h">{esc(glabel)}</h3><span class="ghub__count">{len(groups2[grp])}</span></summary>\n        <div class="ghub__chips">\n{chips}\n        </div>\n        </details>')
    if not inner:
        inner.append(f'        <p class="ghub__empty">{esc(name)} 지역 안내 글은 준비 중입니다. {esc(name)} 사건도 상담하실 수 있습니다.</p>')
    blocks.append(f'''      <details class="ghub__city" id="{code}"{" open" if code == "gunsan" else ""}>
        <summary><span class="ghub__name">{esc(name)}</span><span class="ghub__count">{n}개 안내</span></summary>
        <p class="ghub__court">관할 법원 {esc(court)} · 관할 공소청 {esc(pros)} · 관할 경찰서 {esc(police)}</p>
{chr(10).join(inner)}
      </details>''')
main = phero([('홈', 'index.html'), ('지역별 안내', None)], 'Regional Guide', '지역별 안내') + f'''
  <section class="sec sec--paper sec--list">
    <div class="wrap">
      <p class="sec-lead">법률사무소 차민은 군산에 있지만, 지역과 관계없이 사건을 맡습니다. 지역별로 관할 법원·공소청·경찰서와 관련 안내를 모았습니다.</p>
{chr(10).join(blocks)}
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
