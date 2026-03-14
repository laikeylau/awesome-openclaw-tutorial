#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

# CSDN 文章模板
CSDN_TEMPLATE = """# {title}

> 📚 **OpenClaw 2026.3.12 完整教程** - 从零开始打造你的AI工作助手
> 🌐 **在线阅读**：[https://awesome.tryopenclaw.asia](https://awesome.tryopenclaw.asia)
> 💻 **GitHub仓库**：[https://github.com/xianyu110/awesome-openclaw-tutorial](https://github.com/xianyu110/awesome-openclaw-tutorial)

---

{content}

---

## 📚 更多章节

- [第1章：认识 OpenClaw](https://awesome.tryopenclaw.asia/docs/01-basics/01-introduction/)
- [第2章：环境搭建](https://awesome.tryopenclaw.asia/docs/01-basics/02-installation/)
- [第3章：快速上手](https://awesome.tryopenclaw.asia/docs/01-basics/03-quick-start/)
- [第4章：本地文件管理](https://awesome.tryopenclaw.asia/docs/02-core-features/04-file-management/)
- [第5章：个人知识库](https://awesome.tryopenclaw.asia/docs/02-core-features/05-knowledge-management/)

## 🎯 相关资源

- **OpenClaw 官网**：[https://openclaw.ai](https://openclaw.ai)
- **OpenClaw 官方文档**：[https://docs.openclaw.ai](https://docs.openclaw.ai)
- **ClawHub 技能市场**：[https://clawhub.ai](https://clawhub.ai)
- **GitHub 教程仓库**：[https://github.com/xianyu110/awesome-openclaw-tutorial](https://github.com/xianyu110/awesome-openclaw-tutorial)

---

**版权声明**：本文采用 [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html) 许可证
**作者**：[MaynorAI](https://github.com/xianyu110)
**发布时间**：{publish_date}

> 💡 **温馨提示**：如果这篇教程对你有帮助，欢迎点赞、收藏、评论三连支持！
"""

