// 站点全局配置 - 在这里改站名/简介/导航
export const SITE = {
  title: '营养师笔记',
  description: '一个注册营养师的个人博客 — 营养健康、效率工具、读书与生活。',
  author: '大哥',
  // 这里换成你的社交链接，没有就留空
  social: {
    xhs: 'https://www.xiaohongshu.com/user/profile/你的ID',  // 小红书
    weibo: '',  // 微博
    email: 'your-email@example.com',
  },
  // 默认语言
  lang: 'zh-CN',
};

// 分类配置 - 在这里增删改分类
export const CATEGORIES = {
  nutrition: {
    label: '营养健康',
    desc: '饮食、营养与健康的科学笔记',
    color: '#16a34a',
  },
  reading: {
    label: '读书',
    desc: '读书心得与笔记摘录',
    color: '#2563eb',
  },
  tools: {
    label: '效率工具',
    desc: 'AI、效率工具与工作流',
    color: '#9333ea',
  },
  money: {
    label: '财务保险',
    desc: '保险、财务规划与消费思考',
    color: '#ea580c',
  },
  life: {
    label: '生活随笔',
    desc: '生活观察与杂记',
    color: '#64748b',
  },
} as const;

export type CategoryKey = keyof typeof CATEGORIES;