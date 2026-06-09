小红书内容转博客 Markdown工具 v2主要改进：
-清理所有不可见字符（零宽字符、BOM 等）
- 文件名拼接规范化-标题由用户手动输入（不再从内容提取）
- 自动生成 description- YAML字段安全转义用法：
python3 scripts/xhs-to-md.py"""

import sysimport reimport osfrom datetime import datetime# ============================================================
#文本清理工具# ============================================================

def remove_invisible_chars(text: str) -> str:
 """移除所有不可见字符（小红书复制会带这些）"""
 invisible_patterns = [
 r'\u200B', #零宽空格 r'\u200C', #零宽非连接符 r'\u200D', #零宽连接符 r'\u200E', # 左到右标记 r'\u200F', # 右到左标记 r'\u202A', # 从左到右嵌入 r'\u202B', # 从右到左嵌入 r'\u202C', #弹出方向格式 r'\u202D', # 从左到右覆盖 r'\u202E', # 从右到左覆盖 r'\u2060', #词连接符 r'\uFEFF', #字节顺序标记 (BOM)
 r'\u00AD', #软连字符 ]
 for pat in invisible_patterns:
 text = re.sub(pat, '', text)
 return textdef normalize_spaces(text: str) -> str:
 """规范化所有空白字符"""
 text = text.replace('\u3000', ' ')
 text = text.replace('\u2003', ' ')
 text = text.replace('\u00A0', ' ')
 text = text.replace('\t', ' ')
 text = re.sub(r' {2,}', ' ', text)
 return textdef clean_xhs_text(text: str) -> str:
 """完整清理小红书复制的内容"""
 text = remove_invisible_chars(text)
 text = normalize_spaces(text)
 lines = [line.rstrip() for line in text.split('\n')]
 text = '\n'.join(lines)
 return text.strip()


# ============================================================
# 文件名安全处理# ============================================================

def safe_filename(title: str, max_length: int =25) -> str:
 """生成安全的文件名片段"""
 title = remove_invisible_chars(title)
 punctuation = '，。、！？：；·…—「」『』《》（）()【】[]""\'\''
 for p in punctuation:
 title = title.replace(p, '-')
 title = title.replace(' ', '-')
 title = re.sub(r'[^\w\u4e00-\u9fff-]', '-', title)
 title = re.sub(r'-+', '-', title)
 title = title.strip('-')
 title = title[:max_length]
 title = title.rstrip('-')
 if not title:
 title = 'untitled'
 return title# ============================================================
# YAML 转义# ============================================================

def yaml_escape(text: str) -> str:
 """转义 YAML字符串中的特殊字符"""
 if not text:
 return '""'
 if any(c in text for c in [':', '"', "'", '#', '\n', '\r', '%', '@', '`']):
 escaped = text.replace('\\', '\\\\').replace('"', '\\"')
 return f'"{escaped}"'
 return text# ============================================================
# Markdown转换# ============================================================

def xhs_to_markdown(text: str) -> str:
 """基础的小红书文本转 Markdown"""
 text = clean_xhs_text(text)
 lines = text.split('\n')
 md_lines = []
 in_list = False list_type = None for line in lines:
 line = line.rstrip()
 if not line:
 if in_list:
 md_lines.append('')
 in_list = False list_type = None md_lines.append('')
 continue emoji_pattern = r'^[🎈⭐️🔥💡📌✅❌🌟💪🍎🥗📝🎯🏷️📖💰❤️]\s*'

 if line.startswith('##') or line.startswith('#'):
 cleaned = re.sub(r'^#+\s*', '', line)
 cleaned = re.sub(emoji_pattern, '', cleaned).strip()
 if cleaned:
 md_lines.append(f'## {cleaned}')
 continue if len(line)< 30 and not re.match(r'^[•·\-\d]', line):
 if not in_list and len(line)< 20:
 cleaned = re.sub(emoji_pattern, '', line).strip()
 if cleaned:
 md_lines.append(f'## {cleaned}')
 continue if re.match(r'^[•·]\s*', line):
 content = re.sub(r'^[•·]\s*', '', line)
 md_lines.append(f'- {content}')
 in_list = True list_type = 'ul'
 continue if re.match(r'^-\s+\S', line):
 content = re.sub(r'^-\s+', '', line)
 md_lines.append(f'- {content}')
 in_list = True list_type = 'ul'
 continue if re.match(r'^\d+[.、]\s*', line):
 content = re.sub(r'^\d+[.、]\s*', '', line)
 md_lines.append(f'1. {content}')
 in_list = True list_type = 'ol'
 continue if in_list:
 md_lines.append('')
 in_list = False md_lines.append(line)

 return '\n'.join(md_lines).strip()


def auto_description(content: str, max_length: int =60) -> str:
 """从内容自动生成 description"""
 text = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
 text = re.sub(r'[*_`>\-\[\]]+', '', text)
 text = re.sub(r'\n+', ' ', text).strip()
 if len(text) > max_length:
 desc = text[:max_length].rstrip() + '…'
 else:
 desc = text return yaml_escape(desc)


def generate_frontmatter(title: str, description: str, category: str, tags: list, source: str = '小红书') -> str:
 today = datetime.now().strftime('%Y-%m-%d')
 tag_str = ', '.join(tags)
 return f"""---
