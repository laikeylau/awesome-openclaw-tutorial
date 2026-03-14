#!/bin/bash
# CSDN 附录发布助手 - 本地交互式版本

echo "================================================"
echo "     CSDN 附录发布助手"
echo "================================================"
echo ""
echo "这个助手会帮助您逐步发布附录文章到 CSDN"
echo ""

# 检查 Python 依赖
echo "检查依赖..."
python3 -c "import selenium" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装依赖..."
    pip3 install selenium webdriver-manager
fi

echo ""
echo "================================================"
echo "选择发布模式："
echo "================================================"
echo ""
echo "1) 自动化辅助发布（推荐）"
echo "   - 自动打开浏览器"
echo "   - 自动填写文章内容"
echo "   - 您只需扫码登录和点击发布"
echo ""
echo "2) 手动发布指南"
echo "   - 查看详细的手动发布步骤"
echo ""
read -p "请选择 (1/2): " mode

case $mode in
    1)
        echo ""
        echo "================================================"
        echo "自动化辅助发布模式"
        echo "================================================"
        echo ""
        echo "即将启动自动化脚本..."
        echo "请确保您已："
        echo "  1. 安装了 Chrome 浏览器"
        echo "  2. 安装了 CSDN App（用于扫码登录）"
        echo ""
        read -p "按 Enter 键继续..."

        # 运行 Python 脚本
        cd /Users/chinamanor/Downloads/cursor编程/awesome-openclaw-tutorial-1
        python3 batch_publish_appendix.py
        ;;

    2)
        echo ""
        echo "================================================"
        echo "手动发布指南"
        echo "================================================"
        echo ""
        cat 附录发布分步指南.md
        ;;

    *)
        echo "无���选项"
        exit 1
        ;;
esac

echo ""
echo "================================================"
echo "发布完成！"
echo "================================================"
echo ""
echo "感谢您的使用！"
