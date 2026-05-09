# 学术作品集网站使用与维护指南 (Portfolio Usage Guide)

本指南旨在为您（以及协助您的 AI 助手）提供一份详尽的手册，说明该 Astro 网站的架构层级、运作机制，以及如何高效地登载新的学术项目、转换 LaTeX 文件和管理多语言内容。

---

## 0. 给 AI 助手的硬性约定 (Read-First Contract for AI Agents)

> **任何 AI 在改动这个仓库前，必须先读完这一节，再读相关章节。** 这些规则都是过去踩坑后总结出来的，违反它们会立刻产生 404 / 三语不一致 / 卡片点击错位等可见 bug。

### 0.1 三语路由是结构对称的，**不要**手动复制 ja/zh 副本
- 一篇 `src/content/blog/foo.md` 自动展开为 `/blog/foo`、`/ja/blog/foo`、`/zh/blog/foo`，由 `src/pages/{blog,ja/blog,zh/blog}/[slug].astro` 共享同一个 `getCollection("blog")` 完成。
- **永远不要** 把同一篇 md 复制到 `src/pages/ja/blog/` 或 `src/pages/zh/blog/` 目录里——那样不会被 collection 读取，反而会污染路由。
- 如果某语言的 blog 路由"打不开"，先 `npm run build` 然后看 `dist/{,/ja,/zh}/blog/<slug>/index.html` 是否都生成；都生成而线上 404，是 GitHub Pages 部署延迟或浏览器缓存。

### 0.2 Works 的 `projectUrl` **必须写成单字符串**，由系统按 locale 自动展开
**这是避免 ja/zh 卡片 404 的强制写法。** `src/lib/works.ts` 中的 `localizeStringUrl()` 已经处理：

```yaml
# ✅ 正确：一行字符串，系统自动加 locale 前缀
projectUrl: "/blog/foo"
# → en:/blog/foo, ja:/ja/blog/foo, zh:/zh/blog/foo

projectUrl: "/projects"
# → en:/projects, ja:/ja/projects, zh:/zh/projects

projectUrl: "https://github.com/xxx/yyy"
# → 三语都用同一外部链接（不加前缀）
```

**禁止**：
```yaml
# ❌ 错误：手写三语对象时，ja/zh 极易写错或填占位
projectUrl:
  en: "/blog/foo"
  ja: "/ja/projects"   # ← 旧 bug 模式：变成跳转到 projects 列表而非文章
  zh: "/zh/projects"
```

只有当某语种**真的需要**指向不同 URL（极少）才允许写 `{ en, ja, zh }` 对象。**默认全部用单字符串。**

### 0.3 主页 Selected works 不要传 `url` 覆盖
`src/pages/{,/ja,/zh}/index.astro` 中 Selected works 的卡片渲染 **不要** 传 `url: projectRoutes.xx`：

```ts
// ✅ 正确：让 workCard 使用 projectUrl 自动跳到文章
const card = workCard(work, "en", { useSummary: true });

// ❌ 错误：传 url 覆盖，会导致点击只能跳到 /projects 列表
const card = workCard(work, "en", { useSummary: true, url: projectRoutes.en });
```

理由：Selected works 的卡片应该**直接跳到对应文章**，与 `/projects` 页面的卡片行为一致。`projectRoutes.en` 这种覆盖只在没有具体文章时才有用，而当前每个 featured 卡片都有 `projectUrl`。

### 0.4 图片必须放进 `public/<subfolder>/`，不许散到根目录
- 根目录只允许：`favicon*.svg`、`profile.{webp,svg}`、`analysis.svg`、`research.svg`、`writing.svg`、`robots.txt`。
- 课题/项目图片一律放进语义化子文件夹：`public/<project-slug>/`。
- Markdown 中引用绝对路径：`![](/<subfolder>/file.jpg)`，**不要**写嵌套的 `public/`。

### 0.5 Works 的 `pubDate` 是必填字段
- `src/content/config.ts` 中 works schema 的 `pubDate` 是必填，build 会校验。`order` 是可选的 tiebreaker。
- 排序由 `pubDate` 倒序决定（`src/lib/works.ts` 中的 `visibleWorks`）。

### 0.6 文件名一律英文
- `GENERATE_SLUG_FROM_TITLE = false`，URL = 文件名。
- **禁止用中文/日文文件名**，会导致 slug 被剥离成空字符串，全语种 404。

### 0.7 文章页 Google Translate widget — **唯一**实现位置和触发方式

#### 实现架构（不要改散）
- **引擎挂载点**：`src/layouts/AcademicNoteLayout.astro` 中的 `<div id="google_translate_element">` + 紧跟其后的 `<script>` 块。**全站只允许这一处加载** `translate_a/element.js`，绝不允许复制到 `BaseLayout.astro`、`PostLayout.astro`、或其他任何位置。
- **触发按钮**：所有带 `[data-translate-cycle]` 属性的元素都会被脚本自动绑定 click 事件。当前两处：
  - 桌面端：`src/components/notes/NoteSideBar.astro` —— 圆形按钮，与"返回笔记列表"按钮同款样式，叠在它**正下方**。
  - 移动端：`src/layouts/AcademicNoteLayout.astro` `lg:hidden` 区域顶部，紧跟 mobile 返回链接旁边的小药丸。
