#!/usr/bin/env python3
"""AI 검색·챗봇용 요약 파일 /llms.txt 를 만든다(사무소 정보 + 칼럼 목록). build_post.py 가 자동 호출."""
import re, html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from practice_data import AREAS
ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://www.chaminlaw.com/'
idx = (ROOT / 'blog/index.html').read_text(encoding='utf-8')
a = idx.index('<!-- POSTS:START -->'); b = idx.index('<!-- POSTS:END -->')
groups = {'형사': [], '민사': [], '행정': [], '가사': []}
cmap = {'형사': '형사', '민사': '민사', '행정': '행정', '학교폭력': '행정', '노동': '행정', '이혼': '가사', '가사': '가사'}
for href, tag, title, desc in re.findall(
        r'<a class="post" href="([^"]+)">.*?post__tag">([^<]*)</span>.*?post__h">(.*?)</h2>.*?post__d">(.*?)</p>', idx[a:b], re.S):
    k = cmap.get(re.split(r'[\s·]+', tag.strip())[0])
    if k:
        groups[k].append(f'- [{html.unescape(title)}]({SITE}blog/{href}): {html.unescape(desc)}')

areas_line = ' / '.join(f'[{x["name"]}]({SITE}{x["slug"]}.html)' for x in AREAS)
body = f'''# 법률사무소 차민 (Law office CHAMIN)

> 전북특별자치도 군산시에 있는 법률사무소입니다. 박차오름·이민규 대표변호사가 형사, 민사, 가사(이혼·상간·상속·후견), 행정(징계·학교폭력) 사건을 상담부터 재판까지 직접 수행합니다. 사무소는 군산 한 곳이며, 지역에 관계없이 전국 사건을 맡고 있습니다.

## 사무소 정보
- 상호: 법률사무소 차민
- 주소: 전북특별자치도 군산시 미장안7길 6, 3층 (우편번호 54094)
- 전화: 063-452-9075 / 팩스: 063-452-9076
- 사업자등록번호: 174-28-01906
- 상담 시간: 평일 09:00–18:00 (미리 예약하면 업무 시간 외 상담 가능)
- 카카오톡 채널: 법률사무소 차민 (http://pf.kakao.com/_xhEenX)
- 홈페이지: {SITE}
- 네이버 블로그: https://blog.naver.com/chaminlaw
- 인스타그램: https://www.instagram.com/lawoffice_chamin
- 지도: 구글 https://maps.google.com/?cid=17095718723793884728 / 카카오 https://place.map.kakao.com/461027372
- 주요 상담 지역: 군산, 익산, 전주, 김제, 부안, 서천, 보령, 논산 등 전북·충남 서부 (전국 사건 수임)

## 변호사
- 박차오름 대표변호사: 원광대학교 법학전문대학원. 前 법무법인 YK, 前 제53보병사단 군사경찰대 지원과장. 전주지방법원 조정위원(민사·가사), 전주교육지원청 학교폭력대책심의위원회·교권보호심의위원회 위원. 연락처 chaoreum@chaminlaw.com
- 이민규 대표변호사: 경찰대학, 원광대학교 법학전문대학원. 前 법무법인(유한) 바른 형사그룹, 前 법무법인 YK 경찰형사부, 前 군산경찰서 수사과, 前 경찰청 경무국. 군산시 의정비심의위원회 위원, 익산지방국토관리청 청원심의회 위원. 연락처 mingyu@chaminlaw.com

## 주요 페이지
- [변호사 소개]({SITE}attorneys.html)
- [업무분야]({SITE}practice.html): 형사(경찰 조사 동행, 구속영장 심사, 성범죄, 음주운전, 교통사고), 민사(손해배상, 대여금, 임대차·보증금, 명예훼손, 부동산), 가사(이혼, 상간, 양육권, 재산분할, 상속, 후견), 행정(행정처분 불복, 행정심판, 공무원 징계, 학교폭력)
- 분야별 안내: {areas_line}
- [성공사례]({SITE}results.html)
- [상담 안내]({SITE}booking.html)
- [오시는 길]({SITE}location.html)
- [법률 칼럼]({SITE}blog/) (RSS: {SITE}blog/rss.xml)

## 법률 칼럼 — 형사
{chr(10).join(groups['형사'])}

## 법률 칼럼 — 민사
{chr(10).join(groups['민사'])}

## 법률 칼럼 — 행정
{chr(10).join(groups['행정'])}

## 법률 칼럼 — 가사
{chr(10).join(groups['가사'])}

## 참고
칼럼은 일반적인 법률 정보이며 개별 사건의 결론을 보장하지 않습니다. 광고책임변호사: 박차오름.
'''
(ROOT / 'llms.txt').write_text(body, encoding='utf-8')
print('llms.txt:', sum(len(v) for v in groups.values()), 'columns')
