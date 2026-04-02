# 📚 装修家具知识库 - 本地索引

**版本**: 1.2.0
**更新**: 2026-03-30

---

## 🔍 快速检索指南

### 按主题查找

| 主题 | 文件位置 | 关键词 |
|------|---------|--------|
| 装修风格 | `knowledge_base/styles.md` | 奶油风/北欧/日式/新中式 |
| 家具选配 | `knowledge_base/furniture.md` | 沙发/床/餐桌/衣柜 |
| 人体尺度 | `references/06_Ergonomics_in_Interior_Design_CN.md` | 身高/尺寸/通道 |
| 色彩搭配 | `references/university_textbooks/05_color_theory.md` | 配色/色相/冷暖 |
| 预算规划 | `references/07_GB_Standards_Guide.md` | 预算/造价/省钱 |
| 施工标准 | `references/05_Decoration_Materials_CN.md` | 施工/验收/规范 |
| 灯光设计 | `references/01_Interior_Design_Illustrated.md` | 照明/色温/照度 |
| 装修避坑 | `references/BOOK_INDEX.md` | 猫腻/陷阱/合同 |

### 按书籍/教材查找

| 书籍/教材 | 文件 | 来源 |
|-----------|------|------|
| Ching 室内设计图解 | `01_Interior_Design_Illustrated.md` | 权威书籍 |
| Norman 设计心理学 | `02_Design_of_Everyday_Things.md` | 权威书籍 |
| 室内设计原理(高校) | `university_textbooks/01_interior_design_theory.md` | 高校教材 |
| 家具设计基础(高校) | `university_textbooks/02_furniture_design_fundamentals.md` | 高校教材 |
| 色彩理论(高校) | `university_textbooks/05_color_theory.md` | 高校教材 |
| GB标准规范 | `07_GB_Standards_Guide.md` | 国标 |

---

## 📁 目录结构

```
home-decor-kb/
├── SKILL.md                    # Skill定义
├── QUICK_REFERENCE.md         # 快速参考
├── README.md                 # 说明
├── knowledge_base/           # 基础知识库
│   ├── styles.md            # 8种装修风格
│   ├── furniture.md       # 家具选配
│   └── style_guide.md     # 风格完整指南
└── references/           # 专业参考文献
    ├── 01_Interior_Design_Illustrated.md
    ├── 02_Design_of_Everyday_Things.md
    ├── 03_Space_Planning_Basics.md
    ├── 04_Interior_Design_Principles_CN.md
    ├── 05_Decoration_Materials_CN.md
    ├── 06_Ergonomics_in_Interior_Design_CN.md
    ├── 07_GB_Standards_Guide.md
    ├── BOOK_INDEX.md               # 书籍索引
    ├── university_textbooks/       # 高校教材
    │   ├── 01_interior_design_theory.md
    │   ├── 02_furniture_design_fundamentals.md
    │   ├── 05_color_theory.md
    │   └── UNIVERSITY_COURSES.md
    └── books_original/            # 原始下载资源
        ├── download_textbooks.sh  # 下载脚本
        └── BOOK_INDEX.md       # 在线资源索引
```

---

## 💻 命令行查询

```bash
# 查看所有可用文件
ls -la ~/.agents/skills/home-decor-kb/references/

# 搜索关键词
grep -r "奶油风" ~/.agents/skills/home-decor-kb/
grep -r "人体尺度" ~/.agents/skills/home-decor-kb/
grep -r "预算" ~/.agents/skills/home-decor-kb/

# 统计行数
wc -l ~/.agents/skills/home-decor-kb/references/*.md
```

---

## 📊 内容统计

| 模块 | 文件数 | 总行数 | 核心概念 |
|------|--------|--------|----------|
| 装修风格 | 2 | 500+ | 8种风格 |
| 家具选配 | 1 | 300+ | 50+家具类型 |
| 权威书籍 | 7 | 2500+ | 200+专业术语 |
| 高校教材 | 4 | 2000+ | 150+知识点 |
| 在线资源 | 1 | 100+ | 20+链接 |

**总计**: 19个文件, 5500+行专业知识

---

## 🔗 在线资源（需联网）

see `books_original/BOOK_INDEX.md` for more resources.

---

## 📝 使用方法

**当用户咨询装修问题时：**
1. 先在 `knowledge_base/` 查找基础答案
2. 需要专业依据时��引用 `references/` 中的书籍内容
3. 高校教材内容更权威，可用于教学式回答

**引用格式示例**：
> 根据《室内设计原理》(高校教材)，室内设计的核心原则是...
> 根据 GB 50222-2017《建筑内部装修设计防火规范》...
> Ching 在《Interior Design Illustrated》中提出...

---

*本索引文件帮助快速定位知识库中的内容*