- **label 显示位置**：所有带 `[data-translate-label]` 属性的 `<span>` 都会被同步更新成当前语言缩写（`EN` / `JP` / `CN`）。

#### 触发机制：cookie + reload（**不要**改回事件 dispatch）
点击按钮 → 写 cookie `googtrans=/auto/<lang>; path=/; max-age=31536000` → `location.reload()` → 页面重新加载时 Google widget 读取 cookie 并自动翻译。

**为什么用这种方式？** 早期版本用 `select.dispatchEvent(new Event("change"))` 直接触发 hidden select，但是：
1. Google 异步注入 select，需要复杂重试逻辑
2. 某些 widget 版本对 dispatch 的 `change` 事件不响应（必须是真实用户点击）
3. cookie + reload 跨浏览器一致、无竞态、Google 官方推荐

代价：每次切换会刷新页面（约 0.5–1 秒）。这是可接受的。**不要**为了"无刷新"切回 dispatch 方案。

#### 三步交互
1. 用户进入 `/blog/foo`，没有 cookie → 按钮 label 由 URL locale 推断（`/blog/` → `EN`、`/ja/blog/` → `JP`、`/zh/blog/` → `CN`）。
2. 用户点击按钮 → 写 cookie 到下一种语言 → reload → Google widget 翻译整篇。
3. 用户切换文章后 cookie 仍在，新文章自动同样语言翻译；按钮 label 与 cookie 同步。

#### 严禁做的事
- **不要**重新引入"右上角悬浮按钮"或"右下角浮窗"——已经由用户明确否决，统一改到左侧 NoteSideBar 与移动端顶部。
- **不要**改 `pageLanguage: "auto"`——三语文章源语言识别依赖它。
- **不要**改 `includedLanguages: "en,ja,zh-CN"`——多语言会污染 cookie 状态机。
- **不要**修改 `<style is:global>` 中关于 `#google_translate_element` 离屏定位（`position: absolute; left:-9999px;`）的部分。**不能用 `display: none`**，否则 Google widget 会因为元素不可见拒绝挂载，导致 cookie 即使写了也不会翻译。
- **不要**改 cookie 的写法。`googtrans=/auto/<lang>` 中的两个斜杠**不能**被 URL-encode；`path=/` 必须有，否则只在 `/blog/...` 路径生效不到子文章。
- **不要**把按钮做成下拉框。
- **不要**复制 widget 到 BaseLayout——只有 AcademicNoteLayout 渲染的页面（即文章详情页）需要翻译。

#### 降级路径
若 Google 停服 `translate_a/element.js`：从 `AcademicNoteLayout.astro` 删除整块 `<div id="google_translate_element">` + `<script>` + `<style is:global>`，再删除 NoteSideBar 中的翻译按钮即可。文章功能不受影响。

### 0.8 三语 tag 路由是结构对称的（这次审计后修复）
- `/blog/tag/<tag>`、`/ja/blog/tag/<tag>`、`/zh/blog/tag/<tag>` **三套都存在**，分别由：
  - `src/pages/blog/tag/[tag]/[...page].astro`
  - `src/pages/ja/blog/tag/[tag]/[...page].astro`
  - `src/pages/zh/blog/tag/[tag]/[...page].astro`
- PostLayout 中 tag chip `<a href={tagPrefix + "/" + tag}>` 中的 `tagPrefix` 由当前 URL locale 决定，点击不会切换 locale。
- **新增 tag 页面布局功能时**（例如自定义 sort、加 RSS link 等），三个文件都要改。或者抽出共享 component。

### 0.9 隐藏的 placeholder 博文用 `src/lib/blogFilters.ts` 集中管理
- 不再在每个 `index.astro` 重复声明 `HIDDEN_NOTE_SLUGS`。`isPublicNote` helper 是唯一过滤入口。
- 添加新 placeholder：编辑 `src/lib/blogFilters.ts` 的 `HIDDEN_NOTE_SLUGS`，三语主页自动同步。
- 注意：被隐藏的文章 URL 仍然能直接访问，只是不出现在主页 Latest notes。如果要彻底下线，删除 md 文件本身。

### 0.10 404 页面是 locale-aware
- `src/pages/404.astro` 通过 `Astro.url.pathname` 检测前缀，把"返回主页"按钮指向当前 locale 的根（`/`、`/ja/`、`/zh/`），并展示对应语种的提示文字。
- 新增其他全站语言时，记得更新 `404.astro` 的 `labels` 字典。

### 0.8 三语 UI 标签集中在两处
- 侧边栏标签（Home/Works/Notes/CV/Contact）：`src/components/SideBarMenu.astro` 中的 `labels` 字典。
- Works 分类标题：`src/lib/works.ts` 的 `workSectionTitles`。
- 想新增导航条目时，**两处都要更新**，否则某 locale 会出现"未翻译"标签。

---

## 1. 网站层级与架构运作机制

本网站基于 **Astro** 框架构建，搭配 **TailwindCSS** 和 **DaisyUI** 提供样式支持。网站区分为“常规展示页”和“学术阅读页”两种主要形态。

