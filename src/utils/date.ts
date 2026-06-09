// 日期格式化工具
export const localeMap: Record<string, string> = {
  'zh-CN': 'zh-CN',
  'en': 'en-US',
};

export function formatDate(date: Date, lang = 'zh-CN'): string {
  return date.toLocaleDateString(localeMap[lang] || lang, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export function formatDateShort(date: Date, lang = 'zh-CN'): string {
  return date.toLocaleDateString(localeMap[lang] || lang, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
}

// 估算阅读时间（中文按字符数计算，英文按单词数）
export function estimateReadingTime(content: string, lang = 'zh-CN'): string {
  const cleanText = content.replace(/```[\s\S]*?```/g, '').replace(/<[^>]+>/g, '');
  let minutes: number;
  if (lang === 'zh-CN') {
    // 中文按每分钟 400 字
    const charCount = cleanText.length;
    minutes = Math.ceil(charCount / 400);
  } else {
    const words = cleanText.split(/\s+/).length;
    minutes = Math.ceil(words / 200);
  }
  return minutes <= 1 ? '1 分钟阅读' : `${minutes} 分钟阅读`;
}