# 需要同步到 CSDN 的章节列表
CHAPTERS_TO_SYNC = {
    # 基础章节
    "docs/01-basics/01-introduction.md": {
        "title": "OpenClaw 是什么？能帮你做什么？（含完整功能介绍）",
        "category": "OpenClaw从入门到精通",
        "tags": ["OpenClaw", "AI助手", "国产AI", "Agent"]
    },
    "docs/01-basics/02-installation.md": {
        "title": "OpenClaw 安装教程：5分钟完成本地/云端部署（含视频教程）",
        "category": "OpenClaw从入门到精通",
        "tags": ["OpenClaw", "安装教程", "云端部署", "Docker"]
    },
    "docs/01-basics/03-quick-start.md": {
        "title": "OpenClaw 快速上手：发送第一条消息，配置你的专属AI助手",
        "category": "OpenClaw从入门到精通",
        "tags": ["OpenClaw", "快速上手", "AI配置", "模型选择"]
    },

    # 核心功能
    "docs/02-core-features/04-file-management.md": {
        "title": "OpenClaw 本地文件管理神器：效率提升81%（含实战案例）",
        "category": "OpenClaw核心功能",
        "tags": ["OpenClaw", "文件管理", "AI助手", "效率提升"]
    },
    "docs/02-core-features/05-knowledge-management.md": {
        "title": "OpenClaw 个人知识库：网页/论文/GitHub一键存档",
        "category": "OpenClaw核心功能",
        "tags": ["OpenClaw", "知识管理", "第二大脑", "笔记系统"]
    },
    "docs/02-core-features/06-schedule-management.md": {
        "title": "OpenClaw 日程管理：微信截图秒变日历事件",
        "category": "OpenClaw核心功能",
        "tags": ["OpenClaw", "日程管理", "日历同步", "自动化"]
    },
    "docs/02-core-features/07-automation-workflow.md": {
        "title": "OpenClaw 自动化工作流：定时任务/网站监控/AI日报",
        "category": "OpenClaw核心功能",
        "tags": ["OpenClaw", "自动化", "定时任务", "工作流"]
    },

    # 进阶技能
    "docs/03-advanced/08-skills-extension.md": {
        "title": "OpenClaw Skills 扩展：492,000+个技能让AI无所不能",
        "category": "OpenClaw进阶技能",
        "tags": ["OpenClaw", "Skills", "技能扩展", "AI生态"]
    },
    "docs/03-advanced/09-multi-platform-integration.md": {
        "title": "OpenClaw 多平台集成：飞书/企微/钉钉/QQ一键接入",
        "category": "OpenClaw进阶技能",
        "tags": ["OpenClaw", "飞书", "企业微信", "钉钉", "QQ"]
    },
    "docs/03-advanced/10-api-integration.md": {
        "title": "OpenClaw API 服务集成：AI绘图/Notion/视频/语音",
        "category": "OpenClaw进阶技能",
        "tags": ["OpenClaw", "API集成", "AI绘图", "Notion"]
    },
    "docs/03-advanced/11-advanced-configuration.md": {
        "title": "OpenClaw 高级配置：多模型切换/成本优化/性能调优",
        "category": "OpenClaw进阶技能",
        "tags": ["OpenClaw", "高级配置", "成本优化", "性能调优"]
    },

    # 实战案例
    "docs/04-practical-cases/12-personal-productivity.md": {
        "title": "OpenClaw 实战案例：5类人群的效率提升（含真实数据）",
        "category": "OpenClaw实战案例",
        "tags": ["OpenClaw", "实战案例", "效率提升", "超级个体"]
    },
    "docs/04-practical-cases/13-advanced-automation.md": {
        "title": "OpenClaw 高级自动化工作流：Coding Agent/多Agent头脑风暴",
        "category": "OpenClaw实战案例",
        "tags": ["OpenClaw", "自动化", "Coding Agent", "多Agent"]
    },
    "docs/04-practical-cases/14-creative-applications.md": {
        "title": "OpenClaw 创意应用探索：AI绘画/视频/翻译/数据分析",
        "category": "OpenClaw实战案例",
        "tags": ["OpenClaw", "AI绘画", "视频生成", "数据分析"]
    },
    "docs/04-practical-cases/15-solo-entrepreneur-cases.md": {
        "title": "OpenClaw 超级个体实战案例：一人公司/自由职业/个人品牌",
        "category": "OpenClaw实战案例",
        "tags": ["OpenClaw", "超级个体", "一人公司", "自由职业"]
    },
}