### 1.1 核心目录结构
- `src/pages/`：静态页面的路由目录。
  - `index.astro`：英文主页。
  - `projects.astro`：英文项目列表页（Works）。
  - `cv.astro`：英文简历页。
  - `contact.astro`：英文联系方式与地图页。
  - `zh/` 和 `ja/`：对应的中文和日文翻译页面。
  - `blog/`：用于展示学术笔记和文章详情的动态路由（`[...page].astro` 和 `[slug].astro`）。
- `src/content/blog/`：存放长篇学术文章、研究笔记和项目详情页。所有文件为 `.md` 或 `.mdx` 格式，会生成 `/blog/...` 详情页。
- `src/content/works/`：存放 Works / Projects 页面使用的项目卡片数据。这里不写长正文，而是维护项目标题、简介、分类、图片、链接和多语言文本。
- `src/lib/works.ts`：Works 数据的读取、排序、筛选和多语言文本选择逻辑。主页和三语 Projects 页面都会读取这里的工具函数。
- `src/layouts/`：页面布局模板。
  - `BaseLayout.astro`：常规页面的带侧边栏和粒子动画的布局。
  - `AcademicNoteLayout.astro`：专为长篇学术文章设计的三栏极简布局（左侧返回、中间正文、右侧自动目录），支持数学公式。
- `public/`：存放静态资源（如 `.svg`, `.png`, `.jpg`, `.gif` 等图片）。

### 1.2 运作机制
当前网站把“文章详情”和“项目卡片”分开管理：

- `src/content/blog/`：负责生成 `/blog/...` 文章详情页，并自动出现在 `/blog/`（Notes 页面）和首页的 Latest notes / 研究笔记区域。
- `src/content/works/`：负责生成主页 Selected works / 代表性内容，以及 `/projects`、`/ja/projects`、`/zh/projects` 的 Works 卡片。
- 一个项目如果既要有卡片，又要有详细文章，通常需要两个文件：一个放在 `src/content/works/` 作为卡片索引，一个放在 `src/content/blog/` 作为详情页正文。然后在 works 文件的 `projectUrl` 中指向对应的 `/blog/...` 路径。

---

## 2. 如何登载新的学术项目或文章

当前维护方式分为两类：

- **文章 / Notes / 项目详情页**：写在 `src/content/blog/`，会生成 `/blog/...` 页面。
- **Works / Projects 卡片**：写在 `src/content/works/`，会显示在主页和三语 Projects 页面。

### 2.1 新建一篇学术笔记或项目详情页

> **核心心智模型**：你只需要做 **三件事**——放一个 md、放图片、git push。三语路由、tag 页、列表分页、首页 Latest notes 全部由 Astro 自动生成。**永远不要去 `src/pages/` 下手动建 ja/zh 副本**。

#### 标准工作流（每次新增博文）

1. **准备图片**：在 `public/` 下创建（或选择）一个语义化子文件夹，例如 `public/<project-slug>/`，把所有相关图片放进去。**不要散到 `public/` 根目录**（详见第 7.1 节）。
2. **新建 Markdown**：在 `src/content/blog/` 目录下新建文件，**文件名必须是英文/数字/连字符**（参见第 ⚠️ 章常见故障 1），例如 `jssc-pre1-experience.md`。
3. **写好 Frontmatter**：

   ```markdown
   ---
   title: "你的项目或论文标题"
   description: "简短的一两句话摘要，将显示在卡片上"
   pubDate: "2026-06-15"                           # 必填，YYYY-MM-DD
   updatedDate: "2026-07-01"                       # 可选，更新日期
   heroImage: "/<project-slug>/cover.jpg"          # 可选，题图
   badge: "AI"                                     # 可选，卡片右上角徽章
   tags: ["machine-learning", "causal-inference"]  # 可选，会生成 /blog/tag/<tag> 列表页
   ---

   这里开始写正文内容...
   ```

4. **写正文**：可以使用标准 Markdown + LaTeX 公式（`$...$`、`$$...$$`）+ 图片引用 `![描述](/<project-slug>/figure.png)`。
5. **本地验证**：`npm run dev`，访问以下三个 URL 都应该能打开同一篇文章：
   - `/blog/<filename>` — 英文站
   - `/ja/blog/<filename>` — 日文站
   - `/zh/blog/<filename>` — 中文站
6. **构建检查**：`npm run build`。看到 `[build] Complete!` 即可。**注意**：每篇博文会让总页面数增加 `3 + 3×N_tags`（3 个详情页 + 每个 tag 一个分页）。这是 Astro 自动生成的，**不是你需要维护的**。
7. **提交推送**：`git add . && git commit -m "..." && git push`。GitHub Actions 会自动部署到 GitHub Pages。

#### 一篇博文实际生成多少页？

举例：一篇带 3 个 tag 的新博文 `foo.md` 会让 `npm run build` 输出多 6 个页面：

| 自动生成的页面 | 数量 |
|---|---:|
| `/blog/foo`、`/ja/blog/foo`、`/zh/blog/foo` | 3 |
| `/blog/tag/<tag1>`、`<tag2>`、`<tag3>` | 3 |
| **合计** | **6** |

