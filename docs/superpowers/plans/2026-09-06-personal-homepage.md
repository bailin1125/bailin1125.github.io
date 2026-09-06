# 个人主页实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从零搭建暗色极简的中文综合型个人主页（介绍+作品+博客+联系），Astro 静态生成，push 到 GitHub 自动发布到 GitHub Pages。

**Architecture:** Astro v5 纯 SSG，内容全部来自 `src/content/` 下的 Markdown（Content Collections + zod 校验）。首页单页滚动（Hero/精选作品/最新文章/联系），博客有列表/详情/标签/归档页。默认零客户端 JS，仅评论区加载外部脚本。

**Tech Stack:** Astro 5、Tailwind CSS 4（`@tailwindcss/vite`）、@astrojs/rss、@astrojs/sitemap、giscus 评论、GitHub Actions（withastro/action@v3 + actions/deploy-pages@v4）。

**Spec:** `docs/superpowers/specs/2026-09-06-personal-homepage-design.md`

## Global Constraints

- 配色（仅限这 6 个 token）：底 `#0d1117`、卡片 `#161b22`、边框 `#21262d`、正文 `#e6edf3`、次要文字 `#8b949e`、强调色 `#58a6ff`
- 强调色 `#58a6ff` 仅用于：链接、悬停态、标签、名字点缀；无渐变、无光效
- 字体：系统字体栈，禁止引入中文 webfont
- 内容中文为主，代码/项目名保留英文；不做 i18n、不做亮色主题、不做作品详情页、不做搜索/分页/CMS（spec 第 9 节 YAGNI 清单）
- 站点最终 URL：`https://wangzhi.github.io`（`astro.config.mjs` 的 `site` 必须用它）
- git 身份（已配置在本仓库）：WangZhi / wangzhi@example.com
- 所有验证命令在仓库根目录执行；每个任务结束时工作树必须干净（已提交）
- 测试策略：本站为纯静态站点，"测试"= `npm run build`（构建即内容校验）+ 对 `dist/` 产物的 grep 断言；schema 校验器本身用"坏数据构建必须失败"验证

---

### Task 1: 项目脚手架（Astro + Tailwind + main 分支）

**Files:**
- Create: `package.json`、`astro.config.mjs`、`tsconfig.json`、`src/pages/index.astro`（脚手架生成）
- Modify: `astro.config.mjs`（设 site）、`.gitignore`（脚手架会合并）

**Interfaces:**
- Produces: 可运行的 Astro 5 + Tailwind 4 工程；`npm run build` 产出 `dist/`；分支名 `main`

- [ ] **Step 1: 非交互创建 Astro minimal 工程**

在 `/home/administrator/personalPage`（非空目录，已有 docs/.gitignore 可共存）执行：

```bash
npm create astro@latest -- --template minimal --no-install --no-git --yes .
```

期望：生成 `package.json`、`astro.config.mjs`、`tsconfig.json`、`src/pages/index.astro`、`public/`。

- [ ] **Step 2: 安装依赖 + 添加 Tailwind**

```bash
npm install
npx astro add tailwind --yes
```

期望：安装 `tailwindcss`、`@tailwindcss/vite`；`astro.config.mjs` 出现 vite plugins 配置；生成 `src/styles/global.css`（内含 `@import "tailwindcss";`）。

- [ ] **Step 3: 配置 site 并改名分支**

`astro.config.mjs` 改为：

```js
// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://wangzhi.github.io',
  vite: {
    plugins: [tailwindcss()],
  },
});
```

```bash
git branch -m master main
```

- [ ] **Step 4: 验证构建**

```bash
npm run build
```

