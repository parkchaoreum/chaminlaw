#!/usr/bin/env python3
"""칼럼 <title>(검색 결과에 보이는 제목) 앞에 '도시+키워드+변호사'를 붙인다. 화면의 큰 제목(h1·og:title)은 그대로 둔다.
형사 칼럼의 '형사전문변호사'/'경찰출신변호사'는 칼럼마다 고정해 둔다(2026-10-25 대표 지시: 새 글이 끼어들어도 기존 제목은 바뀌지 않게). 새 형사 칼럼은 두 문구 수가 균형을 이루도록, 군산 글은 가능하면 형사전문으로 지정해 M 에 직접 적는다. 다시 돌려도 결과가 같다."""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CITY = {'gunsan':'군산','iksan':'익산','jeonju':'전주','buan':'부안','gimje':'김제','seocheon':'서천','nonsan':'논산','boryeong':'보령','gochang':'고창','buyeo':'부여','jeongeup':'정읍'}
# slug: (키워드들, 분야 키워드)  분야 'CRIM' = 형사전문/경찰출신 교대
M = {
 '20261016-gunsan-sonhaebaesang': (['손해배상'], '민사전문'),
 'boryeong-gongmuwon-jinggye': (['공무원징계'], '징계전문'),
 'buan-jeonsesagi-daeeung': (['전세사기'], '부동산전문'),
 'buan-sanggan-sosong-jeunggeo': (['상간소송'], '이혼전문'),
 'gimje-sanggan-sosong': (['상간소송'], '이혼전문'),
 'gunsan-budang-haego-guje': (['부당해고'], '노동전문'),
 'gunsan-bulsongchi-iuisincheong': (['불송치이의신청'], '경찰출신'),
 'gunsan-daepo-tongjang-myeongija-sonhaebaesang': (['대포통장'], '민사전문'),
 'gunsan-dongeop-taltoe-jeongsan': (['동업분쟁'], '민사전문'),
 'gunsan-eommu-banghae-beolgeum-wijaryo': (['업무방해'], '형사전문'),
 'gunsan-eommusang-hoengnyeong': (['횡령'], '형사전문'),
 'gunsan-eumju-unjeon-gyeongchal-josa': (['음주운전'], '음주운전전문'),
 'gunsan-gangje-jiphaeng-jeongji-gongtak': (['강제집행정지'], '민사전문'),
 'gunsan-gangje-jiphaeng-myeontal': (['강제집행면탈'], '경찰출신'),
 'gunsan-geojitmal-tamjigi-geomsa': (['거짓말탐지기'], '형사전문'),
 'gunsan-gongmuwon-gamsa-josa': (['공무원감사'], '징계전문'),
 'gunsan-gongyumul-bunhal': (['공유물분할'], '부동산전문'),
 'gunsan-gosoin-josa-daeeung': (['고소대리'], '형사전문'),
 'gunsan-gunhyeongsa-yeongnae-pokhaeng': (['군형사', '군인폭행'], None),
 'gunsan-gusok-yeongjang-silji-simsa': (['구속영장', '영장실질심사'], '형사전문'),
 'gunsan-pokhaeng-pihae-hapui': (['폭행', '폭행전문'], '경찰출신'),
 'iksan-sanghae-pokhaeng-gubun': (['상해', '폭행'], '형사전문'),
 'gunsan-sagi-goso-gosojang': (['사기', '사기전문'], '경찰출신'),
 'gunsan-stalking-piuija-daeeung': (['스토킹', '스토킹전문'], '경찰출신'),
 'gunsan-hyeopbak-seongnip-goso': (['협박', '협박전문'], '경찰출신'),
 'gunsan-mugo-seongnip-gijun': (['무고', '무고전문'], '형사전문'),
 'gunsan-hyeongsa-hapui-sigi': (['형사합의', '형사합의전문'], '경찰출신'),
 'gunsan-hyeongsa-gongtak': (['형사공탁'], '형사전문'),
 'gunsan-giso-jiphaeng-yuye-chai': (['집행유예', '기소유예'], '경찰출신'),
 'iksan-chobeom-giso-yuye': (['기소유예', '기소유예전문'], '형사전문'),
 'jeonju-giso-yuye-geomsa-panjeon': (['기소유예', '기소유예전문'], '경찰출신'),
 'gunsan-muhyeomui-mujoe-daeeung': (['무혐의', '무죄'], '형사전문'),
 'iksan-giso-hu-mujoe-jeollyak': (['무죄', '무죄전문'], '경찰출신'),
 'gunsan-yaksik-myeongryeong-jeongsik-jaepan': (['약식명령', '정식재판청구'], '형사전문'),
 'iksan-jeongsik-jaepan-cheonggu-hyeongjong': (['정식재판청구', '약식명령'], '경찰출신'),
 'gunsan-hangsosim-geomsa-hangso-daebi': (['형사항소심', '항소심'], '형사전문'),
 'gunsan-gusok-jeokbusim-cheongu': (['구속적부심', '구속'], '경찰출신'),
 'gunsan-boseok-cheongu-seokbang': (['보석', '구속'], '형사전문'),
 'gunsan-gongsocheong-sasilgwangye-hwagin': (['공소청조사', '검찰조사'], '경찰출신'),
 'gunsan-apsu-susaek-daeeung': (['압수수색', '포렌식'], '형사전문'),
 'gunsan-gyeongchal-josa-dongseok': (['경찰조사'], '경찰출신'),
 'gunsan-gyotong-sago-byeonhosa-sigi': (['교통사고'], '교통사고전문'),
 'gunsan-hakpok-haengjeongsimpan-chamga': (['학폭행정심판'], '학교폭력전문'),
 'gunsan-hakpokwi-yesang-jilmun': (['학폭위'], '학교폭력전문'),
 'gunsan-ihon-gyeolsim-hu-junbi': (['이혼소송'], '이혼전문'),
 'gunsan-imdaecha-bojeunggeum-hoesu': (['전세보증금'], '부동산전문'),
 'gunsan-imdaecha-wonsang-hoebok': (['원상회복'], '부동산전문'),
 'gunsan-imgeum-toejikgeum-cheburi': (['임금체불'], '노동전문'),
 'gunsan-instagram-gyejeong-jeongji': (['인스타그램계정정지'], '민사전문'),
 'gunsan-jeoldojoe-cheobeol': (['절도'], '형사전문'),
 'gunsan-jikjang-goerophim-sayongja-jochi': (['직장내괴롭힘'], '노동전문'),
 'gunsan-jikjangnae-seonghuirong-daeeung': (['직장내성희롱'], '노동전문'),
 'gunsan-jun-gangje-chuhaeng': (['준강제추행'], '성범죄전문'),
 'gunsan-jutaek-imdaecha-gaengsin': (['임대차갱신'], '부동산전문'),
 'gunsan-kamera-deung-iyong-chwaryeong': (['카촬'], '성범죄전문'),
 'gunsan-minsa-jojeong': (['민사조정'], '민사전문'),
 'gunsan-moyokjoe': (['모욕'], '경찰출신'),
 'gunsan-myeongye-hweson': (['명예훼손'], '경찰출신'),
 'gunsan-samunseo-wijo': (['사문서위조'], '형사전문'),
 'gunsan-sanggan-wijaryo-aeksu': (['상간소송', '상간위자료'], None),
 'gunsan-sangsok-gaesi-hal-il': (['상속포기', '한정승인'], None),
 'gunsan-sangsok-jaesan-bunhal-simpan': (['상속재산분할'], '상속전문'),
 'gunsan-seongbeomjoe-jeongeon-songchi': (['성범죄송치'], '성범죄전문'),
 'gunsan-seongbeomjoe-muhyeomui': (['성범죄무혐의'], '성범죄전문'),
 'gunsan-seongbeomjoe-neujeun-goso': (['성범죄고소'], '성범죄전문'),
 'gunsan-seongbeomjoe-pihaeja': (['성범죄피해자'], '성범죄전문'),
 'gunsan-seongnyeon-hugyeon': (['성년후견'], '상속전문'),
 'gunsan-sonyeon-jaepan-simni': (['소년사건'], '경찰출신'),
 'gunsan-sonyeon-tongmaeeum': (['통매음'], '성범죄전문'),
 'gunsan-unjeonja-pokhaeng': (['운전자폭행'], '형사전문'),
 'gunsan-voice-phishing-sugeochaek': (['보이스피싱'], '형사전문'),
 'gunsan-wiheom-unjeon-chisang-gyoteuk': (['위험운전치상'], '교통사고전문'),
 'gunsan-yeonin-jeungyeo-daeyeo': (['대여금'], '민사전문'),
 'gunsan-yuryubun-banhwan': (['유류분'], '상속전문'),
 'iksan-daeyeogeum-banhwan': (['대여금'], '민사전문'),
 'iksan-dongeop-hoengnyeong': (['횡령'], '형사전문'),
 'iksan-eumju-unjeon-josa-ihu': (['음주운전'], '음주운전전문'),
 'iksan-gangje-chuhaeng-muhyeomui-gijun': (['강제추행'], '성범죄전문'),
 'iksan-hakgyopokryeok-jeolcha': (['학교폭력'], '학교폭력전문'),
 'iksan-imdaecha-wonsanghoebok-tongsang-sonmo': (['원상회복'], '부동산전문'),
 'iksan-jeonse-bojeunggeum-banhwan': (['전세보증금'], '부동산전문'),
 'iksan-kamera-chwaryeong-forensic': (['카촬'], '성범죄전문'),
 'iksan-moyokjoe-seongnip-yogeon': (['모욕'], '경찰출신'),
 'iksan-pigosoin-josa-daeeung': (['경찰조사'], '형사전문'),
 'iksan-sanggan-sosong-baeuja-jeungin': (['상간소송'], '이혼전문'),
 'iksan-sonyeon-boho-cheobun': (['소년사건'], '경찰출신'),
 'jeonju-eogulhan-hakpok-gahaeja': (['학폭가해학생'], '학교폭력전문'),
 'jeonju-eumju-unjeon-byeonhosa': (['음주운전'], '음주운전전문'),
 'jeonju-eumju-unjeon-chulseok-josa': (['음주운전'], '음주운전전문'),
 'jeonju-naeyongjeungmyeong': (['내용증명'], '민사전문'),
 'jeonju-sanggan-sosong-ihon-eopsi': (['상간소송'], '이혼전문'),
 'nonsan-ihon-sosong-gigan': (['이혼소송'], '이혼전문'),
 'seocheon-gunhyeongbeop-hyeongbeop': (['군형사'], None),
}
if __name__ == '__main__':
    SUF = ' | 법률사무소 차민'
    def date(s): 
        m = re.search(r'"datePublished":\s*"(\d{4}-\d\d-\d\d)', s); return m.group(1) if m else ''
    files = []
    for slug in M:
        p = ROOT / 'blog' / f'{slug}.html'
        if not p.exists(): continue
        files.append((date(p.read_text(encoding='utf-8')), slug, p))
    crim_i = 0
    for d, slug, p in sorted(files):
        s = p.read_text(encoding='utf-8')
        code = re.sub(r'^\d{8}-', '', slug).split('-')[0]; city = CITY[code]
        kws, field = M[slug]
        if field == 'CRIM':
            field = '형사전문' if crim_i % 2 == 0 else '경찰출신'; crim_i += 1
        words = [city + k + '변호사' for k in kws] + ([city + field + '변호사'] if field else [])
        t = re.search(r'<title>(.*?)</title>', s).group(1)
        body = t.split(SUF)[0]
        if ' | ' in body and body.split(' | ')[0].endswith('변호사'):   # 이미 붙어 있으면 원문만 남긴다
            body = body.split(' | ', 1)[1]
        body = re.sub(r'^' + city + r'\s+', '', body); body = re.sub(r'\s+—\s+' + city + '$', '', body)
        new = '·'.join(words) + ' | ' + body + SUF
        s = s.replace(f'<title>{t}</title>', f'<title>{new}</title>', 1)
        p.write_text(s, encoding='utf-8')
        print(new)