如果不写 `tags` 字段则只有 3 个新页面。**你不需要为这些页面写任何代码**，全部由 `src/pages/blog/[...page].astro`、`[slug].astro` 与三语 `pages/{ja,zh}/blog/*` 共用同一份 content collection 自动展开。

#### 文章 URL 规则

`src/config.ts` 中 `GENERATE_SLUG_FROM_TITLE = false`，所以 URL = 文件名（去掉 `.md`）。
- 文件 `jssc-pre1-experience.md` → URL `/blog/jssc-pre1-experience`、`/ja/blog/jssc-pre1-experience`、`/zh/blog/jssc-pre1-experience`。
- **不要用中文/日文文件名**，否则 URL 会被剥离成空 slug 导致 404。

### 2.2 新建一张 Works / Projects 卡片
如果希望项目出现在主页 Selected works / 代表性内容，或出现在 `/projects`、`/ja/projects`、`/zh/projects`，请在 `src/content/works/` 新建一个 `.md` 文件，例如 `my-new-work.md`。

Works 文件只维护卡片元数据，不写长正文。推荐模板如下：

```markdown
---
title:
  en: "English title"
  ja: "日本語タイトル"
  zh: "中文标题"
description:
  en: "Short English description for the Projects page."
  ja: "Projects ページに表示する短い説明。"
  zh: "显示在 Projects 页面的简短中文说明。"
summaryTitle:
  en: "Homepage title if different"
  ja: "首页用タイトル"
  zh: "首页用标题"
summary:
  en: "Shorter homepage description if needed."
  ja: "必要に応じた首頁用の短い説明。"
  zh: "必要时填写首页用的更短说明。"
section: "research"
badge: "AI"
heroImage: "/analysis.svg"
projectUrl:
  en: "/blog/my-new-research"
  ja: "/blog/my-new-research"
  zh: "/blog/my-new-research"
pubDate: "2026-06-15"
order: 70
featured: false
visibleIn: ["en", "ja", "zh"]
---
```

字段说明：

- `title` / `description`：Projects 页面使用的三语标题和说明。
- `summaryTitle` / `summary`：可选。主页 Selected works / 代表性内容使用；不填则回退到 `title` / `description`。
- `section`：决定项目出现在 Projects 页面的哪个分类。只能填 `"research"` 或 `"writing"`。
- `badge`：卡片右侧标签，例如 `AI`、`Research`、`Data`、`Writing`。
- `heroImage`：卡片图片路径，必须指向 `public/` 下的静态资源。
- `projectUrl`：点击卡片后的链接。**推荐写成单行字符串**（例如 `projectUrl: "/blog/foo"`），`workCard()` 会自动展开为：
  - English 站：`/blog/foo`
  - 日本語 站：`/ja/blog/foo`
  - 中文 站：`/zh/blog/foo`

  对 `/projects`、`/cv` 同样生效。指向外部链接（`https://...`、`mailto:`、`#`）会原样使用，不加 locale 前缀。如果某些 locale 需要单独指向不同 URL，仍然可以写成三语对象 `projectUrl: { en: "...", ja: "...", zh: "..." }`，但 99% 情况下用单行字符串即可，**这是避免 ja/zh 链接 404 的标准做法**。
- `pubDate`：**必填**。项目发布日期，格式 `"YYYY-MM-DD"`。Works 现在按 `pubDate` 倒序显示（越新越靠前），通常应与对应 blog 文章的 `pubDate` 一致；没有对应博客文章时填写项目实际开始/完成日期。
- `order`：可选。仅作为 `pubDate` 相同时的次级排序键（数值越小越靠前）。新建项目可省略。
- `featured`：是否出现在主页 Selected works / 代表性内容区域。
- `visibleIn`：可选。控制该卡片在哪些语言页面显示。若省略，则三种语言都显示。例如 `visibleIn: ["en"]` 表示只在英文 Projects 显示。

### 2.3 插入图片（静态图片或 GIF）
1. 将您的图片（如 `result.png`, `demo.gif`, `chart.svg`）直接放入项目的根目录下的 **`public/`** 文件夹中。
2. 在 Markdown 文件中，使用绝对路径（以 `/` 开头）引用它们：
```markdown
![这是图片的替代文字](/demo.gif)
```

如果一个项目有多张图片，建议在 `public/` 下建立子文件夹，例如：

```text
public/irt-etesting/
```

然后在 Markdown 中引用：

```markdown
![系统界面示例](/irt-etesting/demo.png)
```

---

## 3. LaTeX 文件的转化与登载

由于该网站已经配置了 `remark-math` 和 `rehype-katex`，它完全支持标准的 LaTeX 数学公式渲染，并且使用了符合学术阅读习惯的排版。

### 3.1 LaTeX 公式语法
- **行内公式**：使用单个美元符号包裹。例如 `$E = mc^2$`。
- **块级公式**：使用双美元符号包裹，支持换行和对齐。
```markdown
$$
\hat{\beta} = (X^T X)^{-1} X^T Y
$$
```

### 3.2 如何将现有的 `.tex` 文件快速转化为网页内容
如果交给其他 AI（如 Claude 或 ChatGPT）处理，请直接复制以下 Prompt（提示词）给 AI：