期望：`dist/index.html` 生成，无报错。

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: Astro 5 + Tailwind 4 脚手架"
```

---

### Task 2: 站点配置、全局样式、BaseLayout/Header/Footer

**Files:**
- Create: `src/config.ts`、`src/styles/global.css`（覆盖）、`src/layouts/BaseLayout.astro`、`src/components/Header.astro`、`src/components/Footer.astro`
- Modify: `src/pages/index.astro`（临时占位，Task 4 重写）

**Interfaces:**
- Produces:
  - `SITE` 对象（`src/config.ts`）：`{ name: string; title: string; description: string; email: string; github: string; giscus: { repo: string; repoId: string; category: string; categoryId: string } }`
  - Tailwind 颜色 token：`bg-bg` `bg-surface` `border-line` `text-ink` `text-muted` `text-accent`
  - `BaseLayout` props：`{ title?: string; description?: string; type?: 'website' | 'article'; publishedTime?: Date }`

- [ ] **Step 1: 写 src/config.ts**

```ts
export const SITE = {
  name: 'WangZhi',
  title: 'WangZhi 的主页',
  description: '写代码，也写字。',
  email: 'wangzhi@example.com',
  github: 'https://github.com/WangZhi', // TODO(你): 改成真实 GitHub 主页
  // giscus 全留空 = 不渲染评论区；配置方法见 README
  giscus: {
    repo: '',
    repoId: '',
    category: '',
    categoryId: '',
  },
} as const;
```

- [ ] **Step 2: 覆盖 src/styles/global.css**

```css
@import "tailwindcss";

@theme {
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-line: #21262d;
  --color-ink: #e6edf3;
  --color-muted: #8b949e;
  --color-accent: #58a6ff;
  --font-sans: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}

html {
  color-scheme: dark;
}

body {
  @apply bg-bg text-ink font-sans antialiased;
}

::selection {
  background: #58a6ff44;
}
```

- [ ] **Step 3: 写 Header.astro**

```astro
---
import { SITE } from '../config';

const links = [
  { href: '/', label: '首页' },
  { href: '/blog', label: '博客' },
  { href: '/archive', label: '归档' },
];
const current = Astro.url.pathname;
---
<header class="border-b border-line">
  <div class="mx-auto flex max-w-3xl items-center justify-between px-4 py-4">
    <a href="/" class="font-semibold text-ink hover:text-accent">{SITE.name}</a>
    <nav class="flex items-center gap-5 text-sm">
      {links.map((l) => (
        <a
          href={l.href}
          class:list={[
            'transition-colors',
            current === l.href || (l.href !== '/' && current.startsWith(l.href))
              ? 'text-accent'
              : 'text-muted hover:text-ink',
          ]}
        >
          {l.label}
        </a>
      ))}
      <a
        href={SITE.github}
        target="_blank"
        rel="noopener"
        aria-label="GitHub"
        class="text-muted transition-colors hover:text-ink"
      >
        <svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"></path>
        </svg>
      </a>
    </nav>
  </div>
</header>
```

- [ ] **Step 4: 写 Footer.astro**

```astro
---
import { SITE } from '../config';
const year = new Date().getFullYear();
---
<footer class="mt-20 border-t border-line">
  <div class="mx-auto flex max-w-3xl flex-col gap-2 px-4 py-8 text-sm text-muted sm:flex-row sm:items-center sm:justify-between">
    <span>© {year} {SITE.name}</span>
    <div class="flex gap-4">
      <a href={`/rss.xml`} class="hover:text-accent">RSS</a>
      <a href={`mailto:${SITE.email}`} class="hover:text-accent">邮箱</a>
      <a href={SITE.github} target="_blank" rel="noopener" class="hover:text-accent">GitHub</a>
    </div>
  </div>
</footer>
```

- [ ] **Step 5: 写 BaseLayout.astro**

```astro
---
import '../styles/global.css';
import { SITE } from '../config';
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';

interface Props {
  title?: string;
  description?: string;
  type?: 'website' | 'article';
  publishedTime?: Date;
}

