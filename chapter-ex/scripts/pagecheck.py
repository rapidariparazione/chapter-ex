# 用法：python3 pagecheck.py <md> <原书.pdf>
# 每个小节（### N-M）要有一行「**页码：** 第 A 到 B 页」。
# 拿这一节第一句 📖 引文，到 PDF 第 A 到 B 页里找。找到才算页码对。
import re,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pdftext import page_text
try: sys.stdout.reconfigure(encoding='utf-8',errors='replace')  # Windows 控制台默认不是 UTF-8
except Exception: pass
md=open(sys.argv[1],encoding='utf-8').read().replace('\r\n','\n')
norm=lambda s:re.sub(r'\s+',' ',s.replace('\f','').replace('“','"').replace('”','"').replace('’',"'").replace('‘',"'"))
secs=re.split(r'\n(?=### \d+-\d+ )',md)[1:]
ok=0
for s in secs:
    name=s.split('\n',1)[0][4:40]
    m=re.search(r'\*\*页码：\*\*\s*第\s*(\d+)(?:\s*到\s*(\d+))?\s*页',s)
    q=re.search(r'📖[^"]*"([^"]+)"',s)
    if not m: print('无页码:',name); continue
    if not q: print('无引文:',name); continue
    a=int(m.group(1)); b=int(m.group(2) or a)
    t=norm(page_text(sys.argv[2],a,b))
    if norm(q.group(1)).rstrip('.') in t: ok+=1
    else: print(f'不在第 {a}-{b} 页:',name)
cites=re.findall(r'\[\^(\d+)\|📖[^"]*"([^"]+)"\]',md); cok=0
for p,q in cites:
    t=norm(page_text(sys.argv[2],int(p),int(p)))
    if norm(q).rstrip('.') in t: cok+=1
    else: print(f'角标不在第 {p} 页:',q[:40])
print('角标',cok,'/',len(cites))
print(ok,'/',len(secs))
