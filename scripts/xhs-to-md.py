#!/usr/bin/env python3
"""
小红书内容转博客 Markdown 工具

用法：
1. 在小红书 App 打开你想同步的笔记
2. 长按正文 → 复制
3. 运行: python3 scripts/xhs-to-md.py
4. 把剪切板内容粘进去，按两次回车结束
5. 脚本会输出 Markdown，直接粘到博客对应分类目录

依赖：pip install pyperclip（可选）
"""

import sys
import re
from datetime import datetime
import os


def clean_xhs_text(text: str) -> str:
    """清理小红书文本中的特殊字符"""
    # 小红书的特殊空格
    text = text.replace('\u2003', ' ')  # 全角空格
    text = text.replace('\u3000', ' ')  # 全角空格
    text = text.replace('\xa0', ' ')    # 不间断空格
    return text.strip()


def xhs_to_markdown(text: str) -> str:
    """基础的小红书文本转 Markdown"""
    text = clean_xhs_text(text)

    lines = text.split('\n')
    md_lines = []
    in_list = False
    list_type = None

    for line in lines:
        line = line.rstrip()
        if not line:
            if in_list:
                md_lines.append('')
                in_list = False
                list_type = None
            md_lines.append('')
            continue

        # 小红书的 emoji 开头（很多笔记是 🎈标题🎈 这样的）
        emoji_pattern = r'^[🎈⭐️🔥💡📌✅❌🌟💪🍎🥗📝🎯]+\s*'

        # 标题检测：行末以 emoji 结尾的短行
        if len(line) < 30 and not line.startswith('-') and not line.startswith('•'):
            cleaned = re.sub(emoji_pattern, '', line).strip()
            if cleaned and not in_list:
                # 检查是否像标题
                md_lines.append(f'## {cleaned}')
                continue

        # 无序列表 - 以 • · 或者数字开头
        if re.match(r'^[•·\-]\s+', line):
            content = re.sub(r'^[•·\-]\s+', '', line)
            md_lines.append(f'- {content}')
            in_list = True
            list_type = 'ul'
            continue

        # 数字列表
        if re.match(r'^\d+[.、]\s+', line):
            content = re.sub(r'^\d+[.、]\s+', '', line)
            md_lines.append(f'1. {content}')
            in_list = True
            list_type = 'ol'
            continue

        # 普通段落
        if in_list:
            md_lines.append('')
            in_list = False
        md_lines.append(line)

    return '\n'.join(md_lines).strip()


def generate_frontmatter(title: str, category: str, tags: list, source: str = '小红书') -> str:
    """生成博客文章的 frontmatter"""
    today = datetime.now().strftime('%Y-%m-%d')
    tag_str = ', '.join(tags)
    return f"""---
title: {title}
description:
pubDatetime: {today}
category: {category}
tags: [{tag_str}]
source: {source}
---

"""


def main():
    print('=' * 50)
    print('📝 小红书内容转博客 Markdown 工具')
    print('=' * 50)
    print()

    # 读取多行输入
    print('请粘贴小红书内容（输入两行空行结束）:')
    print()
    lines = []
    empty_count = 0
    while empty_count < 2:
        try:
            line = input()
            if not line:
                empty_count += 1
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break

    text = '\n'.join(lines).strip()
    if not text:
        print('❌ 没有输入内容')
        sys.exit(1)

    # 提取标题（第一行通常就是标题）
    raw_lines = [l for l in text.split('\n') if l.strip()]
    title = raw_lines[0].strip()[:50] if raw_lines else '未命名'

    # 询问分类
    print()
    print('分类选择 (输入数字):')
    print('1. nutrition (营养健康)')
    print('2. reading (读书)')
    print('3. tools (效率工具)')
    print('4. money (财务保险)')
    print('5. life (生活随笔)')
    cat_choice = input('请输入 [1-5]: ').strip()
    cat_map = {'1': 'nutrition', '2': 'reading', '3': 'tools', '4': 'money', '5': 'life'}
    category = cat_map.get(cat_choice, 'life')

    # 询问标签
    tags_input = input('标签 (用空格分隔，回车跳过): ').strip()
    tags = tags_input.split() if tags_input else ['小红书']

    # 转换
    md_content = xhs_to_markdown(text)
    frontmatter = generate_frontmatter(title, category, tags)
    full_md = frontmatter + md_content + '\n'

    # 生成文件名
    today = datetime.now().strftime('%Y-%m-%d')
    safe_title = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title)[:30]
    filename = f'{today}-{safe_title}.md'

    # 输出
    print()
    print('=' * 50)
    print('✅ 转换完成！')
    print('=' * 50)
    print()
    print(f'📁 建议保存到: src/content/posts/{category}/{filename}')
    print()
    print('--- 完整内容 ---')
    print(full_md)
    print('--- 结束 ---')

    # 询问是否保存
    save = input('\n是否保存到文件？[y/N]: ').strip().lower()
    if save == 'y':
        target_dir = f'src/content/posts/{category}'
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, filename)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(full_md)
        print(f'✅ 已保存到: {target_path}')
    else:
        print()
        print('💡 手动复制上面"完整内容"部分，保存到对应目录即可。')


if __name__ == '__main__':
    main()