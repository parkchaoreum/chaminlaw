#!/usr/bin/env python3
"""칼럼 날짜를 2026-06-02 ~ 고정 최신글(2026-10-15) 사이에 고르게 배치하고 전부 다시 빌드한다.
원래 네이버 발행일(orig_date) 순서를 유지한다. 주말은 피한다.
usage: redate.py <spec_dir>
"""
import json, sys, glob, subprocess, hashlib, pathlib, datetime as dt
START = dt.date(2026, 6, 2)
END   = dt.date(2026, 10, 15)          # 손해배상 글(고정) 날짜
specs = sorted(glob.glob(f'{sys.argv[1]}/*.json'),
               key=lambda f: json.loads(open(f, encoding='utf-8').read())['orig_date'])
n = len(specs); span = (END - START).days
used, prev = [], START - dt.timedelta(days=1)
for i, f in enumerate(specs):
    s = json.loads(open(f, encoding='utf-8').read())
    d = START + dt.timedelta(days=round(i * span / n))
    if i:                                                   # 첫 글은 6/2 고정, 나머지는 ±2일 흔들기
        j = int(hashlib.md5(s['slug'].encode()).hexdigest(), 16) % 5 - 2
        d += dt.timedelta(days=j)
    if d.weekday() == 5: d -= dt.timedelta(days=1)          # 토 → 금
    if d.weekday() == 6: d += dt.timedelta(days=1)          # 일 → 월
    while d <= prev: d += dt.timedelta(days=1)
    assert d < END
    prev = d; s['date'] = d.isoformat()
    open(f, 'w', encoding='utf-8').write(json.dumps(s, ensure_ascii=False, indent=1))
    subprocess.run(['python3', str(pathlib.Path(__file__).with_name('build_post.py')), f], check=True)
    used.append((s['orig_date'], s['date'], 'MTWTFSS'[d.weekday()], s['slug']))
for u in used: print('네이버 %s → 홈페이지 %s(%s)  %s' % u)
