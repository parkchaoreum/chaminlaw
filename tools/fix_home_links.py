"""홈·칼럼 목록 링크를 index.html 대신 디렉터리 주소(/ , /blog/)로 바꾼다.
index.html 로 링크하면 구글이 /index.html 을 따로 크롤링해 '대체 페이지(표준 태그)'로 분류한다. build_post.py 가 마지막에 호출."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
n = 0
for f in list(ROOT.glob('*.html')) + list((ROOT / 'blog').glob('*.html')):
    t = f.read_text(encoding='utf-8'); o = t
    if f.parent.name == 'blog':
        t = t.replace('href="../index.html', 'href="../').replace('href="index.html', 'href="./')
    else:
        t = t.replace('href="index.html', 'href="./').replace('href="blog/index.html', 'href="blog/')
    if t != o: f.write_text(t, encoding='utf-8'); n += 1
print('home links fixed:', n)
