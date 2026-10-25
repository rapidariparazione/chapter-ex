# 用法：python3 quotecheck.py <md> <原文.txt>
# 📖 后面引号里的英文，逐句到原文里找。弯引号、换页符、空白都先归一。
import re,sys
try: sys.stdout.reconfigure(encoding='utf-8',errors='replace')  # Windows 控制台默认不是 UTF-8
except Exception: pass
md=open(sys.argv[1],encoding='utf-8').read().replace('\r\n','\n')
norm=lambda s:re.sub(r'\s+',' ',s.replace('\f','').replace('“','"').replace('”','"').replace('’',"'").replace('‘',"'"))
S=norm(open(sys.argv[2],encoding='utf-8').read().replace('\r\n','\n'))
qs=re.findall(r'📖[^"]*"([^"]+)"',md)
ok=0
for q in qs:
    if norm(q).rstrip('.') in S: ok+=1
    else: print('MISS:',q)
print(ok,'/',len(qs))
