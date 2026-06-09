# 🥗 个人博客

一个用 [Astro](https://astro.build) 构建的极简静态博客。专为"无代码经验"的内容创作者设计——**全程用浏览器点几下就能发布文章**。

## ✨ 特性

- ⚡ 静态生成，极速访问
- 📱 完全响应式，自带深色模式
- 🔍 自动 sitemap + RSS
- 🏷️ 5 个内容分类（营养健康 / 读书 / 工具 / 财务 / 生活）
- 📝 支持小红书内容同步
- 🚀 一键部署到 Vercel（免费）
- 💰 整体成本：~80 元/年（仅域名费）

---

## 🚀 5 分钟上线指南

### 第一步：把代码传到 GitHub

1. 注册/登录 [github.com](https://github.com)
2. 点右上角 `+` → `New repository`，名字随便起，比如 `my-blog`
3. **不要**勾选 "Initialize with README"
4. 在你电脑上打开终端（Terminal），进入 `blog` 目录：
   ```bash
   cd /Users/xueyu/Desktop/OH-WorkSpace/blog
   git init
   git add .
   git commit -m "init"
   git branch -M main
   git remote add origin https://github.com/Legendto/myblog.git
   git push -u origin main
   ```

### 第二步：部署到 Vercel（免费 + 自动）

1. 访问 [vercel.com](https://vercel.com)，用 GitHub 账号登录
2. 点 `Add New...` → `Project`
3. 选择你刚才创建的 `my-blog` 仓库，点 `Import`
4. **什么都不用改**，直接点 `Deploy`
5. 等 1-2 分钟，部署完成，会给你一个 `xxx.vercel.app` 的网址
6. **以后你 push 代码，Vercel 会自动重新部署**

### 第三步（可选）：绑定自己的域名

等你买了域名后，在 Vercel 项目设置 → Domains 里添加，跟着提示走即可。

---

## 📝 发布文章（最核心的部分）

### 🌟 推荐：GitHub 网页直接编辑（3 步）

**全程只用浏览器，不用装任何软件。**

1. 打开你的博客仓库：`https://github.com/你的用户名/my-blog`
2. 进入 `src/content/posts/营养/`（或者你想发布的分类）
3. 点 `Add file` → `Create new file`
4. 文件名以 `.md` 结尾，例如：`2026-06-09-我的早餐心得.md`
5. 把下面这段"文章模板"粘进去，改成你自己的内容：

```markdown
---
title: 我的早餐心得
description: 一句话简介
pubDatetime: 2026-06-09
category: nutrition
tags: [早餐, 蛋白质]
---

# 正文从这里开始

支持 Markdown 语法，**加粗** *斜体* [链接](https://example.com)

- 列表项 1
- 列表项 2

![图片说明](/images/photo.jpg)
```

6. 滚到底部，点绿色的 `Commit changes` 按钮
7. **等 1-2 分钟**，博客自动更新 ✅

### 方式 2：本地用编辑器（适合经常写）

推荐下载 [MarkText](https://marktext.app/)（免费，所见即所得）：

1. 用 MarkText 写文章，保存为 `.md` 文件
2. 把文件放到 `src/content/posts/对应分类/` 目录下
3. 安装 [GitHub Desktop](https://desktop.github.com/)（图形化 Git 工具）
4. 用它打开 `blog` 文件夹
5. 看到新文件后，写个说明（比如"新增早餐文章"），点 `Commit to main`
6. 点 `Push origin`，Vercel 自动部署

### 方式 3：小红书内容同步

用 `scripts/xhs-to-md.py` 工具：

```bash
cd /Users/xueyu/Desktop/OH-WorkSpace/blog
python3 scripts/xhs-to-md.py
```

按提示操作即可。脚本会生成符合博客格式的 Markdown 文件。

---

## 📁 目录结构

```
blog/
├── src/
│   ├── content/posts/    # 👈 你的所有文章放在这里
│   │   ├── nutrition/    # 营养健康
│   │   ├── reading/      # 读书
│   │   ├── tools/        # 效率工具
│   │   ├── money/        # 财务保险
│   │   └── life/         # 生活随笔
│   ├── pages/            # 网站页面（一般不用动）
│   ├── layouts/          # 布局模板
│   ├── styles/           # 全局样式
│   ├── consts.ts         # 👈 改站名、分类在这里
│   └── utils/            # 工具函数
├── public/
│   └── images/           # 👈 你的图片放在这里
├── scripts/
│   └── xhs-to-md.py      # 小红书同步工具
├── astro.config.mjs      # Astro 配置
└── package.json
```

## 🎨 个性化定制

### 改站名、导航

打开 `src/consts.ts`，修改：
- `SITE.title`：站名
- `SITE.description`：简介
- `CATEGORIES`：分类配置（颜色、说明）

### 改主题颜色

打开 `src/styles/global.css`，修改：
- `--accent`：主题强调色（默认绿色）

### 加分类

1. `src/consts.ts` 的 `CATEGORIES` 里加新分类
2. `src/content/posts/` 下创建对应目录
3. 在首页会自动出现

---

## 🛠️ 本地开发（可选）

如果你想在本地预览效果：

```bash
cd /Users/xueyu/Desktop/OH-WorkSpace/blog
npm install     # 第一次需要装依赖
npm run dev     # 启动本地预览，访问 http://localhost:4321
```

修改文件后浏览器会自动刷新。

---

## 📋 文章 frontmatter 字段说明

每篇文章开头要有一段元信息：

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `title` | ✅ | 文章标题 | `早餐搭配指南` |
| `pubDatetime` | ✅ | 发布日期 | `2026-06-09` |
| `category` | ✅ | 分类（5选1） | `nutrition` |
| `description` | | 一句话简介 | `一份扛饿早餐的营养学逻辑` |
| `tags` | | 标签数组 | `[早餐, 蛋白质]` |
| `source` | | 内容来源 | `小红书` |
| `draft` | | 是否草稿 | `false` |
| `modDatetime` | | 最后修改时间 | `2026-06-10` |
| `cover` | | 封面图路径 | `/images/cover.jpg` |

---

## ❓ 常见问题

**Q：博客更新后多久生效？**
A：GitHub push 后，Vercel 一般 1-2 分钟内自动部署完成。

**Q：分类写错了会怎样？**
A：网站会报错。必须是 `nutrition / reading / tools / money / life` 之一。

**Q：图片太大影响加载怎么办？**
A：把图片压缩到 500KB 以内（可以用 tinypng.com 压缩）。

**Q：怎么删除文章？**
A：GitHub 网页打开对应文件，点右上角 🗑️ 图标。

**Q：博客可以加评论功能吗？**
A：可以集成 Giscus（基于 GitHub Discussion，免费），后续教程会加。

**Q：怎么让搜索引擎收录？**
A：Vercel 自动生成 sitemap，Google Search Console 提交一下即可。

---

## 📜 License

MIT - 随便用，但保留原作者信息即可。