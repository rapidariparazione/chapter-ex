import re,html,sys
md=open(sys.argv[1],encoding='utf-8').read().split('\n')
E=html.escape
def inl(s):
    s=E(s,quote=False)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'(?<![\*\w])\*([^*]+?)\*(?!\*)',r'<i>\1</i>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',r'<a href="\2">\1</a>',s)
    s=re.sub(r'\[\^(\d+)\|([^\]]+)\]',r'<sup class="cite"><button type="button" class="cbtn">p.\1</button><span class="cpop" hidden>\2</span></sup>',s)
    return s
out=[];toc=[];i=0;in_card=False;mode='pre';intro=[];sty=''
title=md[0].lstrip('# ').replace('📝 ','')
def close():
    global in_card
    if in_card: out.append('</section>'); in_card=False
cards=0
while i<len(md):
    l=md[i]
    if i==0: i+=1; continue
    if l.startswith('> ') and mode=='pre':
        m=re.match(r'风格：\s*(\S+)',l[2:].strip())
        if m: sty={'手绘笔记':'sty-notes','杂志':'sty-mag','蓝图':'sty-blue','铜版':'sty-plate'}.get(m.group(1),'')
        intro.append(inl(l[2:])); i+=1; continue
    if l.strip()=='---' or not l.strip(): i+=1; continue
    if l.startswith('```html'):
        j=i+1; buf=[]
        while not md[j].startswith('```'): buf.append(md[j]); j+=1
        out.append('\n'.join(buf)); i=j+1; continue
    if l.startswith('```svg'):
        j=i+1; buf=[]
        while not md[j].startswith('```'): buf.append(md[j]); j+=1
        j+=1
        while j<len(md) and not md[j].strip(): j+=1
        cap=''
        if j<len(md) and (md[j].startswith('*图：') or md[j].startswith('*这张图回答：')): cap=inl(md[j].strip('*')); j+=1
        out.append('<figure class="pic">'+'\n'.join(buf)+(f'<figcaption>{cap}</figcaption>' if cap else '')+'</figure>'); i=j; continue
    if l.startswith('```'):
        j=i+1; buf=[]
        while not md[j].startswith('```'): buf.append(E(md[j],quote=False)); j+=1
        out.append('<div class="dia"><pre>'+'\n'.join(buf)+'</pre></div>'); i=j+1; continue
    if l.startswith('## '):
        mode='body'; close(); h=l[3:].strip(); sec=h
        if h!='正文': out.append(f'<h2 class="part">{inl(h)}</h2>')
        i+=1; continue
    if l.startswith('### '):
        close(); h=l[4:].strip(); in_card=True
        m=re.match(r'(\d+-\d+)\s+(.*)',h)
        if m:
            no,rest=m.groups(); sid='s'+no
            mm=re.match(r'(.*?)（([A-Za-z].*)）$',rest)
            t,en=(mm.group(1),mm.group(2)) if mm else (rest,None)
            toc.append(f'<a href="#{sid}"><span>{no}</span>{inl(t)}</a>')
            out.append(f'<section class="card" id="{sid}"><div class="cno">{no}</div><h3>{inl(t)}</h3>'+(f'<p class="en">{E(en)}</p>' if en else ''))
        else:
            cards+=1; out.append(f'<section class="card" id="c{cards}"><h3>{inl(h)}</h3>')
        i+=1; continue
    if l.startswith('#### '):
        out.append(f'<h4 class="lab">{inl(l[5:])}</h4>'); i+=1; continue
    if l.startswith('> 📖'):
        q=l[2:]
        if i+1<len(md) and md[i+1].startswith('> **译'):
            q=inl(q)+'<br>'+inl(md[i+1][2:]); i+=2
        else: q=inl(q); i+=1
        out.append(f'<blockquote class="src">{q}</blockquote>'); continue
    if l.startswith('<details>'):
        j=i+1; buf=[]; summ='展开答案'
        while not md[j].startswith('</details>'):
            if md[j].startswith('<summary>'): summ=re.sub(r'</?summary>','',md[j]).strip() or summ
            elif md[j].strip(): buf.append(md[j])
            j+=1
        # 块里一行一段，不并成一大段
        out.append(f'<details><summary>{summ}</summary>'+''.join(f'<p>{inl(x)}</p>' for x in buf)+'</details>'); i=j+1; continue
    if l.startswith('|'):
        rows=[]
        while i<len(md) and md[i].startswith('|'):
            if not re.match(r'^\|[-| ]+\|$',md[i]): rows.append([c.strip() for c in md[i].strip('|').split('|')])
            i+=1
        th=''.join(f'<th>{inl(c)}</th>' for c in rows[0]); tb=''.join('<tr>'+''.join(f'<td>{inl(c)}</td>' for c in r)+'</tr>' for r in rows[1:])
        out.append(f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'); continue
    if re.match(r'^- [A-D]\. ',l):
        opts=[]
        while i<len(md) and re.match(r'^- [A-D]\. ',md[i]):
            k=md[i][2]; opts.append(f'<button type="button" class="opt" data-k="{k}">{inl(md[i][2:])}</button>'); i+=1
        qid=''
        for prev in reversed(out):
            m=re.search(r'<b>((?:Q|猜)\d+)：',prev)  # 正文里的先猜再看
            if m: qid=m.group(1); break
        j=i
        while j<len(md) and not md[j].strip(): j+=1
        ans=''
        if j<len(md) and md[j].startswith('<details>'):
            k2=j
            while not md[k2].startswith('</details>'):
                mm=re.search(r'答案：([A-D])',md[k2])
                if mm: ans=mm.group(1); break
                k2+=1
        out.append(f'<div class="quiz" data-q="{qid}" data-ans="{ans}">'+''.join(opts)+'<p class="qres" hidden></p></div>'); continue
    if re.match(r'^(- |\d+\. )',l):
        tag='ol' if re.match(r'^\d+\. ',l) else 'ul'; items=[]
        while i<len(md) and re.match(r'^(- |\d+\. )',md[i]):
            items.append('<li>'+inl(re.sub(r'^(- |\d+\. )','',md[i]))+'</li>'); i+=1
        out.append(f'<{tag}>'+''.join(items)+f'</{tag}>'); continue
    # paragraph: join consecutive lines (直觉/实际 pairs)
    buf=[l]; i+=1
    while i<len(md) and md[i].strip() and not re.match(r'^(#|>|- |\d+\. |```|\||<|---)',md[i]): buf.append(md[i]); i+=1
    p='<br>'.join(inl(b) for b in buf)
    if p.startswith('<i>') and p.endswith('</i>') and in_card is False and sec not in ('先有困惑，再读理论',): pass
    out.append(f'<p>{p}</p>')
close()
kicker=sys.argv[2]
head=f'<!doctype html>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<title>{sys.argv[3]}</title>\n'  # 单独打开 HTML 时要有编码声明，不然中文乱码
nav=''
if len(sys.argv)>5: nav='\n  <nav class="pages" aria-label="同一篇的几张页">'+''.join(f'<a href="{u}">{n}</a>' for n,u in (x.split('=',1) for x in sys.argv[5].split(',')))+'</nav>'
body=(f'<div class="wrap {sty}">\n<header>\n  <div class="kicker">'+kicker+'</div>'+nav+'\n  <h1>'+inl(title)+'</h1>\n  <div class="intro">'+''.join(f'<div>{x}</div>' for x in intro)+'</div>\n</header>\n<nav class="toc" aria-label="目录">'+''.join(toc)+'</nav>\n'+'\n'.join(out)+'\n</div>\n')
D=__import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/'
open(sys.argv[4],'w',encoding='utf-8').write(head+open(D+'tpl_style.html',encoding='utf-8').read().replace('</style>',open(D+'pic.css',encoding='utf-8').read()+open(D+'styles.css',encoding='utf-8').read()+'</style>')+'\n'+body+open(D+'tpl_script.html',encoding='utf-8').read()+'\n')
print('cards',cards,'toc',len(toc))
