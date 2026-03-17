# 附录E：常见访问题速查

> 💡 **快速定位访问题**：本附录汇总了OpenClaw使用过程中最常见的各类访问题及解决方案，帮助你快速排查和解决访问题。

## 📋 目附录

- [安装配置访问题](#安装配置访问题)
- [API连接访问题](#api连接访问题)
- [Gateway访问题](#gateway访问题)
- [Skills访问题](#skills访问题)
- [平台集成访问题](#平台集成访问题)
- [性能访问题](#性能访问题)

---

## 安装配置访问题

### Q1: 安装失败怎么怎么办？

**症状**：执行安装命令时报错

**解决方案**：

1. **检查Node.js版本**
```bash
node --version  # 需要v18.0.0或更高版本
```

2. **使用官方中文安装脚本**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

3. **使用npm直接安装**
```bash
npm install -g openclaw
```

4. **检查网络连接**
- 如果在国内，建议使用镜像源或中转API

### Q2: 权限错误怎么怎么办？

**症状**：安装或运行时提示权限不足

**解决方案**：

```bash
# macOS/Linux
sudo npm install -g openclaw

# 或者使用nvm（推荐）
nvm install node
nvm use node
npm install -g openclaw
```

### Q3: 网络超时怎么怎么办？

**症状**：安装或更新时网络连接超时

**解决方案**：

1. **使用国内镜像源**
```bash
npm config set registry https://registry.npmmirror.com
```

2. **设置代理**
```bash
npm config set proxy http://proxy-server:port
npm config set https-proxy http://proxy-server:port
```

3. **使用离线安装**
```bash
# 下载安装包后本地安装
npm install -g ./openclaw-*.tgz
```

---

## API连接访问题

### Q4: API连接失败怎么怎么办？

**症状**：提示API连接错误或超时

**解决方案**：

1. **检查API Key是否正确**
```bash
openclaw config get env | grep API_KEY
```

2. **测试API连接**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.anthropic.com/v1/messages
```

3. **检查网络**
```bash
ping api.anthropic.com
```

4. **使用中转API（国内推荐）**
- 参考附录C：API服务商对比

### Q5: API费用太高怎么怎么办？

**症状**：API使用成本超出预算

**解决方案**：

1. **使用国产模型**
- DeepSeek：成本降低95%
- Kimi：长文档处理优惠
- GLM-4：中文友好

2. **多模型组合**
```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-xxx",
    "DEEPSEEK_API_KEY": "sk-xxx"
  },
  "agents": [
    {
      "name": "assistant",
      "model": "claude-3-5-sonnet-20241022"
    },
    {
      "name": "coder",
      "model": "deepseek-chat"
    }
  ]
}
```

3. **设置工具权限**
```bash
openclaw config set tools.profile "coding"  # 限制工具使用
```

---

## Gateway访问题

### Q6: Gateway启动失败怎么怎么办？

**症状**：执行`openclaw daemon start`后Gateway无法启动

**解决方案**：

1. **检查配置文件**
```bash
openclaw doctor  # 诊断配置访问题
```

2. **检查端口占用**
```bash
lsof -i :18789  # macOS/Linux
netstat -ano | findstr :18789  # Windows
```

3. **查看日志**
```bash
tail -f ~/.openclaw/logs/gateway.log
```

4. **重启Gateway**
```bash
openclaw daemon stop
openclaw daemon start
```

### Q7: Gateway认证配置错误（v2026.3.7+）

**症状**：升级后Gateway拒绝启动，提示需要配置认证

**解决方案**：

```bash
# 设置token认证
openclaw config set gateway.auth.mode "token"
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"

# 重启Gateway
openclaw daemon restart
```

### Q8: 端口被占用怎么办？

**症状**：提示18789端口已被占用

**解决方案**：

1. **更改端口**
```bash
openclaw config set gateway.port 18790
```

2. **停止占用端口的进程**
```bash
# 查找并停止占用进程
lsof -ti :18789 | xargs kill -9
```

---

## Skills访问题

### Q9: Skills安装失败怎么怎么办？

**症状**：`clawhub install`命令执行失败

**解决方案**：

1. **检查网络连接**
```bash
ping clawhub.ai
```

2. **使用ClawHub镜像（如有）**
```bash
clawhub install skill-name --registry https://mirror.clawhub.ai
```

3. **手动安装**
```bash
# 下载Skill源码
git clone https://github.com/user/skill-repo.git

# 安装依赖
cd skill-repo
npm install

# 复制到Skills目附录
cp -r . ~/.openclaw/skills/skill-name
```

### Q10: Skills不生效怎么怎么办？

**症状**：安装Skill后功能无法使用

**解决方案**：

1. **检查Skill配置**
```bash
cat ~/.openclaw/skills/skill-name/SKILL.md
```

2. **重启Gateway**
```bash
openclaw daemon restart
```

3. **检查Skill权限**
```bash
openclaw config get skills.allowlist
```

4. **查看错误日志**
```bash
tail -f ~/.openclaw/logs/skills.log
```

### Q11: 如何卸载Skills？

**解决方案**：

```bash
# 使用clawhub卸载
clawhub uninstall skill-name

# 手动删除
rm -rf ~/.openclaw/skills/skill-name

# 重启Gateway
openclaw daemon restart
```

### Q12: Skills冲突怎么怎么办？

**症状**：多个Skills功能冲突

**解决方案**：

1. **检查Skills列表**
```bash
clawhub list
```

2. **禁用冲突Skills**
```json
{
  "skills": {
    "denylist": ["skill-a", "skill-b"]
  }
}
```

3. **使用版本管理**
```bash
clawhub install skill-name@version
```

---

## 平台集成访问题

### Q13: 飞书Bot不回复怎么怎么办？

**症状**：给飞书Bot发布送消息无响应

**解决方案**：

1. **检查Bot状态**
```bash
openclaw status
```

2. **检查飞书配置**
```bash
openclaw config get channels.feishu
```

3. **验证Webhook**
```bash
curl -X POST https://open.feishu.cn/open-apis/bot/v2/hook/xxx \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"测试"}}'
```

4. **使用飞书配置检查清单**
- 参考：附录J：飞书配置检查清单

### Q14: 企业微信Bot配置失败？

**症状**：企业微信Bot无法接入

**解决方案**：

1. **检查应用Secret**
2. **验证回调URL**
3. **检查通讯附录权限**
4. **参考第9章节配置步骤**

### Q15: Telegram Bot无响应？

**症状**：Telegram Bot不回复消息

**解决方案**：

1. **检查Bot Token**
```bash
openclaw config get channels.telegram.botToken
```

2. **与Bot发布起对话**
```bash
curl https://api.telegram.org/bot<TOKEN>/getMe
```

3. **检查Webhook设置**
```bash
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

---

## 性能访问题

### Q16: 响应速度慢怎么怎么办？

**解决方案**：

1. **使用更快的模型**
- DeepSeek：国内访问快
- Claude 3.5 Sonnet：平衡速度和质量

2. **减少上下文**
```bash
# 定期清理会话历史
openclaw chat clear
```

3. **优化配置**
```json
{
  "agents": [{
    "maxTokens": 4096,  # 减少输出长度
    "temperature": 0.7
  }]
}
```

### Q17: 内存占用过高？

**解决方案**：

1. **限制会话数量**
```bash
openclaw config set sessions.max 10
```

2. **定期重启Gateway**
```bash
openclaw daemon restart
```

3. **使用Docker部署**
```bash
docker run -d --memory="2g" openclaw/openclaw
```

### Q18: 磁盘空间不足？

**解决方案**：

1. **清理日志文件**
```bash
rm -rf ~/.openclaw/logs/*.log
```

2. **清理缓存**
```bash
rm -rf ~/.openclaw/cache/*
```

3. **清理旧会话**
```bash
openclaw session prune --days 30
```

---

## 🔍 更多资源

- [第2章节：安装部署](../docs/01-basics/02-installation.md) - 完整安装指南
- [第8章节：Skills扩展](../docs/03-advanced/08-skills-extension.md) - Skills使用管理
- [第9章节：多平台集成](../docs/03-advanced/09-multi-platform-integration.md) - 平台接入配置
- [第11章节：高级配置](../docs/03-advanced/11-advanced-configuration.md) - 性能优化

---

**最后更新**：2026年3月16日
**适用版本**：OpenClaw v2026.3.7+
