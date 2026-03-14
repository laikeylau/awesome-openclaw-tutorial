#!/usr/bin/env python3
"""
生成附录的 CSDN 文章
"""

import os
import re
from pathlib import Path

# 附录文件映射
APPENDIX_FILES = {
    "A": "A-command-reference.md",
    "B": "B-skills-catalog.md",
    "C": "C-api-comparison.md",
    "D": "D-community-resources.md",
    "E": "E-common-problems.md",
    "F": "F-best-practices.md",
    "G": "G-links-validation.md",
    "H": "H-config-templates.md",
    "I": "I-thinking-questions-answers.md",
    "J": "J-feishu-checklist.md",
    "K": "K-api-key-config-guide.md",
    "L": "L-config-file-structure.md",
    "M": "M-search-guide.md",
    "N": "N-skills-ecosystem.md",
    "O": "O-domestic-claw-products.md",
}

# 附录标题映射
APPENDIX_TITLES = {
    "A": "OpenClaw 命令速查表：100+常用命令快速查询",
    "B": "OpenClaw 必装Skills清单：Top 10技能推荐",
    "C": "OpenClaw API服务商对比：10+平台价格详解",
    "D": "OpenClaw 社区资源导航：官方文档+教程+交流群",
    "E": "OpenClaw 常见问题速查：安装/API/Skills问题解决",
    "F": "OpenClaw 避坑指南与最佳实践：新手必看",
    "G": "OpenClaw 文档链接验证：所有链接状态检查",
    "H": "OpenClaw 配置文件模板：开箱即用的配置示例",
    "I": "OpenClaw 思考题参考答案：各章节详解",
    "J": "OpenClaw 飞书配置检查清单：确保Bot配置完整",
    "K": "OpenClaw API Key配置完整指南：多种配置方式",
    "L": "OpenClaw 配置文件结构完整指南：全局配置详解",
    "M": "OpenClaw 搜索功能使用指南：搜索技巧和问题",
    "N": "OpenClaw Skills生态说明：1800+技能介绍",
    "O": "OpenClaw 国产Claw产品选购指南（附对比表）",
}

# 文章分类
ARTICLE_CATEGORY = "OpenClaw附录速查"

# 文章标签
ARTICLE_TAGS = ["OpenClaw", "配置教程", "速查手册", "附录"]


def read_appendix_file(filepath):
    """读取附录文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return content


def generate_csdn_article(title, content, appendix_letter):
    """生成 CSDN 格式的文章"""

    # 添加文章头部
    header = f"""# {title}

> 📚 **OpenClaw 2026.3.12 完整教程** - 附录{appendix_letter}速查手册
> 🌐 **在线阅读**：[https://awesome.tryopenclaw.asia](https://awesome.tryopenclaw.asia)
> 💻 **GitHub仓库**：[https://github.com/xianyu110/awesome-openclaw-tutorial](https://github.com/xianyu110/awesome-openclaw-tutorial)

---

"""

    # 添加文章尾部
    footer = """

---

## 📚 更多章节

- [附录A：命令速查表](https://awesome.tryopenclaw.asia/appendix/A-command-reference/)
- [附录B：必装Skills清单](https://awesome.tryopenclaw.asia/appendix/B-skills-catalog/)
- [附录C：API服务商对比](https://awesome.tryopenclaw.asia/appendix/C-api-comparison/)
- [附录D：社区资源导航](https://awesome.tryopenclaw.asia/appendix/D-community-resources/)
- [附录E：常见问题速查](https://awesome.tryopenclaw.asia/appendix/E-common-problems/)

## 🎯 相关资源

- **OpenClaw 官网**：[https://openclaw.ai](https://openclaw.ai)
- **OpenClaw 官方文档**：[https://docs.openclaw.ai](https://docs.openclaw.ai)
- **ClawHub 技能市场**：[https://clawhub.ai](https://clawhub.ai)
- **GitHub 教程仓库**：[https://github.com/xianyu110/awesome-openclaw-tutorial](https://github.com/xianyu110/awesome-openclaw-tutorial)

---

**版权声明**：本文采用 [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.html) 许可证
**作者**：[MaynorAI](https://github.com/xianyu110)
**发布时间**：2026年03月14日

> 💡 **温馨提示**：如果这篇教程对你有帮助，欢迎点赞、收藏、评论三连支持！
"""

    return header + content + footer


def main():
    """主函数"""

    print("="*60)
    print("OpenClaw 附录 CSDN 文章生成器")
    print("="*60)

    # 获取项目根目录
    project_root = Path(__file__).parent
    appendix_dir = project_root / "appendix"
    output_dir = project_root / "csdn_appendix_articles"

    # 创建输出目录
    output_dir.mkdir(exist_ok=True)

    # 遍历所有附录
    total = len(APPENDIX_FILES)
    success = 0

    for letter, filename in APPENDIX_FILES.items():
        try:
            # 读取原文
            source_file = appendix_dir / filename
            if not source_file.exists():
                print(f"✗ [{letter}] 文件不存在: {filename}")
                continue

            print(f"[{letter}/{total}] 正在处理: {filename}")

            original_content = read_appendix_file(source_file)

            # 生成 CSDN 文章
            title = APPENDIX_TITLES.get(letter, f"OpenClaw 附录{letter}")
            csdn_content = generate_csdn_article(title, original_content, letter)

            # 保存文件
            output_file = output_dir / f"appendix-{letter}-{filename.replace('.md', '_csdn.md')}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(csdn_content)

            print(f"✓ [{letter}] 生成成功: {output_file.name}")
            success += 1

        except Exception as e:
            print(f"✗ [{letter}] 处理失败: {e}")

    print("\n" + "="*60)
    print(f"生成完成！")
    print(f"总计: {total} 篇")
    print(f"成功: {success} 篇")
    print(f"失败: {total - success} 篇")
    print(f"输出目录: {output_dir}")
    print("="*60)


if __name__ == "__main__":
    main()
