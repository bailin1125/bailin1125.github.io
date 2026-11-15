# 个人主页 → 产品门户升级 spec（2026-10-30）

> 状态：草案，待用户确认。确认后作为本轮升级的裁决权威（优先级：本 spec > 原 spec > plan）。

## 1. 目标与定位

站点从「个人博客主页」升级为**独立开发者的产品门户**：

- 首屏传达品牌与定位：做了什么、正在做什么
- 产品成为一等公民：列表页 + 详情页，展示真实产品与状态
- 博客保留（写作仍是站点支柱之一），但首页权重让位给产品
- 访客画像：潜在用户、合作方、同行开发者

原 spec（2026-09-06-personal-homepage-design.md）中与本章冲突的条款以本文为准；未提及的全部沿用（暗色 token、零客户端 JS、系统字体、无中文 webfont、纯 SSG 等）。

## 2. 品牌与文案

| 项 | 决定 |
|---|---|
| 品牌 | 个人品牌工作室（无公司主体，不注册名义）；个人身份收进「关于我」 |
| Hero 品牌名 | **开放项 A（待定）**，默认建议：`WangZhi` 加粗大字 + 定位语「独立开发者 · 做实用的小产品」 |
| CTA | 主 CTA「看产品 →」锚到产品区；次级链接 GitHub / 联系 |
| 站点 title/og | 「WangZhi · 产品与写作」类目调整（实现时定稿） |

## 3. 信息架构

```
导航：首页 · 产品 · 博客 · 归档        ← 新增「产品」
/                     首页：Hero(品牌) → 产品精选(3) → 关于我 → 最新文章 → 联系
/products             产品列表：全部产品卡（按状态分组或按 order 排序）
/products/[slug]      产品详情：标题/状态徽章/截图区/简介/卖点/链接/技术栈
/blog  /archive  /404 /rss  不变
```

- 首页产品精选区：取 `featured` 前 3，卡片升级（见 §5）
- 详情页路由基于现有 `projects` collection 的 entry slug

## 4. 内容模型（projects schema 扩展）

```ts
title        string                  // 产品名（必填）
description  string                  // 一句话（列表卡/og 用，必填）
status       enum                    // live=已上线 beta=内测 development=开发中 self-use=自用 coming-soon=预告（必填，默认 development）
longText     string                  // 详情页首段（可选）
features     string[]                // 卖点短句 3-5 条（可选）
url          url                     // 在线地址（可选）
repo         url                     // 代码仓库（可选）
tech         string[]                // 技术栈（默认 []）
image        string                  // 截图/封面，public/products/<slug>.png（可选，缺省用排版化占位）
featured     boolean                 // 上首页精选（默认 false）
order        number                  // 排序权重（默认 99）
```

- 反向校验（坏数据构建必失败）沿用原 spec 方式
- 修复历史遗留：`url`/`repo` 至少其一**不强制**（预告位/自用工具有链接反而错），但详情页无链接时隐藏入口区

## 5. 组件与视觉

**ProductCard 升级**（首页与列表页共用）：

- 上半：图片区（16:10，有 `image` 用图，无图用 `bg-surface` 色块 + 居中产品名缩写排版）
- 下半：产品名 + 状态徽章 + description + tech 小字
- 卡片整块可点 → 详情页（不再是外链新窗）

**状态徽章（不新增颜色）**：

| status | 徽章样式（chip） |
|---|---|
| live | border-accent text-accent |
| beta | border-accent text-muted（描边亮、字灰） |
| development | border-line text-muted |
| self-use | border-line text-muted，文案「自用」 |
| coming-soon | border-line text-muted，文案「即将上线」 |

**产品详情页**：

- 顶部：面包屑「← 产品」/ 大标题 + 徽章 / description
- 截图区：大图或占位（同卡片策略）
- 正文：longText 段落 + features 列表（无序列表）
- 入口区：url（在线使用）/ repo（源码）按钮式链接；无则整区隐藏
- tech 以 chip 展示（复用 TagList 视觉）
- 布局沿用 BaseLayout + 文章页排版 token，居中 max-w-3xl

**其余视觉纪律**：六 token 不动、无渐变无光效、强调色仍限链接/悬停/标签/名字点缀；徽章归「标签」类。

## 6. 产品清单（首批）

| 产品 | status | 首发内容口径 | 链接 |
|---|---|---|---|
| 火花快讯 SparkFeed | beta | 五源情报（GitHub/HN/国内科技财经 RSS）→ LLM 合成带变现测算的商业点子 + 火花分，每日邮件送达 | 无公开落地页 → 入口区隐藏，卖点写「即将开放订阅」 |
| 《第三战》dierzhan | development | 人生模拟游戏，九域人生/一周目 365 天；Steam 上架筹备中 | repo 私有 → 入口区隐藏；封面用游戏内插画 1 张（开放项 B） |
| AI 虚拟试衣 clothesShow | development | 虚拟试衣 Demo：Flutter App + Node.js BFF + Replicate IDM-VTON 换装生成 | repo 私有 → 入口区隐藏 |
| 量化分析系统 | self-use | 日频基金/个股推荐：真实成本回测、月度调仓、双基准对照；明确自用不对外 | 无外部链接；徽章「自用」 |
| 预留位 ×2 | coming-soon | 只建卡（默认「未命名项目 A/B」，开放项 C） | 无 |
| personal-page | live | 本站本身；升级为新卡片形态，从首页精选撤下（列表页保留） | repo=本仓库 |

**清理**：删除 cli-toolkit / feed-reader / dotfiles 三个占位卡（对应仓库不存在，避免死链）。secret-tool 原本非 featured 不展示，一并删除保持目录干净。

## 7. 明确不做（YAGNI 增补）

不做定价页、不做用户系统/订阅收集表单、不做产品 changelog 页、不做 i18n、不做亮色主题、不做搜索、不做动效（滚动动画/渐显）。原 YAGNI 清单其余全部沿用。

## 8. 验收清单（本地部分）

- [ ] 导航含「产品」，/products 与 /products/[slug] 全部产出
- [ ] 五个产品 + 两个预告位各有详情页；徽章样式按 §5 表格
- [ ] 首页 Hero 传达品牌与定位，产品精选 3 张新形态卡片
- [ ] cli-toolkit/feed-reader/dotfiles/secret-tool 已删，无死链（全站 grep 断言）
- [ ] blog/archive/tags/rss/404 回归不变（产出文件与关键断言复跑）
- [ ] `astro check` 0 错误；`npm run build` 绿；dist 断言含反向断言（无旧占位产品名残留）
- [ ] 线上部署成功且抽查 200

## 9. 开放项（需用户定）

- **A. 品牌名与定位语**：默认「WangZhi」+「独立开发者 · 做实用的小产品」，可换
- **B. 《第三战》插画**：是否同意从本机游戏仓库取 1 张 AI 插画作详情页封面（CC 素材来源标注会在详情页 tech 区旁注明）；不同意则用排版化占位
- **C. 预告位命名**：两个 coming-soon 占位默认「未命名项目 A/B」，可换
