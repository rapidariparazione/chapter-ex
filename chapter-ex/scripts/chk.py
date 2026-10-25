import re,sys
md=open(sys.argv[1],encoding='utf-8').read()
body=re.sub(r'```.*?```','',md,flags=re.S)
body=re.sub(r'\[\^\d+\|[^\]]*\]','',body)  # 角标里的原句不算句长，也别让下一行把整行吞掉
body=re.sub(r'📖.*','',body)
out=[]
for line in body.split('\n'):
    if '|' in line: continue
    line=re.sub(r'^(- |> )?\*\*[^*]{1,12}：\*\*\s*','',line)
    line=re.sub(r'\]\([^)]*\)',']',line)  # 链接的网址不算字数
    for s in re.split(r'[。！？?!]',line):
        n=len(re.sub(r'[A-Za-z][A-Za-z\-\' ]*','A',re.sub(r'[\s*#>\-（）()「」，、：；·0-9]','',s)))
        if n>25: out.append(s.strip())
print(len(out))
for s in out[int(sys.argv[2]) if len(sys.argv)>2 else 0:]: print('•',s)
vis=re.sub(r'<details>.*?</details>','',md,flags=re.S); vis=re.sub(r'```.*?```','',vis,flags=re.S); vis=re.sub(r'\[\^\d+\|[^\]]*\]','',vis)
print('默认可见汉字',len(re.findall(r'[\u4e00-\u9fff]',vis)))
