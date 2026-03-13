# 🎯 Job Radar — 每日职位自动推送

自动抓取 Google Jobs 实时职位，每天定时推送到对话。无需手动搜索，填一次配置，之后每天按时推送，直接看申请链接。

## ✨ 功能特点

- 🚀 **自动抓取**：实时同步 Google Jobs 最新职位信息
- ⏰ **定时推送**：自定义推送时间，每天准时送达
- 🎯 **精准搜索**：支持自定义关键词、地区筛选
- 🌐 **双数据源**：支持 SerpAPI（免费）和 Caravo（付费）两种数据源
- 📊 **智能分析**：自动识别新发职位、远程岗位、薪资信息
- 🔗 **直接申请**：每个职位带直接申请链接，点击即可投递
- 💰 **免费可用**：SerpAPI 每月 100 次免费额度，可使用约 50 天

## 🎯 适合人群

- 🧑💼 求职者
- 👥 HR / 招聘人员
- 🎯 猎头
- 📋 职业规划师

## 🖼️ 效果演示

![职位推送效果演示](demo.png)

## 🚀 快速开始

### 1. 获取 API Key（二选一）

#### 🆓 选项 A：SerpAPI（免费推荐）
- 访问 [serpapi.com](https://serpapi.com) 注册
- 填写邮箱即可获得 API Key
- 每月 100 次免费搜索，每天推送 1 次可用约 50 天

#### 💳 选项 B：Caravo（付费）
- 访问 [caravo.ai](https://caravo.ai) 注册获取 API Key
- 每次搜索约 $0.005，每天推送约 $0.01

### 2. 验证 API Key

```bash
# 验证 SerpAPI Key
python validate_key.py serpapi YOUR_SERPAPI_KEY

# 验证 Caravo Key
python validate_key.py caravo YOUR_CARAVO_KEY
```

验证成功会显示 `✅ 有效，找到X个职位`，否则请检查 Key 是否正确。

### 3. 立即搜索一次

```bash
# 使用 SerpAPI 搜索美国 AI Marketing 职位
python job_radar.py \
  --api-key YOUR_SERPAPI_KEY \
  --query "AI Marketing" \
  --location "United States" \
  --gl us

# 使用 Caravo 搜索新加坡 Data Scientist 职位
python job_radar.py \
  --api-key YOUR_CARAVO_KEY \
  --query "Data Scientist" \
  --location "Singapore" \
  --gl sg \
  --source caravo
```

## ⏰ 设置定时推送

### 方法 1：使用 Claude Code 定时任务（推荐）

1. 对 Claude 说：**"帮我设置职位推送"**
2. 按照提示提供：
   - 搜索关键词（例如：Prompt Engineer、Product Manager）
   - 地区（北美 / 英国 / 新加坡 / 加拿大 / 全球远程等）
   - 推送时间（北京时间几点，每天推几次）
   - 你的 API Key

3. 配置完成后，每天会自动推送职位到对话中。

### 方法 2：使用系统 Cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（例如每天早上8点推送美国 AI 职位）
0 8 * * * /usr/bin/python /path/to/job_radar.py \
  --api-key YOUR_SERPAPI_KEY \
  --query "AI" \
  --location "United States" \
  --gl us >> /path/to/job_logs.txt
```

## 🌍 地区速查表

| 用户输入 | LOCATION | GL  |
|---------|----------|-----|
| 北美 / 美国 | United States | us |
| 英国 | United Kingdom | gb |
| 新加坡 | Singapore | sg |
| 加拿大 | Canada | ca |
| 澳大利亚 | Australia | au |
| 香港 | Hong Kong | hk |
| 全球远程 | 关键词末尾加 Remote | us |

## ⏱️ 北京时间 Cron 对照表

| 北京时间 | CRON（UTC） |
|---------|-------------|
| 早上 8 点 | 0 0 * * * |
| 早上 9 点 | 0 1 * * * |
| 早上 10 点 | 0 2 * * * |
| 中午 12 点 | 0 4 * * * |
| 下午 14 点 | 0 6 * * * |
| 下午 16 点 | 0 8 * * * |
| 晚上 20 点 | 0 12 * * * |
| 晚上 21 点 | 0 13 * * * |
| 两次（10点+16点） | 0 2,8 * * * |

## 📋 指令说明（在 Claude 对话中使用）

| 用户指令 | 操作 |
|---------|------|
| "改成晚上 9 点" | 更新推送时间 |
| "换成搜 Prompt Engineer" | 更换搜索关键词 |
| "改成搜新加坡" | 更换搜索地区 |
| "每天推两次" | 调整推送频率 |
| "暂停" | 暂停推送 |
| "恢复" | 恢复推送 |
| "删除" | 删除定时任务 |
| "现在搜一次" | 立即执行一次搜索，不创建定时任务 |

## 💰 SerpAPI 免费额度说明

| 推送频率 | 每天消耗 | 100次免费额度可用 |
|---------|----------|------------------|
| 每天 1 次 | 2次（两页） | 约 50 天 |
| 每天 2 次 | 4次 | 约 25 天 |

建议每天推送 1 次，免费额度可用约 50 天。

## 📄 输出说明

每条职位信息包含：
- 🔥 24小时内新发职位标识
- 🏢 公司名称
- 📍 工作地点 + 远程/线下标识
- 🕐 发布时间
- 💰 薪资（如有披露）
- 💼 工作类型（全职/实习等）
- 📋 职位简介
- 🔗 直接申请链接

底部还包含今日趋势分析：
- 主要招聘方
- 薪资披露情况
- 远程岗位占比

## 🛠️ 技术实现

- 数据源：Google Jobs 搜索引擎
- API 对接：SerpAPI / Caravo
- 数据处理：自动去重、关键词提取、智能分类
- 定时任务：支持 Claude 内置定时和系统 Cron
- 输出格式：Markdown 结构化展示

## 📝 更新日志

### v1.0.0 (2026-03-13)
- ✅ 基础功能实现
- ✅ 支持 SerpAPI 和 Caravo 双数据源
- ✅ 定时推送功能
- ✅ 智能识别新发、远程职位
- ✅ 结构化输出展示

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