> **[转录 LaTeX 给 AI 的专用 Prompt]**
> "我有一份完整的 LaTeX 论文/研究报告，我想将其转换为 Markdown 格式，以便登载到我的 Astro 学术博客上。请遵循以下规则：
> 1. 将原文件中的 `\section{}`, `\subsection{}` 转换为 Markdown 的 `##`, `###`。
> 2. 保留所有的数学公式，行内公式使用 `$ ... $`，独立公式使用 `$$ ... $$`。
> 3. 去除所有特定于 LaTeX 的页面排版宏（如 `\newpage`, `\vspace`, 复杂的 `\begin{figure}` 浮动体）。
> 4. 将图片引用 `\includegraphics{image.png}` 转换为 Markdown 语法 `![Image Description](/image.png)`，我会把图片放在 public 目录。
> 5. 参考文献（Bibliography）可以直接转换为文末的一个有序列表或无序列表。
> 6. 请为我生成一个符合当前 Astro content schema 的 Frontmatter，只使用 title, description, pubDate, updatedDate, heroImage, badge 和 tags。不要使用 date, course, instructor, authorship, relevance 等未在 schema 中定义的字段，除非我明确要求同时修改 `src/content/config.ts`。
> 
> 以下是我的 LaTeX 代码：[贴入代码]"

**步骤总结**：
1. 让 AI 根据上述 Prompt 帮您把 `.tex` 转换为 `.md`。
2. 将生成的 `.md` 文件放入 `src/content/blog/`。
3. 把 PDF 或编译产生的图片抽取出来，放入 `public/`。
4. 运行 `npm run dev` 即可在本地预览完美排版的学术页面。

---

## 4. 主页和 Projects 页面如何读取 Works 数据

主页和 Projects 页面现在不是手写卡片，而是数据驱动。

### 4.1 Projects 页面
以下三个页面都会读取 `src/content/works/`：

- `src/pages/projects.astro`
- `src/pages/ja/projects.astro`
- `src/pages/zh/projects.astro`

这些页面会调用 `src/lib/works.ts` 中的：

- `worksBySection(works, locale, section)`：按语言和分类筛选。
- `workSectionTitles`：提供各语言分类标题。
- `workCard(work, locale)`：把 works 数据转换为 `<HorizontalCard />` 需要的 props。

因此，新增项目时通常不需要手动编辑 `projects.astro`。只要在 `src/content/works/` 新建或修改对应 `.md` 文件，Projects 页面就会自动更新。

### 4.2 主页 Selected works / 代表性内容
以下三个主页也会读取 `src/content/works/`：

- `src/pages/index.astro`
- `src/pages/ja/index.astro`
- `src/pages/zh/index.astro`

主页只显示 `featured: true` 的作品。排序仍由 `order` 决定。

如果某个项目只想出现在 Projects 页面，不想出现在主页，请设置：

```yaml
featured: false
```

如果某个项目想作为代表性内容出现在主页，请设置：

```yaml
featured: true
```

### 4.3 最新笔记 (Latest notes) 区域是自动更新的
在各个语言的主页（`index.astro`, `ja/index.astro`, `zh/index.astro`）的最下方，有一个“Latest notes”或“研究笔记”区域。
- 这个区域是**自动读取** `src/content/blog/` 中的前 3 篇文章进行展示的。
- 考虑到您有三种语言，日文和中文的主页在代码顶部（大约第 10-25 行）使用了一个名为 `noteCopy` 的字典对象，用于给这些自动生成的卡片做**硬编码翻译**。
- 如果您新发了一篇笔记叫 `new-note.md`，它会自动出现在中日文主页的下端。如果您希望标题显示为中文，只需在 `src/pages/zh/index.astro` 顶部的 `noteCopy` 里加一段：
```javascript
"new-note": {
  title: "我的新笔记中文标题",
  description: "简短中文描述。",
  badge: "新标签",
},
```

---

## 5. 总结：日常登载标准工作流 (Workflow)

1. **准备内容**：整理好您的 `.tex` 代码或草稿，以及相关图片（`.png`, `.gif` 等）。
2. **存放图片**：在 `public/` 下建一个**语义化子文件夹**（例如 `public/<project-slug>/`），把图片放进去。**根目录不放课题/项目图片。**
3. **格式转换**：使用 AI（通过上述提示词）将内容转化为带 Frontmatter 的 Markdown 格式。
4. **新建文章详情页**：在 `src/content/blog/` 下新建 `.md` 文件（**英文文件名**），粘贴转化后的正文，填好 `pubDate` 等 frontmatter。一份 md 自动生成三语路由（`/blog/...`、`/ja/blog/...`、`/zh/blog/...`），**不要手动复制到 ja/zh 目录**。
5. **新建 Works 卡片（可选）**：仅在希望该项目以**卡片**形式出现在 Projects 页面时，才在 `src/content/works/` 下新建 `.md` 文件，填写三语标题、`pubDate`、`section`、`projectUrl`（可指向上一步的 `/blog/...`）。如果只想发博文不开卡片，**跳过此步**即可。
6. **本地预览**：`npm run dev`，访问 `/`、`/projects`、`/blog`、`/ja/blog`、`/zh/blog` 检查卡片、文章排版、LaTeX 公式、图片是否正确。
7. **构建检查**：`npm run build`。0 error 即可。页面数会随内容自动增长——这是正常的，无需关注。
8. **提交发布**：`git add . && git commit -m "..." && git push`。GitHub Actions 自动部署到 GitHub Pages，约 1–2 分钟生效。

