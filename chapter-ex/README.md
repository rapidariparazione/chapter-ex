# chapter-ex

An agent skill that turns one chapter of a book into a Chinese "concept-understanding" reading page:
intuition first, bilingual key quotes, SVG diagrams, clickable quizzes, highlighting, and a printable PDF.
Works with Claude (claude.ai / Claude Code) and Tencent WorkBuddy, or any agent that reads `SKILL.md` skills.

---

把书的一章做成「概念理解版」阅读页。先建直觉再给定义，原文金句中英对照，配 SVG 插图和可点选的选择题。
产出一个单独的 HTML 文件（能划线、能做题、离线可打开）和一份 PDF。

## 安装

先到 GitHub 页面右侧的 **Releases** 下载 `chapter-ex.zip`。

**claude.ai**：在设置里找到技能（Skills），上传这个 zip。菜单名称以你看到的界面为准。

**WorkBuddy**：二选一。
1. 技能板块 → 添加技能 → 上传技能包，选这个 zip。
2. 解压，把 `chapter-ex` 文件夹放到 `~/.workbuddy/skills/`（Windows 是 `%APPDATA%\WorkBuddy\skills\`），重启 WorkBuddy。

**Claude Code**：解压，把 `chapter-ex` 文件夹放到 `~/.claude/skills/`。

## 前置依赖

- Python 3.8 以上（脚本只用标准库）。
- poppler（提供 `pdftotext`、`pdftoppm`）：macOS `brew install poppler`，Ubuntu `apt install poppler-utils`。
- Chrome / Chromium / Edge 任一，用来出 PDF 和给插图截图。找不到时设 `CHROME=浏览器路径`。

在 claude.ai 这类云端环境里，能不能装 poppler、有没有浏览器，取决于平台。缺了的话，HTML 照样能出，PDF 可以自己用浏览器「打印 → 另存为 PDF」。

## 用法

把一章的 PDF 发给 AI，说：

> 用 chapter-ex 把这一章做成概念理解版阅读页。

它会产出 `第N章.md`、`账本-第N章.md`、`第N章.html`、`第N章.pdf`。
用浏览器打开 HTML 就能读。划线和做题记录存在你自己的浏览器里，换浏览器或清缓存会丢。

## 文件

- `SKILL.md`：给 AI 看的流程和写作规矩。
- `references/notes-guide.md`：笔记怎么写。
- `references/md-format.md`：转网页脚本认得的 Markdown 写法。
- `scripts/`：检查脚本、转网页脚本、样式和页面脚本。

## 授权

MIT，见 `LICENSE`。
