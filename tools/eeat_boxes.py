#!/usr/bin/env python3
"""칼럼마다 (1) 맨 위 '핵심 답변' 상자 (2) 본문 끝 '이 글을 쓴 변호사' 경력 한 줄을 넣는다(GEO, 대표 지시 2026-10-28).
- 핵심 답변 = 칼럼 목록 카드의 요약문(card_desc). spec 에 'answer' 가 있으면 build_post 가 카드에 그 문장을 쓰므로 그대로 반영된다.
- 경력 한 줄 = 작성 변호사·분야·주소로 고른 실제 위촉·경력(‘전문’ 표기 없이 사실만).
- JSON-LD author 에도 같은 경력을 description 으로 넣는다.
여러 번 돌려도 같은 결과(표시 주석 사이를 지우고 다시 넣음). build_post.py 가 자동 호출."""
import re, html, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / 'blog'

MIL = '제53보병사단 군사경찰대 지원과장으로 근무한 군사경찰 출신 변호사입니다.'
SCH = '전주교육지원청 학교폭력대책심의위원회·교권보호심의위원회 위원으로 활동하고 있습니다.'
VIC_P = '전주지방공소청 피해자국선변호사로 활동하고 있습니다.'
MED = '전주지방법원 민사·가사 조정위원으로 활동하고 있습니다.'
L_CRIM = '경찰대학을 졸업하고 군산경찰서 수사과에서 근무한 경찰 수사 실무 출신 변호사입니다. 전주지방공소청 피해자국선변호사로도 활동하고 있습니다.'
L_VIC = '경찰대학을 졸업하고 군산경찰서 수사과에서 근무했으며, 전주지방공소청 피해자국선변호사로 활동하고 있습니다.'
L_LAB = '경찰대학을 졸업하고 경찰청 경무국과 군산경찰서 수사과에서 근무했으며, 군산대학교 인권센터 조사위원으로 활동하고 있습니다.'
L_CIV = '경찰대학을 졸업하고 법무법인(유한) 바른 형사그룹과 법무법인 YK 경찰형사부에서 근무했습니다.'
VICTIM_KEYS = ('pihaeja', 'goso-daeri', 'gosoin', 'baesang-myeongryeong', 'bulsongchi')

def cred(author, cat, slug):
    if author == '박차오름':
        if '군형사' in cat or any(k in slug for k in ('gunin', 'gunhyeong', 'gunsabeop')): return MIL
        if '학교폭력' in cat or any(k in slug for k in ('hakpok', 'gyowon', 'gyogwon')): return SCH
        if any(k in slug for k in VICTIM_KEYS): return VIC_P
        return MED
    if author == '이민규':
        if cat.startswith(('노동', '행정')): return L_LAB
        if any(k in slug for k in VICTIM_KEYS) or cat == '형사 · 고소': return L_VIC
        if cat.startswith('형사'): return L_CRIM
        return L_CIV
    return ''

ANCHOR = {'박차오름': 'park', '이민규': 'lee'}
idx = (BLOG / 'index.html').read_text(encoding='utf-8')
cards = dict(re.findall(r'<a class="post" href="([^"]+)">.*?post__d">(.*?)</p>', idx, re.S))

n = 0
for f in sorted(BLOG.glob('*.html')):
    if f.name in ('index.html',) or f.name.startswith('_'): continue
    t = f.read_text(encoding='utf-8'); o = t
    if 'class="article__meta"' not in t: continue
    am = re.search(r'"author": \{ "@type": "Person", "name": "([^"]+)"', t)
    cm = re.search(r'post__tag">([^<]+)</span>\s*<span hidden data-d', t)
    if not am or not cm: continue
    author, cat, slug = am.group(1), html.unescape(cm.group(1)), f.stem
    c = cred(author, cat, slug)
    t = re.sub(r'\n?\s*<!--KEYANS-->.*?<!--/KEYANS-->', '', t, flags=re.S)
    t = re.sub(r'\n?\s*<!--BYLINE-->.*?<!--/BYLINE-->', '', t, flags=re.S)
    ans = cards.get(f.name, '').strip()
    if ans:
        box = ('\n        <!--KEYANS--><div class="keyans"><p class="keyans__h">핵심 답변</p>'
               f'<p class="keyans__a">{ans}</p></div><!--/KEYANS-->')
        t = re.sub(r'(<div class="article__meta">.*?</div>)', lambda m: m.group(1) + box, t, count=1, flags=re.S)
    if c:
        by = ('\n        <!--BYLINE--><aside class="byline" aria-label="글쓴이">'
              f'<p class="byline__h">이 글을 쓴 변호사</p><p class="byline__t"><b>{author} 대표변호사</b> {c} '
              f'<a href="../attorneys.html#{ANCHOR.get(author, "")}">변호사 소개 →</a></p></aside><!--/BYLINE-->\n')
        if '<h2>자주 묻는 질문</h2>' in t:
            t = t.replace('        <h2>자주 묻는 질문</h2>', by + '\n        <h2>자주 묻는 질문</h2>', 1)
        # JSON-LD author 에 경력
        t = re.sub(r'("author": \{ "@type": "Person", "name": "[^"]+", "jobTitle": "대표변호사", "url": "[^"]+")(, "description": "[^"]*")?',
                   lambda m: m.group(1) + ', "description": ' + json.dumps(c, ensure_ascii=False), t, count=1)
    if t != o: f.write_text(t, encoding='utf-8'); n += 1
print('eeat boxes:', n)
