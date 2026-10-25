import subprocess, os, sys
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LABELS={
 '01':('건조물침입·권리행사방해','불송치 (혐의없음)'),'02':('허위사실적시 명예훼손','불송치 (혐의없음)'),
 '03':('사문서위조 및 동행사','불송치 (혐의없음)'),'04':('업무방해','불송치 (혐의없음)'),
 '05':('직무수행군인등 상해','기소유예'),'06':('강제추행 고소대리','검찰 송치'),'07':('체포 고소대리','검찰 송치'),
 '08':('보이스피싱 구속영장 청구','구속영장 기각'),'09':('사기','불송치 (혐의없음)'),
 '10':('사기·공갈·음란물 유포','집행유예'),'11':('사기','불송치 (혐의없음)'),'12':('특수강간','불송치 (혐의없음)'),
 '13':('대부업법 위반','집행유예'),'14':('특가법 위반 (도주치상)','불기소'),
 '15':('보복협박·특수협박·주거침입','집행유예'),'16':('교특법 위반 (치상)·음주운전','집행유예'),'17':('교특법 위반 (치상)','집행유예'),'19':('사기 고소대리','검찰 송치'),
}
out=sys.argv[1] if len(sys.argv)>1 else '/tmp/restamp'
os.makedirs(out,exist_ok=True)
for n,(t,b) in LABELS.items():
    subprocess.run(['python3','tools/restamp.py',f'images/case-{n}.jpg',f'{out}/case-{n}.jpg',t,b,f'{out}/case-{n}-thumb.jpg'],check=True)
tiles=[]
for n in LABELS:
    im=Image.open(f'{out}/case-{n}.jpg'); h=560; im=im.resize((int(im.width*h/im.height),h))
    c=Image.new('RGB',(im.width,h+34),'white'); c.paste(im,(0,34)); ImageDraw.Draw(c).text((8,6),n,fill='black'); tiles.append(c)
cols=6; rows=(len(tiles)+cols-1)//cols; tw=max(t.width for t in tiles); th=tiles[0].height
sheet=Image.new('RGB',(cols*(tw+8),rows*(th+8)),'#ddd')
for i,t in enumerate(tiles): sheet.paste(t,((i%cols)*(tw+8),(i//cols)*(th+8)))
sheet.save('/home/claude/stamp_preview_all.jpg',quality=80)
