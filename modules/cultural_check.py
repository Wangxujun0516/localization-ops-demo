"""
模块 5: 文化敏感度检测
AI 识别内容是否在特定市场有文化敏感问题。
"""

import streamlit as st
from utils.llm_client import ask_deepseek

MARKETS = [
    "东南亚 (SEA) — 印尼、泰国、越南、菲律宾、马来西亚",
    "中东 (MENA) — 沙特、阿联酋、埃及等",
    "拉丁美洲 — 巴西、墨西哥、阿根廷等",
    "日本",
    "韩国",
    "印度",
    "欧洲 — 德法英意西等",
    "北美 — 美国、加拿大",
]

SYSTEM_PROMPT = """你是一位跨文化沟通与本地化专家。分析以下内容在指定目标市场是否存在文化敏感问题。

评估维度：
1. 宗教/信仰敏感度 (Religious Sensitivity) 
2. 政治/历史敏感度 (Political Sensitivity)
3. 颜色/符号敏感度 (Color & Symbol Sensitivity)
4. 性别/社会规范敏感度 (Gender & Social Norms)
5. 幽默/隐喻理解 (Humor & Metaphor)
6. 法律/广告合规风险 (Legal & Advertising Compliance)

每个维度标注风险等级：HIGH / MEDIUM / LOW / NONE

输出格式（严格 JSON，中文回答）：
{
  "overall_risk_level": "HIGH/MEDIUM/LOW/SAFE",
  "market": "目标市场",
  "risk_analysis": [
    {
      "dimension": "风险维度",
      "level": "HIGH/MEDIUM/LOW/NONE",
      "finding": "具体的文化风险发现",
      "recommendation": "如何修改以避免问题"
    }
  ],
  "safe_alternatives": ["替代方案1", "替代方案2", "替代方案3"],
  "summary": "总结（2-3句）"
}"""


def run():
    st.subheader("🕌 文化敏感度检测")
    st.markdown("粘贴内容并选择目标市场，AI 检测是否存在宗教、政治、符号等方面的文化敏感问题。这对于出海产品至关重要。")

    target_market = st.selectbox("选择目标市场", MARKETS)
    content = st.text_area("需要检测的内容", height=250,
                           placeholder="Paste product copy, marketing text, UI strings, or images description...")

    if st.button("检测文化敏感度", type="primary", use_container_width=True):
        if not content:
            st.warning("请先输入需要检测的内容。")
            return

        with st.spinner(f"AI 正在分析 {target_market.split('—')[0].strip()} 的文化敏感度..."):
            user_prompt = f"目标市场：{target_market}\n\n内容：\n{content}"
            result = ask_deepseek(SYSTEM_PROMPT, user_prompt)

        try:
            import json
            data = json.loads(result)

            overall = data.get("overall_risk_level", "UNKNOWN")
            risk_colors = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "SAFE": "✅"}
            st.markdown(f"### 综合风险等级: {risk_colors.get(overall, '❓')} **{overall}**")
            st.caption(f"目标市场: {data.get('market', target_market)}")

            if data.get("risk_analysis"):
                st.markdown("#### 📋 逐项风险分析")
                for item in data["risk_analysis"]:
                    level = item.get("level", "NONE")
                    icons = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "💡", "NONE": "✅"}
                    st.markdown(f"{icons.get(level, '❓')} **[{item.get('dimension', '')}]** — 风险: {level}")
                    st.markdown(f"  📌 *发现：* {item.get('finding', '')}")
                    st.markdown(f"  💡 *建议：* {item.get('recommendation', '')}")
                    st.markdown("")

            if data.get("safe_alternatives"):
                st.markdown("#### ✅ 安全替代方案")
                for alt in data["safe_alternatives"]:
                    st.markdown(f"- {alt}")

            st.divider()
            st.markdown(f"**总结：** {data.get('summary', '')}")

        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"AI 返回格式异常: {e}")
            st.code(result)