const { title, description = SITE.description, type = 'website', publishedTime } = Astro.props;
const pageTitle = title ? `${title} · ${SITE.title}` : SITE.title;
const canonical = new URL(Astro.url.pathname, Astro.site);
---
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{pageTitle}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonical} />
    <meta property="og:type" content={type} />
    <meta property="og:site_name" content={SITE.title} />
    <meta property="og:title" content={pageTitle} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonical} />
    {publishedTime && <meta property="article:published_time" content={publishedTime.toISOString()} />}
    <link rel="alternate" type="application/rss+xml" title={SITE.title} href={`/rss.xml`} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  </head>
  <body class="min-h-screen">
    <Header />
    <main class="mx-auto max-w-3xl px-4">
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

- [ ] **Step 6: 临时首页（Task 4 会重写）**

`src/pages/index.astro`：

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout>
  <h1 class="py-20 text-2xl font-semibold">施工中</h1>
</BaseLayout>
```

- [ ] **Step 7: 验证构建 + 产物断言**

```bash
npm run build && grep -q '<!DOCTYPE html>' dist/index.html && grep -q 'lang="zh-CN"' dist/index.html && echo PASS
```

期望：输出 `PASS`。

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: 站点配置/全局暗色样式/BaseLayout/Header/Footer"
```

---

### Task 3: 内容模型（collections + zod）与示例内容

**Files:**
- Create: `src/content.config.ts`、`src/content/blog/hello-world.md`、`src/content/blog/second-post.md`、`src/content/projects/personal-page.md`、`src/content/projects/secret-tool.md`
- Delete: `src/content/`（若脚手架生成了 demo 目录，先清掉）

**Interfaces:**
- Produces:
  - collection `blog`，entry 字段：`id`(slug)、`body`、`data: { title: string; description: string; pubDate: Date; updatedDate?: Date; tags?: string[]; draft?: boolean }`
  - collection `projects`，entry 字段：`data: { title: string; description: string; url?: string; repo?: string; tech?: string[]; featured?: boolean; order?: number }`

- [ ] **Step 1: 写 src/content.config.ts**

```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    url: z.string().url().optional(),
    repo: z.string().url().optional(),
    tech: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    order: z.number().default(99),
  }),
});

export const collections = { blog, projects };
```

- [ ] **Step 2: 写示例文章**

`src/content/blog/hello-world.md`：

```markdown
---
title: 你好，世界
description: 主页的第一篇文章，说说我为什么做这个站点。
pubDate: 2026-09-06
tags:
  - astro
  - 随笔
---

这里是正文。用 Astro 搭建，Markdown 写作，push 即发布。

## 为什么自己搭

想要一个完全属于自己的角落：介绍、作品、文章都在一处。
```

`src/content/blog/second-post.md`（draft，用于验证不发布）：

```markdown
---
title: 还没写完的草稿
description: 这篇是草稿，构建后不应出现在任何页面。
pubDate: 2026-09-06
draft: true
---
草稿正文。
```

- [ ] **Step 3: 写示例作品**

`src/content/projects/personal-page.md`（featured）：

```markdown
---
title: personal-page
description: 你现在看到的这个主页，Astro + Tailwind 的静态站。
repo: https://github.com/WangZhi/personalPage
tech:
  - Astro
  - Tailwind
featured: true
order: 1
---
```

`src/content/projects/secret-tool.md`（非 featured，验证首页过滤）：

```markdown
---
title: secret-tool
description: 还不方便公开的小工具，不应出现在首页精选区。
tech:
  - TypeScript
featured: false
order: 2
---
```

- [ ] **Step 4: 验证构建通过**

```bash
npm run build
```

期望：成功（此时还没有页面消费 collection）。

- [ ] **Step 5: 验证 schema 校验真的会拦截坏数据（破坏性验证后还原）**

```bash
sed -i 's/^title: 你好，世界/title: 123/' src/content/blog/hello-world.md && \
sed -i 's/^pubDate: 2026-09-06/pubDate: 不是日期/' src/content/blog/hello-world.md && \
(npm run build > /tmp/bad-build.log 2>&1 && echo "FAIL: 应当报错" || echo "PASS: 校验生效") ; \
git checkout -- src/content/blog/hello-world.md && npm run build > /dev/null 2>&1 && echo "RESTORED"
```

