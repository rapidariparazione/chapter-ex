# 用法：python3 figshot.py <art.html> [out.png]
# 把页面里所有插图抽出来排成一页，用 headless Chrome 截图。截完打开 png 看原尺寸。
import re,sys,subprocess,os,shutil,pathlib
try: sys.stdout.reconfigure(encoding='utf-8',errors='replace')  # Windows 控制台默认不是 UTF-8
except Exception: pass
def chrome():
    c=os.environ.get('CHROME')
    if c and os.path.exists(c): return c
    for c in ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','/Applications/Chromium.app/Contents/MacOS/Chromium','/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',r'C:\Program Files\Google\Chrome\Application\chrome.exe',r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe']:
        if os.path.exists(c): return c
    for c in ['google-chrome','google-chrome-stable','chromium','chromium-browser','microsoft-edge','msedge']:
        if shutil.which(c): return shutil.which(c)
    sys.exit('没找到 Chrome / Chromium / Edge。装一个，或设环境变量 CHROME=浏览器路径。')
h=open(sys.argv[1],encoding='utf-8').read().replace('\r\n','\n')
out=sys.argv[2] if len(sys.argv)>2 else sys.argv[1].rsplit('.',1)[0]+'-figs.png'
figs=re.findall(r'<figure class="pic"[^>]*>.*?</figure>',h,re.S)
# 动态图：去掉 data-dyn，滑动的元素直接放到终点，截出来是最后一步
figs=[re.sub(r'--to:([^;"]+)',r'transform:\1',re.sub(r'<figure class="pic"[^>]*>','<figure class="pic">',f,1)) for f in figs]
style=re.search(r'<style>.*?</style>',h,re.S).group(0)
tmp=os.path.abspath(out.rsplit('.',1)[0]+'.html')
open(tmp,'w',encoding='utf-8').write('<html><head><meta charset="utf-8">'+style+'</head><body style="width:760px;padding:20px">'+''.join(figs)+'</body></html>')
subprocess.run([chrome(),'--headless','--disable-gpu','--hide-scrollbars','--window-size=820,%d'%(420*len(figs)+100),'--screenshot='+os.path.abspath(out),pathlib.Path(tmp).as_uri()],stderr=subprocess.DEVNULL)
print(len(figs),'张图 →',out)
