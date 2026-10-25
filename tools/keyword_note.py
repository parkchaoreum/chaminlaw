#!/usr/bin/env python3
"""칼럼 본문 끝(<!-- ===== 본문 끝 ===== --> 앞)에 작성 변호사 소개 한 문단과 관련 검색어 줄을 넣는다.
검색어는 seo_titles.M 의 '도시+키워드+변호사'와 분야 문구(형사 글은 형사전문·경찰출신 둘 다)를 쓴다. 다시 돌려도 결과가 같다."""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from seo_titles import M, CITY
AWK = {'경찰조사','고소대리','불송치이의신청','거짓말탐지기','성범죄송치','성범죄무혐의','성범죄고소','성범죄피해자','학폭위','학폭행정심판',
       '민사조정','강제집행정지','내용증명','원상회복','임대차갱신','공무원감사','대포통장','인스타그램계정정지','구속영장','영장실질심사','한정승인','상속포기'}
CRIMF = {'형사전문','경찰출신'}
AREA = {'이혼전문':'이혼·상간','상속전문':'상속·가사','민사전문':'민사','부동산전문':'부동산·임대차','학교폭력전문':'학교폭력',
        '노동전문':'노동','징계전문':'징계','성범죄전문':'성범죄','음주운전전문':'음주운전','교통사고전문':'교통사고'}
S, E = '<!-- KW:START -->', '<!-- KW:END -->'
def eul(w):  # 을/를
    c = ord(w[-1]) - 0xAC00
    return w + ('을' if 0 <= c < 11172 and c % 28 else '를')
NONE_FIELD = {'상간': '이혼전문', '상속': '상속전문', '한정': '상속전문', '군형사': None, '군인': None}
n = 0
for slug, (kws, field) in M.items():
    p = ROOT / 'blog' / f'{slug}.html'
    s = p.read_text(encoding='utf-8')
    city = CITY[re.sub(r'^\d{8}-', '', slug).split('-')[0]]
    lee = 'attorneys.html#lee' in s
    if field is None:
        for k0, f0 in NONE_FIELD.items():
            if kws[0].startswith(k0): field = f0; break
    words = [city + k + '변호사' for k in kws]
    base = kws[0].replace('전문', '')
    if base not in AWK and not any(k.endswith('전문') for k in kws): words.append(city + base + '전문변호사')
    if lee and (field in CRIMF or field in ('성범죄전문','음주운전전문','교통사고전문') or (field is None and 'gunhyeongsa' not in slug)):
        if field and field not in CRIMF: words.append(city + field + '변호사')
        words += [city + '형사전문변호사', city + '경찰출신변호사']
    elif field and field not in CRIMF:
        words.append(city + field + '변호사')
    if field == '노동전문' or field == '징계전문':
        words = [w for w in words if '형사전문' not in w and '경찰출신' not in w] + [city + field + '변호사']
    seen = []; [seen.append(w) for w in words if w not in seen]
    if lee:
        area = '형사' if (field in CRIMF or field is None) else AREA.get(field, '형사')
        who = (f'이 글을 쓴 이민규 대표변호사는 경찰대학을 졸업하고 군산경찰서 수사과에서 근무한 경찰 출신 변호사로, '
               f'{eul(city)} 비롯한 전북·충남 지역의 {area} 사건을 맡고 있습니다.')
    elif 'gunhyeongsa' in slug:
        who = (f'이 글을 쓴 박차오름 대표변호사는 제53보병사단 군사경찰대 지원과장을 지냈으며, {eul(city)} 비롯한 전북·충남 지역의 군형사 사건을 맡고 있습니다.')
    elif field == '학교폭력전문':
        who = (f'이 글을 쓴 박차오름 대표변호사는 전주교육지원청 학교폭력대책심의위원회 위원으로 활동하며, {eul(city)} 비롯한 전북 지역의 학교폭력 사건을 맡고 있습니다.')
    else:
        area = AREA.get(field, '민사·가사')
        who = (f'이 글을 쓴 박차오름 대표변호사는 전주지방법원 민사·가사 조정위원으로 활동하며, {eul(city)} 비롯한 전북 지역의 {area} 사건을 맡고 있습니다.')
    block = (f'{S}\n<aside class="article__kw"><p>{who}</p>'
             f'<p class="article__kw-tags"><span>관련 검색어</span> {" · ".join(seen)}</p></aside>\n{E}\n')
    s = re.sub(re.escape(S) + r'.*?' + re.escape(E) + r'\n', '', s, flags=re.S)
    mark = '        <!-- ===== 본문 끝 ===== -->'
    if mark not in s: print('no mark', slug); continue
    s = s.replace(mark, block + mark, 1)
    p.write_text(s, encoding='utf-8'); n += 1
print('keyword notes:', n)