---

## 6. 从 `tex文件` 选择和整理 Portfolio 项目的规则

`../tex文件/` 中保存了大量 Overleaf / LaTeX 课程报告、项目草稿和 AI 处理指示。它们可以作为网站作品来源，但不能直接把课程报告原文整篇复制到网站上。更合适的做法是先筛选，再重写成适合 Portfolio 阅读的项目文章。

### 6.1 先做公开展示判定
把任何 LaTeX 报告转成网页前，先判断是否适合公开：

- 内容是否事实正确，没有明显统计、数学或实现错误。
- 是否确实是本人完成；如果是共著或小组作业，必须如实说明，不能写成单独完成。
- 是否包含个人信息、他人未公开数据、课程内部资料、第三方版权内容或不适合公开的材料。
- 是否有方法、代码、实验设计或数据分析价值，而不是单纯课堂题目答案。
- 是否能和当前网站主题产生联系：AI / Machine Learning、Biostatistics、Causal Inference、Data Science、Statistical Modeling、Reproducible Analysis、Information Engineering。

不满足公开条件时，不要强行做成作品。可以只作为个人学习记录，不进入网站。

### 6.2 优先转化的项目类型
根据 `tex文件` 中现有评估文档，优先考虑以下类型：

- 生存分析、Kaplan-Meier、右截尾、log-rank test 等生物统计相关报告。
- 临床试验数据、RCT baseline balance、连续变量和二分类变量的统计分析。
- 回归分析、异常值处理、统计推断、置信区间、假设检验、贝叶斯推断。
- 因果推断、Target Trial Emulation、Clone-Censor-Weight、IPCW 等未来研究计划可连接的方法基础。
- IRT / e-Testing 这类统计建模与 Web 系统实现结合的项目。
- 数值计算、最优化、模式识别、LDA、KNN、图像处理、PDE 数值解等能展示信息工程基础的项目。

优先级大致为：

1. 生物统计、统计建模、因果推断直接相关项目。
2. AI / ML / 最优化 / 数据分析等能支撑研究能力的项目。
3. 系统实现、课程演习、基础编程项目。此类项目只选质量较高、能体现方法或实现深度的少数代表。

### 6.3 不要把“课题答案”直接放到网站
`tex文件/AI_PORTFOLIO_PROJECT_PROMPT.md` 中的核心原则是：课程报告不应以“第 1 问、第 2 问”的作业答案形式直接公开，而应重构为一个完整项目。

推荐结构：

- 项目概要：说明背景、目的、构建或分析了什么。
- Core Theory：整理核心理论，例如 IRT、MLE、Bayesian inference、regression、survival analysis。
- Derivations / Methods：保留关键推导、模型、估计方法和算法流程。
- Implementation：展示最有代表性的代码片段，而不是全部代码。
- Results / Discussion：说明主要结果、局限和改进方向。
- Repository / Reproducibility：如有 GitHub 仓库，在文末加入项目卡片或链接。

写作时要避免夸张表达。不要写“独创”“首次提出”“显著提升”等没有原始材料支持的表述。可以写“実装した”“確認した”“比較した”“検討した”这类事实性表达。

### 6.4 先在 `tex文件` 下做草稿，再进入网站
对于复杂项目，推荐采用三步流程：

1. **精读源材料**：阅读相关 `.tex`、图片、代码和已有草稿，抽取理论、方法、实现、图表和可公开内容。
2. **生成审阅草稿**：先在 `../tex文件/项目名_Draft/` 下生成一个 Markdown 草稿和相关图片，让用户确认内容、图片、代码和表述。
3. **最终整合到网站**：用户确认后，再把正文放入 `src/content/blog/`，图片放入 `public/项目名/`，卡片信息放入 `src/content/works/`。

当前 IRT 项目的处理方式就是这个模式：先参考 `../tex文件/IRT_eTesting_Project_Draft/draft.md` 与其中图片，再将最终文章整理到 `src/content/blog/irt_etesting_system.md`，并通过 `src/content/works/irt-etesting-system.md` 生成 Works 卡片。

### 6.5 `tex文件` 中旧 Prompt 的注意点
`../tex文件/readme.md` 和 `../tex文件/AI_PORTFOLIO_PROJECT_PROMPT.md` 中有些内容是旧流程或申请材料语境下的指示，使用时需要转换为当前网站规则：

- 旧 Prompt 中可能使用 `date`, `course`, `instructor`, `authorship`, `relevance` 等字段；当前网站的 `blog` schema 不接受这些字段作为必需元数据。正式放入 `src/content/blog/` 时，使用 `pubDate`, `heroImage`, `badge`, `tags` 等当前 schema 字段。
- 旧 Prompt 中提到手动插入 `projects.astro`；当前已经改为 `src/content/works/` 数据驱动，不要再手动插入单个 `<HorizontalCard />`。
- 旧 Prompt 中可能包含具体申请对象、教授名或私人申请语境。这些信息不应进入公开网站文章或通用维护指南。
- 旧 Prompt 中对“不要捏造、不夸大、不隐藏共著、不公开个人信息”的限制仍然有效，应继续遵守。

