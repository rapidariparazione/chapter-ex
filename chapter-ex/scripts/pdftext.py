# 用法：python3 pdftext.py <原书.pdf> <原文.txt> [起页 止页]
# 从 PDF 抽文字。有 poppler 的 pdftotext 就用它，没有就用 pypdf（pip install pypdf）。
# 其他脚本也从这里 import page_text。
import shutil,subprocess,sys
try: sys.stdout.reconfigure(encoding='utf-8',errors='replace')
except Exception: pass

def page_text(pdf,first=None,last=None,layout=False):
    if shutil.which('pdftotext'):
        args=['pdftotext']+(['-layout'] if layout else [])
        if first: args+=['-f',str(first),'-l',str(last or first)]
        return subprocess.run(args+[pdf,'-'],capture_output=True,text=True,encoding='utf-8',errors='replace').stdout
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit('抽不了 PDF 文字：没找到 pdftotext，也没装 pypdf。最省事的办法：pip install pypdf')
    r=PdfReader(pdf); n=len(r.pages)
    a=(first or 1)-1; b=min(last or first or n, n) if first else n
    return '\f'.join((r.pages[i].extract_text() or '') for i in range(a,b))

if __name__=='__main__':
    if len(sys.argv)<3: sys.exit('用法：python3 pdftext.py <原书.pdf> <原文.txt> [起页 止页]')
    f=int(sys.argv[3]) if len(sys.argv)>3 else None
    l=int(sys.argv[4]) if len(sys.argv)>4 else f
    t=page_text(sys.argv[1],f,l,layout=True)
    open(sys.argv[2],'w',encoding='utf-8').write(t)
    print('写入',sys.argv[2],len(t),'字符')
