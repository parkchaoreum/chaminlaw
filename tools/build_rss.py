#!/usr/bin/env python3
"""blog/index.html 의 칼럼 카드로 RSS(blog/rss.xml)를 만든다. build_post.py 가 자동 호출."""
import re, html, pathlib, datetime as dt
from email.utils import format_datetime
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://www.chaminlaw.com/blog/'
KST = dt.timezone(dt.timedelta(hours=9))
idx = (ROOT / 'blog/index.html').read_text(encoding='utf-8')
a = idx.index('<!-- POSTS:START -->'); b = idx.index('<!-- POSTS:END -->')
items = []
for href, tag, date, title, desc in re.findall(
        r'<a class="post" href="([^"]+)">.*?post__tag">([^<]*)</span><span hidden data-d="([\d-]+)".*?post__h">(.*?)</h2>.*?post__d">(.*?)</p>',
        idx[a:b], re.S):
    page = (ROOT / 'blog' / href)
    full = ''
    if page.exists():
        m = re.search(r'<meta name="description" content="([^"]*)"', page.read_text(encoding='utf-8'))
        full = m.group(1) if m else ''
    d = dt.datetime.fromisoformat(date).replace(hour=9, tzinfo=KST)
    esc = lambda s: html.escape(html.unescape(s), quote=False)
    items.append(f'''    <item>
      <title>{esc(title)}</title>
      <link>{BASE}{href}</link>
      <guid isPermaLink="true">{BASE}{href}</guid>
      <description>{esc(full or desc)}</description>
      <category>{esc(tag)}</category>
      <pubDate>{format_datetime(d)}</pubDate>
    </item>''')
now = format_datetime(dt.datetime.now(KST).replace(microsecond=0))
rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>법률 칼럼 | 법률사무소 차민</title>
    <link>{BASE}</link>
    <atom:link href="{BASE}rss.xml" rel="self" type="application/rss+xml" />
    <description>전북 군산 법률사무소 차민의 형사·민사·가사·행정 법률 칼럼</description>
    <language>ko</language>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
'''
(ROOT / 'blog/rss.xml').write_text(rss, encoding='utf-8')
print('rss:', len(items), 'items')
