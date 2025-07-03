# 🚀 零本地环境 - Telegram定时自动发送消息云端部署

## 📋 方案概览

| 步骤 | 工具 | 说明 | 时间 |
|------|------|------|------|
| 1 | telegram官网 | 获取API凭据 | 4分钟 |
| 2 | Google Colab | 在线生成Session字符串 | 2分钟 |
| 3 | GitHub Actions | 部署和运行 | 4分钟 |

**总耗时：10分钟搞定！**

---
## 🔥 第一步：获取API凭据

### 1.1 打开官网
访问：https://my.telegram.org

### 1.2 登录验证
- 输入手机号（如：+8613812345678）
- 输入验证码（Telegram会发送到你手机）

### 1.3 创建应用
- 点击"API development tools" 
- 填写应用信息：
  ```
  App title: Telegram Auto Sign Bot
  Short name: auto_sign_bot  
  Platform: Desktop
  ...
  # 其他非必填
  ```

### 1.4 获取凭据
- 创建成功后会显示：
  ```
  API_ID: 12345678
  API_HASH: 1234567890abcdef...
  ```

### **重要提醒：**

✅ **保存好这两个信息**：
- `API_ID`：8位数字
- `API_HASH`：32位字母数字混合
- 不要分享给任何人

❓ **提示ERROR**：
- 一般来说是网络问题，换个干净的节点

## 🔥 第二步：在线生成Session字符串

### 2.1 打开Google Colab
访问：[生成SESSION_STRING](https://colab.research.google.com/drive/1WlFEL46tLWgeZmr2_HE0e3bAzZ3WQztz?usp=sharing)

### 2.2 执行代码
1. 点击运行按钮 ▶️
2. 输入API ID、API Hash、手机号
3. 输入验证码完成登录
4. 复制生成的Session字符串（长长的一串字符）

---

## 🐙 第三步：GitHub部署和运行

### 3.1 配置GitHub仓库

1. fork本仓库到你自己的账户
2. 点击"Settings"标签
3. 左侧选择"Secrets and variables" → "Actions"
4. 点击"New repository secret"

依次添加以下secrets：

| Name | Value | 说明 |
|------|-------|------|
| `API_ID` | 你的API ID | 从my.telegram.org获取 |
| `API_HASH` | 你的API Hash | 从my.telegram.org获取 |
| `SESSION_STRING` | 刚才生成的字符串 | Google Colab生成的长字符串 |
| `SIGN_CONFIG` | `{"@checkin_bot": "/sign", "@daily_bot": "/checkin", "@reward_bot": "领取奖励", "username": "hello"}` | 目标和需要发送的消息，逗号分隔(填你自己的，这只是样例) |

### 3.2 手动测试
1. 进入仓库的"Actions"标签
2. 选择"Telegram Auto Sign"
3. 点击"Run workflow" → "Run workflow"
4. 等待执行完成，查看日志

### 3.3 设置完成！
✅ 现在你的账号会：
- 每天上午9点自动发送消息
- 每天晚上9点自动发送消息
- 所有日志都可以在Actions中查看
---

❗ **Telegram提示异地登录**：
- Github的服务器在登你的Telegram账号
- 正常来说不用管
  
---

## 🔧 自定义配置

### 修改签到时间
编辑 `.github/workflows/auto-sign.yml` 文件：

```yaml
schedule:
  # 修改这里的时间（UTC时间，需要-8小时）
  - cron: '0 1 * * *'   # 北京时间09:00
  - cron: '0 5 * * *'   # 北京时间13:00  
  - cron: '0 13 * * *'  # 北京时间21:00
```

### 添加更多消息发送目标
在Secrets中修改 `SIGN_CONFIG`：
```
{"@bot1":"Hello", "@bot2":"World"}
```
