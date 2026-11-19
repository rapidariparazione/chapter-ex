"""英文页检查：python3 en_check.py ch.md
报：平均句长、长句占比、未注生僻词占比、FK 年级、括号外汉字数、每大节题数、末尾有没有题。
判据（Lexile 850 的近似，不是官方 Lexile 分）：
  平均句长 11-15 词；超过 22 词的句子 <= 10%；未注生僻词（Zipf<3.2，句中小写，后面没跟（中文））<= 2%；
  括号外汉字 = 0；每个 ### NN-N 大节恰好 5 道 Q；最后一个大节之后没有 Q。"""
import re,sys
try: sys.stdout.reconfigure(encoding='utf-8',errors='replace')  # Windows 控制台默认不是 UTF-8
except Exception: pass

from wordfreq import zipf_frequency
def zipf(word):  # 粗略还原词形，取最常见的那个
    w=word.lower().strip("'’-"); v=[w]
    for suf,rep in (("ies","y"),("es",""),("s",""),("ied","y"),("ed",""),("ed","e"),("ing",""),("ing","e"),("ly",""),("er",""),("est","")):
        if w.endswith(suf) and len(w)-len(suf)>=3:
            b=w[:-len(suf)]+rep; v.append(b)
            if len(b)>=2 and b[-1]==b[-2]: v.append(b[:-1])
    return max(zipf_frequency(x,'en') for x in v)
t=open(sys.argv[1],encoding='utf-8').read().replace('\r\n','\n')
t=re.sub(r'^## Key words.*?(?=^## )','',t,flags=re.S|re.M)  # 关键词那一节的解释是中文，不算
gl_terms=re.findall(r'\{\{([^|{}]+)\|[^{}]+\}\}',t)
print('点查词组',len(gl_terms),'个')
t=re.sub(r'\{\{([^|{}]+)\|[^{}]+\}\}',r'\1',t)
# 去掉代码块、引文、角标、原文折叠块、html 标签
body=re.sub(r'```.*?```','',t,flags=re.S)
body=re.sub(r'<details>\s*<summary>Original text.*?</details>','',body,flags=re.S|re.I)
body=re.sub(r'\[\^\d+\|[^\]]*\]','',body)
body='\n'.join(l for l in body.split('\n') if not l.startswith('> 📖') and not re.match(r'^\s*<',l))
body=re.sub(r'<[^>]+>','',body)
# 括号外汉字
han_out=len(re.findall(r'[一-鿿]',re.sub(r'（[^）]*）','',body)))
glossed=set(w.lower() for g in gl_terms for w in re.findall(r"[A-Za-z][A-Za-z'-]*",g))|set(w.lower() for w in re.findall(r"([A-Za-z][A-Za-z'-]*)\s*（[^）]*[一-鿿][^）]*）",body))
plain=re.sub(r'（[^）]*）','',body)
plain=re.sub(r'[#*>`|]','',plain)
sents=[s for s in re.split(r'(?<=[.!?])\s+|\n+',plain) if len(re.findall(r"[A-Za-z]+",s))>=3]
wc=[len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*",s)) for s in sents]
words=[];rare=[]
for s in sents:
    for i,m in enumerate(re.finditer(r"[A-Za-z][A-Za-z'’-]*",s)):
        w=m.group(0); words.append(w)
        if len(w)<3 or (i>0 and w[0].isupper()): continue
        if w.lower() in glossed: continue
        if zipf(w)<3.2: rare.append(w.lower())
def syl(w):
    w=w.lower(); n=len(re.findall(r'[aeiouy]+',w)); n-= w.endswith('e') and n>1; return max(1,n)
fk=0.39*sum(wc)/len(wc)+11.8*sum(syl(w) for w in words)/len(words)-15.59
print(f'句子 {len(sents)}，平均句长 {sum(wc)/len(wc):.1f} 词，>22 词 {sum(x>22 for x in wc)/len(wc):.0%}')
print(f'未注生僻词 {len(rare)}/{len(words)} = {len(rare)/len(words):.1%}；FK 年级 {fk:.1f}')
from collections import Counter
print('最常见未注生僻词：',', '.join(f'{w}×{n}' for w,n in Counter(rare).most_common(15)))
print('括号外汉字',han_out)
# 题数
secs=[(m.start(),m.group(1)) for m in re.finditer(r'^### (\d+-\d+)',t,flags=re.M)]
qs=[m.start() for m in re.finditer(r'^\*\*Q\d+[：:]',t,flags=re.M)]
nxt=[m.start() for m in re.finditer(r'^#{2,3} ',t,flags=re.M)]
for k,(p,no) in enumerate(secs):
    end=min([x for x in nxt if x>p]+[len(t)])
    print(no,'题数',sum(p<q<end for q in qs))
last=max(p for p,_ in secs); lastend=min([x for x in nxt if x>last]+[len(t)])
print('最后一节之后的 Q',sum(q>lastend for q in qs))
ids=re.findall(r'^\*\*((?:Q|G)\d+)[：:]',t,flags=re.M); print('题号重复',[x for x,n in Counter(ids).items() if n>1])