---

## ⚠️ 常见故障排查与结构规范 (Troubleshooting & Structural Conventions)

### 1. 为什么项目链接 (URL) 打不开？
**原因**：Astro 默认配置中，如果启用了 GENERATE_SLUG_FROM_TITLE = true，系统会根据文件标题自动生成 URL 路径。由于它会使用正则表达式过滤掉所有非英文字符，当您的文章标题为全中文或日文时，生成的 slug 会被错误地剥离，导致手动填写的 url 发生 404 错误。
**解决方案**：已在 src/config.ts 中将 GENERATE_SLUG_FROM_TITLE 设置为 false。这意味着直接使用 Markdown 文件名作为 URL 路径。请务必用英文为文件命名（如 irt_etesting_system.md）。

### 2. 为什么数学公式会重复出现两遍？
**原因**：Astro 中的 rehype-katex 插件默认会同时输出视觉渲染的 HTML 标签和屏幕阅读器使用的 MathML 标签。在某些 Markdown 排版组件干扰下，原本应该隐藏的 MathML 标签被显示出来，导致公式看起来出现两次。
**解决方案**：已在 astro.config.mjs 中将 KaTeX 的输出模式强制设定为纯 HTML。以后无需担心此问题，正常使用双美元符号即可。

### 2.1 为什么 LaTeX 公式没有正常显示？
**原因**：Markdown 中的数学公式渲染分为两步。第一步由 `remark-math` 和 `rehype-katex` 将 `$...$` 与 `$$...$$` 转换为 KaTeX HTML；第二步由 KaTeX CSS 负责把这些 HTML 显示成正常数学公式。如果 KaTeX CSS 没有加载成功，公式可能会看起来像一堆异常的 HTML 结构，即使公式转换本身已经执行。

**当前修复**：不要再依赖外部 CDN 加载 KaTeX 样式。当前项目已经在 `src/styles/global.css` 中本地导入：

```css
@import "katex/dist/katex.min.css";
```

这样 KaTeX 样式会被 Astro/Vite 打包进网站自己的 CSS，能在本地预览和 GitHub Pages 静态部署中保持稳定。除非有明确理由，不要把它改回 `cdn.jsdelivr.net` 之类的外部样式链接。

**公式书写建议**：尽量使用 KaTeX 兼容且规范的写法。例如条件概率建议写成：

```latex
P(\theta \mid X)
```

而不是：

```latex
P(\theta | X)
```

较长的块级公式请在 `$$ ... $$` 内拆成多行，避免在手机端或较窄文章栏中挤压排版。

### 3. 项目分类与插入 projects.astro 的最佳实践
当前 Projects 页面已经改为数据驱动。一般情况下，不要再直接修改 `src/pages/projects.astro`、`src/pages/ja/projects.astro`、`src/pages/zh/projects.astro` 来插入单个项目卡片。

新增或调整项目时，优先修改 `src/content/works/` 下的 `.md` 文件。

分类由 works 文件中的 `section` 字段决定：

- `section: "research"`：进入 **Research and analysis**。适合研究计划、毕业研究、AI/ML 项目、生物统计、因果推断、数据分析、统计建模等更偏研究与分析的内容。
- `section: "writing"`：进入 **Writing and notes**。适合学习笔记、技术文章、课程演习、报告整理、LaTeX 文档、系统实现说明等更偏写作和记录的内容。

其他显示控制：

- `featured: true`：出现在主页 Selected works / 代表性内容。
- `featured: false`：只出现在 Projects 页面，不进入主页代表性内容。
- `visibleIn: ["en"]`：只在英文页面显示。
- 省略 `visibleIn`：默认在 English / 日本語 / 中文 三语页面都显示。

只有在要改变整体页面结构、分类标题、卡片渲染方式时，才需要编辑 `src/pages/*/projects.astro` 或 `src/lib/works.ts`。

---

## 7. 维护历史与已知约定 (Maintenance log)

本节记录 2026-05-09 后引入的几条新约定，**新增内容时必须遵守**。

### 7.1 `public/` 图片必须放进命名子文件夹
原本 `public/` 根目录混入了多个旧课题（教育システム1/2/3、情報工学実験等）的零散图片（`kadai*.jpg`、`0.05.jpg`、`venn_diagram.jpg` 等）。已经按照来源整理到子文件夹中：

| 子文件夹 | 来源 / 用途 |
|---|---|
| `public/edu-system-1/` | 教育システム1（`venn_diagram.jpg` 等） |
| `public/edu-system-2/` | 教育システム2（`kadai1-4.jpg`、`kadai7_*.jpg`、`0.05.jpg`、`0.2.jpg`、`1-4.jpg`） |
| `public/edu-system-3/` | 教育システム3（`3-1.jpg`、`3-2.jpg`、`3-4.jpg`、`3-5.jpg`） |
| `public/irt-etesting/` | IRT eTesting 项目（包括从根目录迁入的 `samplegraph2.jpg`） |
| `public/synchronization-analysis/` | 节拍器同步项目 |

