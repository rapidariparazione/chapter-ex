#!/bin/bash
# 用法：bash topdf.sh <page.html> <out.pdf>
# 答案展开、保留底色，用无界面的 Chrome / Chromium / Edge 打印成 PDF。图跟着页面一起出来。
# 找不到浏览器时，设环境变量 CHROME 指向它的可执行文件。
set -e
find_chrome() {
  if [ -n "$CHROME" ] && [ -x "$CHROME" ]; then echo "$CHROME"; return; fi
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  for c in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge msedge; do
    command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return; }
  done
}
CH="$(find_chrome)"
if [ -z "$CH" ]; then
  echo "没找到 Chrome / Chromium / Edge。装一个，或设 CHROME=浏览器路径 再跑。" >&2
  echo "退路：用浏览器打开 $1，按打印，选「另存为 PDF」。" >&2
  exit 1
fi
tmp="${1%.html}-print.html"
sed -e 's/<details>/<details open>/g' -e 's#</style>#body{-webkit-print-color-adjust:exact;print-color-adjust:exact}</style>#' "$1" > "$tmp"
"$CH" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")" "file://$(cd "$(dirname "$tmp")" && pwd)/$(basename "$tmp")" 2>/dev/null
rm -f "$tmp"
ls -l "$2"
