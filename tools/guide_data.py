# 키워드별 안내 페이지 데이터 (guide-*.html). 페이지마다 내용을 따로 쓴다 — 키워드만 바꾼 복제 금지.
GUIDES = [
 dict(slug='guide-gunsan-gangje-chuhaeng', group='성범죄', kw='군산 강제추행',
  h1='군산 강제추행 변호사 상담 안내',
  title='군산 강제추행 변호사 — 고소당했을 때와 피해를 입었을 때 | 법률사무소 차민',
  desc='군산에서 강제추행으로 고소당했거나 피해를 입었다면. 성립 기준과 쟁점, 2026. 10. 2. 이후 진행 순서, 군산경찰서·전주지방법원 군산지원 관할, 관련 칼럼과 자주 묻는 질문을 정리했습니다.',
  info=[('관할','군산경찰서 → 전주지방공소청 군산지청 → 전주지방법원 군산지원'),
        ('관련 법조','형법 제298조(강제추행: 10년 이하의 징역 또는 1천500만 원 이하의 벌금), 성폭력처벌법'),
        ('담당 변호사','이민규 대표변호사 (경찰대 졸업, 군산경찰서 수사과 근무)'),
        ('관련 분야','<a class="ilink" href="practice-sexual.html">성범죄 분야 안내 →</a>')],
  intro=['강제추행은 폭행이나 협박으로 상대방의 의사에 반해 성적 수치심을 일으키는 신체 접촉을 한 경우를 말합니다. 손이나 손목을 반복해 붙잡거나 몸을 쓸어내리는 행동도 사정에 따라 강제추행으로 평가될 수 있어, 당사자가 생각하는 것보다 인정 범위가 넓습니다.',
         '강제추행은 성폭력범죄이므로 2026. 10. 2.부터는 경찰이 혐의가 없다고 보더라도 사건을 공소청에 송치합니다. 고소를 당한 쪽이든 피해를 입은 쪽이든, 첫 조사 전에 그날의 경위와 남아 있는 자료를 정리해 두는 것이 중요합니다.'],
  points=[('신체 접촉이 있었는지, 어떤 접촉이었는지','접촉 부위와 방식, 반복 여부, 당시 자리 배치가 모두 판단 요소가 됩니다.'),
          ('상대방의 의사에 반했는지','손을 빼거나 자리를 옮기는 등 거부 의사를 표시했는지, 주변 사람이 제지했는지가 함께 검토됩니다.'),
          ('고의가 있었는지','실수나 우연한 접촉이라는 주장이 받아들여지려면 당시 상황과 맞아떨어져야 합니다.'),
          ('진술의 일관성','증거가 진술뿐인 사건이 많아, 고소인과 피고소인 진술의 구체성과 일관성이 결론을 좌우합니다.'),
          ('객관적 자료','CCTV, 메시지, 동석자 진술, 결제·이동 기록이 진술을 뒷받침하거나 반박합니다.'),
          ('합의와 부수처분','합의는 처분과 양형에 반영되지만 그것만으로 사건이 끝나지는 않으며, 유죄가 확정되면 신상정보 등록 등이 함께 문제 될 수 있습니다.')],
  steps=[('고소 사실 확인','출석 요구를 받으면 고소 내용과 사건 번호를 확인하고, 필요하면 정보공개청구로 고소장을 확인합니다.'),
         ('경위와 자료 정리','그날의 시간 순서, 동석자, 메시지와 위치 기록을 정리하고 인정할 부분과 다툴 부분을 나눕니다.'),
         ('경찰 조사','조사에 변호인이 동석할 수 있고, 조서는 서명 전에 끝까지 확인합니다.'),
         ('처분 · 재판','송치 후 공소청 검사가 혐의없음, 기소유예, 약식기소, 정식기소 중 처분을 정하고, 기소되면 전주지방법원 군산지원에서 재판이 진행됩니다.')],
  cols=['iksan-gangje-chuhaeng-muhyeomui-gijun','gunsan-jun-gangje-chuhaeng','gunsan-seongbeomjoe-muhyeomui','gunsan-seongbeomjoe-jeongeon-songchi','gunsan-seongbeomjoe-neujeun-goso','gunsan-seongbeomjoe-pihaeja'],
  faq=[('합의하면 강제추행 사건은 끝나나요?','강제추행은 피해자가 처벌을 원하지 않아도 처벌할 수 있는 범죄입니다. 합의와 처벌불원 의사는 처분과 양형에서 중요하게 고려되지만, 그것만으로 사건이 종결되지는 않습니다.'),
       ('CCTV가 없으면 혐의가 인정되지 않나요?','그렇지 않습니다. 진술의 구체성과 일관성, 메시지, 동석자 진술 같은 정황을 종합해 판단하므로 CCTV가 없어도 혐의가 인정될 수 있고, 반대로 CCTV가 있어도 그것만으로 결론이 나지는 않습니다.'),
       ('경찰이 혐의가 없다고 보면 사건이 바로 끝나나요?','2026. 10. 2.부터 성폭력범죄는 경찰의 판단과 관계없이 공소청으로 송치되므로, 최종 처분은 공소청 검사가 정합니다.')]),
]
from guide_pages import PAGES
GUIDES += PAGES
for _m in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
    GUIDES += __import__('guide_pages_' + _m).PAGES

