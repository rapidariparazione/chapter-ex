# chapter-ex

An agent skill that turns one chapter of a book into a Chinese "concept-understanding" reading page:
intuition first, bilingual key quotes, SVG diagrams, clickable quizzes, and highlighting, delivered as a single HTML file.
Works with Claude (claude.ai / Claude Code) and Tencent WorkBuddy, or any agent that reads `SKILL.md` skills.

---

把书的一章做成「概念理解版」阅读页。先建直觉再给定义，原文金句中英对照，配 SVG 插图和可点选的选择题。
产出一个单独的 HTML 文件：能划线、能做题，双击就能在浏览器里打开，不用联网也能读。

## 它基于什么做出这个页面

**输入：** 一章书的 PDF（或一篇长文）。

**依据的方法：**
1. **先建直觉，再给定义。** 每个概念先用读者生活里的一个场景引出来，再讲原文的说法。例子取刚工作的年轻人不用查就懂的事。
2. **艾德勒《如何阅读一本书》的分析阅读。** 页面里有几块直接对应书中的规则：
   - 「关键词」一节：找出作者用的关键词，弄清他在这篇里指什么（规则 5）。
   - 「作者的问题答上了没」：作者想回答哪些问题，答上了几个（规则 4、规则 8）。
   - 「作者哪里能挑错」：知识不够、说错了、推不出、没讲完四样（规则 12 到 15）。
3. **每句话都能对回原文。** 先建一本事实账本，每条改写都配原文原句和页码。用脚本逐句核对引文和页码，查 9 类常见改写错误。
4. **读完就测。** 7 道四选一的选择题，加两处「先猜再看」，错的选项取原文里容易混的说法。

**输出：** 一个单独的 HTML 阅读页。里面有中英对照的原文金句、插图、可点的选择题、可以划线、点术语看解释。

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
- （可选）Chrome / Chromium / Edge：只用来给插图截图做检查，没有也能出页面。

没装 poppler 时，HTML 照样能出，只是查页码那道检查跑不了。

## 用法

把一章的 PDF 发给 AI，说：

> 用 chapter-ex 把这一章做成概念理解版阅读页。

它会交给你 `第N章.html`。同一个文件夹里还会留下笔记源文件 `第N章.md` 和事实账本 `账本-第N章.md`，不用管。
用浏览器打开 HTML 就能读。划线和做题记录存在你自己的浏览器里，换浏览器或清缓存会丢。

## 文件

- `SKILL.md`：给 AI 看的流程和写作规矩。
- `references/notes-guide.md`：笔记怎么写。
- `references/md-format.md`：转网页脚本认得的 Markdown 写法。
- `scripts/`：检查脚本、转网页脚本、样式和页面脚本。

## 授权

MIT，见 `LICENSE`。
