# 🍪 CSDN Cookie 获取详细教程

## 📸 图文教程

### 步骤 1：登录 CSDN
1. 打开浏览器，访问：https://www.csdn.net
2. 点击右上角「登录」
3. 使用你的账号密码登录

### 步骤 2：打开开发者工具
1. **按 F12** 键
2. 或者：右键点击页面 → 选择「检查」

### 步骤 3：切换到 Application 标签
1. 在顶部工具栏找到 **"Application"**
2. 点击进入

### 步骤 4：找到 Cookies
1. 在左侧边栏找到 **"Storage"**
2. 展开找到 **"Cookies"**
3. 点击 **https://www.csdn.net**

### 步骤 5：复制关键 Cookie
查找并复制以下值：

#### 🔑 重要 Cookie 列表：

| Cookie 名称 | 作用 | 是否必需 |
|------------|------|----------|
| `SESSION` | 会话ID | ✅ 必需 |
| `token` | 认证令牌 | ✅ 必需 |
| `UserInfo` | 用户信息 | ⭕ 可选 |
| `UserName` | 用户名 | ⭕ 可选 |
| `UserToken` | 用户令牌 | ⭕ 可选 |

### 步骤 6：复制 Cookie 值

**方法 A：单个复制**
1. 点击某个 cookie（如 SESSION）
2. 在右侧 "Value" 字段中
3. 复制整个值

**方法 B：全部导出**
1. 在 "Cookies" https://www.csdn.net 上右键
2. 选择 "Export"
3. 保存为 JSON 文件

---

## 📝 快速复制格式

### 格式 1：JSON 格式（推荐）

复制所有需要的 cookie 后，按这个格式整理：

```json
{
  "SESSION": "你复制的SESSION值",
  "token": "你复制的token值"
}
```

### 格式 2：单行格式

```
SESSION=你的SESSION值; token=你的token值
```

---

## 🎯 完成后

将复制好的 cookie 粘贴给我，格式可以是：

```
SESSION=xxxxxx; token=xxxxxx
```

或者直接复制每个值告诉我：

```
SESSION: xxxxxx
token: xxxxxx
```

我会帮你配置到 agent-browser 中！

---

## ⚠️ 注意事项

1. **安全性**：Cookie 包含你的登录信息，不要分享给他人
2. **有效期**：Cookie 通常会过期，如果失效需要重新获取
3. **只复制必需的**：SESSION 和 token 通常就够用了

---

## 🚀 下一步

获取到 cookie 后，告诉我：
- "cookie 已获取好了"
- 粘贴 cookie 值

我会帮你：
1. 配置到浏览器
2. 打开 CSDN 发布页面
3. 填写文章内容
4. 等你点击发布按钮
