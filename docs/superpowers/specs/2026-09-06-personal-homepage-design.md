# 个人主页设计文档

日期：2026-09-06
状态：已与用户确认（布局、风格、强调色、功能范围均经可视化对比选定）

## 1. 背景与目标

从零搭建一个综合型个人主页：自我介绍 + 作品展示 + 博客 + 联系方式。
内容以 Markdown 文件维护，push 即发布，免服务器、免运维。

**成功标准**：
- 首页一屏内看清「我是谁、做什么、怎么联系」
- 写一篇新文章只需新建一个 `.md` 文件并 push
- Lighthouse 性能/SEO 接近满分，页面默认零 JS
- 全站构建（含内容校验）通过即视为可发布

## 2. 已确认的决策

| 决策点 | 结论 |
|---|---|
| 站点类型 | 综合型：介绍 + 作品 + 博客 + 联系 |
| 内容更新 | 静态 Markdown（无后台、无数据库） |
| 技术栈 | Astro v5 + Tailwind CSS |
| 部署 | GitHub Pages + GitHub Actions |
| 布局 | 单页首页（滚动）+ 博客列表/详情 + 标签页 + 归档页 |
| 视觉风格 | 极简暗色，深灰底 `#0d1117`，强调色链接蓝 `#58a6ff` |
| 语言 | 中文为主，代码/项目名保留英文，不做 i18n |
| 附加功能 | RSS、SEO（meta/sitemap/OG）、giscus 评论、标签/归档 |
| 作品详情页 | **不做**。作品卡片外链到 repo/在线地址；长介绍写博客文章 |

## 3. 架构

```
personalPage/
├── astro.config.mjs              # site URL、sitemap 集成
├── .github/workflows/deploy.yml  # push main → build → gh-pages
├── src/
│   ├── config.ts                 # 姓名、一句话介绍、社交链接、giscus 配置
│   ├── content/
│   │   ├── blog/                 # 文章 Markdown
│   │   ├── projects/             # 作品 Markdown
│   │   └── content.config.ts     # Content Collections + zod schema
│   ├── layouts/
│   │   ├── BaseLayout.astro      # <head>、导航、页脚、meta/OG
│   │   └── PostLayout.astro      # 文章详情布局（标题/日期/标签/正文/评论）
│   ├── components/
│   │   ├── Header.astro          # 顶部导航：名字 + 首页/博客/归档 + GitHub 图标
│   │   ├── Footer.astro
│   │   ├── ProjectCard.astro     # 作品卡片（标题/介绍/技术标签/外链）
│   │   ├── PostItem.astro        # 文章列表项（日期/标题/摘要/标签）
│   │   ├── TagList.astro         # 标签渲染
│   │   └── Comments.astro        # giscus 封装（仅文章详情页加载）
│   └── pages/
│       ├── index.astro           # Hero → 精选作品 → 最新 5 篇 → 联系
│       ├── blog/
│       │   ├── index.astro       # 全部文章，按 pubDate 倒序
│       │   ├── tags/[tag].astro  # 单标签文章列表（静态生成）
│       │   └── [slug].astro      # 文章详情（getStaticPaths 渲染 collection）
│       ├── archive.astro         # 按年份分组的纯文字归档
│       ├── rss.xml.js            # @astrojs/rss
│       └── 404.astro
```

- 纯静态输出（SSG），默认零客户端 JS；全站仅 giscus 评论区引入外部脚本。
- 页面间导航使用 Astro `<ClientRouter />`？——**不使用**，保持原生跳转，最简。

## 4. 内容模型

`src/content/content.config.ts` 用 zod 校验，字段缺失/拼错即构建失败。

**blog**（`src/content/blog/*.md`）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | ✓ | 标题 |
| description | string | ✓ | 一句话摘要，用于列表页与 og:description |
| pubDate | date | ✓ | 发布日期 |
| updatedDate | date | — | 修改日期（可选展示） |
| tags | string[] | — | 标签，用于标签页 |
| draft | boolean | — | 默认 false；true 时所有页面跳过 |