title: {yaml_escape(title)}
description: {description}
pubDatetime: {today}
category: {category}
tags: [{tag_str}]
source: {source}
---

"""def main():
 print('=' *50)
 print('📝 小红书内容转博客 Markdown工具 v2')
 print('=' *50)
 print()

 print('--- 第1步：输入文章标题 ---')
 title = input('标题: ').strip()
 if not title:
 print('❌标题不能为空')
 sys.exit(1)
 title = clean_xhs_text(title)
 print(f' ✓标题：{title}')
 print()

 print('--- 第2步：粘贴小红书正文 ---')
 print('（粘贴完内容后，输入两次回车结束）')
 print()
 lines = []
 empty_count =0 while empty_count< 2:
 try:
 line = input()
 if not line:
 empty_count +=1 else:
 empty_count =0 lines.append(line)
 except EOFError:
 break text = '\n'.join(lines).strip()
 if not text:
 print('❌ 没有输入正文内容')
 sys.exit(1)

 print(f' ✓ 正文 {len(text)} 个字符')
 print()

 print('--- 第3步：选择分类 ---')
 print('1. nutrition (营养健康)')
 print('2. reading (读书)')
 print('3. tools (效率工具)')
 print('4. money (财务保险)')
 print('5. life (生活随笔)')
 cat_choice = input('请输入 [1-5] (默认5): ').strip() or '5'
 cat_map = {'1': 'nutrition', '2': 'reading', '3': 'tools', '4': 'money', '5': 'life'}
 category = cat_map.get(cat_choice, 'life')
 print(f' ✓分类：{category}')
 print()

 print('--- 第4步：输入标签 ---')
 tags_input = input('标签 (用空格分隔，回车用默认 [小红书]): ').strip()
 tags = tags_input.split() if tags_input else ['小红书']
 print(f' ✓标签：{tags}')
 print()

 print('--- 第5步：转换中... ---')

 md_content = xhs_to_markdown(text)
 description = auto_description(md_content)
 frontmatter = generate_frontmatter(title, description, category, tags)
 full_md = frontmatter + md_content + '\n'

 today = datetime.now().strftime('%Y-%m-%d')
 safe_title = safe_filename(title)
 filename = f'{today}-{safe_title}.md'

 print()
 print('=' *50)
 print('✅转换完成！')
 print('=' *50)
 print()
 print(f'📁建议保存到: src/content/posts/{category}/{filename}')
 print()
 print('--- Frontmatter ---')
 print(frontmatter.rstrip())
 print()
 print('--- 正文预览 (前20 行) ---')
 preview = '\n'.join(md_content.split('\n')[:20])
 print(preview)
 if len(md_content.split('\n')) >20:
 print('... (省略后续内容)')
 print()
 print('---结束 ---')

 print()
 save = input('是否保存到文件？[y/N]: ').strip().lower()
 if save == 'y':
 target_dir = f'src/content/posts/{category}'
 os.makedirs(target_dir, exist_ok=True)
 target_path = os.path.join(target_dir, filename)
 if os.path.exists(target_path):
 overwrite = input(f'⚠️ 文件已存在，覆盖吗？[y/N]: ').strip().lower()
 if overwrite != 'y':
 print('❌ 已取消保存')
 sys.exit(0)
 with open(target_path, 'w', encoding='utf-8') as f:
 f.write(full_md)
 print(f'✅ 已保存到: {target_path}')
 else:
 print()
 print('💡手动复制上面"完整内容"部分，保存到对应目录即可。')
 print()
 print('完整 Markdown 内容：')
 print('---START---')
 print(full_md)
 print('---END---')


if __name__ == '__main__':
 main()
