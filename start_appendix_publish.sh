#!/bin/bash
# 在新终端窗口中启动附录发布

echo "正在启动 CSDN 附录发布工具..."
echo ""

# 检查操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell application "Terminal"
        do script "cd /Users/chinamanor/Downloads/cursor编程/awesome-openclaw-tutorial-1 && python3 batch_publish_appendix.py"
        activate
    end tell'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd /Users/chinamanor/Downloads/cursor编程/awesome-openclaw-tutorial-1 && python3 batch_publish_appendix.py; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd /Users/chinamanor/Downloads/cursor编程/awesome-openclaw-tutorial-1 && python3 batch_publish_appendix.py" &
    else
        echo "无法找到终端模拟器"
        echo "请手动运行："
        echo "cd /Users/chinamanor/Downloads/cursor编程/awesome-openclaw-tutorial-1"
        echo "python3 batch_publish_appendix.py"
    fi
fi

echo ""
echo "✓ 新终端窗口已打开"
echo "请在新窗口中跟随提示操作"
echo ""
echo "操作步骤："
echo "1. 在新窗口中输入 'y' 确认开始"
echo "2. 使用 CSDN App 扫描二维码登录"
echo "3. 检查文章内容后手动点击'发布'按钮"
echo "4. 按回车继续下一篇"
echo ""