期望：输出 `PASS: 校验生效` 和 `RESTORED`。

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: blog/projects 内容模型与示例内容（zod 校验）"
```

---

### Task 4: 首页四区块 + ProjectCard/PostItem 组件

**Files:**
- Create: `src/components/ProjectCard.astro`、`src/components/PostItem.astro`
- Modify: `src/pages/index.astro`（整体重写）

**Interfaces:**
- Consumes: Task 3 的 collections；Task 2 的 `SITE`、颜色 token、`BaseLayout`
- Produces:
  - `ProjectCard` props：`{ project: CollectionEntry<'projects'> }`
  - `PostItem` props：`{ post: CollectionEntry<'blog'> }`（渲染 `/blog/${post.id}/` 链接）

- [ ] **Step 1: 写 ProjectCard.astro**

```astro
---
import type { CollectionEntry } from 'astro:content';
interface Props { project: CollectionEntry<'projects'>; }
const { project } = Astro.props;
const { title, description, repo, url, tech } = project.data;
const link = url ?? repo;
---
<a
  href={link}
  target="_blank"
  rel="noopener"
  class="block rounded-lg border border-line bg-surface p-5 transition-colors hover:border-accent"
>
  <div class="flex items-baseline justify-between gap-3">
    <h3 class="font-semibold text-ink">{title}</h3>
    {tech.length > 0 && <span class="text-xs text-muted">{tech.join(' · ')}</span>}
  </div>
  <p class="mt-2 text-sm text-muted">{description}</p>
</a>
```

- [ ] **Step 2: 写 PostItem.astro**

```astro
---
import type { CollectionEntry } from 'astro:content';
interface Props { post: CollectionEntry<'blog'>; }
const { post } = Astro.props;
const date = post.data.pubDate.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
---
<a href={`/blog/${post.id}/`} class="group block border-b border-line py-4">
  <div class="flex items-baseline justify-between gap-4">
    <h3 class="font-medium text-ink group-hover:text-accent">{post.data.title}</h3>
    <time datetime={post.data.pubDate.toISOString()} class="shrink-0 text-xs text-muted">{date}</time>
  </div>
  <p class="mt-1 text-sm text-muted">{post.data.description}</p>
</a>
```

- [ ] **Step 3: 重写 src/pages/index.astro**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';
import ProjectCard from '../components/ProjectCard.astro';
import PostItem from '../components/PostItem.astro';
import { SITE } from '../config';

const projects = (await getCollection('projects', ({ data }) => data.featured))
  .sort((a, b) => a.data.order - b.data.order);

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf())
  .slice(0, 5);
---
<BaseLayout>
  <!-- Hero -->
  <section class="py-20">
    <h1 class="text-3xl font-bold tracking-tight">
      你好，我是 <span class="text-accent">{SITE.name}</span>
    </h1>
    <p class="mt-4 text-muted">{SITE.description}</p>
    <div class="mt-6 flex gap-4 text-sm">
      <a href={`mailto:${SITE.email}`} class="text-accent hover:underline">发邮件给我</a>
      <a href={SITE.github} target="_blank" rel="noopener" class="text-accent hover:underline">GitHub</a>
    </div>
  </section>

  <!-- 精选作品 -->
  {projects.length > 0 && (
    <section class="py-10">
      <h2 class="text-lg font-semibold text-ink">精选作品</h2>
      <div class="mt-5 grid gap-4 sm:grid-cols-2">
        {projects.map((p) => <ProjectCard project={p} />)}
      </div>
    </section>
  )}

  <!-- 最新文章 -->
  <section class="py-10">
    <div class="flex items-baseline justify-between">
      <h2 class="text-lg font-semibold text-ink">最新文章</h2>
      <a href="/blog" class="text-sm text-accent hover:underline">全部 →</a>
    </div>
    <div class="mt-3">
      {posts.map((p) => <PostItem post={p} />)}
    </div>
  </section>

  <!-- 联系 -->
  <section class="py-10 pb-20">
    <h2 class="text-lg font-semibold text-ink">找到我</h2>
    <p class="mt-3 text-sm text-muted">
      邮箱 <a href={`mailto:${SITE.email}`} class="text-accent hover:underline">{SITE.email}</a>，
      或到 <a href={SITE.github} target="_blank" rel="noopener" class="text-accent hover:underline">GitHub</a> 逛逛。
    </p>
  </section>
</BaseLayout>
```

