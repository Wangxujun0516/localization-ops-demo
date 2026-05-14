# LocalizationOps AI — 国际化产品运营 Demo 平台

AI 驱动的国际化产品运营 & 内容本地化 Demo 平台。

## 功能模块

1. **🎯 翻译质量评估** — 多维度 AI 翻译质量评分（准确度、风格、术语、文化适配、流畅度）
2. **📖 术语一致性检查** — 确保多语言内容中的术语翻译一致
3. **🌍 国际化就绪度评分** — 评估产品内容在不同海外市场的就绪程度
4. **✍️ 双语产品文案生成** — 生成英文产品文案 + 中文本地化备注
5. **🕌 文化敏感度检测** — 检测内容在特定市场的文化敏感问题
6. **💬 用户反馈分析器** — 自动分类海外用户评价并排优先级
7. **📊 运营数据看板** — 模拟国际化产品运营核心指标追踪

## 技术栈

- **Streamlit** — 交互式 Web 应用框架
- **DeepSeek API** — AI 分析引擎
- **Plotly** — 数据可视化
- **Pandas** — 数据处理

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 设置 API Key
export DEEPSEEK_API_KEY="your-api-key-here"

# 或者直接修改 .streamlit/secrets.toml

# 启动应用
streamlit run app.py
```

## 在线部署

推荐部署到 [Streamlit Cloud](https://streamlit.io/cloud)（免费）：

1. 将此仓库推送到 GitHub
2. 登录 streamlit.io/cloud
3. 点击 "New app" → 选择此仓库 → 部署
4. 在 Settings → Secrets 中添加 `DEEPSEEK_API_KEY`