# 지역별 안내 — 도시 순서와 관할
CITIES = [
 ('gunsan','군산','전주지방법원 군산지원','군산경찰서','전주지방공소청 군산지청'),
 ('iksan','익산','전주지방법원 군산지원','익산경찰서','전주지방공소청 군산지청'),
 ('jeonju','전주','전주지방법원','전주완산경찰서·전주덕진경찰서','전주지방공소청'),
 ('buan','부안','전주지방법원 정읍지원','부안경찰서','전주지방공소청 정읍지청'),
 ('gimje','김제','전주지방법원','김제경찰서','전주지방공소청'),
 ('seocheon','서천','대전지방법원 홍성지원','서천경찰서','대전지방공소청 홍성지청'),
 ('nonsan','논산','대전지방법원 논산지원','논산경찰서','대전지방공소청 논산지청'),
 ('boryeong','보령','대전지방법원 홍성지원','보령경찰서','대전지방공소청 홍성지청'),
 ('gochang','고창','전주지방법원 정읍지원','고창경찰서','전주지방공소청 정읍지청'),
 ('buyeo','부여','대전지방법원 논산지원','부여경찰서','대전지방공소청 논산지청'),
 ('jeongeup','정읍','전주지방법원 정읍지원','정읍경찰서','전주지방공소청 정읍지청'),
]
# 칼럼 → 키워드 이름(도시 이름 없이). 칼럼을 새로 만들면 여기에 한 줄 추가한다(없으면 표지 문구로 대신함).
LABELS = {
 'gunsan-muhyeomui-mujoe-daeeung':'무혐의·무죄',
 'jeonju-giso-yuye-geomsa-panjeon':'기소유예 판단 기준',
 'gunsan-gyotong-sago-byeonhosa-sigi':'교통사고 변호사 상담 시기','jeonju-eumju-unjeon-chulseok-josa':'음주운전경찰조사',
 'gunsan-seongbeomjoe-jeongeon-songchi':'성범죄 전건송치','20261016-gunsan-sonhaebaesang':'불법행위 손해배상',
 'gunsan-sonyeon-tongmaeeum':'청소년 통매음(통신매체이용음란)','iksan-gangje-chuhaeng-muhyeomui-gijun':'강제추행',
 'iksan-sanggan-sosong-baeuja-jeungin':'상간소송','iksan-jeonse-bojeunggeum-banhwan':'전세보증금 반환',
 'gunsan-sangsok-jaesan-bunhal-simpan':'상속재산분할 심판','gunsan-gongmuwon-gamsa-josa':'공무원 감사 조사',
 'gunsan-budang-haego-guje':'부당해고 구제신청','gunsan-kamera-deung-iyong-chwaryeong':'카메라등이용촬영(카촬)',
 'gunsan-jikjangnae-seonghuirong-daeeung':'직장 내 성희롱','gunsan-jikjang-goerophim-sayongja-jochi':'직장 내 괴롭힘',
 'iksan-sonyeon-boho-cheobun':'소년보호처분','gunsan-gongyumul-bunhal':'공유물분할소송','gunsan-ihon-gyeolsim-hu-junbi':'이혼 준비',
 'gunsan-geojitmal-tamjigi-geomsa':'거짓말탐지기 검사','gunsan-imgeum-toejikgeum-cheburi':'임금·퇴직금 체불',
 'buan-sanggan-sosong-jeunggeo':'상간소송','gunsan-imdaecha-wonsang-hoebok':'임대차 원상회복','gunsan-eommusang-hoengnyeong':'업무상횡령',
 'gunsan-hakpokwi-yesang-jilmun':'학폭위 심의','gunsan-eommu-banghae-beolgeum-wijaryo':'업무방해','iksan-hakgyopokryeok-jeolcha':'학교폭력',
 'gunsan-gangje-jiphaeng-myeontal':'강제집행면탈','gunsan-dongeop-taltoe-jeongsan':'동업 탈퇴·정산','jeonju-sanggan-sosong-ihon-eopsi':'상간소송',
 'gunsan-seongbeomjoe-pihaeja':'성범죄 피해자 고소','jeonju-eumju-unjeon-byeonhosa':'음주운전 벌금','gunsan-samunseo-wijo':'사문서위조',
 'gunsan-daepo-tongjang-myeongija-sonhaebaesang':'대포통장 손해배상','seocheon-gunhyeongbeop-hyeongbeop':'군형사',
 'iksan-moyokjoe-seongnip-yogeon':'모욕죄','gunsan-seongbeomjoe-muhyeomui':'성범죄 무혐의','gunsan-wiheom-unjeon-chisang-gyoteuk':'위험운전치상·교특치상',
 'gunsan-jutaek-imdaecha-gaengsin':'전월세 갱신','gunsan-seongbeomjoe-neujeun-goso':'성범죄고소대응','gunsan-sanggan-wijaryo-aeksu':'상간 위자료',
 'gunsan-hakpok-haengjeongsimpan-chamga':'학폭 행정심판','jeonju-naeyongjeungmyeong':'내용증명','gunsan-voice-phishing-sugeochaek':'보이스피싱 수거책',
 'iksan-imdaecha-wonsanghoebok-tongsang-sonmo':'원상회복','gunsan-gunhyeongsa-yeongnae-pokhaeng':'군 영내 폭행',
 'gunsan-gyeongchal-josa-dongseok':'경찰조사 변호인 동석','iksan-dongeop-hoengnyeong':'동업자 횡령','gunsan-moyokjoe':'모욕죄 고소',
 'gunsan-instagram-gyejeong-jeongji':'인스타그램 계정정지','nonsan-ihon-sosong-gigan':'이혼소송','iksan-pigosoin-josa-daeeung':'피고소인조사',
 'gunsan-myeongye-hweson':'명예훼손 고소','jeonju-eogulhan-hakpok-gahaeja':'학폭가해학생','gunsan-jeoldojoe-cheobeol':'절도죄',
 'gunsan-gangje-jiphaeng-jeongji-gongtak':'강제집행정지','gunsan-bulsongchi-iuisincheong':'불송치 이의신청','gunsan-jun-gangje-chuhaeng':'준강제추행',
 'gimje-sanggan-sosong':'상간소송','gunsan-gosoin-josa-daeeung':'고소인 조사','gunsan-yeonin-jeungyeo-daeyeo':'연인 간 돈 반환',
 'iksan-eumju-unjeon-josa-ihu':'음주운전','gunsan-sangsok-gaesi-hal-il':'상속 기한','iksan-kamera-chwaryeong-forensic':'카메라등이용촬영',
 'gunsan-imdaecha-bojeunggeum-hoesu':'전세보증금 회수','boryeong-gongmuwon-jinggye':'공무원 징계','gunsan-sonyeon-jaepan-simni':'소년재판 심리',
 'gunsan-unjeonja-pokhaeng':'운전자폭행','iksan-daeyeogeum-banhwan':'대여금','gunsan-seongnyeon-hugyeon':'성년후견','gunsan-minsa-jojeong':'민사조정',
 'gunsan-eumju-unjeon-gyeongchal-josa':'음주운전 경찰조사','gunsan-yuryubun-banhwan':'유류분 반환','buan-jeonsesagi-daeeung':'전세사기',
}
def tag_group(tag):
    t = tag.strip()
    if '성범죄' in t: return '성범죄'
    if '음주' in t or '교통' in t: return '음주운전·교통'
    if '소년' in t: return '소년사건'
    if t.startswith('형사'): return '형사'
    if t.startswith('이혼'): return '이혼·상간'
    if t.startswith('가사'): return '상속·가사'
    if t.startswith('민사'): return '민사·부동산'
    if t.startswith('학교폭력'): return '학교폭력'
    return '노동·징계'
