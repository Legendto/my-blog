import { defineCollection, z } from 'astro:content';
import { CATEGORIES } from '../consts';

const categoryKeys = Object.keys(CATEGORIES) as [keyof typeof CATEGORIES, ...(keyof typeof CATEGORIES)[]];

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDatetime: z.coerce.date(),
    modDatetime: z.coerce.date().optional(),
    category: z.enum(categoryKeys),
    tags: z.array(z.string()).default([]),
    // 是否从其他平台同步过来
    source: z.string().optional(), // 例如 "小红书", "公众号"
    draft: z.boolean().default(false),
    // 可选封面图
    cover: z.string().optional(),
  }),
});

export const collections = { posts };