"""Build the printable agenda from the website's single itinerary dataset."""
import json,re,html
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image,ImageOps

ROOT=Path(__file__).parent
s=(ROOT/'index.html').read_text(encoding='utf-8')
days=json.loads(re.search(r'const days=(\[.*?\]);',s).group(1))
pdfmetrics.registerFont(TTFont('Agenda','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('AgendaBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Agenda',normal='Agenda',bold='AgendaBold')
OUT=ROOT/'output/pdf/sicily-daily-agenda.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(OUT),pagesize=(595,842))
c.setTitle('Sicilija | Tomas ir Elena | 2026-10-24 - 2026-11-03')
ink=HexColor('#183e47'); gold=HexColor('#bc653b'); muted=HexColor('#526568')
style=ParagraphStyle('body',fontName='Agenda',fontSize=10,leading=14,textColor=ink,spaceAfter=8)
y=0
def text(t,size=10,bold=False,color=None):
 global y
 st=ParagraphStyle('p',parent=style,fontSize=size,leading=size*1.4,fontName='AgendaBold' if bold else 'Agenda',textColor=color or ink)
 p=Paragraph(html.escape(t).replace('\n','<br/>'),st); w,h=p.wrap(503,800)
 if y-h<48: raise ValueError('Page overflow: '+t[:60])
 p.drawOn(c,46,y-h); y-=h+9
def base(label):
 global y
 c.setFillColor(HexColor('#fbf8f1'));c.rect(0,0,595,842,fill=1,stroke=0)
 c.setFillColor(gold);c.rect(46,790,44,4,fill=1,stroke=0)
 c.setFont('Agenda',9);c.setFillColor(muted);c.drawString(46,808,label)
 c.drawString(46,27,'Tomas ir Elena  |  Sicilija  |  Peržiūrėta 2026-10-22')
 c.drawRightString(549,27,str(c.getPageNumber()))
 y=771
def photo(path,caption,height=155):
 global y
 im=Image.open(path).convert('RGB'); im=ImageOps.fit(im,(1509,int(height*3)))
 fn=ROOT/('tmp/pdfs/banner-'+Path(path).stem+'-'+str(height)+'.jpg'); im.save(fn,quality=88)
 c.drawImage(str(fn),46,y-height,width=503,height=height); y-=height+5
 text(caption,8,color=muted)
notes={
'10-24':'Oras: Giardini Naxos apie 22/13 °C, popietę galimas lietus. Palikite lengvą atvykimo dieną.',
'10-25':'ORO ALTERNATYVA: Giardini Naxos prognozėje apie 17/13 °C ir lietus. Tai nėra Etnos kalnų prognozė. 10-24 vakare su gidu patikrinti vėją, matomumą, kritulius ir prieigą; prireikus tartis dėl 10-26. Bėgimų datos lieka tos pačios.',
'10-26':'Galima atsarginė Etnos diena tik gavus gido patvirtinimą. Po 12 km bėgimo reikėtų išvykti anksčiau nei į Savoca: aptarti vėlesnį gido laiką arba kitą variantą, neskubinti bėgimo. Pakrantėje apie 20/14 °C, galimi rytiniai lietūs.',
'10-27':'Pakrantėje prognozuojami lietaus periodai, apie 20/13 °C. Taorminą lankyti per oro tarpus; Castelmola ir Isola Bella trumpinti esant lietui, vėjui ar prastam matomumui.',
'10-28':'Rytų pakrantėje apie 20/16 °C, daugiausia saulėta. Cefalù ir vakarų maršruto orus dar tikrinti atskirai. Persikėlimo dienos papildomai neapkrauti.',
'10-31':'Šeštadienį papildyti atsargas lapkričio 1 d. šventei. Konkrečios dienos orų šiame leidime netvirtiname; Erice vizitą trumpinti esant rūkui ar vėjui.',
'11-01':'2026-10-22 oficialus Zingaro puslapis nurodo visus takus atvirus ir 08:00-16:00. 10-31 patikrinti dar kartą. Po dviejų 14 km bėgimų rinktis 4-6 km, išeiti iki 15:30. Lapkričio 1 d. orų šiame leidime netvirtiname.'}
base('KELIONĖS AGENDA  /  11 DIENŲ')
text('Sicilija',40,True)
text('2026 m. spalio 24 - lapkričio 3 d.',17)
photo(ROOT/'assets/coast.jpg','Zingaro pakrantė. The Cosmonaut / CC BY-SA 2.5 CA; apkirpta.',230)
text('Dvi bazės. Vulkanas. Miesteliai. Pajūris.',18,True)
text('10-24-10-28: Donna Lucia, Giardini Naxos\n10-28-11-02: Sofia Rooms, Castellammare del Golfo\n11-02-11-03: grįžimas per Varšuvą')
text('Mano prioritetai',13,True)
text('Etna Nord su gidu; Taormina ir Castelmola; Cefalù trumpam sustojimui; Erice ir salinos; Zingaro bei Scopello. Montelepre ir Corleone palikti jūsų „Siciliečio“ temai.')
text('Svarbiausias mažas pakeitimas',13,True)
text('Etnos datą laikyti lanksčią. 10-25 prognozuojamas pakrantės lietus; 10-26 aptarti kaip atsargą, tik suderinus gidą ir 12 km bėgimo rytą. Nakvynių ir treniruočių kalendoriaus nekeisti automatiškai.')
c.showPage()
for d in days:
 base('DIENOS PLANAS  /  2026-'+d['date'])
 text(d['date']+'  |  '+d['dow'],13,True,color=gold)
 text(d['title'],22,True)
 text(d['brief'],11,color=muted)
 if d['date']=='10-25': photo(ROOT/'assets/etna.jpg','Etna, 2002 m. krateriai. Nuotraukos šaltinis: pianoprovenzana.com.',115)
 if d['date']=='11-01': photo(ROOT/'assets/coast.jpg','Zingaro pakrantė. The Cosmonaut / CC BY-SA 2.5 CA; apkirpta.',115)
 text('RYTAS',10,True,color=gold)
 text(d['morning'],9)
 text('DIENOS EIGA',10,True,color=gold)
 for step in d['steps']:
  # Morning has its own block; keep the detailed timeline concise.
  text(step,8.8)
 if d['date'] in notes:
  text('REKOMENDACIJA IR ORAS',10,True,color=gold);text(notes[d['date']],9)
 elif d['date']>='10-29':
  text('ORAS',10,True,color=gold);text('Šios dienos patikimos prognozės šiame leidime netvirtiname. Patikrinkite vietinę prognozę likus 48 val. ir išvykimo rytą.',9)
 if d.get('meal') and y>120:
  text('VAKARAS  |  '+d.get('dinnerTime',''),10,True,color=gold)
  text(d.get('dishRecommendation',''),9)
 text('Nakvynė: '+d['night'],9,True)
 c.showPage()
base('ŠALTINIAI IR PRAKTINĖ ATMINTINĖ')
text('Prieš išvykstant',25,True)
for t in ['Etna: patvirtinti datą, 10:00 susitikimą ir leidžiamą maršrutą. Operatorius skelbia 5 km, apie 3 val., +300 m, 30 € žmogui; rezervacija ir minimalus dalyvių skaičius būtini.', 'Zingaro: 10-31 dar kartą patikrinti prieigą ir orą. Turėti vandens, užkandžių, tinkamus batus; trumpas maršrutas grįžta prie to paties automobilio.', 'Orų duomenys tikrinti 2026-10-22, pakrantės prognozė Giardini Naxos 10-24-10-28. Kalnų orai atskiri; vėlesnių dienų prognozės nepateikiamos kaip patvirtintos.', 'Spalio 25 d. Italija pereina į žiemos laiką. Agenda Italijoje naudoja vietinį laiką; Lietuva viena valanda priekyje. Gidai, muziejai, vakarienių ir autobusų vietos nėra užsakyti šiuo dokumentu.']:
 text(t)
sources=[('Interaktyvus planas','https://tomlebedev-cloud.github.io/sicily-trip/'),('Etna Nord programa','https://pianoprovenzana.com/excursion/hike-craters-2002/'),('Etnos prieigos taisyklės','https://parcoetna.it/ordinanze-sindaci/'),('Zingaro: takai ir valandos','https://www.riservazingaro.it/en/home/'),('Orų įspėjimai','https://www.meteoam.it/'),('Pakrantės orų pakartotinė patikra','https://www.meteoam.it/it/meteo-citta/giardini-naxos'),('Pakrantės nuotrauka: The Cosmonaut, CC BY-SA 2.5 CA','https://commons.wikimedia.org/wiki/File:Zingaro_coast_viewed_from_the_Coastal_Trail.jpg'),('Nuotraukos licencija; kadras apkirptas','https://creativecommons.org/licenses/by-sa/2.5/ca/'),('Etnos nuotrauka: Piano Provenzana; teisės priklauso šaltiniui','https://pianoprovenzana.com/excursion/hike-craters-2002/')]
for label,url in sources:
 text(label,10,True);top=y;text(url,8,color=muted);c.linkURL(url,(46,y+7,549,top+3),relative=0)
c.save()
print(OUT)


