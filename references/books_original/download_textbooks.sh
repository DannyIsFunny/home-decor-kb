#!/bin/bash
# 下载装修/家具/室内设计相关免费教学资源
# 运行: cd ~/.agents/skills/home-decor-kb/references/books_original && bash download_textbooks.sh

DOWNLOAD_DIR="$(dirname "$0")"
mkdir -p "$DOWNLOAD_DIR"

echo "📥 开始下载教学资源..."

# 标准文档 (GB规范)
echo "📚 下载国家标准规范..."
curl -L -o "$DOWNLOAD_DIR/GB50222-2017_excerpt.txt" "https://open.stdmsg.com/gb/50222" 2>/dev/null &
curl -L -o "$DOWNLOAD_DIR/GB50327_excerpt.txt" "https://open.stdmsg.com/gb/50327" 2>/dev/null &

# MIT OpenCourseWare 室内设计相关课程
echo "📚 下载MIT课程资料..."
curl -L -o "$DOWNLOAD_DIR/mit_interior_design.txt" "https://ocw.mit.edu/courses/architecture/4-212-interior-design-anthropology-of-human-behavior-spring-2014/" 2>/dev/null &
curl -L -o "$DOWNLOAD_DIR/mit_architecture_studio.txt" "https://ocw.mit.edu/courses/architecture/4-301-architecture-studio-fall-2006/" 2>/dev/null &

# Wikipedia 离线版内容（可选）
echo "📚 准备Wikipedia内容..."
curl -s "https://en.wikipedia.org/wiki/Interior_design" 2>/dev/null | head -500 > "$DOWNLOAD_DIR/wikipedia_interior_design.txt" &
curl -s "https://en.wikipedia.org/wiki/Furniture" 2>/dev/null | head -500 > "$DOWNLOAD_DIR/wikipedia_furniture.txt" &
curl -s "https://en.wikipedia.org/wiki/Interior_design" 2>/dev/null | head -500 > "$DOWNLOAD_DIR/wikipedia_color_theory.txt" &

wait
echo "✅ 下载完成！"
ls -la "$DOWNLOAD_DIR"/*.txt 2>/dev/null | head -10