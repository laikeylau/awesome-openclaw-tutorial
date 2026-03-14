#!/usr/bin/env python3
"""
CSDN 附录自动发布脚本（全自动版本）
自动跳过确认，直接开始发布
"""

import sys
import time
from pathlib import Path

# 导入 CSDNAutoPublisher
from scripts.csdn_auto_publisher import CSDNAutoPublisher, load_article


def get_all_appendix_articles():
    """获取所有待发布的附录文章"""
    articles_dir = Path(__file__).parent / "csdn_appendix_articles"

    if not articles_dir.exists():
        print(f"错误: 文章目录不存在 - {articles_dir}")
        sys.exit(1)

    # 获取所有 *_csdn.md 文件并排序
    articles = sorted(articles_dir.glob("*_csdn.md"))

    print(f"找到 {len(articles)} 篇附录文章待发布\n")

    return articles


def main():
    """主函数"""
    print("="*60)
    print("CSDN 附录自动发布工具（全自动模式）")
    print("="*60 + "\n")

    # 自动确认模式
    print("⚠️  自动模式：将自动开始发布，无需确认\n")

    # 获取所有文章
    articles = get_all_appendix_articles()

    if not articles:
        print("错误: 没有找到任何文章")
        sys.exit(1)

    # 显示文章列表
    print("待发布文章列表:")
    print("-"*60)
    for i, article in enumerate(articles, 1):
        title, _ = load_article(article)
        print(f"{i:2d}. {title}")
    print("-"*60 + "\n")

    # 创建发布器
    publisher = CSDNAutoPublisher(headless=False)

    try:
        # 启动浏览器
        print("正在启动浏览器...")
        publisher.start()

        # 手动登录
        print("\n" + "="*60)
        print("第一步: 登录 CSDN")
        print("="*60)
        print("请在打开的浏览器窗口中:")
        print("1. 使用 CSDN App 扫描二维码登录")
        print("2. 登录成功后，脚本将自动继续")
        print("\n等待登录...\n")

        if not publisher.login_manual():
            print("登录失败，退出...")
            sys.exit(1)

        # 批量发布文章
        print("\n" + "="*60)
        print("第二步: 批量发布附录文章")
        print("="*60 + "\n")

        success_count = 0
        failed_count = 0

        for i, article_file in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] 正在处理: {article_file.name}")

            try:
                # 加载文章
                title, content = load_article(article_file)
                print(f"标题: {title}")

                # 发布文章
                if publisher.publish_article(
                    title=title,
                    content=content,
                    category="OpenClaw附录速查",
                    tags=["OpenClaw", "配置教程", "速查手册", "附录"]
                ):
                    success_count += 1
                    print(f"✓ [{success_count}/{len(articles)}] 发布成功: {title}")
                else:
                    failed_count += 1
                    print(f"✗ 发布失败: {title}")

                # 等待一下再发布下一篇（自动模式）
                if i < len(articles):
                    print(f"\n⏳ 等待 5 秒后继续下一篇...")
                    time.sleep(5)

            except Exception as e:
                failed_count += 1
                print(f"✗ 处理失败: {e}")
                import traceback
                traceback.print_exc()

                # 自动模式下继续发布下一篇
                if i < len(articles):
                    print(f"\n⏳ 等待 5 秒后继续下一篇...")
                    time.sleep(5)

        # 显示统计
        print("\n" + "="*60)
        print("发布完成！")
        print("="*60)
        print(f"总计: {len(articles)} 篇")
        print(f"成功: {success_count} 篇")
        print(f"失败: {failed_count} 篇")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\n用户中断，退出...")
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n浏览器将保持打开状态 60 秒...")
        print("您可以手动检查已发布的文章")
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            pass
        publisher.stop()


if __name__ == "__main__":
    main()