- [ ] **Step 4: 验证构建 + 产物断言**

```bash
npm run build \
  && grep -q '你好，我是' dist/index.html \
  && grep -q 'personal-page' dist/index.html \
  && ! grep -q 'secret-tool' dist/index.html \
  && ! grep -q '还没写完的草稿' dist/index.html \
  && echo PASS
```

期望：输出 `PASS`（精选作品出现、非 featured 和草稿被过滤）。

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: 首页 Hero/精选作品/最新文章/联系四区块"
```

---

### Task 5: 博客列表页 + 文章详情页 + PostLayout

**Files:**
- Create: `src/pages/blog/index.astro`、`src/pages/blog/[slug].astro`、`src/layouts/PostLayout.astro`、`src/components/TagList.astro`
- Consumes: Task 3 collections、Task 2 BaseLayout、Task 4 PostItem

**Interfaces:**
- Produces: 路由 `/blog/`（列表）、`/blog/[slug]/`（详情）；`TagList` props：`{ tags: string[] }`，链接到 `/blog/tags/[tag]/`

- [ ] **Step 1: 写 TagList.astro**

```astro
---
interface Props { tags: string[]; }
const { tags } = Astro.props;
---
{tags.length > 0 && (
  <div class="flex flex-wrap gap-2">
    {tags.map((t) => (
      <a
        href={`/blog/tags/${t}/`}
        class="rounded-full border border-line px-2.5 py-0.5 text-xs text-muted transition-colors hover:border-accent hover:text-accent"
      >
        {t}
      </a>
    ))}
  </div>
)}
```

- [ ] **Step 2: 写 PostLayout.astro**

```astro
---
import BaseLayout from './BaseLayout.astro';
import TagList from '../components/TagList.astro';
import type { CollectionEntry } from 'astro:content';

interface Props { post: CollectionEntry<'blog'>; }
const { post } = Astro.props;
const { title, description, pubDate, updatedDate, tags } = post.data;
const date = pubDate.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
---
<BaseLayout title={title} description={description} type="article" publishedTime={pubDate}>
  <article class="py-12">
    <header class="border-b border-line pb-6">
      <h1 class="text-2xl font-bold tracking-tight text-ink">{title}</h1>
      <div class="mt-3 flex flex-wrap items-center gap-4 text-xs text-muted">
        <time datetime={pubDate.toISOString()}>发布于 {date}</time>
        {updatedDate && <span>更新于 {updatedDate.toLocaleDateString('zh-CN')}</span>}
        <TagList tags={tags} />
      </div>
    </header>
    <div class="prose-invert py-8 [&_a]:text-accent [&_a]:underline [&_a]:underline-offset-2
                [&_h2]:mt-10 [&_h2]:mb-3 [&_h2]:text-xl [&_h2]:font-semibold [&_h2]:text-ink
                [&_h3]:mt-8 [&_h3]:mb-2 [&_h3]:font-semibold [&_h3]:text-ink
                [&_p]:my-4 [&_p]:leading-7 [&_p]:text-ink
                [&_ul]:my-4 [&_ul]:list-disc [&_ul]:pl-6 [&_ul]:text-ink [&_ul]:leading-7
                [&_ol]:my-4 [&_ol]:list-decimal [&_ol]:pl-6 [&_ol]:text-ink [&_ol]:leading-7
                [&_code]:font-mono [&_code]:text-sm [&_code]:bg-surface [&_code]:rounded [&_code]:px-1.5 [&_code]:py-0.5
                [&_pre_code]:bg-transparent [&_pre]:bg-surface [&_pre]:border [&_pre]:border-line [&_pre]:rounded-lg [&_pre]:p-4 [&_pre]:overflow-x-auto [&_pre]:text-sm [&_pre]:leading-6
                [&_blockquote]:border-l-2 [&_blockquote]:border-line [&_blockquote]:pl-4 [&_blockquote]:text-muted">
      <slot />
    </div>
  </article>