**规则**：
- **不要在 `public/` 根目录新增散装的课题图片**。新增图片前先创建（或选择）一个语义化的子文件夹，例如 `public/<project-slug>/`。
- 根目录只允许保留站点级公共资源：`favicon*.svg`、`profile.{webp,svg}`、`analysis.svg`、`research.svg`、`writing.svg`、`robots.txt` 等。
- 在 Markdown 中引用时使用绝对路径：`![desc](/edu-system-2/kadai1.jpg)`。
- 移动已有图片时，**先全局搜索 `src/` 与 `dist/` 是否引用了该路径**，再做迁移并同步修改引用。

### 7.2 Works 与 Notes 一律按 `pubDate` 倒序
- **Works**：`src/lib/works.ts` 中的 `visibleWorks` 已改为按 `pubDate` 降序排序，`order` 仅作为 `pubDate` 相同时的次级 tiebreaker。`src/content/config.ts` 中 `pubDate` 已设为必填、`order` 设为可选。
- **Blog / Notes**：原本就在 `src/pages/blog/[...page].astro` 和三语主页中按 `pubDate` 降序排序，无需修改。
- **新增 works 卡片必须填写 `pubDate`**，否则 `npm run build` 会因 zod schema 校验失败而报错。
- 如果只想调整两个同一天发布项目的相对顺序，使用 `order`；不要再依赖 `order` 控制全局顺序。

### 7.3 Notes 已支持三语路由
原本只有 `/blog/`（英文）一套路由，语言切换器把 `/blog/<slug>` 重写为 `/ja/blog/<slug>` 和 `/zh/blog/<slug>` 时直接 404。现在已经新增三语 blog 路由，语言切换器可以正常工作。

**新增的文件**：
- `src/pages/ja/blog/[...page].astro` — 日文 listing（标题"ノート"，分页按钮"新しい記事 / 以前の記事"）
- `src/pages/ja/blog/[slug].astro` — 日文文章详情
- `src/pages/zh/blog/[...page].astro` — 中文 listing（标题"笔记"）
- `src/pages/zh/blog/[slug].astro` — 中文文章详情

**实现要点（重要，不要踩坑）**：

1. **共用 `blog` content collection**：三语 blog 路由全部从同一个 `getCollection("blog")` 读取数据，**不复制 Markdown 文件**。这样新增/修改一篇文章时，三语路由会自动同步。
2. **正文不会自动翻译**：当前每篇 `src/content/blog/*.md` 仍然是单语种（多数为日文）。`/ja/blog/<slug>`、`/zh/blog/<slug>`、`/blog/<slug>` 三个 URL 显示的正文是同一份。区别仅在 **侧边栏、页面标题、分页按钮、卡片链接** 是按 locale 本地化的。
3. **若日后要做真正的多语正文**：可以选两条路径：
   - 简单方案：在 frontmatter 加 `lang: "ja" | "zh" | "en"` 字段，三语路由各自只展示匹配 locale 的文章。这样需要给同一主题准备三份 Markdown。
   - 进阶方案：把 `src/content/blog/` 拆成 `blog-en/`、`blog-ja/`、`blog-zh/` 三个 collection。改动较大。
4. **listing 页 / 详情页的卡片链接必须带 locale 前缀**：`/ja/blog/...` 和 `/zh/blog/...`。各 `index.astro`（en/ja/zh）的 "Latest notes" 块也已分别改为 `/blog/`、`/ja/blog/`、`/zh/blog/`。新建索引/列表组件时不要再写死 `"/blog/"`。
5. **`SideBarMenu.astro` 的 Notes 链接**已使用 `routes.blog`，根据当前 locale 自动指向对应路径。新增导航条目时务必也走 `localizedRoutes`，并在 `labels` 字典中加入三语标签。
6. **`Header.astro` 的语言切换器**保持简单的"加 locale 前缀"逻辑——因为三语 blog 路由都存在，所以 `/blog/foo` ↔ `/ja/blog/foo` ↔ `/zh/blog/foo` 互相切换不会 404。

**关键不要做的事**：
- 不要在 `src/pages/blog/` 里再写死 `/blog/` 链接，应让三套路由各自负责自己的链接前缀。
- 不要复制 Markdown 文件到 `src/pages/ja/blog/` 之类的目录里——blog 路由读 `content/blog/`，不会自动扫页面目录里的 md。
- 不要把博文的 frontmatter 改成多语对象（仿照 works）——除非你愿意同时改 schema、`PostLayout` 和三处路由。当前架构刻意保持简单。

### 7.4 后续检查清单（每次新增 works / blog 时）
1. 新建 works 时，frontmatter 至少包含 `title`/`description`/`section`/`badge`/`pubDate`，并且 `pubDate` 是 `YYYY-MM-DD` 字符串。
2. 新增图片必须放在 `public/<subfolder>/` 下；不要散到根目录。
3. 本地跑 `npm run dev`，验证：
   - 主页和 `/projects` 中新项目按 `pubDate` 出现在正确位置。
   - 在 `/blog/` 或任意 `/blog/<slug>` 上点击 日本語 / 中文，跳转到 `/ja/` 或 `/zh/`，**不要**出现 404。
   - 图片正常加载。
4. `npm run build` 必须 0 error。
