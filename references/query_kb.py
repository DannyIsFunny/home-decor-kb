#!/usr/bin/env python3
"""
🏠 装修知识库本地检索工具
用法: 
  python3 query_kb.py [关键词]
  python3 query_kb.py --interactive
"""

import os
import sys
import argparse

# 知识库根目录
KB_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_all_md_files():
    """获取所有markdown文件"""
    files = []
    for root, dirs, filenames in os.walk(KB_ROOT):
        for f in filenames:
            if f.endswith('.md') and not f.startswith('.'):
                files.append(os.path.join(root, f))
    return files

def search_kb(keyword, verbose=False):
    """搜索知识库"""
    results = []
    files = get_all_md_files()
    
    for filepath in files:
        rel_path = os.path.relpath(filepath, KB_ROOT)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if keyword.lower() in line.lower():
                    # 获取上下文（前后各1行）
                    context_start = max(0, i-2)
                    context_end = min(len(lines), i+2)
                    context = ''.join(lines[context_start:context_end])
                    
                    results.append({
                        'file': rel_path,
                        'line': i,
                        'content': line.strip()[:100],
                        'context': context[:200]
                    })
    
    # 去重
    seen = set()
    unique_results = []
    for r in results:
        key = (r['file'], r['line'], r['content'][:50])
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    return unique_results[:20]  # 最多返回20条

def print_result(result):
    """打印单条结果"""
    print(f"\n📄 {result['file']} (第{result['line']}行)")
    print(f"   {result['content']}")

def interactive_mode():
    """交互模式"""
    print("🏠 装修知识库 - 交互式检索")
    print("输入关键词搜索，输入 'quit' 退出\n")
    
    while True:
        try:
            keyword = input("🔍 搜索: ").strip()
            if not keyword:
                continue
            if keyword.lower() in ['quit', 'q', 'exit']:
                break
                
            results = search_kb(keyword)
            if results:
                print(f"\n找到 {len(results)} 条结果:\n")
                for r in results[:10]:
                    print_result(r)
            else:
                print("未找到相关内容")
                
        except (EOFError, KeyboardInterrupt):
            break
    
    print("\n再见！")

def main():
    parser = argparse.ArgumentParser(description="装修知识库检索工具")
    parser.add_argument('keyword', nargs='?', help='搜索关键词')
    parser.add_argument('-i', '--interactive', action='store_true', help='交互模式')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    args = parser.parse_args()
    
    if args.interactive or (not args.keyword and sys.stdin.isatty()):
        interactive_mode()
    elif args.keyword:
        results = search_kb(args.keyword, args.verbose)
        if results:
            print(f"🔍 搜索 '{args.keyword}' - 找到 {len(results)} 条结果:\n")
            for r in results:
                print_result(r)
        else:
            print(f"未找到 '{args.keyword}' 相关内容")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()