</BaseLayout>
```

- [ ] **Step 3: 写 blog/index.astro（列表页）**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import PostItem from '../../components/PostItem.astro';
import TagList from '../../components/TagList.astro';

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

const tags = [...new Set(posts.flatMap((p) => p.data.tags))].sort();
---
<BaseLayout title="博客" description="全部文章">
  <section class="py-12">
    <h1 class="text-2xl font-bold tracking-tight">博客</h1>
    <div class="mt-4"><TagList tags={tags} /></div>
    <div class="mt-4">{posts.map((p) => <PostItem post={p} />)}</div>
  </section>
</BaseLayout>
```

- [ ] **Step 4: 写 blog/[slug].astro（详情页）**

```astro
---
import { getCollection, render } from 'astro:content';
import PostLayout from '../../layouts/PostLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.map((post) => ({ params: { slug: post.id }, props: { post } }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---
<PostLayout post={post}>
  <Content />
</PostLayout>
```

- [ ] **Step 5: 验证构建 + 产物断言**

```bash
npm run build \
  && test -f dist/blog/index.html \
  && test -f dist/blog/hello-world/index.html \
  && grep -q '想要一个完全属于自己的角落' dist/blog/hello-world/index.html \
  && ! test -f dist/blog/second-post/index.html \
  && echo PASS
```

期望：输出 `PASS`（详情页渲染正文、草稿无产物）。

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: 博客列表/详情页与文章排版"
```

---

### Task 6: 标签页 + 归档页

**Files:**
- Create: `src/pages/blog/tags/[tag].astro`、`src/pages/archive.astro`
- Consumes: Task 5 的 PostItem、BaseLayout

**Interfaces:**
- Produces: 路由 `/blog/tags/[tag]/`、`/archive`

- [ ] **Step 1: 写 blog/tags/[tag].astro**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';
import PostItem from '../../../components/PostItem.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const tags = [...new Set(posts.flatMap((p) => p.data.tags))];
  return tags.map((tag) => ({
    params: { tag },
    props: { posts: posts.filter((p) => p.data.tags.includes(tag)) },
  }));
}

const { tag } = Astro.params;
const { posts } = Astro.props;
---
<BaseLayout title={`标签：${tag}`} description={`标签「${tag}」下的文章`}>
  <section class="py-12">
    <p class="text-sm text-muted"><a href="/blog" class="text-accent hover:underline">博客</a> / 标签</p>
    <h1 class="mt-2 text-2xl font-bold tracking-tight">#{tag}</h1>
    <div class="mt-4">{posts.map((p) => <PostItem post={p} />)}</div>
  </section>
</BaseLayout>
```

- [ ] **Step 2: 写 archive.astro**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';

const posts = (await getCollection('blog', ({ data }) => !data.draft))
  .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

