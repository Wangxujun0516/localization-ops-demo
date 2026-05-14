"""
模块 6: 用户反馈分析器
粘贴海外用户评价，AI 自动分类、情感分析、优先级排序。
"""

import streamlit as st
from utils.llm_client import ask_deepseek

# Sample data for quick demo
SAMPLE_REVIEWS = """⭐⭐⭐⭐⭐ Amazing platform! The AI agent creation is incredibly intuitive. Would love to see more template options for e-commerce use cases. — User from US
⭐⭐⭐ Good but localization needs work. Some Chinese characters still showing in the English UI. The translation of "Workflow" as "工作流" in tooltips is confusing. — User from UK
⭐⭐⭐⭐⭐ Best AI agent builder I've used. The API documentation is comprehensive and clear. — User from Germany
⭐⭐ The mobile responsiveness is poor on iOS Safari. Buttons overlap on iPhone 14. Also, the pricing page is confusing in USD but showing in some regions without local currency conversion. — User from Brazil
⭐⭐⭐⭐ Solid product. Need better onboarding for non-technical users. The concept of "agents" is not obvious to business users. — User from Australia
⭐ Can't sign up with my work email from Saudi Arabia. Getting a region block error. Very frustrating. — User from Saudi Arabia
⭐⭐⭐⭐ Great potential. The SDK docs are excellent but some code samples still reference the old API v1. Please update! — User from India
⭐⭐⭐ Need support for RTL languages. The UI breaks completely when I switch to Arabic. — User from UAE"""

SYSTEM_PROMPT = """你是一位产品运营专家，负责分析海外用户反馈。请分析以下用户评论：

输出格式（严格 JSON）：
{
  "total_reviews": N,
  "sentiment_breakdown": {
    "positive": N,
    "neutral": N,
    "negative": N
  },
  "top_issues": [
    {"category": "分类名（如：本地化/功能/Bug/定价/文档等）", "frequency": N, "severity": "high/medium/low", "description": "问题描述", "urgent_fix": "建议的改进措施"}
  ],
  "positive_highlights": ["用户提到最多的3个优点"],
  "action_items": [
    {"priority": "P0/P1/P2", "action": "具体行动项", "expected_impact": "预期效果"}
  ],
  "recommended_response_template": "可以回复用户的英文模板（简要版本）"
}"""


def run():
    st.subheader("💬 用户反馈分析器")
    st.markdown("粘贴海外用户的 App Store / Google Play 评论或产品反馈，AI 自动分类、情感分析、排优先级，模拟产品运营日常的数据分析工作。")

    sample_btn = st.button("📥 加载示例数据（模拟海外用户评论）")
    reviews = st.text_area("粘贴用户评论（每条一行或分段）", height=250,
                           placeholder="Paste user reviews, one per line or paragraph...")

    if sample_btn:
        reviews = SAMPLE_REVIEWS
        st.rerun()

    if st.button("分析反馈", type="primary", use_container_width=True):
        if not reviews:
            st.warning("请粘贴用户评论，或点击「加载示例数据」。")
            return

        with st.spinner("AI 正在分析用户反馈..."):
            user_prompt = f"以下是用户反馈：\n\n{reviews}"
            result = ask_deepseek(SYSTEM_PROMPT, user_prompt, temperature=0.3)

        try:
            import json
            data = json.loads(result)

            # Sentiment overview
            st.markdown("### 📊 情感分析概览")
            s = data.get("sentiment_breakdown", {})
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("总评论数", data.get("total_reviews", "N/A"))
            col2.metric("😊 正面", s.get("positive", 0))
            col3.metric("😐 中性", s.get("neutral", 0))
            col4.metric("😞 负面", s.get("negative", 0))

            # Top issues
            if data.get("top_issues"):
                st.markdown("### 🚨 主要问题（按优先级）")
                for issue in sorted(data["top_issues"],
                                    key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("severity", "low"), 3)):
                    severity = issue.get("severity", "low")
                    icon = {"high": "🔴 P0", "medium": "🟡 P1", "low": "💡 P2"}.get(severity, "💡")
                    freq = issue.get("frequency", 0)
                    freq_bar = "█" * min(freq, 20) + f" ({freq}条)"
                    st.markdown(f"{icon} **{issue.get('category', '')}**")
                    st.markdown(f"  {freq_bar}")
                    st.markdown(f"  {issue.get('description', '')}")
                    if issue.get("urgent_fix"):
                        st.markdown(f"  → *建议：* {issue['urgent_fix']}")

            # Positive highlights
            if data.get("positive_highlights"):
                st.markdown("### 👍 用户好评项")
                for h in data["positive_highlights"]:
                    st.markdown(f"- ✅ {h}")

            # Action items
            if data.get("action_items"):
                st.markdown("### 📋 运营行动项")
                for item in data["action_items"]:
                    priority = item.get("priority", "P2")
                    st.markdown(f"**{priority}** — {item.get('action', '')}")
                    st.caption(f"预期效果: {item.get('expected_impact', '')}")

            # Response template
            if data.get("recommended_response_template"):
                st.markdown("### 💌 用户回复模板")
                st.info(data["recommended_response_template"])

        except (json.JSONDecodeError, KeyError) as e:
            st.error(f"AI 返回格式异常: {e}")
            st.code(result)
