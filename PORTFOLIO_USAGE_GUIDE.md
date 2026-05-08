# 学术作品集网站使用与维护指南 (Portfolio Usage Guide)

本指南旨在为您（以及协助您的 AI 助手）提供一份详尽的手册，说明该 Astro 网站的架构层级、运作机制，以及如何高效地登载新的学术项目、转换 LaTeX 文件和管理多语言内容。

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
- `src/content/blog/`：**这里是存放所有学术文章、笔记和项目的核心数据仓库**。所有文件为 `.md` 或 `.mdx` 格式。
- `src/layouts/`：页面布局模板。
  - `BaseLayout.astro`：常规页面的带侧边栏和粒子动画的布局。
  - `AcademicNoteLayout.astro`：专为长篇学术文章设计的三栏极简布局（左侧返回、中间正文、右侧自动目录），支持数学公式。
- `public/`：存放静态资源（如 `.svg`, `.png`, `.jpg`, `.gif` 等图片）。

### 1.2 运作机制
当您在 `src/content/blog/` 目录下添加一个 `.md` 文件时，Astro 会自动将其解析，并根据文件顶部的信息（Frontmatter）生成对应的文章详情页，同时会自动出现在 `/blog/`（Notes 页面）的列表中。

---

## 2. 如何登载新的学术项目或文章

所有文章和笔记都通过 Markdown (`.md` 或 `.mdx`) 文件进行管理。

### 2.1 新建一篇学术笔记
1. 在 `src/content/blog/` 目录下新建一个文件，例如 `my-new-research.md`。
2. 文件顶部**必须**包含以下 Frontmatter (YAML 格式) 的元数据：

```markdown
---
title: "你的项目或论文标题"
description: "简短的一两句话摘要，将显示在卡片上"
pubDate: "2026-06-15"
heroImage: "/analysis.svg"  # 题图的路径，放置在 public/ 目录下
badge: "AI"                 # 可选，显示在卡片右上角的徽章标签
tags: ["machine-learning", "causal-inference"] # 可选，文章标签
---

这里开始写正文内容...
```

### 2.2 插入图片（静态图片或 GIF）
1. 将您的图片（如 `result.png`, `demo.gif`, `chart.svg`）直接放入项目的根目录下的 **`public/`** 文件夹中。
2. 在 Markdown 文件中，使用绝对路径（以 `/` 开头）引用它们：
```markdown
![这是图片的替代文字](/demo.gif)
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
> 6. 请为我生成一个符合 Astro 规范的 Frontmatter，包含 title, description, pubDate, badge 和 tags。
> 
> 以下是我的 LaTeX 代码：[贴入代码]"

**步骤总结**：
1. 让 AI 根据上述 Prompt 帮您把 `.tex` 转换为 `.md`。
2. 将生成的 `.md` 文件放入 `src/content/blog/`。
3. 把 PDF 或编译产生的图片抽取出来，放入 `public/`。
4. 运行 `npm run dev` 即可在本地预览完美排版的学术页面。

---

## 4. 如何将新项目链接到主页和 Projects 页面的表格/卡片中

主页（Home）和 项目页（Works）中的“卡片”是**静态且可高度定制的**。由于您拥有中、日、英三种语言的页面，如果一个项目非常重要，您需要手动在页面代码中添加一个 `<HorizontalCard />`。

### 4.1 在主页/项目页添加一张新卡片
打开对应语言的主页（如 `src/pages/index.astro` 或 `src/pages/zh/index.astro`）或者 项目页（如 `src/pages/projects.astro`）。

找到您想插入新项目的位置（通常在 `<div><div class="text-2xl ...">代表性内容</div></div>` 之后）。使用以下格式插入一个新组件：

```astro
<div class="divider my-0"></div>
<HorizontalCard
  title="新论文或项目标题"
  img="/你的图片路径.gif"
  desc="一段非常精炼的项目介绍，展示在卡片中。"
  url="/blog/my-new-research"  <!-- 这里的 url 对应你在 src/content/blog 里的文件名 -->
  target="_self"
  badge="New!"
/>
```

**注意事项：**
- `url` 属性非常重要。如果您在 `src/content/blog/` 里建了名为 `my-new-research.md`，那么它的路由就是 `/blog/my-new-research`。
- 如果您只想外链到外部网站（如 arXiv 的 PDF），直接把 `url` 改为外部链接，并将 `target` 改为 `"_blank"`。

### 4.2 最新笔记 (Latest notes) 区域是自动更新的
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
2. **存放图片**：将图片拖入项目的 `public/` 文件夹。
3. **格式转换**：使用 AI（通过上述提示词）将内容转化为带 Frontmatter 的 Markdown 格式。
4. **新建文件**：在 `src/content/blog/` 下新建 `.md` 文件并粘贴转化后的代码。
5. **本地预览**：在终端运行 `npm run dev`，访问 `http://localhost:4321/blog` 查看排版和 LaTeX 公式是否正确。
6. **主页展示（可选）**：如果该项目是核心成果，将其作为 `<HorizontalCard />` 手动添加到 `src/pages/projects.astro` 和各国语言的主页中。
7. **提交发布**：完成检查后，运行标准的 Git 命令 (`git add .`, `git commit -m "add new paper"`, `git push`) 推送到 GitHub 自动部署。

本指南至此结束。将此文档提供给任何辅助您的 AI 助手，它们即可完美地代您执行所有繁琐的代码迁移与页面排版工作。