const byYear = new Map<number, typeof posts>();
for (const p of posts) {
  const y = p.data.pubDate.getFullYear();
  byYear.set(y, [...(byYear.get(y) ?? []), p]);
}
const years = [...byYear.keys()].sort((a, b) => b - a);
---
<BaseLayout title="归档" description="全部文章归档">
  <section class="py-12">
    <h1 class="text-2xl font-bold tracking-tight">归档</h1>
    {years.map((year) => (
      <div class="mt-8">
        <h2 class="text-sm font-semibold text-muted">{year}</h2>
        <ul class="mt-2 divide-y divide-line">
          {byYear.get(year)!.map((p) => (
            <li>
              <a
                href={`/blog/${p.id}/`}
                class="flex items-baseline justify-between gap-4 py-2.5 text-ink transition-colors hover:text-accent"
              >
                <span>{p.data.title}</span>
                <time datetime={p.data.pubDate.toISOString()} class="shrink-0 text-xs text-muted">
                  {p.data.pubDate.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })}
                </time>
              </a>
            </li>
          ))}
        </ul>
      </div>
    ))}
  </section>
</BaseLayout>
```

- [ ] **Step 3: 验证构建 + 产物断言**

```bash
npm run build \
  && test -f dist/blog/tags/astro/index.html \
  && test -f dist/archive/index.html \
  && grep -q '2026' dist/archive/index.html \
  && echo PASS
```

期望：输出 `PASS`。

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: 标签页与按年归档页"
```

---

### Task 7: RSS + sitemap + OG 完备

**Files:**
- Create: `src/pages/rss.xml.js`
- Modify: `astro.config.mjs`（加 sitemap 集成）

**Interfaces:**
- Consumes: Task 2 的 `SITE`、`astro.config.mjs` 已设 `site`
- Produces: `/rss.xml`、`/sitemap-index.xml`（OG/canonical 已在 Task 2 BaseLayout 完成）

- [ ] **Step 1: 添加 sitemap 集成**

```bash
npx astro add sitemap --yes
```

期望：`astro.config.mjs` 自动加入 `import sitemap from '@astrojs/sitemap'` 与 `integrations: [sitemap()]`。检查文件确认。

- [ ] **Step 2: 写 src/pages/rss.xml.js**

```js
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE } from '../config';

export async function GET(context) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  return rss({
    title: SITE.title,
    description: SITE.description,
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.id}/`,
    })),
  });
}
```

- [ ] **Step 3: 验证构建 + 产物断言**

```bash
npm run build \
  && grep -q '<rss' dist/rss.xml \
  && ! grep -q '还没写完的草稿' dist/rss.xml \
  && test -f dist/sitemap-index.xml \
  && grep -q 'og:title' dist/index.html \
  && echo PASS
```

期望：输出 `PASS`。

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: RSS 订阅源与 sitemap"
```

---

### Task 8: giscus 评论组件 + 404 页

**Files:**
- Create: `src/components/Comments.astro`、`src/pages/404.astro`
- Modify: `src/layouts/PostLayout.astro`（文章尾部挂评论区）

**Interfaces:**
- Consumes: Task 2 `SITE.giscus`（空字符串 = 不渲染）
- Produces: `Comments` 无 props，自读配置；`SITE.giscus.repo/repoId/category/categoryId` 四项齐全才渲染

- [ ] **Step 1: 写 Comments.astro**

```astro
---
import { SITE } from '../config';

const g = SITE.giscus;
const enabled = Boolean(g.repo && g.repoId && g.category && g.categoryId);
---
{enabled && (
  <section class="mt-12 border-t border-line pt-8">
    <h2 class="mb-4 text-lg font-semibold">评论</h2>
    <script
      is:inline
      src="https://giscus.app/client.js"
      data-repo={g.repo}
      data-repo-id={g.repoId}
      data-category={g.category}
      data-category-id={g.categoryId}
      data-mapping="pathname"
      data-strict="0"
      data-reactions-enabled="1"
      data-emit-metadata="0"
      data-input-position="top"
      data-theme="dark_dimmed"
      data-lang="zh-CN"
      data-loading="lazy"
      crossorigin="anonymous"
      async
    ></script>
  </section>
)}
```

- [ ] **Step 2: PostLayout 挂评论区**

在 `src/layouts/PostLayout.astro` 的 `</article>` 之前插入：