def extract_title_from_content(file_path):
    """从文件内容中提取标题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        if first_line.startswith('# '):
            return first_line[2:].strip()
    return os.path.basename(file_path).replace('.md', '')

def clean_content(content):
    """清理内容，移除不适合CSDN的部分"""
    # 移除在线阅读链接部分
    content = re.sub(r'---\n\n## 🌐 在线阅读.*?(?=\n\n---|\n\n## |\Z)', '', content, flags=re.DOTALL)

    # 移除"下一章"、"返回目录"等导航链接
    content = re.sub(r'\*\*下一章\*\*.*', '', content)
    content = re.sub(r'\*\*返回目录\*\*.*', '', content)

    # 调整图片路径（如果需要）
    # content = content.replace('](docs/', '](https://github.com/xianyu110/awesome-openclaw-tutorial/blob/main/docs/')

    return content.strip()

def generate_csdn_article(file_path, metadata):
    """生成CSDN文章"""
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 清理内容
    content = clean_content(content)

    # 获取当前日期
    publish_date = datetime.now().strftime("%Y年%m月%d日")

    # 使用配置的标题或从内容提取
    title = metadata.get('title', extract_title_from_content(file_path))

    # 生成完整文章
    article = CSDN_TEMPLATE.format(
        title=title,
        content=content,
        publish_date=publish_date
    )

    return article, title, metadata

def save_csdn_articles():
    """保存所有CSDN文章到文件"""
    output_dir = "csdn_articles"
    os.makedirs(output_dir, exist_ok=True)

    generated_articles = []

    for file_path, metadata in CHAPTERS_TO_SYNC.items():
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {file_path}")
            continue

        try:
            # 生成文章
            article, title, meta = generate_csdn_article(file_path, metadata)

            # 保存文章
            filename = os.path.basename(file_path).replace('.md', '_csdn.md')
            output_path = os.path.join(output_dir, filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(article)

            generated_articles.append({
                'file': output_path,
                'title': title,
                'category': meta['category'],
                'tags': meta['tags']
            })

            print(f"✅ 已生成: {title}")
            print(f"   保存位置: {output_path}")
            print()

        except Exception as e:
            print(f"❌ 生成失败: {file_path}")
            print(f"   错误: {e}")
            print()

    # 生成发布清单
    generate_checklist(generated_articles, output_dir)

    print(f"\n🎉 完成！共生成 {len(generated_articles)} 篇CSDN文章")
    print(f"📁 文章保存在: {output_dir}/")
    print(f"📋 发布清单: {output_dir}/PUBLISH_CHECKLIST.md")

def generate_checklist(articles, output_dir):
    """生成发布清单"""
    checklist_path = os.path.join(output_dir, "PUBLISH_CHECKLIST.md")

    content = "# CSDN 发布清单\n\n"
    content += f"生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n\n"
    content += f"总计文章：{len(articles)} 篇\n\n"
    content += "---\n\n"
    content += "## 📋 发布步骤\n\n"
    content += "### 方法1：手动发布（推荐）\n\n"
    content += "1. 访问 [CSDN写作平台](https://mp.csdn.net/mp/blog/editBlog/publish)\n"
    content += "2. 点击「写文章」\n"
    content += "3. 复制下方文章内容\n"
    content += "4. 填写标题和分类\n"
    content += "5. 添加标签\n"
    content += "6. 发布文章\n\n"
    content += "### 方法2：Markdown导入\n\n"
    content += "1. 将文章文件保存为 .md 格式\n"
    content += "2. 在CSDN编辑器中选择「Markdown」模式\n"
    content += "3. 粘贴内容或导入文件\n\n"
    content += "---\n\n"
    content += "## 📝 文章列表\n\n"

    for i, article in enumerate(articles, 1):
        content += f"### {i}. {article['title']}\n\n"
        content += f"- **文件**: `{article['file']}`\n"
        content += f"- **分类**: {article['category']}\n"
        content += f"- **标签**: {', '.join(article['tags'])}\n"
        content += f"- **状态**: ⬜ 待发布\n\n"
        content += "---\n\n"

    content += "## 🎯 发布建议\n\n"
    content += "1. **发布顺序**：按章节顺序发布（第1章→第2章...）\n"
    content += "2. **发布频率**：每天1-2篇，避免被限流\n"
    content += "3. **最佳时间**：工作日 9:00-10:00 或 20:00-21:00\n"
    content += "4. **互动回复**：发布后及时回复评论和私信\n\n"
    content += "## 📊 发布后统计\n\n"
    content += "- [ ] 发布日期：______\n"
    content += "- [ ] 文章链接：______\n"
    content += "- [ ] 阅读量：______\n"
    content += "- [ ] 点赞数：______\n"
    content += "- [ ] 评论数：______\n"
    content += "- [ ] 收藏数：______\n\n"
    content += "---\n\n"
    content += "## 💡 发布技巧\n\n"
    content += "1. **封面图**：使用教程截图或相关配图\n"
    content += "2. **摘要**：用1-2句话概括文章亮点\n"
    content += "3. **关键词**：选择热门搜索词作为标签\n"
    content += "4. **互动引导**：文末添加「点赞、收藏、评论」提示\n\n"

    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 发布清单已生成: {checklist_path}")

if __name__ == "__main__":
    print("🚀 开始生成CSDN文章...\n")
    save_csdn_articles()
