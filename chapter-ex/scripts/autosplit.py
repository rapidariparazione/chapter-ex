import re,sys
try: sys.stdout.reconfigure(encoding='utf-8',errors='replace')  # Windows 控制台默认不是 UTF-8
except Exception: pass
F=sys.argv[1]; write=len(sys.argv)>2
def L(s): return len(re.sub(r'[A-Za-z][A-Za-z\-\' ]*','A',re.sub(r'[\s*#>\-（）()「」，、：；·0-9]','',s)))
text=open(F,encoding='utf-8').read().replace('\r\n','\n')
parts=re.split(r'(```.*?```)',text,flags=re.S)
changes=[]
def fix_line(line):
    if '|' in line or line.startswith('📖') or '📖' in line: return line
    m=re.match(r'^((?:- |> |\d+\. )?(?:\*\*[^*]{1,12}：\*\*\s*)?)(.*)$',line)
    pre,body=m.groups()
    segs=re.split(r'(?<=[。！？?!])',body)
    out=[]
    for s in segs:
        if L(s)<=25: out.append(s); continue
        # candidate commas outside brackets
        depth=0; cands=[]
        for i,ch in enumerate(s):
            if ch in '「（(': depth+=1
            elif ch in '」）)': depth-=1
            elif ch in '，；：' and depth==0: cands.append(i)
        best=None
        for i in cands:
            a,b=s[:i],s[i+1:]
            if L(a)<=25 and L(b)<=25 and L(a)>=4 and L(b)>=4:
                sc=abs(L(a)-L(b))
                if best is None or sc<best[0]: best=(sc,i)
        if best:
            i=best[1]; end='。' 
            ns=s[:i]+end+s[i+1:]
            changes.append((s,ns)); out.append(ns)
        else: out.append(s); changes.append((s,'!!未拆'))
    return pre+''.join(out)
for k in range(0,len(parts),2):
    parts[k]='\n'.join(fix_line(l) for l in parts[k].split('\n'))
for a,b in changes: print('-',a.strip()[:70]); print('+',b.strip()[:70])
if write: open(F,'w',encoding='utf-8').write(''.join(parts))