GROUP_ORDER = ['형사','성범죄','음주운전·교통','소년사건','이혼·상간','상속·가사','민사·부동산','학교폭력','노동·징계']

# 군산 키워드 지도 — (화면에 보일 키워드, 연결 대상). 대상이 None 이면 '작성 예정'(사이트에는 표시하지 않음).
# 같은 주제의 키워드는 한 페이지를 함께 가리킨다(키워드만 바꾼 복제 페이지를 만들지 않는다).
P = lambda s: f'practice-{s}.html'
B = lambda s: f'blog/{s}.html'
Q = lambda s: f'guide-gunsan-{s}.html'
KEYMAP = {
 '형사': [('형사변호사', P('criminal')), ('형사전문변호사', P('criminal')),
   ('경찰출신변호사', P('criminal')), ('경찰조사변호사', Q('gyeongchal-josa')), ('피의자변호사', Q('gyeongchal-josa')),
   ('공소청조사변호사', Q('gongsocheong-josa')), ('검찰조사변호사', Q('gongsocheong-josa')),
   ('구속영장변호사', Q('gusok-yeongjang')), ('영장실질심사변호사', Q('gusok-yeongjang')),
   ('구속적부심변호사', Q('gusok-jeokbusim-boseok')), ('보석변호사', Q('gusok-jeokbusim-boseok')),
   ('압수수색변호사', Q('apsu-susaek')),
   ('무혐의변호사', Q('muhyeomui')), ('무죄변호사', Q('mujoe')), ('기소유예변호사', Q('giso-yuye')), ('집행유예변호사', Q('jiphaeng-yuye')), ('선고유예변호사', Q('jiphaeng-yuye')),
   ('약식명령변호사', Q('yaksik-myeongryeong')), ('정식재판청구변호사', Q('yaksik-myeongryeong')),
   ('형사항소심변호사', Q('hangsosim')), ('형사합의변호사', Q('hapui-gongtak')), ('형사공탁변호사', Q('hapui-gongtak')),
   ('고소대리변호사', Q('goso-daeri')), ('범죄피해자변호사', Q('beomjoe-pihaeja')), ('피해자변호사', Q('beomjoe-pihaeja')),
   ('불송치이의신청변호사', Q('bulsongchi-iui')),
   ('폭행변호사', Q('pokhaeng-sanghae')), ('상해변호사', Q('pokhaeng-sanghae')), ('사기변호사', Q('sagi')), ('배임변호사', Q('baeim')), ('장물취득변호사', Q('jangmul')),
   ('공갈변호사', Q('gonggal')), ('협박변호사', Q('hyeopbak')), ('스토킹변호사', Q('stalking')),
   ('보이스피싱변호사', Q('voice-phishing')), ('횡령변호사', Q('hoengnyeong')),
   ('명예훼손변호사', Q('myeongye-hweson')), ('모욕변호사', Q('moyok')),
   ('업무방해변호사', Q('eommu-banghae')), ('사문서위조변호사', Q('samunseo-wijo')),
   ('절도변호사', Q('jeoldo')), ('무고변호사', Q('mugo')), ('마약변호사', None),
   ('거짓말탐지기', Q('geojitmal-tamjigi')), ('군형사변호사', Q('gunhyeongsa')),
   ('소년사건변호사', Q('sonyeon'))],
 '성범죄': [('성범죄변호사', P('sexual')), ('성범죄전문변호사', P('sexual')),
   ('강제추행변호사', 'guide-gunsan-gangje-chuhaeng.html'), ('준강제추행변호사', Q('jun-gangje-chuhaeng')),
   ('강간변호사', Q('gangan')), ('준강간변호사', Q('gangan')), ('성폭행변호사', Q('gangan')),
   ('카메라등이용촬영변호사', Q('kamera')), ('카촬변호사', Q('kamera')),
   ('통신매체이용음란변호사', Q('tongmaeeum')), ('통매음변호사', Q('tongmaeeum')),
   ('성범죄피의자변호사', Q('seongbeomjoe-piuija')), ('성범죄피해자변호사', Q('seongbeomjoe-pihaeja')),
   ('성범죄고소변호사', Q('seongbeomjoe-pihaeja')), ('성범죄무혐의변호사', Q('seongbeomjoe-muhyeomui')),
   ('성범죄합의변호사', None), ('성범죄뒤늦은고소변호사', Q('seongbeomjoe-piuija')), ('성범죄구속변호사', Q('gusok-yeongjang')), ('성범죄집행유예변호사', Q('jiphaeng-yuye')),
   ('성범죄항소심변호사', Q('hangsosim')), ('성범죄무고변호사', Q('mugo')),
   ('신상정보등록변호사', Q('sinsang-jeongbo')), ('아청법변호사', Q('acheongbeop')), ('성매매변호사', Q('seongmaemae')),
   ('직장내성희롱변호사', Q('seonghuirong'))],
 '음주운전·교통': [('음주운전변호사', P('dui')), ('음주운전전문변호사', P('dui')),
   ('음주운전경찰조사변호사', Q('eumju-josa')), ('음주운전재범변호사', Q('eumju-jaebeom')),
   ('면허취소변호사', Q('myeonheo-chwiso')), ('면허취소행정심판변호사', Q('myeonheo-chwiso')),
   ('교통사고변호사', Q('gyotong-sago')), ('교통사고전문변호사', Q('gyotong-sago')),
   ('위험운전치상변호사', Q('wiheom-unjeon')), ('뺑소니변호사', Q('ppaengsoni')), ('도주치상변호사', Q('ppaengsoni')),
   ('운전자폭행변호사', Q('unjeonja-pokhaeng')), ('무면허운전변호사', Q('mumyeonheo'))],
 '이혼·상간': [('이혼변호사', P('divorce')), ('이혼전문변호사', P('divorce')),
   ('이혼소송변호사', Q('ihon-sosong')), ('협의이혼변호사', Q('hyeopui-ihon')), ('이혼조정변호사', Q('ihon-jojeong')),
   ('유책배우자이혼변호사', Q('yuchaek-baeuja')), ('사실혼해소변호사', Q('sasilhon')),
   ('재산분할변호사', Q('jaesan-bunhal')), ('이혼후재산분할변호사', Q('jaesan-bunhal')),
   ('친권변호사', Q('chingwon-yangyuk')), ('양육권변호사', Q('chingwon-yangyuk')), ('면접교섭변호사', Q('myeonjeop-gyoseop')),
   ('양육비청구변호사', Q('yangyukbi')), ('과거양육비변호사', Q('yangyukbi')),
   ('상간소송변호사', Q('sanggan')), ('상간위자료변호사', Q('sanggan'))],
 '상속·가사': [('상속변호사', P('family')), ('상속전문변호사', P('family')),
   ('상속재산분할변호사', Q('sangsok-jaesan-bunhal')), ('유류분변호사', Q('yuryubun')),
   ('상속포기변호사', Q('sangsok-pogi')), ('한정승인변호사', Q('sangsok-pogi')),
   ('유언장변호사', Q('yueon')), ('유언효력변호사', Q('yueon')), ('성년후견변호사', Q('seongnyeon-hugyeon'))],
 '민사·부동산': [('민사변호사', P('civil')), ('민사전문변호사', P('civil')), ('부동산변호사', P('civil')),
   ('전세보증금변호사', Q('jeonse-bojeunggeum')), ('전세사기변호사', Q('jeonse-sagi')),
   ('대여금변호사', Q('daeyeogeum')), ('손해배상변호사', Q('sonhae-baesang')),
   ('공사대금변호사', Q('gongsa-daegeum')), ('명도소송변호사', Q('myeongdo')),
   ('공유물분할변호사', Q('gongyumul-bunhal')), ('강제집행정지변호사', Q('gangje-jiphaeng-jeongji')),
   ('강제집행면탈변호사', Q('gangje-jiphaeng-myeontal')), ('민사조정변호사', Q('minsa-jojeong')),
   ('원상회복변호사', Q('wonsang-hoebok')), ('임대차갱신변호사', Q('imdaecha-gaengsin')), ('동업분쟁변호사', Q('dongeop')),
   ('대포통장변호사', Q('voice-phishing')), ('SNS계정정지변호사', Q('sns-gyejeong'))],
 '학교폭력': [('학교폭력변호사', P('school')), ('학교폭력전문변호사', P('school')),
   ('학폭위변호사', Q('hakpokwi')), ('학폭행정심판변호사', Q('hakpok-haengjeongsimpan')),
   ('학폭가해학생변호사', Q('hakpok-gahae')), ('학폭피해학생변호사', Q('hakpok-pihae'))],
 '노동·징계': [('노동변호사', P('discipline')), ('징계변호사', P('discipline')),
   ('부당해고변호사', Q('budang-haego')), ('임금체불변호사', Q('imgeum-chebul')),
   ('직장내괴롭힘변호사', Q('goerophim')), ('공무원징계변호사', Q('gongmuwon-jinggye')),
   ('공무원감사변호사', Q('gongmuwon-gamsa')), ('군인징계변호사', Q('gunin-jinggye')), ('교원징계변호사', Q('gyowon-jinggye'))],
}

