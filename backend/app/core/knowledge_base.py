"""
Home Decor Knowledge Base - Simple File-based Retrieval
使用 MiniMax LLM 实现知识检索和问答（简化版，无需额外依赖）
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import re


class KnowledgeBase:
    """知识库核心类 - 简化版，使用关键词匹配"""

    def __init__(self, knowledge_dir: str = None):
        self.knowledge_dir = knowledge_dir or self._get_default_knowledge_dir()
        self.documents = []
        self._load_documents()

    def _get_default_knowledge_dir(self) -> str:
        """获取默认知识库目录"""
        # __file__ = backend/app/core/knowledge_base.py
        # 往上走 3 层: app/core -> app -> backend -> 项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

        # 先检查 knowledge_base 目录
        kb_dir = os.path.join(project_root, "knowledge_base")
        if os.path.exists(kb_dir):
            return kb_dir

        # 再检查 references 目录
        ref_dir = os.path.join(project_root, "references")
        if os.path.exists(ref_dir):
            return ref_dir

        return project_root

    def _load_documents(self):
        """加载知识库文档"""
        # 同时加载 knowledge_base 和 references 目录
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)
        ))))

        knowledge_dirs = []
        kb_dir = os.path.join(project_root, "knowledge_base")
        if os.path.exists(kb_dir):
            knowledge_dirs.append(kb_dir)
        ref_dir = os.path.join(project_root, "references")
        if os.path.exists(ref_dir):
            knowledge_dirs.append(ref_dir)

        for knowledge_path_str in knowledge_dirs:
            knowledge_path = Path(knowledge_path_str)

            if not knowledge_path.exists():
                continue

            # 扫描所有 md 文件
            for md_file in knowledge_path.glob("**/*.md"):
                # 跳过索引文件
                if md_file.name.startswith('INDEX') or md_file.name.startswith('README'):
                    continue

                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 简单按段落分割
                        paragraphs = content.split('\n\n')
                        for para in paragraphs:
                            if len(para.strip()) > 30:
                                self.documents.append({
                                    "content": para.strip(),
                                    "source": md_file.name,
                                    "category": self._extract_category(md_file.name)
                                })
                except Exception as e:
                    print(f"Error loading {md_file}: {e}")

        print(f"Loaded {len(self.documents)} documents from knowledge base")

    def _extract_category(self, filename: str) -> str:
        """从文件名提取分类"""
        filename_lower = filename.lower()
        category_map = {
            "styles": "装修风格",
            "furniture": "家具选配",
            "ergonomics": "人体工程学",
            "color": "色彩理论",
            "budget": "预算规划",
            "materials": "材料选购",
            "standards": "标准规范",
            "design": "设计原理",
            "space": "空间规划"
        }
        for key, value in category_map.items():
            if key in filename_lower:
                return value
        return "其他"

    def query(self, question: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """简单关键词匹配检索"""
        # 提取问题中的关键词
        keywords = self._extract_keywords(question)

        if not keywords:
            # 如果没有关键词，返回前几个文档
            return self.documents[:top_k]

        # 评分每个文档
        scored = []
        for doc in self.documents:
            score = self._calculate_score(doc["content"], keywords)
            if score > 0:
                scored.append((score, doc))

        # 按分数排序，取前 top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [doc for _, doc in scored[:top_k]]

        return results

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词 - 简单按字符拆分"""
        # 提取中文字符
        chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')
        chars = chinese_pattern.findall(text)

        # 生成 2-4 个字的词组
        keywords = []
        for i in range(len(chars)):
            for length in [2, 3, 4]:
                if i + length <= len(chars):
                    word = ''.join(chars[i:i+length])
                    keywords.append(word)

        # 过滤掉太短的词，返回前 20 个
        return list(set(keywords))[:20]

    def _calculate_score(self, content: str, keywords: List[str]) -> float:
        """计算文档与关键词的匹配度"""
        score = 0

        for keyword in keywords:
            # 中文不需要转小写，直接计数
            score += content.count(keyword)

        return score

    def query_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """按分类查询"""
        results = [doc for doc in self.documents if doc["category"] == category]
        return results[:limit]

    def get_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set(doc["category"] for doc in self.documents)
        return sorted(list(categories))

    def rebuild_index(self):
        """重建索引"""
        self.documents = []
        self._load_documents()


# 全局实例
_knowledge_base = None


def get_knowledge_base() -> KnowledgeBase:
    """获取知识库单例"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base