```astro
---
// （文件头部 import 区追加）
import Comments from '../components/Comments.astro';
---
```

并把 `</article>` 前追加 `<Comments />`（即 `<slot />` 所在 div 之后、`</article>` 之前）。

- [ ] **Step 3: 写 404.astro**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout title="页面不存在" description="404">
  <section class="py-24 text-center">
    <p class="text-5xl font-bold text-accent">404</p>
    <p class="mt-4 text-muted">这个页面不存在，可能被我删掉了。</p>
    <a href="/" class="mt-6 inline-block text-accent hover:underline">← 回首页</a>
  </section>
</BaseLayout>
```

- [ ] **Step 4: 验证构建 + 产物断言（未配置 giscus 时无评论脚本）**

```bash
npm run build \
  && test -f dist/404.html \
  && ! grep -q 'giscus.app' dist/blog/hello-world/index.html \
  && echo PASS
```

期望：输出 `PASS`。

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: giscus 评论占位与 404 页"
```

---

### Task 9: 部署 workflow、README、类型检查、总验收

**Files:**
- Create: `.github/workflows/deploy.yml`、`README.md`
- Modify: `package.json`（`check` 脚本）

**Interfaces:**
- Consumes: 全部前序任务的产物
- Produces: push main 自动部署到 GitHub Pages（Source: GitHub Actions 方式，比 spec 原文的 gh-pages 分支更简单，属对 spec 的实现细节修正）

- [ ] **Step 1: 安装类型检查工具并加脚本**

```bash
npm install -D @astrojs/check typescript
npm pkg set scripts.check="astro check"
```

- [ ] **Step 2: 写 .github/workflows/deploy.yml**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Install, build, and upload
        uses: withastro/action@v3

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: 写 README.md**

````markdown
# personal-page

WangZhi 的个人主页。Astro + Tailwind，静态生成，部署在 GitHub Pages。

## 本地开发

```bash
npm install
npm run dev      # http://localhost:4321
```

## 写文章 / 加作品

- 文章：`src/content/blog/` 新建 `xxx.md`，frontmatter 见 `src/content.config.ts`（title/description/pubDate 必填；`draft: true` 不发布）
- 作品：`src/content/projects/` 新建 `xxx.md`，`featured: true` 才会出现在首页精选区

## 发布

push 到 `main` 自动部署。首次使用需在 GitHub 仓库 **Settings → Pages → Source 选 "GitHub Actions"**（一次性）。

## 上线前需要改的占位

- `src/config.ts`：`github` 改成真实 GitHub 主页；`description` 按喜好改
- `astro.config.mjs`：若用自定义域名，改 `site` 并在 `public/` 加 `CNAME`
- 评论（可选）：到 https://giscus.app 按提示生成 `repo/repoId/category/categoryId` 四项填入 `src/config.ts` 的 `giscus`，评论区自动出现

## 检查

```bash
npm run check   # astro 类型检查
npm run build   # 构建即内容校验
```
````

- [ ] **Step 4: 全量验证（spec 验收清单的本地部分）**

```bash
npm run check && npm run build \
  && test -f dist/index.html && test -f dist/blog/index.html \
  && test -f dist/blog/hello-world/index.html \
  && test -f dist/blog/tags/astro/index.html \
  && test -f dist/archive/index.html && test -f dist/404.html \
  && test -f dist/rss.xml && test -f dist/sitemap-index.xml \
  && echo ALL-PASS
```

期望：`astro check` 无错误，输出 `ALL-PASS`。

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: GitHub Pages 部署 workflow 与 README"
```

- [ ] **Step 6: 推送上线（需用户确认）**

提醒用户：仓库建好后（如 `WangZhi/personalPage`）：

```bash
git remote add origin git@github.com:WangZhi/personalPage.git
git push -u origin main
```

再到仓库 Settings → Pages → Source 选 **GitHub Actions**。此步骤涉及远端操作，执行前必须获得用户明确同意。