# 안내 페이지에 붙일 성공사례 (results.html 의 case-xx). 결과를 과장하지 않도록 사례 원문 그대로 옮긴다.
CASEMAP = {
 'guide-gunsan-gusok-yeongjang': ['case-18', 'case-08'], 'guide-gunsan-voice-phishing': ['case-08'],
 'guide-gunsan-gusok-jeokbusim-boseok': ['case-15'],
 'guide-gunsan-myeongye-hweson': ['case-02'], 'guide-gunsan-samunseo-wijo': ['case-03'],
 'guide-gunsan-eommu-banghae': ['case-04'], 'guide-gunsan-muhyeomui': ['case-01', 'case-09', 'case-02'], 'guide-gunsan-mujoe': ['case-12', 'case-09'],
 'guide-gunsan-gunhyeongsa': ['case-05'], 'guide-gunsan-giso-yuye': ['case-05'],
 'guide-gunsan-goso-daeri': ['case-06', 'case-07'], 'guide-gunsan-beomjoe-pihaeja': ['case-07', 'case-06'],
 'guide-gunsan-gangje-chuhaeng': ['case-06'], 'guide-gunsan-seongbeomjoe-pihaeja': ['case-06'],
 'guide-gunsan-sagi': ['case-09', 'case-11', 'case-18', 'case-10'], 'guide-gunsan-gonggal': ['case-10'],
 'guide-gunsan-gangan': ['case-12'], 'guide-gunsan-seongbeomjoe-muhyeomui': ['case-12'],
 'guide-gunsan-ppaengsoni': ['case-14'], 'guide-gunsan-gyotong-sago': ['case-14', 'case-17'],
 'guide-gunsan-hyeopbak': ['case-15'], 'guide-gunsan-hapui-gongtak': ['case-15'],
 'guide-gunsan-jiphaeng-yuye': ['case-15', 'case-13', 'case-17'], 'guide-gunsan-hangsosim': ['case-16'],
 'guide-gunsan-eumju-jaebeom': ['case-16'], 'guide-gunsan-eumju-josa': ['case-16'],
 'guide-gunsan-wiheom-unjeon': ['case-16', 'case-17'],
 'guide-gunsan-hoengnyeong': ['case-18'], 'guide-iksan-hoengnyeong': ['case-18'], 'guide-gunsan-dongeop': ['case-18'],
 'guide-gunsan-baeim': ['case-18'], 'guide-gunsan-mugo': ['case-18'], 'guide-gunsan-pokhaeng-sanghae': ['case-18'],
}