**projects**（`src/content/projects/*.md`）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| title | string | ✓ | 项目名 |
| description | string | ✓ | 一句话介绍 |
| url | string | — | 在线地址 |
| repo | string | — | 仓库地址 |
| tech | string[] | — | 技术栈标签 |
| featured | boolean | — | 默认 false；true 才出现在首页精选区 |
| order | number | — | 精选区排序，小的在前 |

projects 的 Markdown 正文仅作为卡片的扩展介绍保留（当前卡片只展示 frontmatter，正文预留）。

## 5. 视觉设计

- **底色体系**：主底 `#0d1117`，卡片/浮层 `#161b22`，边框 `#21262d`——与已确认的 mockup 一致。
- **文字**：主文字 `#e6edf3`，次要 `#8b949e`。
- **强调色**：链接蓝 `#58a6ff`，用于链接、名字点缀、悬停态、标签。
- **字体**：系统字体栈（`system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`），代码用 `ui-monospace` 系。不引入中文 webfont（体积过大）。
- **布局**：内容列最大宽度约 720px（文章）／全宽网格（作品卡片），移动端优先响应式。
- **细节**：极简留白、细分隔线；无渐变、无光效；少量 hover 过渡即可。

## 6. 附加功能

- **RSS**：`@astrojs/rss` 输出 `/rss.xml`，全量文章按时间倒序，页面页脚放订阅链接。
- **SEO**：`@astrojs/sitemap` 输出 sitemap；BaseLayout 为每页生成 title 模板（`页面名 · 站名`）、description、canonical、OG 标签；文章页带 `article:published_time`。
- **评论**：giscus（GitHub Discussions），配置项集中在 `src/config.ts`；仅 `blog/[slug]` 页按需加载。仓库建立后用户按 giscus 官网指引填 repo id 等四项；**未配置时评论区自动隐藏**（配置为空字符串即不渲染），保证构建永不因它失败。
- **标签**：`/blog/tags/[tag]` 静态生成所有标签页；博客列表页顶部标签云链接到对应页。
- **归档**：`/archive` 按年份分组，纯文字列表，无摘要。

## 7. 部署

- GitHub Actions：push 到 `main` → `npm ci && npm run build` → `withastro/action` 发布到 `gh-pages` 分支。
- 仓库 Settings → Pages → Source 设为 `gh-pages` 分支（一次性手动操作，写入 README 说明）。
- `astro.config.mjs` 的 `site` 填最终域名：`https://<username>.github.io`（若用自定义域名，改此处并在仓库加 CNAME）。

## 8. 错误处理与质量保障

- frontmatter 错误：zod schema 构建期拦截，报错信息含文件名与字段。
- 内容校验：`astro check`（类型）纳入 CI；`npm run build` 成功 = 内容与链接引用合法。
- 404 页面：全站兜底。
- 断链防护：正文内站内链接依赖构建期路由存在性（Astro 动态路由编译校验）。

## 9. 明确不做（YAGNI）

- 不做 i18n / 双语切换
- 不做亮色主题切换（只做暗色）
- 不做作品详情页
- 不做站内搜索、分页（文章量到几十篇再考虑）
- 不做后台管理/CMS
- 不引入分析统计（后续想加再说）

## 10. 验收清单

- [ ] 首页四区块（Hero/精选作品/最新文章/联系）渲染正常
- [ ] 示例文章 + 示例作品各至少 1 篇，frontmatter 校验生效
- [ ] 博客列表、标签页、归档、详情页、404 均可访问
- [ ] `/rss.xml`、`/sitemap-index.xml` 可访问
- [ ] giscus 未配置时不渲染评论区；配置后正常加载
- [ ] 移动端 375px 宽度下布局不破
- [ ] `npm run build` 与 `astro check` 通过
- [ ] GitHub Actions 部署成功，线上可访问
