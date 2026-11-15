# 产品门户升级实现计划（2026-10-30）

> Spec: docs/superpowers/specs/2026-10-30-product-portal-upgrade.md（裁决权威）
> 分支 feature/product-portal，每任务一提交，断言必跑。

## Task 1: schema 扩展 + 产品内容 + 素材

- `src/content.config.ts` projects schema 加：status（enum，默认 development）、longText、features、image
- 产品文件：sparkfeed.md（火花快讯 beta）、dierzhan.md（第三战 development）、tryon.md（虚拟试衣 development）、quant-system.md（self-use）、unnamed-a.md / unnamed-b.md（coming-soon）、personal-page.md（live，featured:false）
- 删：cli-toolkit.md / feed-reader.md / dotfiles.md / secret-tool.md
- 素材：public/products/dierzhan.png（从游戏仓库取插画 1 张，file 确认真实格式）
- 验证：build 绿 + 反向断言（坏 status 构建失败可手工验一次）

## Task 2: StatusBadge + ProductCard 升级

- 新建 `src/components/StatusBadge.astro`（props: status；样式按 spec §5 表）
- 重写 `src/components/ProductCard.astro`：图片区（16:10，有 image 用 <img>，无图 bg-surface 色块+产品名缩写）+ 标题+徽章+description+tech；整卡链接到 /products/[slug]/（内部链接，非新窗）
- 验证：build 绿

## Task 3: 导航 + 产品列表页

- `src/components/Header.astro` 加「产品」（首页与博客之间），当前路由高亮复用既有逻辑
- 新建 `src/pages/products/index.astro`：标题「产品」+ 全部 ProductCard（按 order 排序，grid sm:grid-cols-2）
- 验证：build + dist/products/index.html 存在且含各产品名

## Task 4: 产品详情页

- 新建 `src/pages/products/[slug].astro`：面包屑「← 产品」/ h1+徽章 / description / 大图或占位 / longText / features 列表 / 入口区（url「在线使用」+ repo「源码」，均无则隐藏）/ tech chips
- BaseLayout：title=产品名，description=description，type=website
- 验证：7 个产品详情页产出；私有产品页无外链入口区；404 兜底不受影响

## Task 5: 首页改造

- Hero：大字品牌（WangZhi）+ 定位语「独立开发者 · 做实用的小产品」+ 主 CTA「看产品 →」（锚 #products）+ 次级 GitHub/邮箱
- 产品精选区：id="products"，featured 前 3（新卡片）
- 关于我/最新文章/联系保留
- 站点 title 调整：SITE.title「WangZhi · 产品与写作」（og 同步）
- 验证：build + dist/index.html 含品牌 Hero 与产品区

## Task 6: 回归 + 总验收 + 部署

- 全量断言：/products、7 详情页、导航含产品、blog/archive/tags/rss/404 回归、无旧占位产品名残留（grep 反向断言）、check 0 错误
- 提交、合并 main、push、盯 Actions 至 success、线上抽查 200
