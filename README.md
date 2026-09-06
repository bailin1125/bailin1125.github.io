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
