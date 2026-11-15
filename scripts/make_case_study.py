"""Generate four-page portrait PDF carousel using vector typography and charts."""
from __future__ import annotations
import json
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/'artifacts/evaluation_metrics.json').read_text())
OUT=ROOT/'docs/PROJECT_CASE_STUDY.pdf'
font='/usr/share/fonts/truetype/lato/'
pdfmetrics.registerFont(TTFont('Lato',font+'Lato-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LatoBold',font+'Lato-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LatoHeavy',font+'Lato-Heavy.ttf'))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='LatoBold')
W,H=640,800
BG=HexColor('#120E20'); CARD=HexColor('#231C37'); CARD2=HexColor('#2C2542')
LILAC=HexColor('#C5B5FF'); GOLD=HexColor('#FFC97E'); MINT=HexColor('#64DBC0'); WHITE=HexColor('#FCF8FF'); MUTED=HexColor('#C0B9D0'); LINE=HexColor('#50445D'); CORAL=HexColor('#FF9C9D')
can=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
can.setTitle('Rogue Agent Sentinel Lab | Project 03 — By Adiputera Saadon')
can.setAuthor('Adiputera Saadon')

def rect(x,y,w,h,fill,rad=13,stroke=None):
    can.setFillColor(fill)
    if stroke:
        can.setStrokeColor(stroke);can.setLineWidth(.8)
    can.roundRect(x,y,w,h,rad,stroke=int(stroke is not None),fill=1)

def t(x,y,s,size=12,color=WHITE,fontname='Lato'):
    can.setFont(fontname,size);can.setFillColor(color);can.drawString(x,y,s)

def para(x,y_top,width,s,size=12,leading=None,color=WHITE,bold=False):
    st=ParagraphStyle('dyn',fontName='LatoBold' if bold else 'Lato',fontSize=size,leading=leading or size*1.36,textColor=color,spaceBefore=0,spaceAfter=0,allowWidows=0,allowOrphans=0)
    p=Paragraph(s,st)
    _,height=p.wrap(width,650)
    p.drawOn(can,x,y_top-height)
    return y_top-height

def top(page,label,title,desc):
    can.setFillColor(BG);can.rect(0,0,W,H,fill=1,stroke=0)
    can.setFillColor(GOLD);can.rect(0,H-8,W,8,stroke=0,fill=1)
    t(42,H-52,'ROGUE AGENT SENTINEL  /  LAB 03',9,GOLD,'LatoBold')
    t(W-90,H-52,f'{page:02d} / 04',9,MUTED,'LatoBold')
    can.setStrokeColor(LINE);can.line(42,H-66,W-42,H-66)
    t(42,H-109,title,29,WHITE,'LatoHeavy')
    para(42,H-129,W-84,desc,12,17,MUTED)

def footer(page):
    can.setStrokeColor(LINE);can.line(42,39,W-42,39)
    t(42,24,'FICTIONAL PROPOSALS   |   EDUCATIONAL SIMULATION   |   NO LIVE AGENTS',7.2,MUTED,'LatoBold')
    t(W-91,24,f'{page:02d} / 04',8,GOLD,'LatoBold')

def bar(x,y,w,value,fill):
    rect(x,y,w,18,HexColor('#413957'),7)
    if value>0: rect(x,y,w*value,18,fill,7)

# Page 1 — cover
can.setFillColor(BG);can.rect(0,0,W,H,stroke=0,fill=1)
can.setFillColor(GOLD);can.rect(0,H-8,W,8,stroke=0,fill=1)
t(45,735,'PROJECT 03   /   AGENTIC AI GOVERNANCE',11,GOLD,'LatoBold')
can.setStrokeColor(LINE);can.line(45,712,W-45,712)
t(44,630,'ROGUE AGENT',49,WHITE,'LatoHeavy')
t(44,577,'SENTINEL LAB',49,LILAC,'LatoHeavy')
para(46,545,540,'Monitoring fictional AI-agent behaviour, enforcing bounded authority and preserving human accountability.',17,23,MUTED)
rect(45,303,550,159,CARD,19)
t(66,425,'THE CENTRAL QUESTION',11,GOLD,'LatoBold')
para(66,400,505,'What happens when an autonomous AI agent requests an action beyond its authority?',22,29,WHITE,True)
para(66,332,507,'Detect the deviation. Hold or block the proposed action. Keep a human responsible.',13,18,LILAC)
for i,(name,desc) in enumerate([
    ('01  SANCTIONS','Read and draft, never alter a list'),
    ('02  AML','Analyse and flag, never freeze funds'),
    ('03  INVESTIGATIONS','Summarise evidence, never export cases'),
]):
    y=241-i*64
    rect(45,y,550,52,CARD2,11)
    t(65,y+28,name,11,MINT,'LatoBold')
    t(65,y+11,desc,11,MUTED)
can.setStrokeColor(LINE);can.line(45,43,595,43)
t(45,26,'AN INDEPENDENT EDUCATIONAL PORTFOLIO EXPERIMENT',8,MUTED,'LatoBold')
t(550,26,'01 / 04',8,GOLD,'LatoBold')
can.showPage()

