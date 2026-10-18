#!/usr/bin/env python3
"""칼럼 사이 연결을 갱신한다. build_post.py 가 자동 호출.
 1) 각 칼럼의 '글 · ○○○ 대표변호사' → 변호사 소개(#park/#lee) 링크, 구조화 데이터 author.url 도 같은 주소로
 2) 각 칼럼 하단(사무소 안내 위)에 '함께 읽으면 좋은 칼럼' 3편
 3) 변호사 소개 페이지에 변호사별 칼럼 목록
"""
import re, html, pathlib, datetime as dt
ROOT = pathlib.Path(__file__).resolve().parent.parent
ANCHOR = {'박차오름': 'park', '이민규': 'lee'}
CMAP = {'형사': '형사', '민사': '민사', '행정': '행정', '학교폭력': '행정', '노동': '행정', '이혼': '가사', '가사': '가사'}

idx = (ROOT / 'blog/index.html').read_text(encoding='utf-8')
a = idx.index('<!-- POSTS:START -->'); b = idx.index('<!-- POSTS:END -->')
posts = []
for href, tag, date, title, desc in re.findall(
        r'<a class="post" href="([^"]+)">.*?post__tag">([^<]*)</span><time datetime="([\d-]+)".*?post__h">(.*?)</h2>.*?post__d">(.*?)</p>',
        idx[a:b], re.S):
    f = ROOT / 'blog' / href
    if not f.exists():
        continue
    s = f.read_text(encoding='utf-8')
    m = re.search(r'글 · (?:<a [^>]*>)?(\S+) 대표변호사', s)
    posts.append(dict(href=href, tag=tag.strip(), date=dt.date.fromisoformat(date), title=title, desc=desc,
                      cat=CMAP.get(re.split(r'[\s·]+', tag.strip())[0], ''), author=m.group(1) if m else '',
                      city=title.split('에서')[0] if '에서' in title[:8] else ''))

def related(p):
    def score(q):
        sc = 0
        if q['cat'] == p['cat']: sc += 100
        if q['tag'] == p['tag']: sc += 30
        if q['author'] == p['author']: sc += 5
        return (sc, -abs((q['date'] - p['date']).days))
    others = [q for q in posts if q['href'] != p['href']]
    return sorted(others, key=score, reverse=True)[:3]

def card(q, prefix=''):
    d = q['date']
    return (f'''            <a class="post" href="{prefix}{q['href']}">
              <div class="post__meta"><span class="post__tag">{q['tag']}</span><time datetime="{d.isoformat()}">{d.year}. {d.month}. {d.day}.</time></div>
              <h3 class="post__h">{q['title']}</h3>
              <p class="post__d">{q['desc']}</p>
            </a>''')

for p in posts:
    f = ROOT / 'blog' / p['href']; s = f.read_text(encoding='utf-8')
    an = ANCHOR.get(p['author'])
    if an:
        s = re.sub(r'<span>글 · (?:<a [^>]*>)?(\S+) 대표변호사(?:</a>)?</span>',
                   rf'<span>글 · <a class="article__author" href="../attorneys.html#{an}">\1 대표변호사</a></span>', s, count=1)
        s = s.replace('"url": "https://www.chaminlaw.com/attorneys.html" }', f'"url": "https://www.chaminlaw.com/attorneys.html#{an}" }}', 1)
    block = ('        <!-- RELATED:START -->\n        <section class="related" aria-labelledby="related-h">\n'
             '          <h2 id="related-h">함께 읽으면 좋은 칼럼</h2>\n          <div class="related__list">\n'
             + '\n'.join(card(q) for q in related(p)) +
             '\n          </div>\n        </section>\n        <!-- RELATED:END -->\n\n')
    if '<!-- RELATED:START -->' in s:
        s = re.sub(r'        <!-- RELATED:START -->.*?<!-- RELATED:END -->\n\n', block, s, flags=re.S)
    else:
        s = s.replace('        <aside class="office-box"', block + '        <aside class="office-box"', 1)
    f.write_text(s, encoding='utf-8')

# 변호사 소개 페이지
att_p = ROOT / 'attorneys.html'; att = att_p.read_text(encoding='utf-8')
def col(name):
    mine = [q for q in posts if q['author'] == name]
    li = lambda q: f'              <li><a href="blog/{q["href"]}">{q["title"]}</a></li>'
    head, rest = mine[:5], mine[5:]
    more = ''
    if rest:
        more = ('            <details class="attcols__more">\n'
                f'              <summary>칼럼 {len(rest)}편 더 보기</summary>\n              <ul class="attcols__list">\n'
                + '\n'.join('  ' + li(q) for q in rest) + '\n              </ul>\n            </details>\n')
    return (f'''          <div class="attcols__col">
            <h3 class="attcols__h"><a href="#{ANCHOR[name]}">{name} 대표변호사</a><span>{len(mine)}편</span></h3>
            <ul class="attcols__list">
{chr(10).join(li(q) for q in head)}
            </ul>
{more}          </div>''')
sec = f'''  <!-- ATTCOLS:START -->
  <section class="sec sec--paper attcols" aria-labelledby="attcols-h">
    <div class="wrap">
      <p class="eyebrow">Columns</p>
      <h2 class="sec-title" id="attcols-h">변호사가 직접 쓴 법률 칼럼</h2>
      <div class="attcols__grid">
{col('박차오름')}
{col('이민규')}
      </div>
      <p class="attcols__all"><a class="ilink" href="blog/">법률 칼럼 전체 보기 →</a></p>
    </div>
  </section>
  <!-- ATTCOLS:END -->
'''
if '<!-- ATTCOLS:START -->' in att:
    att = re.sub(r'  <!-- ATTCOLS:START -->.*?<!-- ATTCOLS:END -->\n', sec, att, flags=re.S)
else:
    att = att.replace('  <section class="sec sec--ink" aria-label="사무소에 걸린 표창장과 위촉장">', sec + '\n  <section class="sec sec--ink" aria-label="사무소에 걸린 표창장과 위촉장">', 1)
att_p.write_text(att, encoding='utf-8')
print('crosslinks:', len(posts), 'posts')
