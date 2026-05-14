"""
模块 3: 国际化就绪度评分
分析一段产品文案/功能描述，评估其国际化就绪度。
"""

import streamlit as st
from utils.llm_client import ask_deepseek

TARGET_MARKETS = [
    "全球 (通用英文市场)",
    "东南亚 (SEA)",
    "中东 (MENA)",
    "拉丁美洲 (LATAM)",
    "日本 (JP)",
    "韩国 (KR)",
    "欧洲 (EU)",
]

SYSTEM_PROMPT = """你是一位国际化产品运营专家。分析以下产品文案/功能描述，评估其"国际化就绪度"。

评估维度（每项 1-10 分）：
1. 文化中性 (Cultural Neutrality) — 是否包含只在特定文化中能理解的引用、幽默、隐喻
2. 格式适配 (Format Readiness) — 日期、货币、单位、地址格式是否需要修改
3. 本地化空间 (L10n Headroom) — 译文是否会过长或过短，是否有硬编码文本
4. 法规合规 (Compliance) — 涉及 GDPR、CCPA、数据跨境等法规意识
5. 市场适配 (Market Fit) — 是否考虑了目标市场的用户习惯和偏好

输出格式（严格 JSON）：
{
  "scores": { "cultural_neutrality": N, "format_readiness": N, "l10n_headroom": N, "compliance": N, "market_fit": N },
  "overall_readiness": N,
  "interpretation": "就绪度说明（如：72分 - 可以国际化，但需做以下优化）",
  "issues": [
    {"dimension": "维度名", "issue": "问题描述", "severity": "high/medium/low", "fix": "具体修改建议"}
  ],
  "quick_wins": ["可以快速改进的 2-3 个点"],
  "verdict": "一句话结论"
}"""


def run():
    st.subheader("🌍 国际化就绪度评分")
    st.markdown("粘贴你的产品文案或功能描述，选择目标市场，AI 从文化、格式、法规等维度评估国际化就绪度。")

    target_market = st.selectbox("选择目标市场", TARGET_MARKETS)

    content = st.text_area("产品文案 / 功能描述", height=250,
                           placeholder="Paste your product copy, feature description, or UI text here...")

    if st.button("评估国际化就绪度", type="primary", use_container_width=True):
        if not content:
            st.warning("请先输入产品文案或功能描述。")
            return

        with st.spinner(f"AI 正在评估 {target_market} 市场的就绪度..."):
            user_prompt = f"目标市场：{target_market}\n\n产品文案：\n{content}"
            result = ask_deepseek(SYSTEM_PROMPT, user_prompt)

        try:
            import json
            data = json.loads(result)
            scores = data.get("scores", {})

            cols = st.columns(5)
            labels = {
                "cultural_neutrality": "文化中性",
                "format_readiness": "格式适配",
                "l10n_headroom": "本地化空间",
                "compliance": "法规合规",
                "market_fit": "市场适配",
            }
            for i, (key, label) in enumerate(labels.items()):
                score = scores.get(key, 0)
                color = "🟢" if score >= 8 else ("🟡" if score >= 5 else "🔴")
                cols[i].metric(f"{color} {label}", f"{score}/10",
                              help=data.get("interpretation", ""))

            total = data.get("overall_readiness", 0)
            bar_color = "green" if total >= 70 else ("orange" if total >= 40 else "red")
            st.markdown(f"### 📊 国际化就绪度总分: **{total}/100**")
            st.markdown(f"""
            <div style="background:#262730; border-radius:10px; padding:3px;">
              <div style="background:{bar_color}; width:{total}%; border-radius:10px; padding:5px; text-align:center; color:white; font-weight:bold;">
                {int(total)}%
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.info(data.get("interpretation", ""))

            if data.get("issues"):
                st.markdown("#### ⚠️ 需要解决的问题")
                for issue in data["issues"]:
                    severity = issue.get("severity", "low")
                    icon = {"high": "🔴", "medium": "🟡", "low": "💡"}.get(severity, "💡")
                    st.markdown(f"{icon} **[{issue['dimension']}]** {issue['issue']}")
                    st.markdown(f"  → *修改建议：* {issue.get('fix', '')}")

            if data.get("quick_wins"):
                st.markdown("#### ⚡ 快速优化建议")
                for q in data["quick_wins"]:
                    st.markdown(f"- {q}")

            st.markdown(f"**结论：** {data.get('verdict', '')}")

        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"AI 返回格式异常: {e}")
            st.code(result)