# Page 2 — the architecture
top(2,'ARCHITECTURE','The authority boundary','Three fictional agents propose actions. An independent policy engine decides whether each proposal should proceed, be blocked or held.')
t(43,600,'THREE REGISTERED AGENTS',10,GOLD,'LatoBold')
for i,(a,role,tools) in enumerate([
    ('01','Sanctions screening','Read fictional watchlists / draft match notes'),
    ('02','AML monitoring','Read fictional transactions / flag cases'),
    ('03','Investigation copilot','Read fictional case files / draft narratives'),
]):
    y=519-i*94
    rect(42,y,556,79,CARD)
    rect(54,y+17,43,43,LILAC,11)
    t(64,y+31,a,14,BG,'LatoHeavy')
    t(112,y+49,role,17,WHITE,'LatoBold')
    t(112,y+24,tools,11,MUTED)
t(43,314,'THE PRE-ACTION CONTROL',10,GOLD,'LatoBold')
steps=[('01','CHECK','Registered agent, approved tool, trusted target'),('02','DECIDE','ALLOW, BLOCK or HOLD for independent review'),('03','RECORD','Evidence, rationale and simulated action outcome')]
for i,(num,heading,desc) in enumerate(steps):
    y=245-i*72
    rect(42,y,556,61,CARD2)
    t(59,y+26,num,15,GOLD,'LatoHeavy')
    t(104,y+33,heading,13,MINT,'LatoBold')
    t(104,y+15,desc,10.8,WHITE)
rect(42,49,556,42,HexColor('#352537'))
para(57,78,525,'<b>Scope limit</b>  No tool is executed, no bank account is affected and suspension changes only the session simulation.',10,13,WHITE)
footer(2);can.showPage()

# Page 3 — results
top(3,'RESULTS','Test what the claims mean','Independent policy gates and anomaly detectors should be evaluated separately. Their weaknesses are not interchangeable.')
for i,(num,name) in enumerate([(str(M['total_events']),'FICTIONAL PROPOSALS'),(str(M['episodes']),'DISJOINT EPISODES'),(str(M['test_events']),'HOLDOUT PROPOSALS')]):
    x=42+i*190
    rect(x,537,176,86,CARD)
    t(x+15,577,num,30,WHITE,'LatoHeavy')
    t(x+15,552,name,9,MUTED,'LatoBold')
t(42,502,'SYNTHETIC HOLDOUT  /  8 SCRIPTED UNSAFE ACTIONS',10,GOLD,'LatoBold')
rect(42,340,556,145,CARD)
t(60,455,'ACTION GATE',13,WHITE,'LatoBold')
t(325,455,'ANOMALY TRIAGE',13,WHITE,'LatoBold')
t(60,420,'8 / 8 detected or held',15,MINT,'LatoBold')
t(325,420,'2 / 8 flagged',15,CORAL,'LatoBold')
bar(60,387,235,1.0,MINT)
bar(325,387,235,.25,CORAL)
t(60,356,'0 false alarms',11,MUTED)
t(325,356,'16 false alarms',11,MUTED)
rect(42,208,556,110,HexColor('#31253B'))
t(57,291,'WHY THE PERFECT POLICY SCORE IS NOT PROOF',11,GOLD,'LatoBold')
para(57,278,520,'The fictional unsafe labels are engineered around the same policy semantics used by the rule gate. Its 100% result is <b>by construction</b>, not evidence that it can resist a real attacker. The anomaly detector also misses six scripted unsafe proposals.',11,15,WHITE)
t(42,171,'THE GOVERNANCE LESSON',10,GOLD,'LatoBold')
para(42,156,552,'<b>Permissions protect the boundary.</b> Anomaly signals can help prioritise investigation, but must never authorise a prohibited tool call or replace human judgement.',13,18,LILAC)
footer(3);can.showPage()

# Page 4 — explore
# custom top for more space
top(4,'EXPLORE','Govern what agents do','Six interactive sections turn governance principles into inspectable fictional workflows and explicit limitations.')
sections=[('01','Agent Registry','Owners, tools and bounded authority'),('02','Activity Monitor','Filter simulated agent actions and outcomes'),('03','Rogue Detection','Compare deterministic and statistical alarms'),('04','Policy Enforcement','Block, hold and simulate suspension'),('05','Human Review','Record decisions and export session CSV'),('06','AI Governance','Evidence matrix, gaps and provenance')]
for i,(num,name,desc) in enumerate(sections):
    row,col=divmod(i,2)
    x=42+col*283;y=492-row*105
    rect(x,y,273,91,CARD)
    t(x+16,y+62,num,11,GOLD,'LatoBold')
    t(x+47,y+62,name,14,WHITE,'LatoBold')
    para(x+16,y+45,245,desc,10.7,14,MUTED)
rect(42,115,556,74,HexColor('#302840'))
t(58,162,'KEY LIMITATIONS',10,GOLD,'LatoBold')
para(58,150,520,'No live AI agents. No genuine tool execution, network access controls, signed audit trail, real incident response or regulatory approval. Results are synthetic and educational.',11,15,WHITE)
t(42,89,'Built for inquiry, testing and constructive challenge.',12,LILAC,'LatoBold')
can.setStrokeColor(LINE);can.line(42,69,W-42,69)
t(42,47,'By Adiputera Saadon',14,GOLD,'LatoBold')
t(W-90,47,'04 / 04',9,MUTED,'LatoBold')
can.showPage()
can.save()
print(OUT,OUT.stat().st_size)
