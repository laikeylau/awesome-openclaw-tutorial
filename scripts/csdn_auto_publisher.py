#!/usr/bin/env python3
"""
CSDN 自动发文脚本
使用 Selenium 自动化发布文章到 CSDN
"""

import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException


class CSDNAutoPublisher:
    """CSDN 自动发布器"""

    def __init__(self, headless=False):
        """初始化浏览器"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)

        self.driver = None
        self.wait = None

    def start(self):
        """启动浏览器"""
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        # 隐藏 webdriver 特征
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })

    def stop(self):
        """停止浏览器"""
        if self.driver:
            self.driver.quit()

    def login_manual(self):
        """
        手动登录
        用户需要扫码登录，脚本等待登录完成
        """
        print("正在打开 CSDN 登录页面...")
        self.driver.get("https://passport.csdn.net/login?code=applets")

        print("\n" + "="*50)
        print("请使用 CSDN App 扫描二维码登录")
        print("登录成功后，脚本会自动继续...")
        print("="*50 + "\n")

        # 等待登录成功（检查 URL 是否跳转）
        try:
            self.wait.until(lambda driver: "passport" not in driver.current_url)
            print("✓ 登录成功！")
            time.sleep(2)
            return True
        except TimeoutException:
            print("✗ 登录超时，请重试")
            return False

    def publish_article(self, title, content, category="OpenClaw从入门到精通", tags=None):
        """
        发布文章

        Args:
            title: 文章标题
            content: 文章内容（Markdown 格式）
            category: 文章分类
            tags: 文章标签列表
        """
        if tags is None:
            tags = ["OpenClaw", "AI助手", "人工智能"]

        try:
            # 打开文章编辑页面
            print(f"正在发布文章: {title}")
            self.driver.get("https://mp.csdn.net/mp/blog/editBlog/publish")
            time.sleep(3)

            # 切换到 Markdown 编辑模式
            try:
                markdown_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Markdown') or contains(text(), 'markdown')]"))
                )
                markdown_btn.click()
                print("✓ 已切换到 Markdown 编辑模式")
                time.sleep(1)
            except:
                print("! 可能已经是 Markdown 模式")

            # 填写标题
            title_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "blog-title"))
            )
            title_input.clear()
            title_input.send_keys(title)
            print(f"✓ 标题已填写: {title}")
            time.sleep(1)

            # 填写内容
            content_textarea = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".markdown_editormd .CodeMirror textarea"))
            )

            # 使用 JavaScript 直接设置内容（更可靠）
            self.driver.execute_script("""
                var textarea = arguments[0];
                textarea.value = arguments[1];
                var event = new Event('input', { bubbles: true });
                textarea.dispatchEvent(event);
            """, content_textarea, content)

            print("✓ 正文内容已填写")
            time.sleep(3)  # 等待内容同步到 CodeMirror

            # 选择分类
            try:
                category_select = self.wait.until(
                    EC.presence_of_element_located((By.ID, "blog-categories"))
                )
                from selenium.webdriver.support.ui import Select
                select = Select(category_select)
                select.select_by_visible_text(category)
                print(f"✓ 分类已选择: {category}")
                time.sleep(1)
            except Exception as e:
                print(f"! 分类选择失败: {e}")

            # 添加标签
            if tags:
                try:
                    tag_input = self.driver.find_element(By.CSS_SELECTOR, ".tag-input")
                    for tag in tags:
                        tag_input.clear()
                        tag_input.send_keys(tag)
                        time.sleep(0.5)
                        tag_input.send_keys(u'\ue007')  # Press Enter
                        print(f"✓ 标签已添加: {tag}")
                        time.sleep(0.5)
                except Exception as e:
                    print(f"! 标签添加失败: {e}")

            print("\n" + "="*50)
            print("✓ 文章内容已填写完成！")
            print("="*50)
            print("\n请检查文章内容，然后手动点击「发布」按钮")
            print("按 Ctrl+C 退出脚本...\n")

            # 保持浏览器打开，等待用户手动发布
            if '--auto' not in sys.argv:
                input("按 Enter 键继续发布下一篇文章...")
            else:
                print("自动模式：等待 30 秒后继续...")
                time.sleep(30)

            return True

        except Exception as e:
            print(f"✗ 发布失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def load_article(filepath):
    """加载文章文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取标题（第一行 # 开头的内容）
    lines = content.split('\n')
    title = lines[0].replace('#', '').strip()

    return title, content


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python csdn_auto_publisher.py <文章文件路径>")
        print("示例: python csdn_auto_publisher.py ../csdn_articles/01-introduction_csdn.md")
        sys.exit(1)

    article_file = sys.argv[1]

    # 检查文件是否存在
    if not Path(article_file).exists():
        print(f"错误: 文件不存在 - {article_file}")
        sys.exit(1)

    # 加载文章
    print(f"正在加载文章: {article_file}")
    title, content = load_article(article_file)

    # 创建发布器
    publisher = CSDNAutoPublisher(headless=False)

    try:
        # 启动浏览器
        publisher.start()

        # 手动登录
        if not publisher.login_manual():
            print("登录失败，退出...")
            sys.exit(1)

        # 发布文章
        publisher.publish_article(
            title=title,
            content=content,
            category="OpenClaw从入门到精通",
            tags=["OpenClaw", "AI助手", "人工智能", "Agent"]
        )

    except KeyboardInterrupt:
        print("\n\n用户中断，退出...")
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 保持浏览器打开，让用户手动发布
        print("\n浏览器将保持打开状态，您可以继续操作...")
        print("关闭浏览器窗口以退出脚本")
        input("按 Enter 键退出...")
        publisher.stop()


if __name__ == "__main__":
    main()
