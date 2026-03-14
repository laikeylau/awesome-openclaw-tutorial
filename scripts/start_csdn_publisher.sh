#!/bin/bash
# CSDN 自动发文工具 - 快速启动脚本

echo "================================================"
echo "     CSDN 自动发文工具"
echo "================================================"
echo ""
echo "请选择发布模式:"
echo "1) 单篇发布"
echo "2) 批量发布（推荐）"
echo ""
read -p "请输入选项 (1/2): " choice

case $choice in
    1)
        echo ""
        echo "单篇发布模式"
        echo "------------------------------------------------"
        echo "请输入文章文件路径（相对或绝对路径）:"
        echo "示例: ../csdn_articles/01-introduction_csdn.md"
        read -p "> " filepath

        if [ -z "$filepath" ]; then
            echo "错误: 未输入文件路径"
            exit 1
        fi

        echo ""
        echo "正在启动单篇发布..."
        python3 csdn_auto_publisher.py "$filepath"
        ;;
    2)
        echo ""
        echo "批量发布模式"
        echo "------------------------------------------------"
        echo "将发布 csdn_articles/ 目录下的所有文章"
        read -p "确认开始? (y/n): " confirm

        if [ "$confirm" != "y" ]; then
            echo "取消发布"
            exit 0
        fi

        echo ""
        echo "正在启动批量发布..."
        python3 batch_publish_csdn.py
        ;;
    *)
        echo "错误: 无效选项"
        exit 1
        ;;
esac
